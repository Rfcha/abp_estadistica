# Guía de Contribución — abp_cienciadatos

Este documento define el flujo de trabajo colaborativo del proyecto para que **todos los cambios queden registrados, versionados y trazables** mediante commits y pull requests.

## Reglas de oro

- **Nunca** se trabaja ni se hace push directo a `main`.
- Todo cambio entra a `main` **solo a través de un Pull Request (PR) aprobado**.
- Cada PR debe partir de una rama actualizada desde `main`.

## Requisitos previos

1. Tener una cuenta de GitHub y ser **colaborador** del repositorio (el owner los invita en Settings → Collaborators).
2. Tener Git instalado y configurar la identidad una sola vez:

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "tu-correo@ejemplo.com"
```

## Flujo de trabajo paso a paso

### 1. Clonar el repositorio (solo la primera vez)

```bash
git clone https://github.com/Rfcha/abp_cienciadatos.git
cd abp_cienciadatos
```

### 2. Actualizar `main` antes de empezar

```bash
git checkout main
git pull origin main
```

### 3. Crear una rama para tu tarea

Usa nombres descriptivos con prefijo según el tipo de trabajo:

```bash
git checkout -b feature/nombre-tarea      # nueva funcionalidad
git checkout -b fix/correccion-bug        # corrección de error
git checkout -b docs/actualiza-readme     # documentación
```

### 4. Trabajar y registrar cambios (commits)

```bash
git add .
git commit -m "feat: descripcion clara y breve del cambio"
```

### 5. Subir tu rama a GitHub

```bash
git push -u origin feature/nombre-tarea
```

### 6. Abrir el Pull Request

- En GitHub, abre un PR desde tu rama hacia `main`.
- Completa la plantilla del PR.
- Asigna al menos **un revisor**.
- No mezcles (merge) tu propio PR sin aprobación.

### 7. Tras la aprobación y el merge

```bash
git checkout main
git pull origin main
git branch -d feature/nombre-tarea   # borrar rama local ya integrada
```

## Convención de mensajes de commit

Usamos prefijos tipo *Conventional Commits* para que el historial sea legible:

| Prefijo | Uso |
|---------|-----|
| `feat:` | Nueva funcionalidad o entregable |
| `fix:` | Corrección de un error |
| `docs:` | Cambios en documentación |
| `refactor:` | Reorganización de código sin cambiar comportamiento |
| `test:` | Pruebas y validaciones |
| `data:` | Cambios en datasets o datos procesados |
| `chore:` | Tareas de mantenimiento (dependencias, config) |

**Ejemplo:** `feat(F3): agrega notebook de exploración de calidad del aire`

## Buenas prácticas

- Commits pequeños y frecuentes, con un solo propósito cada uno.
- Antes de abrir el PR, sincroniza tu rama con `main` para evitar conflictos:

```bash
git checkout main && git pull origin main
git checkout feature/nombre-tarea
git merge main
```

- No subas entornos virtuales, cachés ni archivos temporales (ya están en `.gitignore`).
- Sí versiona los datasets de las entregas dentro de `data/raw` y `data/processed`.
