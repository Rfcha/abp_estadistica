# Análisis Estadístico de la Calidad del Aire en Santiago

**Inequidad ambiental, meteorología y episodios críticos de material particulado**

Proyecto del curso **MCDI501 — Estadística Computacional para la Toma de Decisiones**, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

|||
|-|-|
|**Grupo**|Grupo 3|
|**Integrantes**|Rodrigo Chinchón Ayala · Pablo Villalobos González · Sergio Fernández Almonacid|
|**Docente**|Jean Paul Maidana González|
|**Dataset**|Red SINCA — Ministerio del Medio Ambiente, Santiago RM|
|**Escala de análisis**|Estación-día · 2022–2025 · 16.071 observaciones iniciales · 11 estaciones · 46 variables|
|**Notebook principal**|`notebooks/01\_analisis\_estadistico\_diario.ipynb`|
|**Salida HTML**|`outputs/01\_analisis\_estadistico\_diario.html`|
|**Repositorio**|`https://github.com/Rfcha/abp\_estadistica`|

\---

## 1\. Objetivo

Caracterizar estadísticamente la contaminación por **MP2.5** y **MP10** en Santiago de Chile, evaluando si la exposición presenta diferencias relevantes entre **zonas geográficas**, **niveles socioeconómicos** y **condiciones meteorológicas**, con énfasis en episodios críticos y toma de decisiones basada en evidencia.

## 2\. Pregunta movilizadora

> ¿Qué evidencia estadística sustenta que la contaminación por material particulado en Santiago presenta diferencias significativas entre zonas, niveles socioeconómicos y temporadas?

\---

## 3\. Resumen ejecutivo de hallazgos

El análisis se ejecutó a **escala estación-día**, reduciendo la dependencia horaria y haciendo más defendible la inferencia estadística aplicada al quedar libre de autocorrelación horaria. Tras aplicar el filtro de exclusión por cobertura, la muestra efectiva de trabajo se consolidó en **11.603 registros**.

* **MP2.5 como contaminante prioritario:** Media diaria de **24,94 µg/m³**; **551 días-estación sobre norma** equivalente a un **4,75%** de los días válidos.
* **MP10:** Media diaria de **56,66 µg/m³**; **66 días-estación sobre norma** equivalente a un **0,57%** de los días válidos.
* **Inequidad ambiental Q1 vs Q5:** El quintil vulnerable (Q1) promedia **29,40 µg/m³** frente a **16,61 µg/m³** en Q5; una diferencia de **+12,8 µg/m³** (**77% mayor**), con un tamaño de efecto crítico (**d de Cohen = 0,97**).
* **Desigualdad territorial Oriente vs Poniente:** Oriente promedia **16,61 µg/m³** y Poniente **26,33 µg/m³**; diferencia de **9,72 µg/m³** con un tamaño de efecto intermedio-alto (**d de Cohen = -0,76**).
* **Inversión térmica:** Los días con alta inversión térmica promedian **32,15 µg/m³** versus **18,95 µg/m³** en baja inversión, manifestando el impacto físico más adverso (**d de Cohen = 1,05**).
* **Riesgo operativo territorial:** Poniente presenta un **7,62%** de días sobre la norma; Oriente registra un **0,00%** en la muestra analizada.
* **Correlaciones relevantes:** MP2.5 se correlaciona fuertemente con MP10 (**r = 0,901**), de manera moderada y opuesta estacionalmente con el Ozono ($O\_3$, **r = -0,476**) y negativamente con la temperatura media diaria (**r = -0,621**).

Todas las conclusiones reportan **p-valor, tamaño de efecto y decisión estadística**, evitando depender únicamente de la significancia estadística abstracta.

\---

## 4\. Metodología

|Etapa|Procedimiento|
|-|-|
|**Configuración reproducible**|Python 3.12.10, semilla fija 2026, entornos virtuales administrados y paleta visual institucional (`navy`, `rojo`, `slate`).|
|**Carga y tipado**|Lectura de `data/calidad\_aire\_diario.csv`, tipado explícito de variables categóricas ordenadas (Nivel socioeconómico $Q1 \\rightarrow Q5$, Nivel de contaminación, Calidad de aire) para respetar su jerarquía real en gráficas.|
|**Depuración**|Transformación de variables binarias a etiquetas interpretables y control exhaustivo de inconsistencias físicas (e.g., Humedad > 100%, viento < 0, $MP2.5 > MP10$).|
|**Calidad de datos**|Auditoría de faltantes: se identificó un 27,80% en MP2.5 y un 27,58% en MP10 por fallas de cobertura horaria diaria (<18 horas). No se aplica imputación en esta fase (reservado para Sumativa 3).|
|**EDA**|Estadística descriptiva con diagnósticos de forma (asimetría, curtosis), frecuencias oficiales de calidad de aire MMA, correlaciones de Pearson y Spearman, y evolución temporal bivariada por comuna.|
|**Estimación**|Intervalos de confianza al 95% con distribución *t* de Student para variables de centro y método de Wilson para proporciones de superación de norma.|
|**Inferencia**|Configuración de 5 pruebas robustas: 3× *t* de Welch para desigualdad de varianzas, 1× $\\chi^2$ de independencia y 1× prueba Z de proporciones.|

\---

## 5\. Resultados inferenciales consolidados

Todos los contrastes se evaluaron bajo un nivel de significancia estricto de $\\alpha = 0,05$.

|Prueba|Estadístico|p-valor|Efecto|Decisión|
|-|-:|-:|-:|-|
|t Welch — Oriente vs Poniente|t = -20,7|6,0e-176|d = -0,76|Rechaza H0|
|t Welch — Q1 vs Q5 (Inequidad)|t = 30,4|2,1e-180|d = 0,97|Rechaza H0|
|t Welch — Inversión térmica|t = 55,5|0,0e+00|d = 1,05|Rechaza H0|
|$\\chi^2$ — Zona vs Nivel de contaminación|$\\chi^2$ = 308,0|7,4e-62|V = 0,12|Rechaza H0|
|Z — Proporción días sobre norma|z = 10,87|0,0e+00|$\\Delta$ = 0,08 pp|Rechaza H0|

**Conclusión:** Las 5 pruebas rechazan formalmente la hipótesis nula ($H\_0$). La evidencia empírica respalda de forma contundente la existencia de marcadas brechas territoriales, inequidad socioambiental activa en la cuenca y un mecanismo físico meteorológico consistente gobernado por la inversión térmica.

\---

## 6\. Intervalos de Confianza Clave (95%)

Gracias al volumen de la muestra efectiva ($n = 11.603$), se lograron estimaciones puntuales de parámetros poblacionales con márgenes de error estándar mínimos y alta precisión:

* **Media MP2.5:** `\[24,68 ; 25,19]` µg/m³ (Media muestral: 24,94)
* **Proporción de Inversión Térmica:** `\[0,35 ; 0,36]` (Media muestral: 0,36)
* **Temperatura Media Diaria:** `\[14,31 ; 14,51]` °C (Media muestral: 14,41)
* **Radiación Media Diaria:** `\[285,76 ; 289,32]` W/m² (Media muestral: 287,54)
* **Días sobre Norma MP2.5 (Wilson):** `\[4,35% ; 5,18%]` (Proporción muestral: 4,75%)
* **Días sobre Norma MP10 (Wilson):** `\[0,45% ; 0,72%]` (Proporción muestral: 0,57%)

\---

## 7\. Estructura del repositorio

```text
abp_estadistica/
│
├── data/
│   └── calidad_aire_diario.csv
│
├── notebooks/
│   └── 01_analisis_estadistico_diario.ipynb
│
├── figures/
│   └── *.png
│
├── reports/
│   ├── 01_analisis_estadistico_diario_limpio.html
│   ├── Sumativa1_Informe_Tecnico_Final.pdf
│   └── Sumativa1_Informe_Tecnico_Final_Latex.zip
│
├── evidencia/
│
├── .git/
│
├── .gitignore
├── README.md
├── requirements.txt
├── GUIA_GIT.md
├── CHANGELOG.md
├── .mailmap
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── SECURITY.md

---

## 8. Reproducibilidad

El desarrollo técnico fue validado integralmente con Python 3.12.10 y el kernel .venv. Se recomienda encarecidamente inicializar el entorno virtual fuera de carpetas compartidas o sincronizadas de manera activa (como OneDrive o Dropbox) para prevenir bloqueos en la lectura o escritura de archivos durante la instalación de dependencias.

Windows PowerShell

python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name abp\_estadistica --display-name "ABP Estadística"

Ejecutar notebook y generar HTML

jupyter nbconvert --to notebook --execute --inplace notebooks/01\_analisis\_estadistico\_diario.ipynb
jupyter nbconvert --to html notebooks/01\_analisis\_estadistico\_diario.ipynb --output-dir outputs

Verificación rápida del entorno

python -c "import numpy, pandas, matplotlib, seaborn, scipy; print('Entorno OK')"


## 9. Entorno validado (Versiones de la Pila Científica)

Componente             Versión
Python                  3.12.10   
NumPy                   2.5.0   
pandas                  3.0.3   
matplotlib              3.11.0
seaborn                 0.13.2
SciPy                   1.18.0
ipykernel               6.29.5

## 10. Roadmap del Proyecto

\[x] Sumativa 1: Análisis exploratorio formal, estimación puntual, cálculo de intervalos de confianza robustos e inferencia estadística a escala estación-día. 
\[ ] Formativa 2: Profundización en técnicas de estimación robusta, análisis de sesgos e intervalos de confianza avanzados.
\[ ] Sumativa 2: Validación y remuestreo de métricas mediante metodologías de Bootstrap, tests de permutación y simulación estocástica de Monte Carlo.
\[ ] Sumativa 3: Diseño, entrenamiento y evaluación de un modelo de clasificación predictivo binario para la anticipación de episodios críticos (mala\_calidad\_mp25), optimizando métricas operacionales de negocio con foco estricto en Recall, F1-Score y AUC-ROC.

## 11. Fuentes

\*\* Ministerio del Medio Ambiente — Sistema de Información Nacional de Calidad del Aire (SINCA). Gobierno de Chile.  
\*\* Ministerio del Medio Ambiente — D.S. N°12/2011, norma primaria de calidad ambiental para material particulado fino respirable MP2.5.  
\*\* INE, MINVU y CNDU — Sistema de Indicadores y Estándares de Desarrollo Urbano (SIEDU).
\*\* Ministerio de Desarrollo Social — Encuesta de Caracterización Socioeconómica Nacional (CASEN).
\*\* McKinney, W. (2010). Data structures for statistical computing in Python.  
\*\* Montgomery, D. C., \& Runger, G. C. (2018). Applied Statistics and Probability for Engineers.
\*\* Cohen, J. (1988). Statistical power analysis for the behavioral sciences (2.ª ed.). 
\*\* Virtanen et al. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. Nature Methods.  

