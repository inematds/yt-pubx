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

## Distribuição das publicações diretas — lives1 e lives4

Após publicar diretamente no **lives1**, encaminhar também o conteúdo ao **Metricool da conta inematds**, marca **inema.tds**, como no lives4 (ordem do Nei, 16/11/2026). Não pedir outro OK para essa etapa. Conector correto: `metricool-inematds`; redes Instagram/TikTok vinculadas à marca. Referência: `~/projetos/metricool-inematds/README.md` e `publicar.sh` com `MARCA=inema.tds`.

Respeitar a validação de formato/duração e `intervalo.py` (mínimo de uma hora entre posts da mesma marca). Se o arquivo não for aceito pelo fluxo existente, registrar/avisar a pendência, sem cortar ou converter arbitrariamente e sem dizer que agendou. Não republicar histórico por causa dessa nova regra. O upload do YouTube só conclui a etapa YouTube; exigir recibo próprio do Metricool antes de declarar essa distribuição concluída.

A integração executável existe desde v2.9.1 e está configurada localmente em lives1 e lives4. Ver [docs/pos-publicacao.md](docs/pos-publicacao.md) para configuração, estados e retomada. Não chamar o publicador novamente por fora após o hook concluir.

## Self-learning

When I correct you, or you catch yourself making a mistake: before continuing, add the lesson as a one-line rule under ## Lessons, so it never happens again.

## Lessons
- `yt-pubx auth`: nunca reiniciar o comando depois de mandar o link à pessoa — cada execução tem state e PKCE próprios e o código do link antigo não serve. Em 10/10 (canal Aventuras) reiniciei para testar um atalho e a autorização da pessoa se perdeu. (10/10/2026)
