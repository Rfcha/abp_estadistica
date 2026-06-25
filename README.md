# Análisis estadístico de la calidad del aire en Santiago de Chile

**MCDI501 — Estadística Computacional para la Toma de Decisiones**
Magíster en Ciencias de Datos e Inteligencia Artificial · Universidad Andrés Bello (UNAB)

Proyecto ABP — **Sumativa 1, Fase 2: Informe técnico de avance**.

---


## ⚠️ Ajuste metodológico (retroalimentación docente)

El análisis se realiza a **escala diaria** (una fila por estación y día), no horaria. Las
mediciones horarias no son independientes (autocorrelación temporal), lo que invalidaría los
intervalos de confianza y las pruebas de hipótesis. La agregación diaria coincide con la escala
normativa del MMA. El dataset pasó de 192.720 filas horarias a **8.030 diarias**.

El componente socioeconómico se mantiene como **motivación del problema**; el producto evaluado
es estadístico (descriptiva, inferencia, validación por remuestreo y modelo de clasificación),
no un proyecto de inversión con VAN.

---

## Descripción

Análisis estadístico descriptivo e inferencial sobre **datos reales de la red SINCA**
(Sistema de Información Nacional de Calidad del Aire, MMA): mediciones horarias 2022–2023 de
**11 estaciones** del Gran Santiago. El dataset se enriquece con variables contextuales (áreas
verdes INE-SIEDU) y derivadas documentadas, para caracterizar el material particulado (MP2.5,
MP10), estimar parámetros poblacionales con intervalos de confianza y contrastar hipótesis sobre
diferencias territoriales, estacionales y de tipo de día.

### Pregunta movilizadora

> ¿Qué evidencia estadística sustenta que la contaminación por material particulado en Santiago
> presenta diferencias significativas entre zonas, temporadas y tipos de día, y qué factores
> meteorológicos y urbanos explican la exposición de la población a episodios críticos?

## Hallazgos principales

- **Desigualdad territorial:** zona Oriente 16.6 vs Poniente 28.8 µg/m³ de MP2.5 (t de Welch,
  p < 0.001, d = 0.72).
- **Estacionalidad crítica:** el invierno casi duplica la media de MP2.5 (105% mayor, d = 1.24).
- **Efecto del tráfico:** días laborales superan a fines de semana (p < 0.001).
- **Asociación zona ↔ nivel de contaminación** (χ², p < 0.001).
- **Áreas verdes:** tendencia negativa con MP2.5 (r ≈ −0.49), moderada y no significativa
  (n = 11), lo que evidencia el factor confusor socioeconómico.
- **Inversión térmica** (variable real del SINCA): correlación positiva fuerte con MP2.5,
  confirmando el mecanismo físico de los episodios críticos.
- **Inequidad ambiental cuantificada:** las comunas de menor nivel socioeconómico (Q1) presentan
  92% más MP2.5 que las de mayor ingreso (Q5), con efecto grande (t de Welch, p < 0.001, d = 0.89).
- **Contraste fotoquímico:** el ozono (O3) muestra el patrón estacional inverso al MP2.5
  (máximo en verano vs. invierno), evidenciando dos problemas de contaminación opuestos.

## Estructura del repositorio

```
abp_estadistica/
├── data/
│   ├── sinca_santiago.csv             # Datos REALES SINCA 2022-2023 (fuente primaria)
│   ├── calidad_aire_santiago.csv      # Dataset enriquecido (generado)
│   ├── areas_verdes_siedu.csv         # Áreas verdes por comuna (INE-SIEDU)
│   ├── enriquecer_dataset.py          # Pipeline de enriquecimiento (horario)
│   ├── agregar_diario.py              # Agregación a escala diaria (corrección docente)
│   ├── modelo_economico.py            # (obsoleto: enfoque VAN descartado por el docente)
│   └── calidad_aire_diario.csv        # Dataset DIARIO (8.030 filas) — el que se analiza
├── notebooks/
│   ├── 01_analisis_estadistico_diario.ipynb  # Notebook principal (escala diaria, válido)
│   └── _version_horaria_obsoleta/            # Versiones anteriores (no entregar)
├── figures/                           # 9 gráficos en alta resolución
├── reports/
│   └── (informes generados por sumativa)
├── notebooks/_version_horaria_obsoleta/   # versiones previas archivadas (NO entregar):
│       ├── 01_analisis_calidad_aire.ipynb       (escala horaria, inválida)
│       ├── 02_evaluacion_economica.ipynb        (enfoque VAN, descartado)
│       └── Informe_Fase3_Evaluacion_Economica.docx
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
├── GUIA_GIT.md
└── README.md
```

## Reproducibilidad

```bash
git clone https://github.com/<usuario>/abp_estadistica.git
cd abp_estadistica
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (Opcional) regenerar el dataset enriquecido desde los datos reales SINCA
cd data && python enriquecer_dataset.py && cd ..

jupyter lab notebooks/01_analisis_calidad_aire.ipynb   # Kernel -> Restart & Run All
```

## Variables del dataset

| Tipo | Variables |
|---|---|
| Numéricas continuas | mp2_5, mp10, temperatura, humedad, presion, viento, radiacion, isoterma_0, precipitacion |
| Circular | direccion_viento (0–360°, tratada con componentes seno/coseno) |
| Nominales | estacion, comuna, zona_geografica, tipo_dia, estacion_anio, temporada_critica |
| Ordinales | calidad_aire_mp25, calidad_aire_mp10 (Bueno→Emergencia), nivel_contaminacion |
| Binarias | inversion_termica, es_finde, es_festivo, **periodo_gec**, critico_mp25, critico_mp10 |
| **Nominal (nueva)** | **tipo_estacion** (urbana tráfico/fondo/suburbana) — SINCA/MMA |
| **Ordinal (nueva)** | **nivel_socioeconomico** (quintil Q1–Q5 comunal) — CASEN |
| **Continua (nueva)** | **o3** (ozono troposférico) — SINCA, norma 120 µg/m³N |
| **Discreta (nueva)** | **estaciones_en_episodio** (conteo 0–11) — red MACAM |

**Procedencia:** las variables MP2.5, MP10, temperatura, humedad, presión, viento, radiación,
inversión térmica, día de semana y marcas de fin de semana/festivo son **reales del SINCA**.
La isoterma 0 °C, precipitación y dirección del viento se derivaron con relaciones físicas
ancladas a las variables reales (ver `data/enriquecer_dataset.py`). Áreas verdes: INE-SIEDU.

## Metodología estadística

| Etapa | Técnicas |
|---|---|
| Calidad de datos | Faltantes, duplicados, inconsistencias físicas; imputación robusta por mediana de estación |
| Descriptiva | Tendencia central, dispersión, CV, asimetría, curtosis; histogramas, boxplots |
| Categóricas | Frecuencias de variables nominales y ordinales; tablas de contingencia |
| Bivariado | Correlación de Pearson; dirección del viento como variable circular (rosa de los vientos) |
| Estimación | IC al 95% (t de Student) para tres variables |
| Pruebas de hipótesis | t de Welch (3) + χ² de independencia (1); tamaños de efecto (d de Cohen, V de Cramér) |

## Integrantes del grupo

| Nombre | Rol | Usuario GitHub |
|---|---|---|
| _Integrante 1_ | _rol_ | _@usuario_ |
| _Integrante 2_ | _rol_ | _@usuario_ |
| _Integrante 3_ | _rol_ | _@usuario_ |

**Docente:** _Nombre del docente_

## Licencia

Proyecto académico con fines educativos (Magíster UNAB).
