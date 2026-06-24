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

## [3.0.0] - Fase 3 · Evaluación económica

### Agregado
- Reorientación a evaluación social de inversiones: sistema predictivo de episodios críticos.
- Modelo predictivo (regresión logística) con AUC 0.898 para anticipar episodios MP2.5.
- Módulo económico (modelo_economico.py) con parámetros oficiales (VSL-SNI, FONASA, DEIS).
- Flujo de caja a 10 años, VAN, TIR y razón B/C en perspectivas fiscal y social.
- Análisis de sensibilidad univariado y simulación de Monte Carlo (5.000 iteraciones).
- Notebook Fase 3 (02_evaluacion_economica.ipynb) ejecutable sin errores.
- Documentación de Fase 3 en formato Word (DOCX): Informe_Fase3_Evaluacion_Economica.docx.
