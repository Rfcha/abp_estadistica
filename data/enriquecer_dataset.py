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
df = pd.read_csv("sinca_santiago.csv", sep=";", decimal=",")
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
# 6) Guardado
# ----------------------------------------------------------------------
# Reordenar columnas de forma lógica
cols = ["fecha_hora", "estacion", "comuna", "zona_geografica",
        "mp2_5", "mp10", "temperatura", "humedad", "presion", "viento",
        "direccion_viento", "radiacion", "isoterma_0", "precipitacion",
        "inversion_termica", "dia_semana", "es_finde", "es_festivo",
        "tipo_dia", "estacion_anio", "temporada_critica",
        "calidad_aire_mp25", "calidad_aire_mp10", "nivel_contaminacion",
        "critico_mp25", "critico_mp10"]
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
