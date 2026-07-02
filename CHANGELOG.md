# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y el proyecto sigue un versionado por fases del curso MCDI501.

---

## [1.0.1] — 2026-07-01 — Actualización documental según notebook ejecutado y salida HTML

Actualización de documentación del repositorio en base al notebook `01_analisis_estadistico_diario.ipynb` y su salida HTML ejecutada.

### Actualizado
- `README.md` alineado con los resultados efectivos del notebook y la salida HTML.
- `requirements.txt` actualizado con dependencias de ejecución, render HTML y kernel Jupyter.
- `GUIA_GIT.md` reforzada con flujo de ramas, Pull Requests, exportación HTML, manejo de notebooks y checklist de entrega.
- `.mailmap` revisado para consolidar identidades del Grupo 3 y variantes de GitHub.
- Se corrige la documentación de inferencia: el notebook contiene **5 pruebas**, no 4.

### Resultados documentados
- MP2.5: media diaria **24,94 µg/m³** y **551 días-estación sobre norma** (**4,75 %**).
- MP10: **66 días-estación sobre norma** (**0,57 %**).
- Oriente vs Poniente: medias **16,61** vs **26,33 µg/m³**, diferencia **9,72 µg/m³**, *d* = **-0,76**.
- Q1 vs Q5: medias **29,40** vs **16,61 µg/m³**, diferencia **12,8 µg/m³**, *d* = **0,97**.
- Alta vs baja inversión térmica: medias **32,15** vs **18,95 µg/m³**, *d* = **1,05**.
- Zona × nivel de contaminación: χ² = **308,2**, V de Cramér = **0,115**.
- Proporción sobre norma Poniente vs Oriente: **7,62 %** vs **0,00 %**, z = **10,87**.
- Síntesis inferencial: **5 de 5 pruebas rechazan H0** con α = 0,05.

---

## [1.0.0] — 2026-06-28 — Sumativa 1: Informe técnico de avance

Primera entrega evaluada: análisis exploratorio, estimación e inferencia estadística a escala estación-día.

### Añadido
- Notebook `01_analisis_estadistico_diario.ipynb` con análisis completo, ejecutable de principio a fin y documentado celda a celda.
- Dataset `data/calidad_aire_diario.csv` a escala estación-día: 2022–2025, 11 estaciones y 36 variables.
- Helper `guardar_figura()` para exportación robusta de figuras.
- `requirements.txt` con versiones exactas del entorno validado.
- README inicial con objetivo, hallazgos, metodología, estructura y guía de reproducibilidad.

### Análisis incluido
- **Calidad de datos:** auditoría de faltantes, duplicados e inconsistencias físicas.
- **Estadística descriptiva:** tendencia central, dispersión, CV %, asimetría, curtosis y frecuencias de categóricas.
- **Análisis bivariado:** correlaciones Pearson/Spearman y lectura meteorológica.
- **Estimación:** intervalos de confianza al 95 % e IC Wilson para proporciones.
- **Inferencia:** pruebas de Welch, chi-cuadrado y proporciones con tamaño de efecto.

---

## [No publicado] — Próximas fases

### Planificado — Sumativa 2
- Intervalos de confianza por **bootstrap**.
- **Tests de permutación** y simulación de **Monte Carlo** para validar hallazgos sin depender de supuestos paramétricos.

### Planificado — Sumativa 3
- Modelo de **clasificación binaria** de episodios críticos (`mala_calidad_mp25`).
- Evaluación con recall, F1 y AUC.
- División estratificada temporal para reducir riesgo de fuga de información.
- Imputación y tratamiento metodológico de faltantes reales.
