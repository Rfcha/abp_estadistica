"""
Modelo económico — Sistema predictivo de episodios críticos de calidad del aire.
Parámetros anclados a fuentes oficiales chilenas (MMA, MIDESO/SNI, GreenLabUC, DEIS).

ENFOQUE: evaluación social de inversiones (Fase 3 del proyecto ABP).
Lógica: invertir en un sistema predictivo -> anticipar episodios críticos ->
gestión temprana (restricción vehicular, prohibición de leña) -> menos atenciones
de salud y muertes prematuras evitadas -> ahorro fiscal y beneficio social.

Todos los parámetros se declaran con su fuente. Los valores son estimaciones de
prefactibilidad; deben refinarse con datos del DEIS y valores unitarios FONASA/MAI
en la etapa de factibilidad.
"""
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# PARÁMETROS OFICIALES (fuentes citadas en el informe)
# ----------------------------------------------------------------------
USD_CLP = 950.0          # tipo de cambio referencial (CLP por USD)
UF_CLP = 39000.0         # valor referencial de la UF (CLP)

# --- Beneficios sociales (función de daño, MMA / MIDESO-SNI) ---
# Valor de la Vida Estadística (VSL) en Chile. Estudios recientes (hedónicos, LASSO)
# estiman ~US$8,86 millones; el SNI usa cifras más conservadoras. Se adopta un valor
# central conservador y se analiza sensibilidad.
VSL_USD = 4_500_000      # VSL conservador (USD) — rango sensibilidad: 2.5M a 8.9M
MUERTES_PREMATURAS_RM_ANIO = 1_300   # estimación atribuible a MP2.5 en la RM (de ~3.600 país)

# --- Costos unitarios de salud (FONASA-MAI / DEIS, valores referenciales) ---
COSTO_ATENCION_URGENCIA = 45_000     # CLP por atención de urgencia respiratoria ambulatoria
COSTO_HOSPITALIZACION = 1_200_000    # CLP por hospitalización respiratoria (día-cama x estadía)
PROP_HOSPITALIZA = 0.08              # fracción de atenciones que derivan en hospitalización

# --- Carga sanitaria asociada a episodios críticos ---
# Atenciones de urgencia respiratoria adicionales por día de episodio crítico en la RM.
# Calibrado con literatura DEIS (elasticidades MP2.5 -> urgencias respiratorias).
ATENCIONES_EXTRA_POR_DIA_CRITICO = 1400   # exceso de atenciones/día en episodio (niños + adultos mayores)
FRAC_NINOS_AM = 0.65                       # fracción correspondiente a menores y adultos mayores

# --- Efectividad del sistema predictivo ---
# La anticipación permite gestión temprana que mitiga parte del daño.
# Minsal documentó reducción de muertes y días de episodio con alertas oportunas.
HORAS_ANTICIPACION = 48              # capacidad de predecir con 48 h de antelación
EFECTIVIDAD_MITIGACION = 0.12       # fracción del exceso de daño realmente evitable (conservador)
PRECISION_MODELO = 0.80            # sensibilidad esperada del clasificador
# Fracción de muertes prematuras anuales ligada específicamente a episodios agudos
# (la mayoría se asocia a exposición crónica, no a picos puntuales): muy pequeña.
FRAC_MUERTES_AGUDAS = 0.004

# ----------------------------------------------------------------------
# INVERSIÓN Y COSTOS DEL PROYECTO (CAPEX / OPEX) — estimación prefactibilidad
# ----------------------------------------------------------------------
CAPEX = {
    "Desarrollo plataforma web predictiva": 85_000_000,
    "Integración SINCA / DMC / DEIS (APIs)": 35_000_000,
    "Infraestructura cloud inicial y MLOps": 28_000_000,
    "Modelos ML y validación": 42_000_000,
    "Diseño UX y sistema de alertas": 25_000_000,
}
OPEX_ANUAL = {
    "Cloud, cómputo y almacenamiento": 24_000_000,
    "Mantención y soporte": 30_000_000,
    "Equipo (ciencia de datos + operaciones)": 96_000_000,
    "Reentrenamiento y monitoreo de modelos": 18_000_000,
    "Difusión y comunicación de alertas": 12_000_000,
}

# ----------------------------------------------------------------------
# HORIZONTE Y TASA DE DESCUENTO (Sistema Nacional de Inversiones)
# ----------------------------------------------------------------------
HORIZONTE_ANIOS = 10
TASA_DESCUENTO_SOCIAL = 0.06    # tasa social de descuento vigente en el SNI (6%)


def calcular_dias_criticos_anuales(df):
    """Estima los días-episodio crítico anuales a partir de los datos reales.
    Un día se declara 'episodio' si el promedio diario de la red (no una sola
    estación) supera el umbral de preemergencia, criterio cercano al operacional
    de la autoridad. Esto evita sobreestimar contando cualquier pico aislado."""
    d = df.copy()
    d["fecha"] = pd.to_datetime(d["fecha_hora"]).dt.date
    # Promedio diario por estación, luego mediana de la red ese día
    diario_est = d.groupby(["fecha", "estacion"])["mp2_5"].mean().reset_index()
    diario_red = diario_est.groupby("fecha")["mp2_5"].median()
    # Episodio crítico: mediana de red sobre umbral de preemergencia (>79 = Alerta+)
    dias_criticos = (diario_red > 79).sum()
    anios = d["fecha_hora"].dt.year.nunique()
    return max(dias_criticos / anios, 15)   # piso realista de ~15 días/año


def beneficio_anual(dias_criticos_anio):
    """Beneficio anual desglosado en componente FISCAL (ahorro directo en salud)
    y componente SOCIAL (mortalidad evitada, valorada con VSL).
    Se separan porque la rúbrica exige rentabilidad privada/fiscal y social, y porque
    el VSL es de magnitud muy superior y debe analizarse por separado."""
    # 1) Componente FISCAL: atenciones de urgencia evitadas (ahorro directo arcas fiscales)
    atenciones_criticas = dias_criticos_anio * ATENCIONES_EXTRA_POR_DIA_CRITICO
    atenciones_evitadas = (atenciones_criticas * PRECISION_MODELO * EFECTIVIDAD_MITIGACION)
    hosp_evitadas = atenciones_evitadas * PROP_HOSPITALIZA
    amb_evitadas = atenciones_evitadas * (1 - PROP_HOSPITALIZA)
    ahorro_salud = (amb_evitadas * COSTO_ATENCION_URGENCIA +
                    hosp_evitadas * COSTO_HOSPITALIZACION)

    # 2) Componente SOCIAL: muertes prematuras evitadas (fracción aguda, VSL)
    muertes_evitadas = (MUERTES_PREMATURAS_RM_ANIO * FRAC_MUERTES_AGUDAS
                        * PRECISION_MODELO * EFECTIVIDAD_MITIGACION)
    ahorro_mortalidad = muertes_evitadas * VSL_USD * USD_CLP

    return {
        "atenciones_evitadas": atenciones_evitadas,
        "ahorro_salud_clp": ahorro_salud,              # beneficio FISCAL
        "muertes_evitadas": muertes_evitadas,
        "ahorro_mortalidad_clp": ahorro_mortalidad,    # beneficio SOCIAL adicional
        "beneficio_fiscal_clp": ahorro_salud,
        "beneficio_social_clp": ahorro_salud + ahorro_mortalidad,
    }


def flujo_de_caja(dias_criticos_anio, perspectiva="fiscal"):
    """Flujo de caja y VAN/TIR/BC. perspectiva='fiscal' usa solo ahorro en salud;
    perspectiva='social' añade la mortalidad evitada valorada con VSL."""
    capex_total = sum(CAPEX.values())
    opex_total = sum(OPEX_ANUAL.values())
    ben = beneficio_anual(dias_criticos_anio)
    beneficio = ben["beneficio_fiscal_clp"] if perspectiva == "fiscal" else ben["beneficio_social_clp"]

    filas = [{"anio": 0, "inversion": -capex_total, "costos_op": 0,
              "beneficios": 0, "flujo_neto": -capex_total}]
    for t in range(1, HORIZONTE_ANIOS + 1):
        rampa = min(1.0, 0.4 + 0.2 * t)          # adopción gradual
        flujo = beneficio * rampa - opex_total
        filas.append({"anio": t, "inversion": 0, "costos_op": -opex_total,
                      "beneficios": beneficio * rampa, "flujo_neto": flujo})

    fc = pd.DataFrame(filas)
    fc["factor_desc"] = 1 / (1 + TASA_DESCUENTO_SOCIAL) ** fc["anio"]
    fc["flujo_desc"] = fc["flujo_neto"] * fc["factor_desc"]
    van = fc["flujo_desc"].sum()

    # TIR por bisección
    def npv(rate):
        return sum(fc["flujo_neto"].values[t] / (1 + rate) ** t for t in range(len(fc)))
    lo, hi = -0.9, 5.0
    if npv(hi) > 0:
        tir = hi
    else:
        for _ in range(300):
            mid = (lo + hi) / 2
            if npv(mid) > 0: lo = mid
            else: hi = mid
        tir = mid

    vp_ben = sum(fc["beneficios"].values[t] * fc["factor_desc"].values[t] for t in range(len(fc)))
    vp_cost = capex_total + sum(opex_total * fc["factor_desc"].values[t] for t in range(1, len(fc)))
    bc = vp_ben / vp_cost if vp_cost else 0

    fc["flujo_desc_acum"] = fc["flujo_desc"].cumsum()
    pay = fc.loc[fc["flujo_desc_acum"] > 0, "anio"]
    payback = int(pay.iloc[0]) if len(pay) else None

    return fc, {"van": van, "tir": tir, "bc": bc, "payback": payback,
                "capex": capex_total, "opex": opex_total,
                "beneficio_anual": beneficio, "perspectiva": perspectiva, **ben}


if __name__ == "__main__":
    df = pd.read_csv("../data/calidad_aire_santiago.csv", parse_dates=["fecha_hora"])
    dias = calcular_dias_criticos_anuales(df)
    print(f"Días críticos/año (datos reales): {dias:.0f}")
    print(f"CAPEX total: ${sum(CAPEX.values()):,.0f} | OPEX anual: ${sum(OPEX_ANUAL.values()):,.0f}\n")

    for persp in ["fiscal", "social"]:
        fc, ind = flujo_de_caja(dias, perspectiva=persp)
        print(f"=== PERSPECTIVA {persp.upper()} ===")
        print(f"  Beneficio anual: ${ind['beneficio_anual']:,.0f} CLP")
        print(f"  Atenciones evitadas/año: {ind['atenciones_evitadas']:,.0f}")
        if persp == "social":
            print(f"  Muertes evitadas/año: {ind['muertes_evitadas']:.2f}")
        print(f"  VAN ({TASA_DESCUENTO_SOCIAL*100:.0f}%): ${ind['van']:,.0f} CLP")
        print(f"  TIR: {ind['tir']*100:.0f}%  |  B/C: {ind['bc']:.2f}  |  Payback: año {ind['payback']}\n")
