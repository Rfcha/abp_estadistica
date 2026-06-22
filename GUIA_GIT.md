# Guía Git/GitHub — Flujo de trabajo del proyecto

Flujo profesional con **commits semánticos** (Conventional Commits) y buenas prácticas de
colaboración grupal.

## 1. Configuración inicial

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tucorreo@ejemplo.com"
git config --global init.defaultBranch main
```

## 2. Crear el repositorio

```bash
cd abp_estadistica
git init
git add .
git commit -m "chore: estructura inicial del proyecto ABP"
git remote add origin https://github.com/<usuario>/abp_estadistica.git
git branch -M main
git push -u origin main
```

## 3. Commits semánticos

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad o análisis |
| `fix` | Corrección de error |
| `docs` | Documentación |
| `style` | Formato, estilos de gráficos |
| `refactor` | Reorganización sin cambiar resultados |
| `data` | Cambios en datasets o su generación |
| `chore` | Mantenimiento, estructura, dependencias |

## 4. Flujo colaborativo (ramas + Pull Requests)

```bash
git checkout -b feat/pruebas-hipotesis
git add notebooks/01_analisis_calidad_aire.ipynb
git commit -m "feat: agregar prueba chi-cuadrado zona vs nivel"
git push -u origin feat/pruebas-hipotesis
# En GitHub: abrir PR -> revisión de un compañero -> merge a main
git checkout main && git pull origin main
```

## 5. Notebooks en Git

```bash
# Limpiar salidas durante el desarrollo (menos conflictos)
jupyter nbconvert --clear-output --inplace notebooks/01_analisis_calidad_aire.ipynb

# Para la ENTREGA: ejecutar todo y commitear CON salidas visibles
jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_calidad_aire.ipynb
git add notebooks/01_analisis_calidad_aire.ipynb
git commit -m "feat: notebook ejecutado de extremo a extremo sin errores"
```

> La versión en `main` debe estar **ejecutada completa**: GitHub renderiza el notebook y el
> evaluador verá los resultados.

## 6. Checklist de entrega Canvas

- [ ] Notebook ejecuta sin errores (`Restart & Run All`).
- [ ] Repositorio público o con acceso del docente.
- [ ] README con enlace e integrantes.
- [ ] Informe PDF (máx. 8 páginas) en `reports/` y subido a Canvas.
- [ ] Enlace al repositorio escrito DENTRO del informe PDF.
- [ ] Versión en `main` con salidas y gráficos visibles.
