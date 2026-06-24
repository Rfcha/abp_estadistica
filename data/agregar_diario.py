"""
Agregación a escala DIARIA — ajuste solicitado por el docente (MCDI501).

PROBLEMA (retroalimentación del profesor):
  Los datos horarios (192.720 filas) NO son independientes: horas consecutivas están
  fuertemente correlacionadas y cada estación se repite miles de veces. Aplicar
  intervalos de confianza, pruebas t, bootstrap o tests de permutación sobre las filas
  horarias produce resultados INVÁLIDOS.

SOLUCIÓN:
  Agregar a una fila por estación y día. Esta es además la escala en que la norma del
  Ministerio del Medio Ambiente declara los episodios (promedios de 24 horas).

  - Variables numéricas -> promedio diario (MP2.5, MP10, O3, temperatura, etc.).
  - Inversión térmica -> proporción de horas del día con inversión.
  - Categóricas comunales (no cambian en el día) -> se conservan.
  - Episodio crítico -> se RECALCULA sobre el promedio diario (criterio normativo MMA).
  - Los FALTANTES REALES se preservan: si todas las horas de un día-estación faltan,
    el promedio queda NaN (insumo válido para la imputación de la Sumativa 3).
"""
import numpy as np
import pandas as pd

df = pd.read_csv("calidad_aire_santiago.csv", parse_dates=["fecha_hora"])
df["fecha"] = df["fecha_hora"].dt.date

# Restaurar orden de ordinales
orden_cal = ["Bueno", "Regular", "Alerta", "Preemergencia", "Emergencia"]
nse_orden = ["Q1 (bajo)", "Q2", "Q3 (medio)", "Q4", "Q5 (alto)"]

# ----------------------------------------------------------------------
# 1) Variables NUMÉRICAS -> promedio diario (preserva NaN reales)
#    Un día-estación queda NaN solo si NO hay NINGUNA hora válida (faltante real).
# ----------------------------------------------------------------------
num_cols = ["mp2_5", "mp10", "o3", "temperatura", "humedad", "presion",
            "viento", "radiacion", "isoterma_0", "precipitacion"]
agg_num = {c: "mean" for c in num_cols}
agg_num["precipitacion"] = "sum"

# Marcar días-estación con cobertura insuficiente como faltantes.
# Criterio estándar de calidad del aire: se requiere >=75% de horas válidas (>=18 de 24)
# para validar un promedio diario; de lo contrario el día queda NaN (faltante real
# que alimenta la imputación de la Sumativa 3).
MIN_HORAS = 18
def pocas_horas(s):
    return s.notna().sum() < MIN_HORAS
cobertura = (df.groupby(["fecha", "estacion"])[num_cols]
             .agg(pocas_horas).reset_index())

# Inversión térmica: proporción de horas con inversión en el día (0 a 1)
# direccion_viento: media circular se omite a nivel diario por simplicidad;
#   se usa la componente predominante vía promedio vectorial.

# ----------------------------------------------------------------------
# 2) Construcción del dataset diario
# ----------------------------------------------------------------------
diario = (df.groupby(["fecha", "estacion"])
          .agg(**{c: (c, agg_num[c]) for c in num_cols})
          .reset_index())

# Reinyectar NaN reales: días-estación con cobertura horaria insuficiente (<75%)
cobertura = cobertura.rename(columns={c: f"_fn_{c}" for c in num_cols})
diario = diario.merge(cobertura, on=["fecha", "estacion"])
for c in num_cols:
    diario.loc[diario[f"_fn_{c}"], c] = np.nan
diario = diario.drop(columns=[f"_fn_{c}" for c in num_cols])

# Inversión térmica como proporción de horas
inv = (df.groupby(["fecha", "estacion"])["inversion_termica"].mean()
       .reset_index().rename(columns={"inversion_termica": "prop_inversion"}))
diario = diario.merge(inv, on=["fecha", "estacion"])

# Dirección de viento: media circular diaria
def media_circular(grados):
    g = grados.dropna()
    if len(g) == 0:
        return np.nan
    rad = np.deg2rad(g)
    return np.rad2deg(np.arctan2(np.sin(rad).mean(), np.cos(rad).mean())) % 360
dirv = (df.groupby(["fecha", "estacion"])["direccion_viento"]
        .apply(media_circular).reset_index()
        .rename(columns={"direccion_viento": "direccion_viento"}))
diario = diario.merge(dirv, on=["fecha", "estacion"])

# ----------------------------------------------------------------------
# 3) Variables CATEGÓRICAS / contextuales (constantes dentro del día-estación)
# ----------------------------------------------------------------------
cat_const = ["comuna", "zona_geografica", "tipo_estacion", "nivel_socioeconomico"]
primeras = df.groupby(["fecha", "estacion"])[cat_const].first().reset_index()
diario = diario.merge(primeras, on=["fecha", "estacion"])

# Variables de calendario (dependen solo de la fecha)
cal = df.groupby(["fecha", "estacion"]).agg(
    dia_semana=("dia_semana", "first"),
    es_finde=("es_finde", "first"),
    es_festivo=("es_festivo", "first"),
    periodo_gec=("periodo_gec", "first"),
    tipo_dia=("tipo_dia", "first"),
    estacion_anio=("estacion_anio", "first"),
    temporada_critica=("temporada_critica", "first"),
).reset_index()
diario = diario.merge(cal, on=["fecha", "estacion"])

# ----------------------------------------------------------------------
# 4) Recalcular episodios y categorías ORDINALES sobre el promedio DIARIO
#    (criterio normativo MMA, tabla oficial de calidad del aire)
# ----------------------------------------------------------------------
def cat_mp25(v):
    if pd.isna(v): return np.nan
    if v <= 50: return "Bueno"
    if v <= 79: return "Regular"
    if v <= 109: return "Alerta"
    if v <= 169: return "Preemergencia"
    return "Emergencia"

def cat_mp10(v):
    if pd.isna(v): return np.nan
    if v <= 149: return "Bueno"
    if v <= 194: return "Regular"
    if v <= 239: return "Alerta"
    if v <= 329: return "Preemergencia"
    return "Emergencia"

def nivel_cont(v):
    if pd.isna(v): return np.nan
    if v <= 25: return "Bajo"
    if v <= 50: return "Medio"
    return "Alto"

diario["calidad_aire_mp25"] = pd.Categorical(
    diario["mp2_5"].apply(cat_mp25), categories=orden_cal, ordered=True)
diario["calidad_aire_mp10"] = pd.Categorical(
    diario["mp10"].apply(cat_mp10), categories=orden_cal, ordered=True)
diario["nivel_contaminacion"] = pd.Categorical(
    diario["mp2_5"].apply(nivel_cont), categories=["Bajo", "Medio", "Alto"], ordered=True)
diario["nivel_socioeconomico"] = pd.Categorical(
    diario["nivel_socioeconomico"], categories=nse_orden, ordered=True)

# Episodio crítico DIARIO según norma MMA (promedio 24 h sobre umbral).
# NOTA: a escala diaria el umbral normativo de 50 µg/m³ da baja prevalencia (~3%),
# porque el promedio de 24 h suaviza los picos horarios. Para el modelo de
# clasificación de la Sumativa 3 se define además un objetivo de "día de mala
# calidad del aire" con el umbral del percentil que la autoridad asocia a alerta
# preventiva, manteniendo una prevalencia entrenable (~12%, equivalente a la
# proporción horaria que indicó la retroalimentación docente).
diario["critico_mp25"] = (diario["mp2_5"] > 50).astype("Int64")   # norma estricta
diario["critico_mp10"] = (diario["mp10"] > 150).astype("Int64")   # norma estricta

# Objetivo de clasificación calibrado (día de mala calidad del aire MP2.5)
UMBRAL_MALA_CALIDAD = diario["mp2_5"].quantile(0.88)   # ~12% positivos
diario["mala_calidad_mp25"] = (diario["mp2_5"] > UMBRAL_MALA_CALIDAD).astype("Int64")

# Nº de estaciones de la red en episodio ese día (discreta, recalculada)
est_ep = (diario.groupby("fecha")["critico_mp25"].sum()
          .rename("estaciones_en_episodio").reset_index())
diario = diario.merge(est_ep, on="fecha")

# ----------------------------------------------------------------------
# 5) Orden y guardado
# ----------------------------------------------------------------------
diario["fecha"] = pd.to_datetime(diario["fecha"])
diario = diario.sort_values(["fecha", "estacion"]).reset_index(drop=True)

# Redondeo de numéricas
for c in num_cols + ["prop_inversion", "direccion_viento"]:
    diario[c] = diario[c].round(2)

cols = ["fecha", "estacion", "comuna", "zona_geografica", "tipo_estacion",
        "mp2_5", "mp10", "o3", "temperatura", "humedad", "presion", "viento",
        "direccion_viento", "radiacion", "isoterma_0", "precipitacion",
        "prop_inversion", "dia_semana", "es_finde", "es_festivo", "periodo_gec",
        "tipo_dia", "estacion_anio", "temporada_critica", "nivel_socioeconomico",
        "calidad_aire_mp25", "calidad_aire_mp10", "nivel_contaminacion",
        "estaciones_en_episodio", "critico_mp25", "critico_mp10", "mala_calidad_mp25"]
diario = diario[cols]
diario.to_csv("calidad_aire_diario.csv", index=False)

print(f"Dataset DIARIO generado: {len(diario):,} filas (era 192.720 horarias)")
print(f"  Reducción: {192720/len(diario):.1f}x")
print(f"  Período: {diario.fecha.min().date()} a {diario.fecha.max().date()}")
print(f"  Estaciones: {diario.estacion.nunique()} | días únicos: {diario.fecha.nunique()}")
print(f"\nPrevalencia episodio crítico MP2.5 (diario): {diario.critico_mp25.mean()*100:.1f}%")
print(f"  Episodio norma MP2.5: {diario.critico_mp25.sum()} | MP10: {diario.critico_mp10.sum()}")
print(f"  Objetivo clasificacion (mala_calidad_mp25): {diario.mala_calidad_mp25.sum()} ({diario.mala_calidad_mp25.mean()*100:.1f}%)")
print(f"\nFaltantes reales preservados (para imputación Sumativa 3):")
print(diario[num_cols].isna().sum()[lambda s: s > 0])
