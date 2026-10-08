# yt-pubx — publica cualquier video en YouTube con un comando

[![yt-pubx](guia/assets/banner-es.jpg)](https://inematds.github.io/yt-pubx/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

yt-pubx es un programa de línea de comandos que publica videos en YouTube por ti. Está pensado para quien publica con frecuencia, en uno o varios canales, y no quiere llenar a mano el título, la descripción, las etiquetas y la miniatura cada vez. A partir de un texto corto o de los subtítulos del video, Codex CLI escribe los textos y crea el arte de la miniatura, y yt-pubx envía todo mediante la API oficial de YouTube. Para usarlo necesitas Python, Codex CLI con sesión iniciada y un proyecto gratuito en Google Cloud con la YouTube Data API habilitada.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/yt-pubx/guia/es/**

---

Tú indicas un video (archivo o enlace) y `yt-pubx` hace el resto:

1. **Escribe el título, la descripción y las etiquetas** con Codex CLI, a partir de tu contexto y/o de los subtítulos.
2. **Crea la miniatura**: el arte sale del generador de imágenes de Codex (`image_gen`) y `yt-pubx`
   aplica encima la frase, la marca y los colores de tu canal.
3. **Publica directo** en el canal elegido (público, no listado, privado o programado),
   aplica la miniatura y, si hay SRT, sube los subtítulos.

Funciona con todos los canales que quieras. Todo corre en tu máquina; el texto y el arte
usan tu suscripción de Codex (ChatGPT), sin clave de API de modelo.

```bash
yt-pubx publicar aula.mp4 --contexto "Clase 3 del curso X. Página: https://..." --legenda aula.srt
```

---

## 1. Lo que necesitas

| Elemento | Para qué |
|---|---|
| Python 3.10+ con `requests` y `Pillow` | ejecutar el script (`pip install requests pillow`) |
| `ffprobe` (viene con ffmpeg) | leer la duración del video |
| [Codex CLI](https://github.com/openai/codex) con sesión iniciada (`npm i -g @openai/codex` → `codex login`) | escribir el texto y generar el arte de la miniatura |
| Un proyecto en Google Cloud con la **YouTube Data API v3** | publicar (paso 3) |
| `yt-dlp` (opcional) | publicar a partir de un enlace de YouTube, TikTok, Instagram… |

## 2. Instalar

```bash
git clone https://github.com/inematds/yt-pubx.git
cd yt-pubx
ln -s "$PWD/yt-pubx" ~/.local/bin/yt-pubx   # opcional: llamarlo desde cualquier carpeta
yt-pubx init                                 # crea ~/.config/yt-pubx/config.json
```

## 3. Habilitar YouTube en Google Cloud (una vez)

1. Entra en <https://console.cloud.google.com/> y crea un proyecto (p. ej.: `meu-yt-pubx`).
2. **APIs y servicios → Biblioteca** → busca **YouTube Data API v3** → **Habilitar**.
3. **APIs y servicios → Pantalla de consentimiento de OAuth** (Google Auth Platform):
   - Tipo de usuario **Externo**; nombre de la app y tu correo.
   - En **Público / Usuarios de prueba**, agrega el correo de la cuenta de Google dueña del canal.
4. **APIs y servicios → Credenciales → Crear credenciales → ID de cliente de OAuth**:
   - Tipo de aplicación: **App de escritorio** (Desktop).
   - Descarga el JSON (`client_secret_....json`). Guárdalo fuera de cualquier repositorio.

> **Trampas de Google que conviene conocer antes:**
> - **App en modo "Prueba"**: el acceso expira en **7 días** y tienes que volver a ejecutar `yt-pubx auth`.
>   Para que no expire, haz clic en **Publicar app** (pasa a "En producción"; para uso propio aparece la pantalla
>   de "app no verificada", basta con seguir en *Avanzado → continuar*).
> - **Proyecto sin auditoría**: YouTube puede bloquear como **privados** los videos subidos por proyectos
>   de API nuevos que aún no pasaron la auditoría de los servicios de API de YouTube. Si tus
>   videos se quedan en privado, solicita la auditoría en el formulario de *YouTube API Services*
>   (es gratuito) o publica como `private` y cámbialo a público en Studio.
> - **Cuota**: la cuota predeterminada es de 10.000 unidades/día; cada subida de video consume la mayor parte
>   (alcanza para pocos videos por día). Puedes pedir un aumento en la consola.
> - **Miniatura personalizada** requiere canal verificado por teléfono (<https://www.youtube.com/verify>).

## 4. Configurar el canal

Edita `~/.config/yt-pubx/config.json`:

```json
{
  "canal_padrao": "principal",
  "codex_modelo": "",
  "baixador": "yt-dlp -f \"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b\" -o \"{outdir}/%(title).80s.%(ext)s\" {url}",
  "imagem_reserva": { "url": "", "modelo": "" },
  "canais": {
    "principal": {
      "nome": "Mi Canal",
      "url": "https://www.youtube.com/@meucanal",
      "sobre": "Canal de tutoriales cortos sobre fotografía con celular.",
      "assinatura": "Suscríbete: https://www.youtube.com/@meucanal",
      "idioma": "pt",
      "categoria": "27",
      "privacy": "public",
      "thumb": {
        "marca": "MI CANAL",
        "fonte": "",
        "cor_texto": "#ffffff",
        "cor_marca": "#f0e805",
        "cor_destaque": "#f91f06"
      }
    }
  }
}
```

| Campo | Qué hace |
|---|---|
| `sobre` | una frase sobre el canal; Codex la usa para acertar el tono |
| `assinatura` | línea fija que cierra cada descripción (enlace del sitio, suscripción…) |
| `categoria` | id de la categoría de YouTube (27 Educación, 28 Ciencia y tecnología, 22 Personas y blogs) |
| `thumb.marca` | texto de la etiqueta en la esquina superior izquierda (vacío = sin etiqueta) |
| `thumb.fonte` | ruta de un `.ttf` (vacío = Montserrat ExtraBold si está instalada; si no, DejaVu Sans Bold) |
| `codex_modelo` | modelo de Codex (vacío = el predeterminado de tu cuenta) |
| `baixador` | comando para descargar enlaces que no son `.mp4` directo; `{url}` y `{outdir}` se reemplazan |
| `imagem_reserva` | opcional: servidor de imágenes local usado si Codex falla (`POST {model, prompt, width, height}` → `{"image": base64}`) |

Después autoriza (abre el navegador; entra con la cuenta dueña del canal):

```bash
yt-pubx auth principal --client-secret ~/Downloads/client_secret_XXXX.json
yt-pubx canais
```

El token queda en `~/.config/yt-pubx/tokens/principal.json` (permiso 600). Para más canales,
repite: un bloque en `canais` + un `yt-pubx auth <nombre>`. El mismo `client_secret` sirve para
todos los canales; cada `auth` se hace con la sesión de la cuenta dueña de ese canal (o eligiendo el canal
de marca en la pantalla de Google).

> ¿Ya tienes las credenciales guardadas en otro lugar? En vez del `auth`, pon en el canal
> `"credenciais_cmd": "<comando>"`: un comando que imprime
> `{"client_id": "...", "client_secret": "...", "refresh_token": "..."}`.

## 5. Publicar

```bash
# revisar sin enviar: genera texto y miniatura y muestra todo
yt-pubx publicar video.mp4 --contexto "De qué trata el video + enlaces oficiales" --dry-run

# ¿te gustó? publica exactamente lo que viste (sin generar otro arte)
yt-pubx publicar video.mp4 --plano ~/.local/share/yt-pubx/trabalhos/<carpeta>/plano.json

# cambiar solo la frase de la miniatura
yt-pubx publicar video.mp4 --plano .../plano.json --frase-thumb "De cero al aire"

# otro canal, a partir de un enlace, programado
yt-pubx publicar https://exemplo.com/video.mp4 --canal segundo --contexto "..." --agendar "2026-12-01 18:00"

# todo a mano, sin Codex
yt-pubx publicar video.mp4 --title "..." --description "..." --tags "a,b,c" --thumb capa.jpg
```

| Opción | |
|---|---|
| `--contexto`, `--contexto-arquivo`, `--legenda` | materia prima para que Codex escriba (los subtítulos SRT también se suben) |
| `--title`, `--description`, `--tags` | fija lo que ya tienes; Codex completa el resto |
| `--frase-thumb`, `--cena-thumb` | texto de la miniatura (2–4 palabras) y la escena del arte |
| `--thumb capa.jpg` / `--thumb-arte arte.png` | miniatura lista / arte listo (solo aplica frase y marca) |
| `--sem-thumb` | no genera ni envía miniatura (automático en video vertical/Short) |
| `--privacy public\|unlisted\|private`, `--agendar "AAAA-MM-DD HH:MM"` | visibilidad; programar sube el video como privado y YouTube lo publica a la hora indicada |
| `--canal`, `--idioma`, `--categoria` | sobrescriben el config |
| `--sem-legenda` | usa el SRT solo como contexto |
| `--dry-run`, `--plano`, `--manter` | revisar antes; publicar lo revisado; conservar el video descargado |

Un video vertical corto (hasta 3 min) se convierte en **Short** automáticamente; pon `#Shorts` en el título si quieres
dejarlo explícito.

**Salidas:** `~/.local/share/yt-pubx/trabalhos/<fecha>-<nombre>/` (plano.json, thumb.jpg, thumb_arte.png)
y `~/.local/share/yt-pubx/historico.jsonl` (una línea por publicación).

**Editar un video ya publicado** (título, descripción o etiquetas; lo demás queda igual):

```bash
./yt-pubx atualizar https://www.youtube.com/watch?v=XXXXXXXXXXX --canal lives1 --description-arquivo descricao.txt
```

## 6. Usar con un agente (Claude Code, Codex)

Pon esto en una instrucción de tu agente (CLAUDE.md / AGENTS.md):

> Cuando te pida publicar un video en YouTube: reúne el contexto (tema, enlaces oficiales,
> SRT), ejecuta `yt-pubx publicar <video> --contexto "..." --dry-run`, abre la `thumb.jpg` y revisa
> que el texto sea legible y que el título y la descripción sean correctos; luego publica con
> `--plano <carpeta>/plano.json` y pásame el enlace.

Así nació yt-pubx: el pedido "publica estos 3 videos" se convirtió en tres dry-runs revisados,
un cambio de frase en la miniatura y tres publicaciones con miniatura en menos de 5 minutos.

## Problemas comunes

| Mensaje | Causa / solución |
|---|---|
| `token OAuth recusado` | token expirado (app en modo Prueba: 7 días) → `yt-pubx auth <canal>` |
| `thumb não aplicada … verify` | canal sin verificación por teléfono |
| `legenda não enviada … force-ssl` | token antiguo sin el alcance de subtítulos → `yt-pubx auth` de nuevo |
| `upload não iniciou (403) quotaExceeded` | se acabó la cuota del día → mañana, o pide un aumento |
| el video publicado queda privado | proyecto de API sin auditoría (ver paso 3) |
| `codex não gerou arte.png` | Codex sin generador de imágenes en tu cuenta → `--thumb-arte`, `--thumb` o `imagem_reserva` |

## Licencia

MIT. Proyecto educativo independiente; no es un producto de Google, de YouTube ni de OpenAI.
