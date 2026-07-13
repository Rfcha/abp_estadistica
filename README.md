# Análisis Estadístico de la Calidad del Aire en Santiago

**Inequidad ambiental, meteorología, validación robusta y nowcasting de mala calidad por MP2.5**

Proyecto del curso **MCDI501 — Estadística Computacional para la Toma de Decisiones**, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

| | |
|-|-|
|**Grupo**|Grupo 3|
|**Integrantes**|Rodrigo Chinchón Ayala · Pablo Villalobos González · Sergio Fernández Almonacid|
|**Docente**|Jean Paul Maidana González|
|**Dataset**|Red SINCA — Ministerio del Medio Ambiente, Santiago RM|
|**Periodo y escala**|Estación-día · 2022–2025 · 11 estaciones|
|**Estructura de datos**|CSV físico: 16.071 × 36 · matriz armonizada: 16.071 × 46|
|**Muestra efectiva S1/S2/S3**|11.603 registros válidos a escala estación-día|
|**Notebook S1**|`notebooks/01_analisis_estadistico_diario.ipynb`|
|**Notebook S2**|`notebooks/02_validacion_simulacion_remuestreo.ipynb`|
|**Notebook S3**|`notebooks/03_Modelamiento_predictivo_binario_mala_calidad_mp25.ipynb`|
|**Resultado S3**|Modelo final `M2_Forward_AIC_BIC` · casos completos · nowcasting estación-día|
|**Repositorio**|`https://github.com/Rfcha/abp_estadistica`|

---

## 1. Objetivo y alcance

Caracterizar estadísticamente la contaminación por **MP2.5** y **MP10** en Santiago de Chile, evaluar diferencias entre **zonas geográficas**, **niveles socioeconómicos**, **temporadas** y **condiciones meteorológicas**, validar la robustez de los hallazgos y desarrollar un clasificador binario de **nowcasting contemporáneo** para `mala_calidad_mp25`.

Este README consolida las Sumativas **1, 2 y 3** y documenta sus datos, decisiones metodológicas, resultados, diagnósticos, limitaciones y mecanismos de reproducibilidad.

---

## 2. Preguntas movilizadoras

> **Pregunta estadística:** ¿Qué evidencia sustenta que la contaminación por material particulado en Santiago presenta diferencias significativas entre zonas, niveles socioeconómicos, temporadas y condiciones meteorológicas?

> **Pregunta predictiva:** ¿Con qué desempeño puede clasificarse la condición diaria contemporánea `mala_calidad_mp25` sin fuga de información y con validación temporal?

---

## 3. Resumen ejecutivo consolidado S1 + S2 + S3

El análisis se realizó a escala **estación-día**. Esta agregación reduce la dependencia intradía respecto de datos horarios, pero no implica ausencia automática de autocorrelación temporal o espacial. La muestra efectiva común fue de **11.603 registros**.

|Sumativa|Propósito|Resultados principales|
|-|-|-|
|**S1 — Análisis e inferencia**|Caracterizar contaminación, desigualdad territorial y efecto meteorológico.|MP2.5: media **24,94 µg/m³** y **4,75%** sobre 50 µg/m³. MP10: media **56,66 µg/m³** y **0,57%** sobre norma. Q1 promedió **29,40** frente a **16,61 µg/m³** en Q5; Poniente **26,33** frente a **16,61 µg/m³** en Oriente. La inversión térmica presentó el mayor efecto observado (**d = 1,05**).|
|**S2 — Validación robusta**|Comprobar estabilidad mediante remuestreo, permutación, Monte Carlo y sensibilidad.|Los IC BCa convergieron con los clásicos; las cinco correlaciones evaluadas fueron robustas. Monte Carlo estimó **P(MP2.5 > 50) = 5,05%**, resultado sensible al supuesto distribucional (**−17,23%** bajo normal truncada).|
|**S3 — Modelamiento binario**|Clasificar `mala_calidad_mp25` para el mismo día observado.|Modelo final `M2_Forward_AIC_BIC`, casos completos, con `mp10_mean`, `temporada_critica` y `viento_mean`. En prueba futura: Recall **0,937**, F2 **0,845**, ROC-AUC **0,979**, PR-AUC **0,823** y Brier **0,044**.|

La prevalencia S3 de **12,01%** corresponde a la etiqueta original `mala_calidad_mp25` y no es equivalente al **4,75%** de observaciones sobre 50 µg/m³ calculado en S1.

---

## 4. Observaciones docentes y decisiones de consistencia

|Observación o riesgo|Acción aplicada|
|-|-|
|Inconsistencia Welch Oriente vs Poniente.|Se consolidó **t = −29,73**, **p = 6,01e−176**, media Oriente **16,61** y Poniente **26,33 µg/m³**.|
|Contradicción entre “cuatro pruebas” y la tabla real.|S1 se documenta con **cinco pruebas**: tres Welch, una chi-cuadrado y una Z de proporciones.|
|Trazabilidad inferencial incompleta.|Se mantienen hipótesis, estadístico, p-valor, tamaño de efecto y decisión.|
|Calidad, faltantes y cobertura.|Se conservaron los faltantes de S1/S2 y se documentó por separado la anomalía del indicador reconstruido en S3.|
|Correlación MP2.5–MP10 y fuga de información.|MP2.5 y sus derivados se bloquearon; `mp10_mean` se restringió al escenario contemporáneo y se controló con VIF.|
|Tratamiento de faltantes.|Se compararon casos completos, mediana agrupada y regresión multivariada, incluyendo retención, error de imputación, métricas e intervalos.|
|Validación y estabilidad del modelo.|Se aplicaron partición temporal, validación expansiva, calibración OOF, inferencia robusta, sensibilidad L2 y bootstrap.|
|Resultados sensibles y reglas de uso.|La excedencia Monte Carlo se mantiene como sensible; el modelo se declara nowcasting y sus asociaciones no se interpretan causalmente.|

---

## 5. Metodología consolidada

|Etapa|Procedimiento|
|-|-|
|**Configuración reproducible**|Python 3.12.10, semilla fija 2026, entorno virtual `.venv`, kernel dedicado y estructura versionada.|
|**Carga y tipado**|Lectura de `data/calidad_aire_diario.csv` y tipado explícito de variables numéricas, binarias y categóricas ordenadas.|
|**Depuración**|Control de fechas, duplicados, rangos físicos y consistencia entre variables ambientales.|
|**Calidad S1/S2**|Faltantes de **27,80% en MP2.5** y **27,58% en MP10** asociados al criterio de cobertura diaria; cero duplicados exactos y cero inconsistencias físicas reportadas. No se imputó la variable objetivo.|
|**EDA e inferencia S1**|Descriptivos, distribución, correlaciones, evolución temporal, IC al 95%, tres Welch, chi-cuadrado y prueba Z.|
|**Validación S2**|10.000 remuestras bootstrap, IC percentil/BCa, 10.000 permutaciones, estabilidad de correlaciones, Monte Carlo y sensibilidad.|
|**Diseño S3**|Objetivo `mala_calidad_mp25`, auditoría de fuga, lista blanca, separación 70/30 sobre el horizonte temporal y cinco bloques de validación expansiva.|
|**Comparación S3**|Tres modelos × tres estrategias de faltantes, selección AIC/BIC, linealidad del logit y calibración Platt OOF.|
|**Inferencia y estabilidad S3**|GLM binomial no ponderado, OR, covarianza agrupada por fecha, VIF, residuos, influencia, sensibilidad L2 y 10.000 bootstrap.|
|**Operación S3**|Umbral F2 con Recall mínimo, escenario de costos FN/FP, análisis por subgrupos y reglas de monitoreo.|

---

## 6. Resultados consolidados de Sumativa 1

### 6.1 Hallazgos descriptivos y efectos

|Dimensión|Resultado|
|-|-|
|MP2.5|Media **24,94 µg/m³**; **551 días-estación** sobre 50 µg/m³ (**4,75%**).|
|MP10|Media **56,66 µg/m³**; **66 días-estación** sobre norma (**0,57%**).|
|Inequidad Q1 vs Q5|Q1 **29,40** frente a Q5 **16,61 µg/m³**; diferencia **+12,8 µg/m³** (**77%**) y **d = 0,97**.|
|Oriente vs Poniente|Oriente **16,61** frente a Poniente **26,33 µg/m³**; diferencia **9,72 µg/m³** y **d = −0,76**.|
|Inversión térmica|Alta inversión **32,15** frente a baja inversión **18,95 µg/m³**; **d = 1,05**.|
|Días sobre norma MP2.5|Poniente **7,62%** frente a Oriente **0,00%**.|

### 6.2 Contrastes inferenciales

Todos los contrastes se evaluaron con **α = 0,05**.

|Prueba|Estadístico|p-valor|Efecto|Decisión|
|-|-:|-:|-:|-|
|t Welch — Oriente vs Poniente|t = −29,73|6,01e−176|d = −0,76|Rechaza H0|
|t Welch — Q1 vs Q5|t = 30,4|2,1e−180|d = 0,97|Rechaza H0|
|t Welch — Inversión térmica|t = 55,5|0,0e+00|d = 1,05|Rechaza H0|
|Chi-cuadrado — Zona vs nivel de contaminación|χ² = 308,0|7,4e−62|V = 0,12|Rechaza H0|
|Z — Proporción de días sobre norma|z = 10,87|0,0e+00|Δ = 0,0762 (**7,62 pp**)|Rechaza H0|

**Conclusión:** las cinco pruebas rechazan la hipótesis nula. La evidencia respalda brechas territoriales y socioeconómicas, además de un mecanismo meteorológico consistente asociado a la inversión térmica.

### 6.3 Intervalos de confianza clave (95%)

|Parámetro|Estimación|IC 95%|
|-|-:|-|
|Media MP2.5|24,94 µg/m³|[24,68; 25,19]|
|Media MP10|56,66 µg/m³|[56,20; 57,09]|
|Proporción de inversión térmica|0,36|[0,35; 0,36]|
|Temperatura media diaria|14,41 °C|[14,31; 14,51]|
|Radiación media diaria|287,54 W/m²|[285,76; 289,32]|
|Días sobre norma MP2.5 — Wilson|4,75%|[4,35%; 5,18%]|
|Días sobre norma MP10 — Wilson|0,57%|[0,45%; 0,72%]|

---

## 7. Validación robusta de Sumativa 2

### 7.1 Bootstrap no paramétrico

Se aplicó bootstrap no paramétrico con **10.000 remuestras** sobre tres parámetros estimados en S1: media MP2.5, media MP10 y proporción de días con mala calidad MP2.5.

|Parámetro|S1|IC clásico Li|IC clásico Ls|BCa Li|BCa Ls|Sesgo|
|-|-:|-:|-:|-:|-:|-:|
|Media MP2.5|24,9382|24,6836|25,1928|24,6850|25,2015|-0,0000|
|Media MP10|56,6438|56,1958|57,0918|56,1934|57,1119|0,0000|
|Proporción mala calidad MP2.5|0,1201|0,1143|0,1261|0,1143|0,1261|-0,0000|

**Conclusión:** los intervalos BCa al 95% se mantienen prácticamente alineados con los intervalos clásicos, validando la estabilidad de los estimadores centrales de S1.

### 7.2 Validación de hipótesis mediante permutación

|Prueba|G1|G2|n1|n2|Dif. obs.|p Welch|p perm.|Conclusión|
|-|-|-|-:|-:|-:|-:|-:|-|
|MP2.5: Invierno vs Resto del año|Invierno|Resto del año|3.915|7.688|22,3165|0,00e+00|0,00e+00|Concordante|

**Conclusión:** la prueba de permutación confirma que la diferencia de medias entre invierno y el resto del año no depende estrictamente de supuestos paramétricos.

### 7.3 Estabilidad de correlaciones

|X|Y|r S1|IC Li|IC Ls|Estado|
|-|-|-:|-:|-:|-|
|mp2_5_mean|mp10_mean|0,9011|0,8961|0,9058|Robusta|
|mp2_5_mean|humedad_mean|0,3261|0,3065|0,3453|Robusta|
|mp2_5_mean|temperatura_mean|-0,6206|-0,6307|-0,6104|Robusta|
|mp2_5_mean|viento_mean|0,1846|0,1591|0,2106|Robusta|
|mp2_5_mean|prop_inversion|0,5194|0,5013|0,5373|Robusta|

**Conclusión:** todas las correlaciones son estables, pero la relación MP2.5–MP10 exige control de multicolinealidad antes de S3.

### 7.4 Simulación Monte Carlo

La simulación Monte Carlo generó **10.000 escenarios diarios de MP2.5**, usando media y desviación estándar estimadas en S1 y una distribución lognormal calibrada.

|Iteraciones|Media S1|SD S1|Media simulada|P95|P(MP2.5 > 50)|P(MP2.5 > 80)|P(MP2.5 > 110)|
|-:|-:|-:|-:|-:|-:|-:|-:|
|10.000|24,94|13,99|24,57|50,05|5,05%|0,65%|0,10%|

**Conclusión:** Monte Carlo entrega una métrica probabilística interpretable para escenarios de riesgo ambiental, útil como referencia de riesgo, aunque sensible a la distribución asumida.

### 7.5 Robustez y sensibilidad

|Resultado|Original|Robusto|Método|Variación %|Conclusión|
|-|-:|-:|-|-:|-|
|Media MP2.5|24,9382|24,2523|Remoción outliers IQR|-2,75%|Confiable|
|Media MP10|56,6438|54,9694|Remoción outliers IQR|-2,96%|Confiable|
|IC media MP2.5|24,9382|24,9382|Jackknife|0,00%|Confiable|
|P(MP2.5 > 50)|0,0505|0,0418|Normal truncada alternativa|-17,23%|Sensible / cautela|

**Conclusión:** las medias son robustas frente a outliers y jackknife. La probabilidad de excedencia debe reportarse con cautela porque depende del supuesto distribucional.

---

## 8. Modelamiento predictivo de Sumativa 3

La Sumativa 3 ejecutó un clasificador logístico binario de **nowcasting contemporáneo** a escala estación-día, orientado a clasificar la condición del mismo día observado.

### 8.1 Diseño, continuidad y variable objetivo

|Estructura|Filas|Columnas|Estado|
|-|-:|-:|-|
|CSV físico original|16.071|36|Consistente|
|Matriz armonizada S1/S2|16.071|46|Consistente|
|Matriz inferencial/modelable S1/S2/S3|11.603|46|Consistente|

El periodo observado se extiende entre **2022-01-01** y **2025-12-31**. El enriquecimiento agrega diez variables mínimas y máximas derivadas de temperatura, presión, humedad, viento y radiación; no representa diez fuentes nuevas.

El archivo puente `resultados/s2_reporte_resultados_validados_para_s3.csv` contiene **19 evidencias**: **14** confirmadas o validadas, **1** sensible y **4** decisiones metodológicas. Al contener evidencia agregada, no se incorpora fila a fila al entrenamiento.

|Elemento|Resultado ejecutado|
|-|-|
|Fuente del objetivo|Columna original `mala_calidad_mp25`, validada únicamente donde existe MP2.5|
|Fallback documentado|`mp2_5_mean > 50 µg/m³`, solo si la columna objetivo no existe|
|Filas originales|16.071|
|Filas sin objetivo excluidas|4.468|
|Filas modelables|11.603|
|Positivos|1.393|
|Prevalencia|12,01%|
|Horizonte|`nowcasting_contemporaneo`|

La etiqueta no se imputó. Su prevalencia de **12,01%** no debe confundirse con el **4,75%** de días-estación sobre 50 µg/m³ de S1, porque representan definiciones diferentes.

### 8.2 Auditoría de fuga y variables bloqueadas

|Variable bloqueada|Motivo|
|-|-|
|`mp2_5_mean`|Derivada directa o proxy prohibido de MP2.5|
|`mp2_5_max`|Derivada directa o proxy prohibido de MP2.5|
|`calidad_aire_mp25`|Derivada directa o proxy prohibido de MP2.5|
|`nivel_contaminacion`|Derivada directa o proxy prohibido de MP2.5|
|`estaciones_en_episodio`|Derivada directa o proxy prohibido de MP2.5|
|`critico_mp25_dia`|Derivada directa o proxy prohibido de MP2.5|
|`mala_calidad_mp25`|Variable objetivo|

La auditoría final confirmó una intersección vacía entre variables prohibidas y predictores. `mp10_mean` se conserva solo porque el horizonte es contemporáneo; por su correlación con MP2.5 (**r = 0,9011**) no debe presentarse como predictor causal ni utilizarse para afirmar pronóstico futuro.

### 8.3 Lista blanca de variables candidatas

|Variable|Familia|Tipo|Faltantes %|M1 dominio|Pool M2/M3|
|-|-|-|-:|-|-|
|`temperatura_mean`|Meteorológica|Numérica|0,000|Sí|Sí|
|`humedad_mean`|Meteorológica|Numérica|0,000|Sí|Sí|
|`viento_mean`|Meteorológica|Numérica|0,000|Sí|Sí|
|`radiacion_mean`|Meteorológica|Numérica|0,000|Sí|Sí|
|`prop_inversion`|Meteorológica|Numérica|0,000|Sí|Sí|
|`presion_mean`|Meteorológica|Numérica|0,000|No|Sí|
|`mes_sin`|Temporal|Numérica|0,000|Sí|Sí|
|`mes_cos`|Temporal|Numérica|0,000|Sí|Sí|
|`invierno`|Temporal|Numérica|0,000|Sí|Sí|
|`es_finde`|Temporal|Numérica|0,000|Sí|Sí|
|`es_festivo`|Temporal|Numérica|0,000|Sí|Sí|
|`periodo_gec`|Temporal|Numérica|0,000|Sí|Sí|
|`zona_geografica`|Territorial|Categórica|0,000|Sí|Sí|
|`nivel_socioeconomico`|Territorial|Categórica|0,000|Sí|Sí|
|`estacion_anio`|Temporal|Categórica|0,000|Sí|Sí|
|`temporada_critica`|Temporal|Categórica|0,000|Sí|Sí|
|`comuna`|Territorial|Categórica|0,000|Sí|Sí|
|`estacion`|Territorial|Categórica|0,000|Sí|Sí|
|`mp10_mean`|Nowcasting/calidad|Numérica|0,112|No|Sí|
|`baja_cobertura_horaria`|Nowcasting/calidad|Numérica|0,000|No|Sí|

### 8.4 Cobertura horaria reconstruida

|Control|Resultado|
|-|-|
|Fuente|Registros horarios reales de MP2.5|
|Criterio|Cobertura < 75% o menos de 18 horas válidas|
|Filas modelables|11.603|
|Filas con cobertura emparejada|11.603|
|Emparejamiento|100,00%|
|Proporción marcada como baja cobertura|100,00%|
|Referencia S2|27,80%|
|Diferencia|+72,20 puntos porcentuales|
|Indicador|`baja_cobertura_horaria`|

El control técnico se ejecutó y el indicador ingresó al pool de selección, pero al quedar constante no aportó información discriminante y no fue seleccionado en el modelo final. La divergencia respecto de S2 debe tratarse como **limitación de calidad o definición de cobertura**, no como evidencia de que toda la serie tenga idéntica calidad operacional.

### 8.5 Separación temporal y bloqueo de la prueba futura

|Partición|n|Fecha mínima|Fecha máxima|Prevalencia|
|-|-:|-|-|-:|
|Desarrollo|8.439|2022-01-01|2024-03-27|0,110|
|Validación|1.003|2024-03-28|2024-10-18|0,223|
|Entrenamiento temporal — primer 70% del horizonte|9.442|2022-01-01|2024-10-18|0,122|
|Bloque futuro reservado — último 30% del horizonte|2.161|2024-10-19|2025-12-31|0,111|

El corte **70/30 se definió sobre el horizonte temporal**, no sobre la cantidad final de filas. Por diferencias de cobertura y por la exclusión de registros sin objetivo válido, los tamaños efectivos no reproducen una proporción exacta de 70/30 en observaciones. La imputación, la selección stepwise, los criterios AIC/BIC, la forma funcional, el modelo, la estrategia de faltantes y el umbral se decidieron sin observar el bloque futuro. El modelo final abrió esta prueba una sola vez.

### 8.6 Mecanismo de faltantes y estrategias comparadas

La ausencia de `mp10_mean` fue baja: **0,012%** en desarrollo y **0,598%** en validación. El AUC para predecir ausencia fue **0,451**, sin evidencia predictiva relevante; el patrón es compatible con MCAR, aunque MNAR no puede descartarse con esta prueba.

La regresión de imputación para `mp10_mean` utilizó `mes_cos`, `radiacion_mean`, `prop_inversion`, `temperatura_mean` y `presion_mean`, con **R² = 0,626**, R² ajustado **0,625** y RMSE residual **12,336**. Jarque–Bera no rechazó normalidad (**p = 0,492**), mientras Breusch–Pagan detectó heterocedasticidad (**p < 0,001**), por lo que se documentó HC3.

|Estrategia|Retención desarrollo|Retención validación|NRMSE/IQR promedio|Encogimiento promedio|
|-|-:|-:|-:|-:|
|Casos completos|99,99%|99,40%|—|—|
|Mediana mes→temporada→global|100,00%|100,00%|0,330|0,159|
|Regresión multivariada|100,00%|100,00%|0,294|0,117|

La regresión obtuvo menor error normalizado, pero **casos completos** fue elegida como estrategia principal porque retuvo al menos 99% y entregó desempeño equivalente sin introducir valores modelados. La contingencia es **regresión** si la cobertura futura cae o la retención de casos completos baja de 99%.

### 8.7 Tres modelos oficiales y selección AIC/BIC

|Modelo|Método|Variables iniciales|Variables finales|Resultado|
|-|-|-:|-:|-|
|`M1_Dominio_S1_S2`|Evidencia S1/S2 y fundamento físico|17|17|Conjunto definido por dominio|
|`M2_Forward_AIC_BIC`|Forward con BIC primario y AIC registrado|0|3|`mp10_mean`, `temporada_critica`, `viento_mean`|
|`M3_Backward_BIC`|Backward desde pool completo|20|19|Elimina `presion_mean`; siguiente eliminación rechazada, ΔBIC = 184,887|

Trayectoria forward del modelo ganador:

|Paso|Variable incorporada|AIC|BIC|Mejora BIC|
|-:|-|-:|-:|-:|
|1|`mp10_mean`|514,609|528,690|∞|
|2|`temporada_critica`|460,031|481,153|47,537|
|3|`viento_mean`|423,158|451,320|29,833|

### 8.8 Nueve combinaciones y efecto de la imputación

|Modelo|Estrategia|CV PR-AUC|CV ROC-AUC|Precision val.|Recall val.|F2 val.|Brier val.|Umbral val.|
|-|-|-:|-:|-:|-:|-:|-:|-:|
|M2 Forward|Completos|0,991|0,998|0,685|0,937|0,873|0,107|0,640|
|M2 Forward|Mediana|0,991|0,998|0,684|0,938|0,873|0,107|0,640|
|M2 Forward|Regresión|0,991|0,998|0,685|0,933|0,870|0,107|0,640|
|M3 Backward|Completos|0,975|0,993|0,611|0,978|0,873|0,133|0,220|
|M3 Backward|Mediana|0,975|0,993|0,610|0,978|0,873|0,136|0,220|
|M3 Backward|Regresión|0,975|0,993|0,610|0,978|0,873|0,134|0,220|
|M1 Dominio|Completos|0,968|0,991|0,349|0,915|0,691|0,392|0,595|
|M1 Dominio|Mediana|0,968|0,991|0,349|0,915|0,691|0,392|0,595|
|M1 Dominio|Regresión|0,968|0,991|0,349|0,915|0,691|0,392|0,595|

La regla jerárquica priorizó equivalencia práctica en PR-AUC, Recall y Brier; luego F2, retención y parsimonia. La decisión no utilizó el conjunto de prueba.

En M2, la brecha máxima entre estrategias fue **0,0000** en CV PR-AUC, **0,0045** en Recall y **0,1837** en el rango de coeficientes. Los signos e intervalos se mantuvieron consistentes, por lo que casos completos fue elegido por parsimonia y alta retención.

### 8.9 Forma funcional y calibración

Box–Tidwell no detectó evidencia fuerte de curvatura para `mp10_mean` (**p = 0,123**) ni `viento_mean` (**p = 0,943**). Se conservó la forma **lineal en el logit**, con BIC de desarrollo **451,320**, CV PR-AUC **0,991**, Recall de validación **0,937**, F2 **0,873** y Brier **0,107**.

La calibración Platt se aprendió con **6.450** predicciones OOF temporales: Brier sin calibrar **0,028**, Brier calibrado **0,025**, intercepto **−1,252** y pendiente **0,339**.

El umbral de validación **0,640** corresponde a probabilidades previas a la calibración final; el umbral operativo **0,260** se aplicó sobre probabilidades calibradas, por lo que ambos valores no son directamente comparables.

### 8.10 Evaluación final en prueba futura

|Partición|n|Positivos|Umbral|Precision|Recall|Especificidad|F1|F2|ROC-AUC|PR-AUC|Brier|
|-|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|Entrenamiento|9.435|1.153|0,260|0,817|0,983|0,969|0,892|0,944|0,992|0,910|0,035|
|Prueba futura|2.155|237|0,260|0,608|0,937|0,925|0,738|0,845|0,979|0,823|0,044|

Los tamaños finales de **9.435** registros de entrenamiento y **2.155** de prueba corresponden a la estrategia de **casos completos**. Respecto de las particiones temporales iniciales de 9.442 y 2.161 filas, se excluyeron respectivamente **7** y **6** registros por ausencia de `mp10_mean`; la variable objetivo no fue imputada.

|Clase real|Predicción buena|Predicción mala|
|-|-:|-:|
|Real buena|1.775|143|
|Real mala|15|222|

La exactitud de prueba fue **0,927** y la balanced accuracy **0,931**. La diferencia de ROC-AUC entre entrenamiento y prueba fue **+0,013** en favor del entrenamiento. La curva PR se prioriza sobre accuracy por la prevalencia positiva de 11,0% en la prueba utilizada.

### 8.11 Inferencia logística, OR e intervalos robustos

La inferencia se reajustó sin ponderación y sin penalización sobre **9.435 observaciones**, con cuatro parámetros, log-likelihood **−745,801**, AIC **1.499,602**, BIC **1.528,210**, covarianza robusta agrupada por **1.022 fechas** y convergencia confirmada.

|Parámetro|Coeficiente|OR|IC robusto coef. 95%|IC robusto OR 95%|p robusto|
|-|-:|-:|-|-|-:|
|Intercepto|−10,923|≈0|[−12,777; −9,070]|≈0|<0,001|
|Resto del año vs Invierno|−8,445|2,149e−4|[−12,400; −4,490]|[4,119e−6; 0,011]|<0,001|
|`mp10_mean` estandarizado|8,218|3.708,503|[6,793; 9,644]|[891,663; 15.423,988]|<0,001|
|`viento_mean` estandarizado|0,585|1,796|[0,238; 0,933]|[1,268; 2,543]|0,001|

Los OR numéricos corresponden a incrementos de **una desviación estándar** dentro del pipeline. Sus magnitudes no deben interpretarse como causalidad ni extrapolarse fuera del rango observado.

Los AIC/BIC de este reajuste inferencial no son comparables directamente con los de la selección predictiva: la selección se realizó durante desarrollo, mientras que la inferencia final se reajustó sobre **9.435 casos completos** del entrenamiento total y con un propósito estadístico distinto.

### 8.12 Multicolinealidad, residuos e influencia

|Predictor|VIF|Nivel|
|-|-:|-|
|Resto del año vs Invierno|1,245|Controlado|
|`mp10_mean`|1,222|Controlado|
|`viento_mean`|1,024|Controlado|

El número de condición fue **5,04**. Se detectaron **65** residuos de Pearson con |r| > 2, **55** con |r| > 3, **1.521** observaciones sobre 2p/n, **190** sobre 4/n, Cook máximo **0,426**, |DFBeta| máximo **0,789** y **6.277** probabilidades extremas. La dispersión Pearson/df de **163,677** exige priorizar sandwich, bootstrap y sensibilidad penalizada sobre una lectura exclusiva de Wald.

La sensibilidad L2 mantuvo los signos de todos los parámetros: `mp10_mean` 8,218→7,276, `viento_mean` 0,585→0,567 y temporada crítica −8,445→−4,315, confirmando dirección estable aunque no causalidad.

### 8.13 Bootstrap del modelo final

|Control|Resultado|
|-|-:|
|Remuestras solicitadas|10.000|
|Remuestras exitosas|10.000|
|Fallos|0|
|Tasa de éxito|100,00%|
|Parámetros inestables|0|
|Tiempo registrado|57,117 s|

|Parámetro|Coef. original|Media bootstrap|Sesgo|SD bootstrap|IC bootstrap 95%|Signo consistente|
|-|-:|-:|-:|-:|-|-:|
|`viento_mean`|0,585|0,590|0,005|0,159|[0,281; 0,909]|100%|
|Intercepto|−10,923|−11,052|−0,128|0,799|[−12,712; −9,625]|100%|
|`mp10_mean`|8,218|8,317|0,099|0,602|[7,236; 9,565]|100%|
|Resto del año vs Invierno|−8,445|−8,991|−0,546|2,260|[−13,452; −4,907]|100%|

Los IC bootstrap de OR fueron: `viento_mean` **[1,325; 2,483]**, `mp10_mean` **[1.388,605; 14.250,894]** y Resto del año vs Invierno aproximadamente **[1,438e−6; 0,007]**. La variación relativa del ancho entre 5.000 y 10.000 remuestras fue como máximo **1,3%**, respaldando convergencia práctica.

### 8.14 Umbral operativo y costo de errores

|Criterio|Umbral|Precision|Recall|Especificidad|F1|F2|ROC-AUC|PR-AUC|Brier|FN|FP|
|-|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|-:|
|F2 + Recall mínimo|0,260|0,608|0,937|0,925|0,738|0,845|0,979|0,823|0,044|15|143|
|Costo FN=5, FP=1|0,165|0,584|0,954|0,916|0,724|0,846|0,979|0,823|0,044|11|161|

El umbral de costo reduce falsos negativos de 15 a 11 a cambio de aumentar falsos positivos de 143 a 161. La elección final depende de capacidad de respuesta, tolerancia a falsas alarmas y costo real de omitir un episodio.

### 8.15 Diagnóstico por subgrupos

|Dimensión|Grupo|n|Positivos|Prevalencia|Recall|Precision|F1|PR-AUC|Brier|
|-|-|-:|-:|-:|-:|-:|-:|-:|-:|
|Comuna|Cerrillos|433|57|0,132|0,965|0,655|0,780|0,858|0,043|
|Comuna|Puente Alto|432|26|0,060|1,000|0,325|0,491|0,780|0,067|
|Comuna|Talagante|432|49|0,113|0,878|0,843|0,860|0,934|0,029|
|Comuna|Quilicura|430|44|0,102|0,841|0,597|0,698|0,696|0,051|
|Comuna|Cerro Navia|428|61|0,143|1,000|0,693|0,819|0,944|0,032|
|Estación del año|Primavera|667|0|0,000|—|—|—|—|—|
|Estación del año|Verano|593|0|0,000|—|—|—|—|—|
|Estación del año|Invierno|453|188|0,415|0,947|0,667|0,782|0,839|0,143|
|Estación del año|Otoño|442|49|0,111|0,898|0,463|0,611|0,761|0,068|
|Nivel socioeconómico|Q3 (medio)|864|75|0,087|0,920|0,527|0,670|0,729|0,048|
|Nivel socioeconómico|Q2 (medio-bajo)|433|57|0,132|0,965|0,655|0,780|0,858|0,043|
|Nivel socioeconómico|Q4 (medio-alto)|430|44|0,102|0,841|0,597|0,698|0,696|0,051|
|Nivel socioeconómico|Q1 (bajo)|428|61|0,143|1,000|0,693|0,819|0,944|0,032|
|Zona|Poniente|1.293|167|0,129|0,952|0,713|0,815|0,886|0,035|
|Zona|Sur|432|26|0,060|1,000|0,325|0,491|0,780|0,067|
|Zona|Norte|430|44|0,102|0,841|0,597|0,698|0,696|0,051|

La brecha máxima de Recall entre grupos evaluables fue **0,159**. Primavera y verano no poseen positivos en la prueba, por lo que no se calculan métricas discriminantes. Las brechas pueden reflejar tamaño muestral, prevalencia, sensores, meteorología o especificación; no deben transformarse automáticamente en conclusiones de inequidad algorítmica.

### 8.16 Archivos exportados por Sumativa 3

Los archivos se generan en `resultados/S3/`:

```text
s3_consistencia_estructura_s1_s2.csv
s3_matriz_consistencia_s1_s2_s3.csv
s3_trazabilidad_reporte_s2.csv
s3_control_cobertura_horaria.csv
s3_auditoria_fuentes_cobertura.csv
s3_validacion_imputador_mediana_agrupada.csv
s3_calibracion_platt_oof.csv
s3_sensibilidad_penalizada_inferencia.csv
s3_matriz_evidencia_s1_s2_por_predictor.csv
s3_auditoria_fuga_variables.csv
s3_diagnostico_mecanismo_faltantes.csv
s3_diagnostico_ols_imputacion.csv
s3_validacion_imputacion_global.csv
s3_resumen_seleccion_tres_modelos.csv
s3_trayectoria_forward_aic_bic.csv
s3_trayectoria_backward_bic.csv
s3_metricas_9_combinaciones_validacion.csv
s3_linealidad_logit_pretest.csv
s3_sensibilidad_forma_funcional.csv
s3_decision_forma_funcional.csv
s3_metricas_modelo_final_train_test.csv
s3_coeficientes_or_ic_wald.csv
s3_residuos_influencia.csv
s3_bootstrap_coeficientes_or.csv
s3_bootstrap_convergencia.csv
s3_impacto_imputacion_metricas.csv
s3_estabilidad_ic_por_imputacion.csv
s3_decision_imputacion.csv
s3_diagnostico_subgrupos.csv
s3_conclusiones_accionables.csv
```

### 8.17 Limitaciones y reglas de uso

* El producto es un clasificador de **nowcasting**, no un forecast de días futuros.
* `mp10_mean` es contemporáneo y altamente correlacionado con MP2.5; su aporte es predictivo, no causal.
* La etiqueta no se imputa y los registros sin objetivo se excluyen.
* La cobertura horaria reconstruida debe revisarse, porque el criterio marcó 100% de baja cobertura.
* La dispersión y las probabilidades extremas sugieren cuasiseparación; por ello se reportan IC robustos, bootstrap y sensibilidad penalizada.
* La calibración Platt, Recall, falsos negativos, cobertura, deriva y brechas territoriales deben monitorearse en producción.
* Ninguna asociación del modelo debe comunicarse como causal.

---

## 9. Estructura del repositorio

```text
abp_estadistica/
│
├── .venv/                         # Entorno local, excluido de Git
│
├── data/
│   └── calidad_aire_diario.csv
│
├── evidencia/
│
├── figures/
│   ├── S3/
│   │   └── *.png
│   └── *.png
│
├── src/
│   ├── agregar_diario.py
│   ├── enriquecer_dataset.py
│   ├── integrar_2022_2025.py
│   └── modelo_economico.py
│
├── notebooks/
│   ├── _version_horaria_obsoleta/
│   ├── 01_analisis_estadistico_diario.ipynb
│   ├── 02_validacion_simulacion_remuestreo.ipynb
│   ├── 03_Modelamiento_predictivo_binario_mala_calidad_mp25.ipynb
│   └── Formativa2_Modelamiento_Predictivo_Grupo3.ipynb
│
├── reports/
│   ├── 01_analisis_estadistico_diario_limpio.html
│   ├── 02_validacion_simulacion_remuestreo.html
│   ├── 03_Modelamiento_predictivo_binario_mala_calidad_mp25.html
│   ├── Formativa2_Modelamiento_Predictivo_Grupo3.html
│   ├── Formativa2_Modelamiento_Predictivo_Grupo3.PDF
│   ├── Formativa2_Modelamiento_Predictivo_Grupo3.zip
│   ├── Sumativa1_Informe_Tecnico_Final.pdf
│   ├── Sumativa1_Informe_Tecnico_Final_Latex.zip
│   ├── Sumativa2_Validacion_Simulacion_Remuestreo_Grupo3.pdf
│   └── Sumativa2_Validacion_Simulacion_Remuestreo_Grupo3.zip
│
├── resultados/
│   ├── S3/
│   │   └── s3_*.csv
│   └── s2_reporte_resultados_validados_para_s3.csv
│
├── .gitignore
├── .mailmap
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt              # Dependencias directas validadas
└── SECURITY.md
```

---

## 10. Reproducibilidad

El desarrollo fue validado con **Python 3.12.10** y kernel `.venv`. Se recomienda crear el entorno fuera de carpetas sincronizadas activamente, como OneDrive o Dropbox, para reducir bloqueos de lectura/escritura.

### 10.1 Crear el entorno en Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name abp_estadistica --display-name "ABP Estadística"
```

### 10.2 Ejecutar Sumativas 1 y 2

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_estadistico_diario.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_validacion_simulacion_remuestreo.ipynb
```

### 10.3 Ejecutar Sumativa 3

```powershell
# Ejecución oficial: 10.000 bootstrap y cinco bloques temporales
Remove-Item Env:S3_FAST -ErrorAction SilentlyContinue
jupyter nbconvert --to notebook --execute --inplace notebooks/03_Modelamiento_predictivo_binario_mala_calidad_mp25.ipynb

# Verificación técnica rápida
$env:S3_FAST = "1"
jupyter nbconvert --to notebook --execute --inplace notebooks/03_Modelamiento_predictivo_binario_mala_calidad_mp25.ipynb
Remove-Item Env:S3_FAST
```

Variables opcionales:

* `S3_FAST=1`: reduce temporalmente bootstrap, repeticiones de enmascaramiento y bloques CV.
* `S3_BOOTSTRAP=<n>`: sobrescribe la cantidad de remuestras.
* `S3_COBERTURA_ESTRICTA=1`: exige cobertura horaria por fila y falla si no puede reconstruirse.

### 10.4 Generar reportes HTML

```powershell
jupyter nbconvert --to html notebooks/01_analisis_estadistico_diario.ipynb --output-dir reports
jupyter nbconvert --to html notebooks/02_validacion_simulacion_remuestreo.ipynb --output-dir reports
jupyter nbconvert --to html notebooks/03_Modelamiento_predictivo_binario_mala_calidad_mp25.ipynb --output-dir reports
```

### 10.5 Verificar el entorno

```powershell
python -c "import sys, numpy, pandas, scipy, matplotlib, seaborn, sklearn, statsmodels; print(f'Python={sys.version.split()[0]} | NumPy={numpy.__version__} | pandas={pandas.__version__} | SciPy={scipy.__version__} | matplotlib={matplotlib.__version__} | seaborn={seaborn.__version__} | scikit-learn={sklearn.__version__} | statsmodels={statsmodels.__version__}')"
```

La salida esperada debe coincidir con las versiones validadas de la sección 11. `pip freeze` puede utilizarse como evidencia de auditoría del entorno completo, pero no debe copiarse íntegramente al README porque incluye numerosas dependencias transitivas.

---

## 11. Entorno validado y dependencias

|Componente|Versión validada|
|-|-:|
|Python|3.12.10|
|NumPy|2.5.0|
|pandas|3.0.3|
|SciPy|1.18.0|
|matplotlib|3.11.0|
|seaborn|0.13.2|
|scikit-learn|1.9.0|
|statsmodels|0.14.6|
|ipykernel|6.29.5|
|notebook|7.6.0|

> Las versiones principales fueron verificadas en el entorno virtual `.venv` utilizado para ejecutar el proyecto, mediante `pip freeze`. El archivo `requirements.txt` conserva únicamente las **dependencias directas y relevantes** del análisis; las dependencias transitivas se resuelven automáticamente durante la instalación y no se duplican en esta documentación.

---

## 12. Estado del proyecto

- [x] **Sumativa 1:** análisis exploratorio formal, estimación puntual, intervalos de confianza robustos e inferencia estadística a escala estación-día.
- [x] **Sumativa 2:** validación y remuestreo de métricas mediante bootstrap, tests de permutación, estabilidad de correlaciones, Monte Carlo y análisis de robustez.
- [x] **Sumativa 3:** diseño, entrenamiento y evaluación de un modelo de clasificación binario de nowcasting para `mala_calidad_mp25`, con selección AIC/BIC, validación temporal, calibración, inferencia robusta y bootstrap.

---

## 13. Fuentes

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
* Universidad Andrés Bello. MCDI501 — Semana 3, notebook de referencia y rúbrica Sumativa 3.
* Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied Logistic Regression* (3.ª ed.). Wiley.
* James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.
* Little, R. J. A., & Rubin, D. B. (2019). *Statistical Analysis with Missing Data* (3.ª ed.). Wiley.
* van Buuren, S. (2018). *Flexible Imputation of Missing Data* (2.ª ed.). Chapman & Hall/CRC.
