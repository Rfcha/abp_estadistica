# Análisis Estadístico de la Calidad del Aire en Santiago

**Inequidad ambiental y episodios críticos de material particulado**

Proyecto del curso **MCDI501 — Estadística Computacional para la Toma de Decisiones**, Magíster en Ciencia de Datos e Inteligencia Artificial, Universidad Andrés Bello.

| | |
|---|---|
| **Grupo** | Grupo 3 |
| **Integrantes** | Rodrigo Chinchón Ayala · Sergio Fernández Almonacid · Pablo Villalobos González |
| **Docente** | Jean Paul Maidana González |
| **Dataset** | Red SINCA (Ministerio del Medio Ambiente), Santiago RM |
| **Escala** | Estación-día · 2022–2025 · 16.071 observaciones · 11 estaciones · 36 variables |

---

## Objetivo

Caracterizar estadísticamente la contaminación por material particulado (MP2.5 y MP10) en Santiago y evaluar, mediante inferencia estadística rigurosa, si la exposición se distribuye de forma desigual entre **zonas geográficas**, **niveles socioeconómicos** y **temporadas**, como base técnica para una eventual gestión sanitaria proactiva.

## Pregunta movilizadora

> ¿Qué evidencia estadística sustenta que la contaminación por material particulado en Santiago presenta diferencias significativas entre zonas, niveles socioeconómicos y temporadas?

---

## Hallazgos principales

El análisis se realiza a **escala estación-día**, garantizando observaciones independientes y, por tanto, la validez de la inferencia estadística (a diferencia de la escala horaria, donde la autocorrelación invalida los supuestos).

- **Inequidad ambiental:** el quintil socioeconómico de menor ingreso (Q1) promedia **29,40 µg/m³** de MP2.5 frente a **16,61 µg/m³** del de mayor ingreso (Q5): una diferencia de **+12,8 µg/m³ (77 % mayor)**, con efecto grande (*d* de Cohen = 0,97; *p* = 2,1×10⁻¹⁸⁰).
- **Desigualdad territorial:** el Poniente está significativamente más expuesto que el Oriente (*d* = −0,76; *p* = 6,0×10⁻¹⁷⁶).
- **Mecanismo físico:** los días con mayor proporción de inversión térmica concentran más MP2.5 (*d* = 0,85), confirmando el motor de los episodios críticos invernales.
- **Magnitud del fenómeno:** el **95,25 %** de los días-estación se clasifican como «Bueno»; **551 días (4,75 %)** superan la norma diaria, constituyendo los episodios críticos.

Todas las conclusiones se sustentan en pruebas con **tamaño de efecto reportado**, no solo en significancia estadística.

---

## Metodología

| Etapa | Procedimiento |
|---|---|
| **Calidad de datos** | Auditoría de faltantes (MP2.5: 27,8 %), duplicados (0) e inconsistencias físicas (0); criterio de cobertura ≥75 % de horas/día |
| **Descriptiva** | Tendencia central, dispersión, CV %, asimetría, curtosis; frecuencias de categóricas; correlación de Pearson |
| **Estimación** | Intervalos de confianza al 95 % (*t* de Student) sobre MP2.5, MP10 y temperatura |
| **Inferencia** | 4 pruebas de hipótesis: 3× *t* de Welch (con verificación de supuestos vía Levene) + 1× χ² de independencia |

---

## Estructura del repositorio

```text
abp_estadistica/
├── data/
│   └── calidad_aire_diario.csv        # dataset estación-día (2022–2025)
├── notebooks/
│   └── 01_analisis_estadistico_diario.ipynb   # análisis completo
├── figures/                            # SALIDA regenerable (no versionada): D1–D7 al ejecutar
├── requirements.txt                    # dependencias con versiones fijadas
├── README.md
├── changelog.md
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── SECURITY.md
```

---

## Reproducibilidad

El notebook es ejecutable de principio a fin sin errores, con **semilla fija (2026)** para reproducibilidad. Se recomienda un entorno virtual ubicado **fuera de carpetas sincronizadas** (OneDrive/Dropbox), que pueden bloquear archivos durante la instalación de paquetes.

```powershell
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows PowerShell

# 2. Instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# 3. Verificar que la pila gráfica carga correctamente
python -c "import matplotlib; from matplotlib.backends import registry; import matplotlib.pyplot; print('matplotlib', matplotlib.__version__, 'OK')"
```

Después, en VS Code: seleccionar `.venv` como **kernel** del notebook (selector arriba a la derecha) y ejecutar **Run All** desde la primera celda.

**Entorno validado:** Python 3.12.10 · NumPy 2.5.0 · pandas 3.0.3 · matplotlib 3.11.0 · seaborn 0.13.2 · SciPy 1.18.0.

---

## Roadmap del proyecto

- **Sumativa 1 (esta entrega):** análisis exploratorio e inferencial (descriptiva, IC 95 %, pruebas de hipótesis).
- **Sumativa 2 (validación):** bootstrap, tests de permutación y simulación de Monte Carlo.
- **Sumativa 3 (modelo):** clasificación binaria de episodios críticos (objetivo `mala_calidad_mp25`, ~12 % positivos), evaluado con F1, recall y AUC, con división estratificada por períodos.

---

## Fuentes

- Ministerio del Medio Ambiente. *Sistema de Información Nacional de Calidad del Aire (SINCA).* https://sinca.mma.gob.cl
- Ministerio del Medio Ambiente. *Norma de calidad primaria para MP2,5 (D.S. N.º 12/2011).*

## Licencia

Ver [LICENSE](LICENSE).
