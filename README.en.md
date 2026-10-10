# yt-pubx — publish any video to YouTube with one command

[![yt-pubx](guia/assets/banner-en.jpg)](https://inematds.github.io/yt-pubx/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

yt-pubx is a command-line program that publishes videos to YouTube for you. It is meant for people who publish often, on one or several channels, and don't want to fill in the title, description, tags and thumbnail by hand every time. From a short text or the video's subtitles, the Codex CLI writes the texts and creates the thumbnail art, and yt-pubx uploads everything through the official YouTube API. To use it, you need Python, a logged-in Codex CLI and a free Google Cloud project with the YouTube Data API enabled.

## 📖 User guide

Full guide (landing + step by step): **https://inematds.github.io/yt-pubx/guia/en/**

---

You point to a video (file or link) and `yt-pubx` does the rest:

1. **Writes the title, description and tags** with the Codex CLI, from your context and/or the subtitles.
2. **Creates the thumbnail**: the art comes from the Codex image generator (`image_gen`) and `yt-pubx`
   overlays the phrase, the brand and your channel's colors.
3. **Publishes directly** to the chosen channel (public, unlisted, private or scheduled),
   applies the thumbnail and, if there is an SRT, uploads the subtitles.

It works with as many channels as you want. Everything runs on your machine; the text and the art
use your Codex (ChatGPT) subscription, with no model API key.

```bash
yt-pubx publicar aula.mp4 --contexto "Lesson 3 of course X. Page: https://..." --legenda aula.srt
```

---

## 1. What you need

| Item | What for |
|---|---|
| Python 3.10+ with `requests` and `Pillow` | run the script (`pip install requests pillow`) |
| `ffprobe` (comes with ffmpeg) | read the video duration |
| [Codex CLI](https://github.com/openai/codex) logged in (`npm i -g @openai/codex` → `codex login`) | write the text and generate the thumbnail art |
| A Google Cloud project with the **YouTube Data API v3** | publish (step 3) |
| `yt-dlp` (optional) | publish from a YouTube, TikTok, Instagram… link |

## 2. Install

```bash
git clone https://github.com/inematds/yt-pubx.git
cd yt-pubx
ln -s "$PWD/yt-pubx" ~/.local/bin/yt-pubx   # optional: call it from any folder
yt-pubx init                                 # creates ~/.config/yt-pubx/config.json
```

## 3. Enable YouTube in Google Cloud (once)

1. Go to <https://console.cloud.google.com/> and create a project (e.g. `meu-yt-pubx`).
2. **APIs & Services → Library** → search for **YouTube Data API v3** → **Enable**.
3. **APIs & Services → OAuth consent screen** (Google Auth Platform):
   - User type **External**; app name and your email.
   - Under **Audience / Test users**, add the email of the Google account that owns the channel.
4. **APIs & Services → Credentials → Create credentials → OAuth client ID**:
   - Application type: **Desktop app**. An existing **Web application** client also works: add a
     `http://localhost:<port>/...` address under *Authorized redirect URIs* (see the guide below).
   - Download the JSON (`client_secret_....json`). Keep it outside any repository.

> **First time?** Read [docs/autorizar-canal.en.md](docs/autorizar-canal.en.md): a step-by-step guide
> with no jargon, covering every error Google shows and what to do.

> **Google pitfalls worth knowing in advance:**
> - **App in "Testing" mode**: access expires in **7 days** and you need to run `yt-pubx auth` again.
>   To keep it from expiring, click **Publish app** (it moves to "In production"; for personal use, the
>   "unverified app" screen appears, just go through *Advanced → continue*).
> - **Unaudited project**: YouTube may lock as **private** the videos uploaded by new API projects
>   that have not yet passed the YouTube API Services audit. If your
>   videos get stuck as private, request the audit through the *YouTube API Services* form
>   (it's free) or publish as `private` and switch to public in Studio.
> - **Quota**: the default quota is 10,000 units/day; each video upload consumes most
>   of it (enough for a few videos per day). You can request an increase in the console.
> - **Custom thumbnail** requires a phone-verified channel (<https://www.youtube.com/verify>).

## 4. Configure the channel

Edit `~/.config/yt-pubx/config.json`:

```json
{
  "canal_padrao": "principal",
  "codex_modelo": "",
  "baixador": "yt-dlp -f \"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b\" -o \"{outdir}/%(title).80s.%(ext)s\" {url}",
  "imagem_reserva": { "url": "", "modelo": "" },
  "canais": {
    "principal": {
      "nome": "My Channel",
      "url": "https://www.youtube.com/@meucanal",
      "sobre": "Channel with short smartphone photography tutorials.",
      "assinatura": "Subscribe: https://www.youtube.com/@meucanal",
      "idioma": "pt",
      "categoria": "27",
      "privacy": "public",
      "thumb": {
        "marca": "MY CHANNEL",
        "fonte": "",
        "cor_texto": "#ffffff",
        "cor_marca": "#f0e805",
        "cor_destaque": "#f91f06"
      }
    }
  }
}
```

| Field | What it does |
|---|---|
| `sobre` | one sentence about the channel; Codex uses it to get the tone right |
| `assinatura` | fixed line that closes every description (site link, subscribe…) |
| `categoria` | YouTube category id (27 Education, 28 Science & Technology, 22 People & Blogs) |
| `thumb.marca` | label text in the top-left corner (empty = no label) |
| `thumb.fonte` | path to a `.ttf` (empty = Montserrat ExtraBold if installed, otherwise DejaVu Sans Bold) |
| `codex_modelo` | Codex model (empty = your account's default) |
| `baixador` | command to download links that are not a direct `.mp4`; `{url}` and `{outdir}` are substituted |
| `imagem_reserva` | optional: local image server used if Codex fails (`POST {model, prompt, width, height}` → `{"image": base64}`) |

Then authorize (it opens the browser; sign in with the account that owns the channel):

```bash
yt-pubx auth principal --client-secret ~/Downloads/client_secret_XXXX.json
yt-pubx canais
```

Browser on another machine (server, remote desktop)? After **Allow** the page shows a connection error:
copy the URL from the address bar, paste it into the `yt-pubx auth` terminal and press Enter.
The authorization link is also saved to `~/.config/yt-pubx/auth-<channel>.txt`, so you can copy it unbroken.

The token is stored in `~/.config/yt-pubx/tokens/principal.json` (permission 600). For more channels,
repeat: one block in `canais` + one `yt-pubx auth <name>`. The same `client_secret` works for
all channels; each `auth` is done signed in to the account that owns that channel (or by choosing the brand
channel on the Google screen).

> Already have the credentials stored somewhere else? Instead of `auth`, put in the channel
> `"credenciais_cmd": "<command>"`: a command that prints
> `{"client_id": "...", "client_secret": "...", "refresh_token": "..."}`.

## 5. Publish

```bash
# review without uploading: generates text and thumbnail and shows everything
yt-pubx publicar video.mp4 --contexto "What the video is about + official links" --dry-run

# like it? publish exactly what you saw (without generating new art)
yt-pubx publicar video.mp4 --plano ~/.local/share/yt-pubx/trabalhos/<folder>/plano.json

# change only the thumbnail phrase
yt-pubx publicar video.mp4 --plano .../plano.json --frase-thumb "From zero to live"

# another channel, from a link, scheduled
yt-pubx publicar https://exemplo.com/video.mp4 --canal segundo --contexto "..." --agendar "2026-12-01 18:00"

# everything by hand, without Codex
yt-pubx publicar video.mp4 --title "..." --description "..." --tags "a,b,c" --thumb capa.jpg
```

| Option | |
|---|---|
| `--contexto`, `--contexto-arquivo`, `--legenda` | raw material for Codex to write from (the SRT subtitles are also uploaded) |
| `--title`, `--description`, `--tags` | pins what you already have; Codex fills in the rest |
| `--frase-thumb`, `--cena-thumb` | thumbnail text (2–4 words) and the art scene |
| `--thumb capa.jpg` / `--thumb-arte arte.png` | ready-made thumbnail / ready-made art (only applies phrase and brand) |
| `--sem-thumb` | do not generate or send a thumbnail (automatic for vertical videos/Shorts) |
| `--privacy public\|unlisted\|private`, `--agendar "AAAA-MM-DD HH:MM"` | visibility; scheduling uploads as private and YouTube publishes at the set time |
| `--canal`, `--idioma`, `--categoria` | override the config |
| `--sem-legenda` | uses the SRT only as context |
| `--dry-run`, `--plano`, `--manter` | review first; publish what was reviewed; keep the downloaded video |

A short vertical video (up to 3 min) automatically becomes a **Short**; add `#Shorts` to the title if you want
to make it explicit.

**Outputs:** `~/.local/share/yt-pubx/trabalhos/<date>-<name>/` (plano.json, thumb.jpg, thumb_arte.png)
and `~/.local/share/yt-pubx/historico.jsonl` (one line per publication).

**Edit a video that is already published** (title, description or tags; everything else stays as is):

```bash
./yt-pubx atualizar https://www.youtube.com/watch?v=XXXXXXXXXXX --canal lives1 --description-arquivo descricao.txt
```

## 6. Use with an agent (Claude Code, Codex)

Put this in your agent's instructions (CLAUDE.md / AGENTS.md):

> When I ask to publish a video to YouTube: gather the context (topic, official links,
> SRT), run `yt-pubx publicar <video> --contexto "..." --dry-run`, open `thumb.jpg` and check
> that the text is legible and the title and description are correct; then publish with
> `--plano <folder>/plano.json` and give me the link.

That is how yt-pubx was born: the request "publish these 3 videos" became three reviewed dry-runs,
one thumbnail phrase swap and three publications with thumbnails in under 5 minutes.

## Common problems

| Message | Cause / fix |
|---|---|
| `redirect_uri_mismatch` | "Web application" client without the local address registered → [docs/autorizar-canal.en.md](docs/autorizar-canal.en.md) |
| `single value: access_type` | link copied broken from the terminal → open it from `~/.config/yt-pubx/auth-<channel>.txt` |
| connection error on `localhost` after Allow | browser on another machine → paste the address-bar URL into the `auth` terminal |
| `token OAuth recusado` | expired token (app in Testing mode: 7 days) → `yt-pubx auth <channel>` |
| `thumb não aplicada … verify` | channel without phone verification |
| `legenda não enviada … force-ssl` | old token without the captions scope → `yt-pubx auth` again |
| `upload não iniciou (403) quotaExceeded` | the day's quota ran out → tomorrow, or request an increase |
| published video stays private | unaudited API project (see step 3) |
| `codex não gerou arte.png` | Codex without an image generator on your account → `--thumb-arte`, `--thumb` or `imagem_reserva` |

## License

MIT. Independent educational project; not a product of Google, YouTube or OpenAI.
