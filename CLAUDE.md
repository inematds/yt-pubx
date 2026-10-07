# CLAUDE.md — yt-pubx

Ferramenta de linha de comando que publica vídeo direto no YouTube (texto e thumb pelo Codex).
Um arquivo só: `yt-pubx` (Python). Config do usuário em `~/.config/yt-pubx/` e dados em
`~/.local/share/yt-pubx/`. Nada de credencial, canal ou caminho pessoal entra neste repo.

Quando pedirem "publica esse vídeo (no canal X)":

1. Canal = `canal_padrao` do config, ou o que a pessoa disser (`yt-pubx canais`).
2. Juntar contexto: assunto, links oficiais, SRT se houver.
3. `yt-pubx publicar <video> --contexto "..." [--legenda srt] --dry-run`; conferir título,
   descrição e OLHAR a `thumb.jpg` (frase legível, sem repetir entre vídeos de um lote).
4. Publicar com `--plano <pasta>/plano.json` (reusa texto e arte; dá pra trocar `--frase-thumb`).
   Informar URL e Studio.

Regras:
- Thumb = Codex image_gen; `imagem_reserva` só se o Codex falhar.
- Versão em `VERSION` dentro de `yt-pubx`; registrar no CHANGELOG.md.
- Testar mudança com `--dry-run` + `--thumb-arte` (não gasta geração nem publica).

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule under ## Lessons, so it never happens again.

## Lessons
