# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)
y el proyecto sigue un versionado por fases del curso MCDI501.

---

## [1.0.0] — 2026-06-28 — Sumativa 1: Informe técnico de avance (Fase 2)

Primera entrega evaluada: análisis exploratorio e inferencial completo a escala estación-día.

### Añadido
- Notebook `01_analisis_estadistico_diario.ipynb` con el análisis completo, ejecutable de principio a fin y documentado celda a celda (encabezados, comentarios e interpretación de cada salida).
- Dataset `data/calidad_aire_diario.csv` a escala estación-día (2022–2025): 16.071 observaciones, 11 estaciones, 36 variables.
- Helper `guardar_figura()` para exportación robusta de figuras (evita el error de Pillow en Windows al escribir PNG).
- `requirements.txt` con versiones exactas del entorno validado y alternativas estables.
- README con objetivo, hallazgos, metodología, estructura y guía de reproducibilidad.

### Análisis incluido
- **Calidad de datos:** auditoría de faltantes (MP2.5 27,8 %), 0 duplicados, 0 inconsistencias físicas; criterio de cobertura ≥75 % de horas/día.
- **Estadística descriptiva:** tendencia central, dispersión, CV %, asimetría y curtosis; frecuencias de categóricas; correlación de Pearson.
- **Estimación:** intervalos de confianza al 95 % (*t* de Student) para MP2.5, MP10 y temperatura.
- **Pruebas de hipótesis:** 4 contrastes (3× *t* de Welch con verificación de supuestos vía Levene + 1× χ² de independencia), con tamaño de efecto (*d* de Cohen, *V* de Cramér).

### Hallazgos clave
- Inequidad ambiental Q1 vs Q5: +12,8 µg/m³ (77 % mayor), *d* = 0,97.
- Desigualdad territorial Oriente vs Poniente: *d* = −0,76.
- Efecto de la inversión térmica sobre MP2.5: *d* = 0,85.
- 551 días-estación en episodio crítico (4,75 % del total válido).

---

## [No publicado] — Próximas fases

### Planificado — Sumativa 2 (validación)
- Intervalos de confianza por **bootstrap**.
- **Tests de permutación** y simulación de **Monte Carlo** para validar los hallazgos sin supuestos paramétricos.

### Planificado — Sumativa 3 (modelo)
- Modelo de **clasificación binaria** de episodios críticos (objetivo `mala_calidad_mp25`, ~12 % positivos).
- Evaluación con F1, recall y AUC; división estratificada por períodos para evitar fuga temporal.
- Imputación sobre los faltantes reales del archivo horario.
