# Registro de cambios (CHANGELOG)

Formato basado en Keep a Changelog.

## [2.0.0] - Sumativa 1 · Fase 2 (datos reales SINCA)

### Agregado
- Base de datos REAL: red SINCA 2022-2023, 11 estaciones, 192.720 registros horarios.
- Pipeline de enriquecimiento (`enriquecer_dataset.py`): isoterma 0 °C, precipitación y
  dirección del viento derivadas con física anclada a variables reales.
- Variables categóricas nominales (zona geográfica, tipo de día, estación del año) y ordinales
  (calidad del aire según tabla oficial MMA, nivel de contaminación).
- Diferenciador temporal laboral / fin de semana / festivo con prueba de hipótesis.
- Tratamiento de dirección del viento como variable circular (rosa de los vientos).
- Variable contextual de áreas verdes (INE-SIEDU) para las 11 comunas reales.
- Cuatro pruebas de hipótesis: tres t de Welch (territorial, estacional, tipo de día) y una χ².
- Análisis de calidad, EDA, estimación con IC 95%, síntesis y próximos pasos (Fases 3-4).

### Por hacer (Fase 3)
- Regresión lineal múltiple y logística.
- Simulación Monte Carlo y block bootstrap.
- Análisis de sensibilidad.
