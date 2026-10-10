# Changelog

## 2.3.0 — 2026-10-10
- `yt-pubx auth` aceita client **Aplicativo da Web**: usa o endereço local cadastrado no JSON, ou `--redirect`.
- Navegador em outra máquina: cole no terminal a URL final (com `code=`) e a autorização termina.
- O link de autorização fica também em `~/.config/yt-pubx/auth-<canal>.txt` (copiar sem quebra de linha); espera 30 min.
- Novo guia leigo [docs/autorizar-canal.md](docs/autorizar-canal.md) com os erros reais do Google e a saída de cada um.

## 2.2.0 — 2026-10-08
- `--sem-thumb`: não gera nem envia thumb. Liga sozinho em vídeo vertical (Short), que não usa thumb.
- Corrige erro depois do envio quando não havia thumb (`ok` indefinido ao gravar o histórico).

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
