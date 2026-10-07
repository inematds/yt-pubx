# Changelog

## 2.1.0 — 2026-10-07
- `yt-pubx atualizar <id|URL>`: edita título, descrição ou tags de um vídeo já publicado.

## 2.0.0 — 2026-10-07
- Ferramenta independente: config em `~/.config/yt-pubx/config.json`, canais ilimitados.
- `yt-pubx init` e `yt-pubx auth` (OAuth "App para computador" com PKCE, escopos de upload, gerência e legendas).
- `credenciais_cmd` por canal para quem já guarda as credenciais em outro lugar.
- Compositor de thumb próprio (frase, marca e cores por canal).
- Baixador configurável (yt-dlp por padrão) e `imagem_reserva` opcional.

## 1.1.1
- `--plano` publica exatamente o que o `--dry-run` gerou; aviso claro para legenda sem escopo.

## 1.0.0
- Publicação direta com texto e thumb pelo Codex.
