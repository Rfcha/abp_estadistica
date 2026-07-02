# Guía Git/GitHub — Flujo de trabajo del proyecto

Flujo profesional para mantener sincronizado el repositorio **abp_estadistica**, versionar notebooks ejecutados y preparar entregas reproducibles en GitHub.

---

## 1. Configuración inicial

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@ejemplo.com"
git config --global init.defaultBranch main
```

Verificar identidad:

```bash
git config --global --list
git shortlog -sne --all
```

Si existen identidades duplicadas, mantener actualizado `.mailmap`.

---

## 2. Clonar o actualizar el repositorio

### Primera vez

```bash
git clone https://github.com/Rfcha/abp_estadistica.git
cd abp_estadistica
```

### Trabajo diario

```bash
git checkout main
git pull origin main
```

---

## 3. Crear rama de trabajo

Usar ramas cortas y descriptivas.

```bash
git checkout -b docs/actualizar-readme-sumativa1
```

Convención recomendada:

| Prefijo | Uso |
|---|---|
| `feat/` | Nueva funcionalidad, análisis o notebook |
| `fix/` | Corrección de error |
| `docs/` | README, guías, changelog, mailmap |
| `data/` | Cambios en datasets o generación de datos |
| `style/` | Formato visual, gráficos o HTML |
| `refactor/` | Reorganización sin cambiar resultados |
| `chore/` | Mantenimiento, dependencias o estructura |

---

## 4. Commits semánticos

Usar **Conventional Commits**:

```bash
git add README.md requirements.txt GUIA_GIT.md CHANGELOG.md .mailmap
git commit -m "docs: actualizar documentación según notebook ejecutado"
```

Ejemplos útiles:

```bash
git commit -m "feat: agregar prueba z de proporciones territoriales"
git commit -m "fix: corregir interpretación de inversión térmica"
git commit -m "docs: documentar salida html y reproducibilidad"
git commit -m "chore: actualizar dependencias del entorno validado"
```

---

## 5. Notebooks en Git

Durante desarrollo, para reducir conflictos:

```bash
jupyter nbconvert --clear-output --inplace notebooks/01_analisis_estadistico_diario.ipynb
```

Para entrega, el notebook debe quedar ejecutado y con salidas visibles:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_analisis_estadistico_diario.ipynb
jupyter nbconvert --to html notebooks/01_analisis_estadistico_diario.ipynb --output-dir outputs
```

Luego versionar:

```bash
git add notebooks/01_analisis_estadistico_diario.ipynb outputs/01_analisis_estadistico_diario.html
git commit -m "feat: ejecutar notebook estadístico y exportar salida html"
```

> La versión en `main` debe quedar ejecutada completa para que GitHub y el evaluador puedan revisar resultados, tablas y gráficos.

---

## 6. Sincronizar con GitHub y abrir Pull Request

```bash
git push -u origin docs/actualizar-readme-sumativa1
```

En GitHub:

1. Abrir Pull Request hacia `main`.
2. Revisar que el notebook renderice correctamente.
3. Confirmar que README, CHANGELOG y requirements estén actualizados.
4. Solicitar revisión del equipo.
5. Hacer merge solo si no hay conflictos.

Después del merge:

```bash
git checkout main
git pull origin main
git branch -d docs/actualizar-readme-sumativa1
```

---

## 7. Resolver conflictos frecuentes

### Notebook con conflicto

Si el conflicto es solo por salidas:

```bash
jupyter nbconvert --clear-output --inplace notebooks/01_analisis_estadistico_diario.ipynb
git add notebooks/01_analisis_estadistico_diario.ipynb
git commit -m "fix: resolver conflicto de salidas del notebook"
```

### Mantener cambios locales y traer main

```bash
git stash
git pull origin main
git stash pop
```

---

## 8. Checklist antes de entregar

- [ ] `main` está actualizado con `git pull origin main`.
- [ ] Notebook ejecuta completo con `Restart & Run All`.
- [ ] HTML exportado en `outputs/`.
- [ ] README describe los hallazgos reales del notebook.
- [ ] `requirements.txt` refleja el entorno validado.
- [ ] `CHANGELOG.md` registra la actualización.
- [ ] `.mailmap` consolida autores si corresponde.
- [ ] No hay archivos temporales ni rutas locales personales.
- [ ] El repositorio está accesible para el docente.
- [ ] El informe PDF incluye el enlace al repositorio.
