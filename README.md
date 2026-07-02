# Análisis Estadístico de la Calidad del Aire en Santiago

**Inequidad ambiental, meteorología y episodios críticos de material particulado**

Proyecto del curso **MCDI501 — Estadística Computacional para la Toma de Decisiones**, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

| | |
|---|---|
| **Grupo** | Grupo 3 |
| **Integrantes** | Rodrigo Chinchón Ayala · Pablo Villalobos González · Sergio Fernández Almonacid |
| **Docente** | Jean Paul Maidana González |
| **Dataset** | Red SINCA — Ministerio del Medio Ambiente, Santiago RM |
| **Escala de análisis** | Estación-día · 2022–2025 · 11 estaciones · 36 variables |
| **Notebook principal** | `notebooks/01_analisis_estadistico_diario.ipynb` |
| **Salida HTML** | `outputs/01_analisis_estadistico_diario.html` |
| **Repositorio** | `https://github.com/Rfcha/abp_estadistica` |

---

## 1. Objetivo

Caracterizar estadísticamente la contaminación por **MP2.5** y **MP10** en Santiago de Chile, evaluando si la exposición presenta diferencias relevantes entre **zonas geográficas**, **niveles socioeconómicos** y **condiciones meteorológicas**, con énfasis en episodios críticos y toma de decisiones basada en evidencia.

## 2. Pregunta movilizadora

> ¿Qué evidencia estadística sustenta que la contaminación por material particulado en Santiago presenta diferencias significativas entre zonas, niveles socioeconómicos y temporadas?

---

## 3. Resumen ejecutivo de hallazgos

El análisis se ejecutó a **escala estación-día**, reduciendo la dependencia horaria y haciendo más defendible la inferencia estadística aplicada en esta fase.

- **MP2.5 como contaminante prioritario:** media diaria de **24,94 µg/m³**; **551 días-estación sobre norma** equivalente a **4,75 %** de los días válidos.
- **MP10:** media diaria de **56,6 µg/m³**; **66 días-estación sobre norma** equivalente a **0,57 %** de los días válidos.
- **Inequidad ambiental Q1 vs Q5:** Q1 promedia **29,40 µg/m³** frente a **16,61 µg/m³** en Q5; diferencia de **+12,8 µg/m³** (**77 % mayor**), con **d de Cohen = 0,97**.
- **Desigualdad territorial Oriente vs Poniente:** Oriente promedia **16,61 µg/m³** y Poniente **26,33 µg/m³**; diferencia de **9,72 µg/m³** y **d de Cohen = -0,76**.
- **Inversión térmica:** los días con alta inversión térmica promedian **32,15 µg/m³** versus **18,95 µg/m³** en baja inversión; **d de Cohen = 1,05**.
- **Riesgo operativo territorial:** Poniente presenta **7,62 %** de días sobre norma; Oriente registra **0,00 %** en la muestra analizada.
- **Correlaciones relevantes:** MP2.5 se correlaciona fuertemente con MP10 (**r = 0,901**) y negativamente con temperatura (**r = -0,621**).

Todas las conclusiones reportan **p-valor, tamaño de efecto y decisión estadística**, evitando depender solo de la significancia estadística.

---

## 4. Metodología

| Etapa | Procedimiento |
|---|---|
| **Configuración reproducible** | Python 3.12.10, semilla fija 2026, versiones registradas y paleta visual institucional |
| **Carga y tipado** | Lectura de `data/calidad_aire_diario.csv`, tipado de variables categóricas ordenadas y preparación de escala estación-día |
| **Depuración** | Transformación de variables binarias a etiquetas interpretables, eliminación de registros sin MP2.5 válido e inventario estadístico de variables |
| **Calidad de datos** | Auditoría de faltantes, duplicados e inconsistencias físicas; criterio de cobertura diaria ≥75 % |
| **EDA** | Estadística descriptiva, frecuencias oficiales, correlaciones Pearson/Spearman, inequidad ambiental y evolución temporal 2022–2025 |
| **Estimación** | Intervalos de confianza al 95 % con distribución *t* de Student e IC Wilson para proporciones sobre norma |
| **Inferencia** | 5 pruebas: 3× *t* de Welch, 1× χ² de independencia y 1× prueba Z de proporciones |

---

## 5. Resultados inferenciales consolidados

| Prueba | Estadístico | p-valor | Efecto | Decisión |
|---|---:|---:|---:|---|
| t Welch — Oriente vs Poniente | t = -29,7 | 6,0e-176 | d = -0,76 | Rechaza H0 |
| t Welch — Q1 vs Q5 | t = 30,4 | 2,1e-180 | d = 0,97 | Rechaza H0 |
| t Welch — Inversión térmica | t = 55,5 | 0,0e+00 | d = 1,05 | Rechaza H0 |
| χ² — Zona vs nivel de contaminación | χ² = 308,2 | 7,45e-62 | V = 0,115 | Rechaza H0 |
| Z — Proporción días sobre norma | z = 10,87 | 0,0e+00 | Δ = 7,62 pp | Rechaza H0 |

**Conclusión:** las 5 pruebas rechazan H0 con α = 0,05. La evidencia respalda diferencias territoriales, inequidad socioambiental y un mecanismo físico consistente asociado a inversión térmica.

---

## 6. Estructura del repositorio

```text
abp_estadistica/
├── data/
│   └── calidad_aire_diario.csv
├── notebooks/
│   └── 01_analisis_estadistico_diario.ipynb
├── outputs/
│   └── 01_analisis_estadistico_diario.html
├── figures/
│   └── *.png
├── README.md
├── requirements.txt
├── GUIA_GIT.md
├── CHANGELOG.md
├── .mailmap
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── SECURITY.md
```

---

## 7. Reproducibilidad

El notebook fue validado con **Python 3.12.10** y kernel `.venv`. Se recomienda crear el entorno virtual fuera de carpetas sincronizadas como OneDrive o Dropbox para evitar bloqueos de archivos durante la instalación.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name abp_estadistica --display-name "ABP Estadística"
```

### Ejecutar notebook y generar HTML

```powershell
jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_estadistico_diario.ipynb
jupyter nbconvert --to html notebooks/01_analisis_estadistico_diario.ipynb --output-dir outputs
```

### Verificación rápida

```powershell
python -c "import numpy, pandas, matplotlib, seaborn, scipy; print('Entorno OK')"
```

---

## 8. Entorno validado

| Componente | Versión |
|---|---:|
| Python | 3.12.10 |
| NumPy | 2.5.0 |
| pandas | 3.0.3 |
| matplotlib | 3.11.0 |
| seaborn | 0.13.2 |
| SciPy | 1.18.0 |
| ipykernel | 6.29.5 |
| IPython | requerido para `display(HTML(...))` |

---

## 9. Roadmap

- **Sumativa 1:** análisis exploratorio, estimación e inferencia estadística a escala estación-día.
- **Formativa 2:** profundización de estimación robusta e intervalos de confianza.
- **Sumativa 2:** validación mediante bootstrap, tests de permutación y simulación Monte Carlo.
- **Sumativa 3:** modelo de clasificación binaria para episodios críticos (`mala_calidad_mp25`), priorizando recall, F1 y AUC.

---

## 10. Fuentes

- Ministerio del Medio Ambiente — Sistema de Información Nacional de Calidad del Aire, SINCA.
- Ministerio del Medio Ambiente — D.S. N°12/2011, norma primaria MP2.5.
- INE, MINVU y CNDU — Sistema de Indicadores y Estándares de Desarrollo Urbano, SIEDU.
- Ministerio de Desarrollo Social — CASEN.
- Montgomery & Runger (2018), *Applied Statistics and Probability for Engineers*.
- Virtanen et al. (2020), SciPy 1.0, *Nature Methods*.

## 11. Licencia

Ver [LICENSE](LICENSE).
