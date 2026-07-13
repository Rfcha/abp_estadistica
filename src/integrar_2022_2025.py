"""
Integración de los datos SINCA 2022-2023 + 2024-2025 -> base unificada 2022-2025.

Maneja las diferencias entre ambos períodos:
  1. PRESIÓN: 2022-2023 venía ajustada a nivel del mar (~1013 hPa); 2024-2025 trae
     presión real de superficie (~952 hPa, correcta para los 520 m de Santiago).
     Se armoniza TODO a presión de superficie (criterio físicamente correcto para
     análisis local), ajustando el período 2022-2023.
  2. ESTACIONES: ambos períodos comparten las mismas 11 estaciones (ya verificado).
  3. FORMATO: ambos usan separador ';', decimal ',', fecha DD-MM-AAAA HH:MM.

Salida: sinca_santiago_2022_2025.csv (horario, mismo formato que el original).
"""
import numpy as np
import pandas as pd

# Diferencia media de presión entre criterios (nivel del mar vs superficie en Santiago)
AJUSTE_PRESION = 1013.0 - 952.3   # ~60.7 hPa

def cargar(path):
    df = pd.read_csv(path, sep=";", decimal=",")
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d-%m-%Y %H:%M")
    return df

print("Cargando períodos...")
a = cargar("sinca_santiago.csv")              # 2022-2023
b = cargar("sinca_santiago_2024_2025.csv")    # 2024-2025
print(f"  2022-2023: {len(a):,} filas | presión media {a.presion.mean():.1f} hPa")
print(f"  2024-2025: {len(b):,} filas | presión media {b.presion.mean():.1f} hPa")

# --- Armonizar presión: llevar 2022-2023 a superficie ---
a["presion"] = (a["presion"] - AJUSTE_PRESION).round(1)
print(f"\nPresión 2022-2023 ajustada a superficie: media {a.presion.mean():.1f} hPa")

# --- Verificar columnas idénticas ---
assert list(a.columns) == list(b.columns), "Columnas no coinciden"
assert sorted(a.estacion.unique()) == sorted(b.estacion.unique()), "Estaciones no coinciden"

# --- Concatenar y ordenar ---
full = pd.concat([a, b], ignore_index=True)
full = full.sort_values(["fecha", "estacion"]).reset_index(drop=True)

# --- Eliminar posibles solapamientos (duplicados fecha+estación) ---
antes = len(full)
full = full.drop_duplicates(subset=["fecha", "estacion"], keep="first").reset_index(drop=True)
print(f"\nDuplicados eliminados: {antes - len(full)}")

# --- Recalcular variables de calendario de forma consistente para todo el rango ---
full["dia_semana"] = full["fecha"].dt.dayofweek          # 0=lunes
full["es_finde"] = (full["dia_semana"] >= 5).astype(int)
# Festivos chilenos 2022-2025 (fijos + principales móviles)
festivos = {
    # 2022
    "2022-01-01","2022-04-15","2022-04-16","2022-05-01","2022-05-21","2022-06-21",
    "2022-06-27","2022-07-16","2022-08-15","2022-09-18","2022-09-19","2022-10-10",
    "2022-10-31","2022-11-01","2022-12-08","2022-12-25",
    # 2023
    "2023-01-01","2023-04-07","2023-04-08","2023-05-01","2023-05-21","2023-06-21",
    "2023-06-26","2023-07-16","2023-08-15","2023-09-18","2023-09-19","2023-10-09",
    "2023-10-27","2023-11-01","2023-12-08","2023-12-25",
    # 2024
    "2024-01-01","2024-03-29","2024-03-30","2024-05-01","2024-05-21","2024-06-20",
    "2024-06-29","2024-07-16","2024-08-15","2024-09-18","2024-09-19","2024-09-20",
    "2024-10-12","2024-10-31","2024-11-01","2024-12-08","2024-12-25",
    # 2025
    "2025-01-01","2025-04-18","2025-04-19","2025-05-01","2025-05-21","2025-06-20",
    "2025-06-29","2025-07-16","2025-08-15","2025-09-18","2025-09-19","2025-10-12",
    "2025-10-31","2025-11-01","2025-12-08","2025-12-25",
}
festivos = set(pd.to_datetime(list(festivos)).date)
full["es_festivo"] = full["fecha"].dt.date.isin(festivos).astype(int)

# --- Guardar ---
full["fecha"] = full["fecha"].dt.strftime("%d-%m-%Y %H:%M")
full.to_csv("sinca_santiago_2022_2025.csv", sep=";", decimal=",", index=False)

# Recargar para reporte
chk = cargar("sinca_santiago_2022_2025.csv")
print(f"\n=== BASE UNIFICADA 2022-2025 ===")
print(f"Filas: {len(chk):,} | Columnas: {chk.shape[1]}")
print(f"Período: {chk.fecha.min()} a {chk.fecha.max()}")
print(f"Estaciones: {chk.estacion.nunique()}")
print(f"Episodios MP2.5>50 (horario): {(chk['MP2.5']>50).sum():,} ({(chk['MP2.5']>50).mean()*100:.1f}%)")
print(f"Faltantes MP2.5: {chk['MP2.5'].isna().sum():,} ({chk['MP2.5'].isna().mean()*100:.1f}%)")
