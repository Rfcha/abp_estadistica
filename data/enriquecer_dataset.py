"""
Enriquecimiento del dataset REAL del SINCA (Santiago, 2022-2023).
Toma 'sinca_santiago.csv' (datos reales) y añade variables derivadas y contextuales
necesarias para el análisis estadístico de la Sumativa 1.

Variables añadidas:
  Numéricas derivadas (físicamente plausibles, ancladas a las variables reales):
    - isoterma_0 (m): altura de la isoterma 0°C, derivada de temperatura/estación + ruido.
    - precipitacion (mm): eventos de lluvia coherentes con humedad alta + invierno.
    - direccion_viento (grados, CIRCULAR): predominante SO, con rotación diaria.
  Categóricas nominales:
    - zona_geografica: Norte/Sur/Oriente/Poniente/Centro según comuna.
    - tipo_dia: Laboral / Fin de semana / Festivo (desde es_finde, es_festivo).
    - estacion_anio: Verano/Otoño/Invierno/Primavera.
    - temporada_critica: Invierno (may-ago) / Resto.
  Categóricas ordinales (según tabla oficial de calidad del aire MMA):
    - calidad_aire_mp25 / calidad_aire_mp10: Bueno < Regular < Alerta < Preemergencia < Emergencia.
    - nivel_contaminacion: Bajo < Medio < Alto.

Las variables reales del SINCA (MP2.5, MP10, temperatura, humedad, presion, viento,
radiacion, inversion_termica, dia_semana, es_finde, es_festivo) se conservan intactas.
"""
import numpy as np
import pandas as pd

SEED = 2026
rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------
# 1) Carga del dataset real
# ----------------------------------------------------------------------
df = pd.read_csv("sinca_santiago_2022_2025.csv", sep=";", decimal=",")
df = df.rename(columns={"MP2.5": "mp2_5", "MP10": "mp10", "fecha": "fecha_hora"})
df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], format="%d-%m-%Y %H:%M")
df = df.sort_values("fecha_hora").reset_index(drop=True)
n = len(df)
print(f"Dataset real cargado: {n:,} filas, {df.shape[1]} columnas")

mes = df["fecha_hora"].dt.month.to_numpy()
hora = df["fecha_hora"].dt.hour.to_numpy()
dia_anio = df["fecha_hora"].dt.dayofyear.to_numpy()

# ----------------------------------------------------------------------
# 2) Variables numéricas derivadas (ancladas a variables reales)
# ----------------------------------------------------------------------

# Isoterma 0°C: anclada DIRECTAMENTE a la temperatura real del SINCA.
# Físicamente, la altura de la isoterma 0°C sube ~150 m por cada °C de temperatura
# en superficie. Como la temperatura real anticorrelaciona con MP (más frío -> más MP),
# la isoterma hereda esa relación: isoterma baja -> más MP.
temp = df["temperatura"].to_numpy()
isoterma = 2950 + 150 * (temp - np.nanmean(temp)) + rng.normal(0, 250, n)
df["isoterma_0"] = np.clip(isoterma, 1400, 4800).round(0)

# Precipitación: eventos coherentes con humedad alta e invierno.
humedad = df["humedad"].fillna(df["humedad"].median()).to_numpy()
prob_lluvia = np.clip(0.002 + 0.05 * np.exp(-((mes - 6.5) ** 2) / 4.0)
                      * (humedad / 100) ** 2, 0, 0.5)
llueve = rng.random(n) < prob_lluvia
df["precipitacion"] = np.where(llueve, rng.gamma(1.6, 1.8, n), 0.0).round(1)

# Dirección del viento (circular): predominante SO, rotación diaria.
dir_base = 225 + 35 * np.sin((hora - 15) / 24 * 2 * np.pi)
df["direccion_viento"] = ((dir_base + rng.normal(0, 30, n)) % 360).round(0)

# ----------------------------------------------------------------------
# 3) Categóricas nominales
# ----------------------------------------------------------------------
zona_map = {
    "Las Condes": "Oriente", "Providencia": "Oriente", "La Florida": "Sur",
    "Puente Alto": "Sur", "El Bosque": "Sur", "Cerrillos": "Poniente",
    "Pudahuel": "Poniente", "Cerro Navia": "Poniente", "Quilicura": "Norte",
    "Independencia": "Centro", "Talagante": "Poniente",
}
df["zona_geografica"] = df["comuna"].map(zona_map)

# Tipo de día (desde variables reales es_finde / es_festivo)
def clasif_dia(row):
    if row["es_festivo"] == 1:
        return "Festivo"
    elif row["es_finde"] == 1:
        return "Fin de semana"
    return "Laboral"
df["tipo_dia"] = df.apply(clasif_dia, axis=1)

# Estación del año (hemisferio sur)
def estacion_anio(m):
    if m in (12, 1, 2): return "Verano"
    if m in (3, 4, 5): return "Otoño"
    if m in (6, 7, 8): return "Invierno"
    return "Primavera"
df["estacion_anio"] = pd.Series(mes).map(estacion_anio).values

# Temporada crítica de gestión de episodios (may-ago)
df["temporada_critica"] = np.where(np.isin(mes, [5, 6, 7, 8]),
                                    "Invierno", "Resto del año")

# ----------------------------------------------------------------------
# 4) Categóricas ORDINALES — tabla oficial de calidad del aire (MMA)
#    MP2.5: Bueno 0-50, Regular 51-79, Alerta 80-109, Preemerg 110-169, Emerg >=170
#    MP10:  Bueno 0-149, Regular 150-194, Alerta 195-239, Preemerg 240-329, Emerg >=330
# ----------------------------------------------------------------------
orden_calidad = ["Bueno", "Regular", "Alerta", "Preemergencia", "Emergencia"]

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

df["calidad_aire_mp25"] = pd.Categorical(
    df["mp2_5"].apply(cat_mp25), categories=orden_calidad, ordered=True)
df["calidad_aire_mp10"] = pd.Categorical(
    df["mp10"].apply(cat_mp10), categories=orden_calidad, ordered=True)

# Nivel de contaminación (ordinal simplificado, tercios sobre MP2.5)
def nivel_cont(v):
    if pd.isna(v): return np.nan
    if v <= 25: return "Bajo"
    if v <= 50: return "Medio"
    return "Alto"
df["nivel_contaminacion"] = pd.Categorical(
    df["mp2_5"].apply(nivel_cont),
    categories=["Bajo", "Medio", "Alto"], ordered=True)

# ----------------------------------------------------------------------
# 5) Indicadores binarios de episodio crítico (umbrales de norma)
# ----------------------------------------------------------------------
df["critico_mp25"] = (df["mp2_5"] > 50).astype("Int64")
df["critico_mp10"] = (df["mp10"] > 150).astype("Int64")

# ----------------------------------------------------------------------
# 5b) NUEVAS VARIABLES (una de cada tipo) con sustento en fuentes oficiales
# ----------------------------------------------------------------------

# (NOMINAL) Tipo de estación de monitoreo según clasificación SINCA/MMA.
#   Fuente: SINCA — estaciones urbanas de tráfico, urbanas de fondo y suburbanas.
#   Asignación según ubicación documentada de cada estación en la red MACAM.
tipo_estacion_map = {
    "Las Condes": "Urbana de fondo", "Providencia": "Urbana de tráfico",
    "La Florida": "Urbana de fondo", "Puente Alto": "Suburbana",
    "El Bosque": "Urbana de fondo", "Cerrillos": "Urbana de tráfico",
    "Pudahuel": "Suburbana", "Cerro Navia": "Urbana de fondo",
    "Quilicura": "Urbana de tráfico", "Independencia": "Urbana de tráfico",
    "Talagante": "Suburbana",
}
df["tipo_estacion"] = df["comuna"].map(tipo_estacion_map)

# (ORDINAL) Nivel socioeconómico comunal (quintil 1=menor a 5=mayor ingreso).
#   Fuente: aproximación basada en CASEN / índice de prioridad social RM y nivel de
#   ingreso comunal conocido. Variable clave para el análisis de equidad ambiental y
#   como control del factor confusor socioeconómico.
#   Asignación de las 11 comunas cubriendo los 5 quintiles:
#     Q1 (bajo): Cerro Navia, El Bosque            -> comunas de menor ingreso
#     Q2 (medio-bajo): Cerrillos, Pudahuel          -> ingreso medio-bajo
#     Q3 (medio): Puente Alto, Talagante            -> ingreso medio
#     Q4 (medio-alto): La Florida, Quilicura, Independencia -> ingreso medio-alto
#     Q5 (alto): Las Condes, Providencia            -> comunas de mayor ingreso
nse_quintil_map = {
    "Cerro Navia": 1, "El Bosque": 1,
    "Cerrillos": 2, "Pudahuel": 2,
    "Puente Alto": 3, "Talagante": 3,
    "La Florida": 4, "Quilicura": 4, "Independencia": 4,
    "Las Condes": 5, "Providencia": 5,
}
nse_orden = ["Q1 (bajo)", "Q2 (medio-bajo)", "Q3 (medio)", "Q4 (medio-alto)", "Q5 (alto)"]
nse_label = {1: "Q1 (bajo)", 2: "Q2 (medio-bajo)", 3: "Q3 (medio)",
             4: "Q4 (medio-alto)", 5: "Q5 (alto)"}
df["nivel_socioeconomico"] = pd.Categorical(
    df["comuna"].map(nse_quintil_map).map(nse_label),
    categories=nse_orden, ordered=True)

# (DICOTÓMICA) Período de Gestión de Episodios Críticos (GEC) del PPDA RM.
#   Fuente: Plan de Prevención y Descontaminación Atmosférica RM (D.S. MMA).
#   El GEC rige oficialmente del 1 de abril al 31 de agosto de cada año.
df["periodo_gec"] = df["fecha_hora"].dt.month.isin([4, 5, 6, 7, 8]).astype(int)

# (CUANTITATIVA CONTINUA) Ozono troposférico O3 (µg/m³).
#   Fuente: SINCA — contaminante criterio, norma primaria 120 µg/m³N (8h).
#   El O3 es FOTOQUÍMICO: alto en verano y sector oriente (inverso al MP2.5).
#   Se modela anclado a radiación y temperatura reales, con patrón estival.
mes_o3 = df["fecha_hora"].dt.month.to_numpy()
hora_o3 = df["fecha_hora"].dt.hour.to_numpy()
rad_norm = (df["radiacion"].fillna(df["radiacion"].median()).to_numpy()
            / (df["radiacion"].max() + 1e-9))
# O3 sube con radiación (fotoquímica), en verano y al mediodía
factor_estival = 1 + 0.8 * np.exp(-((mes_o3 - 1) % 12 - 0) ** 2 / 8.0)
factor_mediodia = np.exp(-((hora_o3 - 15) ** 2) / 18)
# O3 sube con radiación (fotoquímica), en verano y al mediodía
rng_local = np.random.default_rng(SEED + 7)
o3 = (20 + 55 * rad_norm * factor_mediodia * factor_estival
      + rng_local.normal(0, 8, len(df)))
df["o3"] = np.clip(o3, 1, 240).round(1)

# (CUANTITATIVA DISCRETA) Número de estaciones de la red en episodio crítico ese día.
#   Conteo entero 0–11 derivado de la red MACAM (11 estaciones). Mide la
#   EXTENSIÓN ESPACIAL del episodio, no solo su intensidad puntual.
df["_fecha"] = df["fecha_hora"].dt.date
crit_por_est_dia = (df.groupby(["_fecha", "estacion"])["mp2_5"].mean()
                    .reset_index())
crit_por_est_dia["es_crit"] = (crit_por_est_dia["mp2_5"] > 50).astype(int)
est_en_episodio = (crit_por_est_dia.groupby("_fecha")["es_crit"].sum()
                   .rename("estaciones_en_episodio"))
df = df.merge(est_en_episodio, left_on="_fecha", right_index=True, how="left")
df["estaciones_en_episodio"] = df["estaciones_en_episodio"].fillna(0).astype(int)
df = df.drop(columns=["_fecha"])

# ----------------------------------------------------------------------
# 6) Guardado
# ----------------------------------------------------------------------
# Reordenar columnas de forma lógica
cols = ["fecha_hora", "estacion", "comuna", "zona_geografica", "tipo_estacion",
        "mp2_5", "mp10", "o3", "temperatura", "humedad", "presion", "viento",
        "direccion_viento", "radiacion", "isoterma_0", "precipitacion",
        "inversion_termica", "dia_semana", "es_finde", "es_festivo", "periodo_gec",
        "tipo_dia", "estacion_anio", "temporada_critica", "nivel_socioeconomico",
        "calidad_aire_mp25", "calidad_aire_mp10", "nivel_contaminacion",
        "estaciones_en_episodio", "critico_mp25", "critico_mp10"]
df = df[cols]
df.to_csv("calidad_aire_santiago.csv", index=False)

print(f"Dataset enriquecido: {len(df):,} filas, {df.shape[1]} columnas")
print("\nColumnas finales:")
for c in df.columns:
    print(f"  {c:22s} {str(df[c].dtype):12s}")
print("\nDistribución calidad_aire_mp25:")
print(df["calidad_aire_mp25"].value_counts().sort_index())
print("\nTipo de día:")
print(df["tipo_dia"].value_counts())
