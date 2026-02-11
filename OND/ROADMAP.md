# ROADMAP — OND (Epic)

Este documento define el rumbo del producto en orden **piramidal**: primero núcleo/estabilidad, luego música/offline, después social y finalmente creadores (3D + código).

## Norte (visión)

OND evoluciona de un motor visual/audio a:

1) App musical: catálogo del creador gratis por descarga (descarga + offline).
2) Red social: fotos, texto, canciones y letras (tipo Facebook).
3) Plataforma creativa: streaming + 3D + programación con demos (tipo SoundCloud/Spotify + “Spark”).

> Regla base: solo se distribuye o publica contenido sobre el que se tienen derechos/licencias.

## Principios (no negociables)

- Colores vivos + animación fina (identidad OND).
- UX sin fricción (1 tap, rápido, claro).
- Offline-first cuando tenga sentido.
- Privacidad + moderación desde el día 1 de lo social.
- Performance como feature (fluido en móviles).

## Fases (Epic)

### Fase 0 — Núcleo visual/audio (OND v2)

- Visual “haz de ondas” estable y compartible.
- Métricas audio (RMS/bandas) + nota musical (FFT / `librosa` opcional).
- Ajustes/controles robustos + performance.

### Fase 1 — Player + descargas + offline

- Biblioteca local (metadata, carátulas, letras).
- Descargas 1 tap + verificación + reintentos.
- Reproductor (cola, repeat/shuffle, búsqueda).

### Fase 2 — Catálogo del creador (Drops / Releases)

- Releases (álbum/single) + páginas de obra.
- Sistema de updates del catálogo (manifest + versionado).
- Onboarding + branding pulido.

### Fase 3 — Perfiles (base social)

- Registro/login + perfiles.
- Seguidores/seguidos.
- Privacidad por post (público/amigos/privado).
- Moderación inicial (reportes/bloqueos).

### Fase 4 — Feed social (fotos + canciones + letras)

- Posts: texto, fotos, audio, letras.
- Comentarios, reacciones, guardados.
- Notificaciones básicas.

### Fase 5 — Plataforma audio (uploads/streaming)

- Subida de tracks + procesamiento (transcode/normalización/artwork).
- Streaming + caché.
- Playlists públicas/colaborativas.

### Fase 6 — Creadores (3D + código interactivo)

- Publicación 3D (viewer WebGL, glTF, galerías).
- Publicación de código (snippets, demos, repos).
- Playground seguro (sandbox y límites).

### Fase 7 — Confianza, escala y sostenibilidad

- Anti-abuso + moderación avanzada.
- Seguridad y privacidad (permisos, retención).
- Observabilidad (errores, performance, costos).

## Camino rápido (MVP por prioridad)

1) Fase 0 estable + demo compartible.
2) Fase 1 offline + catálogo del creador.
3) Fase 3 perfiles + Fase 4 feed mínimo.
4) Fase 5 streaming/uploads.
5) Fase 6 3D + código.
