# Registro de cambios (CHANGELOG)

Formato basado en Keep a Changelog.

## [5.0.0] - Ampliación del espacio muestral a 2022-2025

### Agregado
- **Datos reales 2024-2025** del SINCA integrados (MP2.5, MP10 validados) con meteorología
  ERA5/open-meteo. Script `integrar_2022_2025.py`.
- Base unificada `sinca_santiago_2022_2025.csv`: 385.704 filas horarias, 4 años completos.
- Dataset diario ampliado a **16.071 filas** (era 8.030).
- Sección de evolución temporal interanual en el notebook.

### Corregido
- **Armonización de presión**: 2022-2023 venía a nivel del mar (~1013 hPa) y 2024-2025 a
  superficie (~952 hPa). Se unificó todo a presión de superficie (correcta para los 520 m de
  Santiago), evitando un salto artificial de 60 hPa.

### Mejora respecto al desbalance
- Más episodios críticos reales: MP10 diario pasó de 0 a 66 días críticos; tendencia interanual
  creciente (2022: 109 días → 2025: 186 días-estación en episodio).
- Faltantes reales preservados (4.468 días con MP2.5 faltante) para la imputación de Sumativa 3.

## [4.0.0] - Reorientación a escala diaria y enfoque estadístico (retroalimentación docente)

### Cambiado
- **Escala de análisis: de horaria a DIARIA.** Las observaciones horarias no son independientes
  (autocorrelación temporal), lo que invalidaba IC y pruebas de hipótesis. Se agrega a una fila
  por estación-día (192.720 → 8.030 filas), escala normativa del MMA. Script: `agregar_diario.py`.
- **Naming con sufijos** `_mean` / `_max` / `_sum` para dejar explícito cada agregado diario.
- Variable objetivo `critico_mp25_dia` (norma MMA) + `mala_calidad_mp25` (calibrada al 12%).
- Se agrega `mp2_5_max` (pico diario) además del promedio.

### Eliminado del producto evaluado
- Enfoque de proyecto de inversión (VAN, TIR, flujo de caja). El curso evalúa validación
  estadística (bootstrap, permutación, Monte Carlo) y un modelo de clasificación, no un caso de
  inversión. El sustento socioeconómico se conserva solo como MOTIVACIÓN del problema.
- Los notebooks de versión horaria y de evaluación económica se archivaron en
  `notebooks/_version_horaria_obsoleta/` (no son entregables).

## [3.0.0] - Enriquecimiento de variables
- 5 variables nuevas (una por tipo) con fuentes oficiales: tipo_estacion (SINCA), 
  nivel_socioeconomico (CASEN), periodo_gec (PPDA), o3 (SINCA), estaciones_en_episodio (MACAM).
- Prueba de inequidad ambiental: Q1 tiene 92% más MP2.5 que Q5 (d=1.47, p<0.001).

## [2.0.0] - Datos reales SINCA
- Base real red SINCA 2022-2023, 11 estaciones.
- Categóricas nominales y ordinales (calidad del aire MMA).
- Diferenciador laboral/fin de semana/festivo.

### Pendiente (próximas sumativas)
- Sumativa 2: bootstrap, tests de permutación, Monte Carlo sobre el dataset diario.
- Sumativa 3: regresión logística (target critico_mp25_dia), split temporal, imputación,
  evaluación con recall/F1/AUC.
