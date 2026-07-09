# Análisis Estadístico de la Calidad del Aire en Santiago

**Inequidad ambiental, meteorología y episodios críticos de material particulado**

Proyecto del curso **MCDI501 — Estadística Computacional para la Toma de Decisiones**, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

| | |
|-|-|
|**Grupo**|Grupo 3|
|**Integrantes**|Rodrigo Chinchón Ayala · Pablo Villalobos González · Sergio Fernández Almonacid|
|**Docente**|Jean Paul Maidana González|
|**Dataset**|Red SINCA — Ministerio del Medio Ambiente, Santiago RM|
|**Escala de análisis**|Estación-día · 2022–2025 · 16.071 observaciones iniciales · 11 estaciones · 46 variables|
|**Muestra efectiva consolidada S1/S2**|11.603 registros válidos a escala estación-día|
|**Notebook S1**|`notebooks/01_analisis_estadistico_diario.ipynb`|
|**Notebook S2**|`notebooks/02_validacion_simulacion_remuestreo.ipynb`|
|**Preparación S3**|Modelamiento predictivo binario de episodios críticos `mala_calidad_mp25`|
|**Repositorio**|`https://github.com/Rfcha/abp_estadistica`|

---

## 1. Objetivo

Caracterizar estadísticamente la contaminación por **MP2.5** y **MP10** en Santiago de Chile, evaluando si la exposición presenta diferencias relevantes entre **zonas geográficas**, **niveles socioeconómicos** y **condiciones meteorológicas**, con énfasis en episodios críticos, robustez inferencial y toma de decisiones basada en evidencia.

Este README consolida el trabajo de **Sumativa 1** y **Sumativa 2**, incorpora las observaciones docentes recibidas y deja preparado el repositorio para la **Sumativa 3**, orientada al diseño, entrenamiento y evaluación de un modelo predictivo.

---

## 2. Pregunta movilizadora

> ¿Qué evidencia estadística sustenta que la contaminación por material particulado en Santiago presenta diferencias significativas entre zonas, niveles socioeconómicos y temporadas?

---

## 3. Resumen ejecutivo consolidado S1 + S2

El análisis se ejecutó a **escala estación-día**, reduciendo la dependencia horaria y haciendo más defendible la inferencia estadística aplicada al quedar libre de autocorrelación horaria. Tras aplicar el filtro de exclusión por cobertura, la muestra efectiva de trabajo se consolidó en **11.603 registros**.

### 3.1 Hallazgos principales de Sumativa 1

* **MP2.5 como contaminante prioritario:** media diaria de **24,94 µg/m³**; **551 días-estación sobre norma**, equivalente a un **4,75%** de los días válidos.
* **MP10:** media diaria de **56,66 µg/m³**; **66 días-estación sobre norma**, equivalente a un **0,57%** de los días válidos.
* **Inequidad ambiental Q1 vs Q5:** el quintil vulnerable (Q1) promedia **29,40 µg/m³** frente a **16,61 µg/m³** en Q5; diferencia de **+12,8 µg/m³** (**77% mayor**), con tamaño de efecto crítico (**d de Cohen = 0,97**).
* **Desigualdad territorial Oriente vs Poniente:** Oriente promedia **16,61 µg/m³** y Poniente **26,33 µg/m³**; diferencia de **9,72 µg/m³**, con tamaño de efecto intermedio-alto (**d de Cohen = -0,76**).
* **Inversión térmica:** los días con alta inversión térmica promedian **32,15 µg/m³** versus **18,95 µg/m³** en baja inversión, manifestando el impacto físico más adverso (**d de Cohen = 1,05**).
* **Riesgo operativo territorial:** Poniente presenta un **7,62%** de días sobre la norma; Oriente registra **0,00%** en la muestra analizada.
* **Correlaciones relevantes:** MP2.5 se correlaciona fuertemente con MP10 (**r = 0,9011**), negativamente con temperatura media diaria (**r = -0,6206**), positivamente con proporción de inversión térmica (**r = 0,5194**) y con humedad media (**r = 0,3261**).

Todas las conclusiones de S1 reportan **p-valor, tamaño de efecto y decisión estadística**, evitando depender únicamente de la significancia estadística abstracta.

### 3.2 Hallazgos principales de Sumativa 2

La Sumativa 2 validó computacionalmente los resultados centrales de S1 mediante **bootstrap no paramétrico**, **test de permutación**, **estabilidad de correlaciones**, **simulación Monte Carlo** y **análisis de robustez**.

* **Bootstrap:** los intervalos BCa al 95% convergen con los intervalos clásicos de S1 para media MP2.5, media MP10 y proporción de mala calidad MP2.5, con sesgo prácticamente nulo.
* **Permutación:** la diferencia de MP2.5 entre invierno y resto del año se mantiene significativa y concordante con Welch, validando que el resultado no depende exclusivamente de supuestos paramétricos.
* **Correlaciones:** las cinco correlaciones evaluadas son robustas; ninguna cruza cero en su intervalo bootstrap al 95%.
* **Colinealidad crítica:** MP2.5 y MP10 presentan **r = 0,9011**; no deben incorporarse simultáneamente en modelos predictivos sin control formal de multicolinealidad, como VIF, PCA o selección de características.
* **Monte Carlo:** usando parámetros de S1 y una distribución lognormal calibrada, se estimó **P(MP2.5 > 50 µg/m³) = 5,05%**, **P(MP2.5 > 80 µg/m³) = 0,65%** y **P(MP2.5 > 110 µg/m³) = 0,10%**.
* **Robustez:** las medias de MP2.5 y MP10 son confiables frente a remoción de outliers IQR; la probabilidad simulada **P(MP2.5 > 50)** es sensible al supuesto distribucional alternativo y debe reportarse con cautela.

---

## 4. Observaciones docentes incorporadas

Se incorporan explícitamente los ajustes derivados de la revisión de Sumativa 1:

|Observación docente|Acción aplicada en README / repositorio|
|-|-|
|Aclarar inconsistencia del estadístico Welch Oriente vs Poniente.|Se consolida la cifra corregida: **t = -29,73**, **p = 6,01e-176**, media Oriente = **16,61**, media Poniente = **26,33**.|
|Evitar contradicción entre “cuatro pruebas” y la tabla real.|Se declara formalmente que S1 contiene **cinco pruebas inferenciales**: tres Welch, una chi-cuadrado y una Z de proporciones.|
|Mantener trazabilidad de H0/H1, p-valor y decisión.|Cada prueba conserva su lectura estadística: hipótesis, estadístico, p-valor, tamaño de efecto y decisión.|
|Documentar calidad de datos.|Se conserva el reporte de faltantes exactos en MP2.5 y MP10, cero duplicados, cero inconsistencias físicas y decisión de postergar imputación a S3.|
|Reforzar temperatura y radiación.|Se agrega control de consistencia para variables meteorológicas y su rol en S3.|
|Preparar S3.|Se define estrategia de cobertura horaria, imputación simple/mediana, control de colinealidad, selección de variables y modelamiento binario.|
|Eliminar instrucciones internas de entrega.|El README queda como documento final del repositorio, sin notas internas dirigidas al equipo.|

---

## 5. Metodología consolidada

|Etapa|Procedimiento|
|-|-|
|**Configuración reproducible**|Python 3.12.10, semilla fija 2026, entorno virtual `.venv`, kernel dedicado y estructura de carpetas versionada.|
|**Carga y tipado**|Lectura de `data/calidad_aire_diario.csv`, tipado explícito de variables categóricas ordenadas: nivel socioeconómico `Q1 → Q5`, nivel de contaminación y calidad de aire.|
|**Depuración**|Transformación de variables binarias a etiquetas interpretables y control exhaustivo de inconsistencias físicas: humedad > 100%, viento < 0, MP2.5 > MP10 y valores imposibles.|
|**Calidad de datos**|Auditoría de faltantes: **27,80% en MP2.5** y **27,58% en MP10** por fallas de cobertura horaria diaria menor a 18 horas. Se confirma cero duplicados y cero inconsistencias físicas. No se imputa en S1/S2; la imputación queda reservada y documentada para S3.|
|**EDA S1**|Estadística descriptiva, diagnósticos de forma, frecuencias oficiales de calidad de aire MMA, correlaciones Pearson/Spearman y evolución temporal bivariada por comuna.|
|**Estimación S1**|Intervalos de confianza al 95% con distribución *t* de Student para variables de centro y método Wilson para proporciones de superación de norma.|
|**Inferencia S1**|Cinco pruebas robustas: 3× *t* de Welch para desigualdad de varianzas, 1× chi-cuadrado de independencia y 1× prueba Z de proporciones.|
|**Validación S2**|Bootstrap no paramétrico con 10.000 remuestras, IC percentil e IC BCa, permutación con 10.000 iteraciones, estabilidad de correlaciones, Monte Carlo y análisis de robustez.|
|**Preparación S3**|Definición de variable objetivo `mala_calidad_mp25`, tratamiento de cobertura horaria, imputación controlada, validación de colinealidad y selección de variables predictoras.|

---

## 6. Resultados inferenciales consolidados de Sumativa 1

Todos los contrastes se evaluaron bajo un nivel de significancia estricto de **α = 0,05**.

|Prueba|Estadístico|p-valor|Efecto|Decisión|
|-|-:|-:|-:|-|
|t Welch — Oriente vs Poniente|t = -29,73|6,01e-176|d = -0,76|Rechaza H0|
|t Welch — Q1 vs Q5 (Inequidad)|t = 30,4|2,1e-180|d = 0,97|Rechaza H0|
|t Welch — Inversión térmica|t = 55,5|0,0e+00|d = 1,05|Rechaza H0|
|Chi-cuadrado — Zona vs Nivel de contaminación|χ² = 308,0|7,4e-62|V = 0,12|Rechaza H0|
|Z — Proporción días sobre norma|z = 10,87|0,0e+00|Δ = 0,08 pp|Rechaza H0|

**Conclusión S1:** las cinco pruebas rechazan formalmente la hipótesis nula. La evidencia empírica respalda la existencia de brechas territoriales, inequidad socioambiental activa en la cuenca y un mecanismo meteorológico consistente asociado a inversión térmica.

---

## 7. Intervalos de confianza clave de Sumativa 1 (95%)

Gracias al volumen de la muestra efectiva (**n = 11.603**), se lograron estimaciones puntuales de parámetros poblacionales con márgenes de error estándar mínimos y alta precisión:

* **Media MP2.5:** `[24,68 ; 25,19]` µg/m³ — media muestral: **24,94**.
* **Media MP10:** `[56,20 ; 57,09]` µg/m³ — media muestral: **56,66**.
* **Proporción de inversión térmica:** `[0,35 ; 0,36]` — media muestral: **0,36**.
* **Temperatura media diaria:** `[14,31 ; 14,51]` °C — media muestral: **14,41**.
* **Radiación media diaria:** `[285,76 ; 289,32]` W/m² — media muestral: **287,54**.
* **Días sobre norma MP2.5 (Wilson):** `[4,35% ; 5,18%]` — proporción muestral: **4,75%**.
* **Días sobre norma MP10 (Wilson):** `[0,45% ; 0,72%]` — proporción muestral: **0,57%**.

---

## 8. Validación robusta de Sumativa 2

### 8.1 Bootstrap no paramétrico

Se aplicó bootstrap no paramétrico con **10.000 remuestras** sobre tres parámetros estimados en S1: media MP2.5, media MP10 y proporción de días con mala calidad MP2.5.

|Parámetro|S1|IC clásico Li|IC clásico Ls|BCa Li|BCa Ls|Sesgo|
|-|-:|-:|-:|-:|-:|-:|
|Media MP2.5|24,9382|24,6836|25,1928|24,6850|25,2015|-0,0000|
|Media MP10|56,6438|56,1958|57,0918|56,1934|57,1119|0,0000|
|Proporción mala calidad MP2.5|0,1201|0,1143|0,1261|0,1143|0,1261|-0,0000|

**Conclusión:** los intervalos BCa al 95% se mantienen prácticamente alineados con los intervalos clásicos, validando la estabilidad de los estimadores centrales de S1.

### 8.2 Validación de hipótesis mediante permutación

|Prueba|G1|G2|n1|n2|Dif. obs.|p Welch|p perm.|Conclusión|
|-|-|-|-:|-:|-:|-:|-:|-|
|MP2.5: Invierno vs Resto del año|Invierno|Resto del año|3.915|7.688|22,3165|0,00e+00|0,00e+00|Concordante|

**Conclusión:** la prueba de permutación confirma que la diferencia de medias entre invierno y el resto del año no depende estrictamente de supuestos paramétricos.

### 8.3 Estabilidad de correlaciones

|X|Y|r S1|IC Li|IC Ls|Estado|
|-|-|-:|-:|-:|-|
|mp2_5_mean|mp10_mean|0,9011|0,8961|0,9058|Robusta|
|mp2_5_mean|humedad_mean|0,3261|0,3065|0,3453|Robusta|
|mp2_5_mean|temperatura_mean|-0,6206|-0,6307|-0,6104|Robusta|
|mp2_5_mean|viento_mean|0,1846|0,1591|0,2106|Robusta|
|mp2_5_mean|prop_inversion|0,5194|0,5013|0,5373|Robusta|

**Conclusión:** todas las correlaciones son estables, pero la relación MP2.5–MP10 exige control de multicolinealidad antes de S3.

### 8.4 Simulación Monte Carlo

La simulación Monte Carlo generó **10.000 escenarios diarios de MP2.5**, usando media y desviación estándar estimadas en S1 y una distribución lognormal calibrada.

|Iteraciones|Media S1|SD S1|Media simulada|P95|P(MP2.5 > 50)|P(MP2.5 > 80)|P(MP2.5 > 110)|
|-:|-:|-:|-:|-:|-:|-:|-:|
|10.000|24,94|13,99|24,57|50,05|5,05%|0,65%|0,10%|

**Conclusión:** Monte Carlo entrega una métrica probabilística interpretable para escenarios de riesgo ambiental, útil como insumo para S3, aunque sensible a la distribución asumida.

### 8.5 Robustez y sensibilidad

|Resultado|Original|Robusto|Método|Variación %|Conclusión|
|-|-:|-:|-|-:|-|
|Media MP2.5|24,9382|24,2523|Remoción outliers IQR|-2,75%|Confiable|
|Media MP10|56,6438|54,9694|Remoción outliers IQR|-2,96%|Confiable|
|IC media MP2.5|24,9382|24,9382|Jackknife|0,00%|Confiable|
|P(MP2.5 > 50)|0,0505|0,0418|Normal truncada alternativa|-17,23%|Sensible / cautela|

**Conclusión:** las medias son robustas frente a outliers y jackknife. La probabilidad de excedencia debe reportarse con cautela porque depende del supuesto distribucional.

---

## 9. Preparación metodológica para Sumativa 3

La Sumativa 3 debe construir un modelo predictivo binario para anticipar episodios críticos de calidad del aire, usando como base los resultados validados de S1 y S2.

### 9.1 Variable objetivo sugerida

|Variable|Definición|Uso en S3|
|-|-|-|
|`mala_calidad_mp25`|Indicador binario asociado a días con mala calidad por MP2.5.|Variable objetivo principal para clasificación.|

### 9.2 Variables candidatas

|Familia|Variables sugeridas|Consideración|
|-|-|-|
|Material particulado|MP2.5, MP10|No usar MP2.5 y MP10 simultáneamente sin control por colinealidad.|
|Meteorología|temperatura, humedad, viento, radiación, inversión térmica|Mantener por fundamento físico y evidencia S1/S2.|
|Temporalidad|mes, estación, periodo GEC, invierno, fin de semana, festivo|Útiles para capturar estacionalidad.|
|Territorio|zona geográfica, comuna, estación, quintil socioeconómico|Útiles para inequidad territorial y segmentación de riesgo.|
|Calidad de datos|cobertura horaria, flags de completitud|Incluir para evitar sesgo por casos completos.|

### 9.3 Controles mínimos exigidos para S3

* Mantener **semilla aleatoria fija 2026**.
* Separar entrenamiento y prueba evitando fuga temporal o territorial.
* Evaluar imputación simple/mediana y documentar su impacto.
* Controlar multicolinealidad con **VIF**, **PCA** o selección de características.
* Reportar matriz de confusión, Recall, Precision, F1-Score, AUC-ROC y curva PR si existe desbalance.
* Priorizar **Recall** para no perder episodios críticos, sin descuidar F1-Score.
* Mantener trazabilidad entre S1, S2 y S3 mediante archivos de resultados validados.

### 9.4 Archivo puente recomendado para S3

Se recomienda mantener y versionar el archivo:

```text
resultados/s2_reporte_resultados_validados_para_s3.csv
```

Este archivo debe consolidar parámetros robustos, correlaciones estables, hallazgos sensibles, decisiones metodológicas y recomendaciones de uso para modelamiento predictivo.

---

## 10. Estructura actualizada del repositorio

```text
abp_estadistica/
│
├── .venv/
│
├── data/
│   └── calidad_aire_diario.csv
│
├── evidencia/
│
├── figures/
│   └── *.png
│
├── notebooks/
│   ├── _version_horaria_obsoleta/
│   ├── 01_analisis_estadistico_diario.ipynb
│   ├── 02_validacion_simulacion_remuestreo.ipynb
│   └── Formativa2_Modelamiento_Predictivo_Grupo3.ipynb
│
├── reports/
│   ├── 01_analisis_estadistico_diario_limpio.html
│   ├── 02_validacion_simulacion_remuestreo.html
│   ├── Formativa2_Modelamiento_Predictivo_Grupo3.html
│   ├── Formativa2_Modelamiento_Predictivo_Grupo3.PDF
│   ├── Formativa2_Modelamiento_Predictivo_Grupo3.zip
│   ├── Sumativa1_Informe_Tecnico_Final.pdf
│   ├── Sumativa1_Informe_Tecnico_Final_Latex.zip
│   ├── Sumativa2_Validacion_Simulacion_Remuestreo_Grupo3.pdf
│   └── Sumativa2_Validacion_Simulacion_Remuestreo_Grupo3.zip
│
├── resultados/
│   └── s2_reporte_resultados_validados_para_s3.csv
│
├── .gitignore
├── .mailmap
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── GUIA_GIT.md
├── LICENSE
├── README.md
├── requirements.txt
└── SECURITY.md
```

---

## 11. Reproducibilidad

El desarrollo técnico fue validado integralmente con **Python 3.12.10** y kernel `.venv`. Se recomienda inicializar el entorno virtual fuera de carpetas compartidas o sincronizadas activamente, como OneDrive o Dropbox, para prevenir bloqueos de lectura/escritura durante la instalación de dependencias.

### 11.1 Crear entorno en Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name abp_estadistica --display-name "ABP Estadística"
```

### 11.2 Ejecutar notebooks principales

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_estadistico_diario.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_validacion_simulacion_remuestreo.ipynb
```

### 11.3 Generar reportes HTML

```powershell
jupyter nbconvert --to html notebooks/01_analisis_estadistico_diario.ipynb --output-dir reports
jupyter nbconvert --to html notebooks/02_validacion_simulacion_remuestreo.ipynb --output-dir reports
```

### 11.4 Verificación rápida del entorno

```powershell
python -c "import numpy, pandas, matplotlib, seaborn, scipy; print('Entorno OK')"
```

---

## 12. Entorno validado

|Componente|Versión|
|-|-:|
|Python|3.12.10|
|NumPy|2.5.0|
|pandas|3.0.3|
|matplotlib|3.11.0|
|seaborn|0.13.2|
|SciPy|1.18.0|
|ipykernel|6.29.5|

---

## 13. Roadmap del proyecto

- [x] **Sumativa 1:** análisis exploratorio formal, estimación puntual, intervalos de confianza robustos e inferencia estadística a escala estación-día.
- [x] **Formativa 2:** preparación exploratoria para modelamiento predictivo y revisión de criterios de clasificación.
- [x] **Sumativa 2:** validación y remuestreo de métricas mediante bootstrap, tests de permutación, estabilidad de correlaciones, Monte Carlo y análisis de robustez.
- [ ] **Sumativa 3:** diseño, entrenamiento y evaluación de un modelo de clasificación predictivo binario para anticipar episodios críticos `mala_calidad_mp25`, optimizando Recall, F1-Score y AUC-ROC.

---

## 14. Checklist de control para entrega

|Criterio|Estado|
|-|-|
|README consolidado S1 + S2|OK|
|Observaciones docentes S1 incorporadas|OK|
|Corrección Welch Oriente vs Poniente|OK|
|Cinco pruebas inferenciales declaradas|OK|
|Calidad de datos documentada|OK|
|Semilla reproducible declarada|OK|
|Repositorio con carpetas `data`, `notebooks`, `figures`, `reports`, `evidencia`, `resultados`|OK|
|Notebook S1 identificado|OK|
|Notebook S2 identificado|OK|
|Archivo puente para S3 recomendado|OK|
|Preparación metodológica S3 documentada|OK|

---

## 15. Fuentes

* Ministerio del Medio Ambiente — Sistema de Información Nacional de Calidad del Aire (SINCA). Gobierno de Chile.
* Ministerio del Medio Ambiente — D.S. N°12/2011, norma primaria de calidad ambiental para material particulado fino respirable MP2.5.
* INE, MINVU y CNDU — Sistema de Indicadores y Estándares de Desarrollo Urbano (SIEDU).
* Ministerio de Desarrollo Social — Encuesta de Caracterización Socioeconómica Nacional (CASEN).
* Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
* Good, P. (2005). *Permutation, Parametric and Bootstrap Tests of Hypotheses*. Springer.
* Rubinstein, R. Y., & Kroese, D. P. (2016). *Simulation and the Monte Carlo Method*. Wiley.
* McKinney, W. (2010). Data structures for statistical computing in Python.
* Montgomery, D. C., & Runger, G. C. (2018). *Applied Statistics and Probability for Engineers*.
* Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2.ª ed.).
* Virtanen et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods*.
* Universidad Andrés Bello. MCDI501 — Estadística Computacional para la Toma de Decisiones. Pauta Sumativa 2.
