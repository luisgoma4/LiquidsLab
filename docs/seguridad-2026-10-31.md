# Seguridad: revisión del 2026-10-31

Contexto: revisión de seguridad de todos los repos tras el «octubre negro» (la IA abarata el ataque: se asume que todo repo, endpoint y clave se escanea en minutos). Este documento recoge lo aplicado a este repo y lo que queda pendiente; el estado vive en `docs/`, no en la conversación.

> Repo **público**: los pendientes se describen por categoría y acción, sin detalles explotables.

## Cambios aplicados

Ninguno en esta tanda.

## Pendientes

- [ ] **Baja** · Scripts `3danimation_*.py`, `compare_relaxtime.py`, `relaxation_time copy.py` (E-04): Rutas absolutas con el nombre de usuario local; usar rutas relativas o argumentos de línea de comandos.
- [ ] **Info** · Informe PDF en la raíz (E-05): Confirmar que su publicación es intencionada.
- [ ] **Info** · Metadatos de commit (E-03): Email `noreply` de GitHub en commits futuros.
- [ ] **Baja** · `.gitignore` (E-28): Añadir regla `.env*` y exclusión de datos brutos.

## Reglas nuevas para agentes de este repo

- .gitignore base: `.env*`, `*.pem`, `*.key`, `*.sqlite*`, `*.db`, `.wrangler/`, y `*.xlsx`/`*.docx`/`*.pdf` en repos con material de cliente. Ejecutar `gitleaks detect --log-opts=--all` antes de hacer público un repo.
- En repos públicos, commits con el email `noreply` de GitHub.
- Los datos de laboratorio y de terceros no se versionan en repos públicos sin permiso.
- Dependabot (npm y github-actions) y alertas de seguridad activas, incluso en repos estáticos.
