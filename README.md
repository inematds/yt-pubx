# yt-pubx — publique qualquer vídeo no YouTube com um comando

[![yt-pubx](guia/assets/banner.jpg)](https://inematds.github.io/yt-pubx/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O yt-pubx é um programa de linha de comando que publica vídeos no YouTube por você. Ele serve para quem publica com frequência, em um ou vários canais, e não quer preencher título, descrição, tags e thumb à mão toda vez. A partir de um texto curto ou da legenda do vídeo, o Codex CLI escreve os textos e cria a arte da thumb, e o yt-pubx envia tudo pela API oficial do YouTube. Para usar, você precisa de Python, do Codex CLI logado e de um projeto gratuito no Google Cloud com a YouTube Data API ativada.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/yt-pubx/guia/**

---

Você aponta um vídeo (arquivo ou link) e o `yt-pubx` faz o resto:

1. **Escreve título, descrição e tags** com o Codex CLI, a partir de um contexto seu e/ou da legenda.
2. **Cria a thumb**: a arte sai do gerador de imagem do Codex (`image_gen`) e o `yt-pubx`
   aplica por cima a frase, a marca e as cores do seu canal.
3. **Publica direto** no canal escolhido (público, não listado, privado ou agendado),
   aplica a thumb e, se houver SRT, envia a legenda.

Funciona com quantos canais você quiser. Tudo roda na sua máquina; o texto e a arte
usam a sua assinatura do Codex (ChatGPT), sem chave de API de modelo.

```bash
yt-pubx publicar aula.mp4 --contexto "Aula 3 do curso X. Página: https://..." --legenda aula.srt
```

---

## 1. O que você precisa

| Item | Para quê |
|---|---|
| Python 3.10+ com `requests` e `Pillow` | rodar o script (`pip install requests pillow`) |
| `ffprobe` (vem com o ffmpeg) | ler a duração do vídeo |
| [Codex CLI](https://github.com/openai/codex) logado (`npm i -g @openai/codex` → `codex login`) | escrever o texto e gerar a arte da thumb |
| Um projeto no Google Cloud com a **YouTube Data API v3** | publicar (passo 3) |
| `yt-dlp` (opcional) | publicar a partir de link do YouTube, TikTok, Instagram… |

## 2. Instalar

```bash
git clone https://github.com/inematds/yt-pubx.git
cd yt-pubx
ln -s "$PWD/yt-pubx" ~/.local/bin/yt-pubx   # opcional: chamar de qualquer pasta
yt-pubx init                                 # cria ~/.config/yt-pubx/config.json
```

## 3. Liberar o YouTube no Google Cloud (uma vez)

1. Entre em <https://console.cloud.google.com/>, crie um projeto (ex.: `meu-yt-pubx`).
2. **APIs e serviços → Biblioteca** → procure **YouTube Data API v3** → **Ativar**.
3. **APIs e serviços → Tela de consentimento OAuth** (Google Auth Platform):
   - Tipo de usuário **Externo**; nome do app e seu e-mail.
   - Em **Público-alvo / Usuários de teste**, adicione o e-mail da conta Google dona do canal.
4. **APIs e serviços → Credenciais → Criar credenciais → ID do cliente OAuth**:
   - Tipo de aplicativo: **App para computador** (Desktop). Se você já tem um client
     **Aplicativo da Web**, ele também serve: cadastre nele um endereço `http://localhost:<porta>/...`
     em *URIs de redirecionamento autorizados* (detalhes no guia abaixo).
   - Baixe o JSON (`client_secret_....json`). Guarde fora de qualquer repositório.

> **Primeira vez?** Leia [docs/autorizar-canal.md](docs/autorizar-canal.md): o passo a passo
> sem termos técnicos, com cada erro que o Google mostra e o que fazer.

> **Duas armadilhas do Google que valem saber antes:**
> - **App em modo "Teste"**: o acesso expira em **7 dias** e você precisa rodar `yt-pubx auth` de novo.
>   Para não expirar, clique em **Publicar app** (passa para "Em produção"; para uso próprio, a tela
>   de "app não verificado" aparece, é só seguir em *Avançado → continuar*).
> - **Projeto sem auditoria**: o YouTube pode travar como **privado** os vídeos enviados por projetos
>   de API novos que ainda não passaram pela auditoria dos serviços de API do YouTube. Se os seus
>   vídeos ficarem presos em privado, peça a auditoria no formulário de *YouTube API Services*
>   (é gratuito) ou publique como `private` e troque para público no Studio.
> - **Cota**: a cota padrão é de 10.000 unidades/dia; cada envio de vídeo consome a maior parte
>   disso (o suficiente para poucos vídeos por dia). Dá para pedir aumento no console.
> - **Thumb personalizada** exige canal verificado por telefone (<https://www.youtube.com/verify>).

## 4. Configurar o canal

Edite `~/.config/yt-pubx/config.json`:

```json
{
  "canal_padrao": "principal",
  "codex_modelo": "",
  "baixador": "yt-dlp -f \"bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b\" -o \"{outdir}/%(title).80s.%(ext)s\" {url}",
  "imagem_reserva": { "url": "", "modelo": "" },
  "canais": {
    "principal": {
      "nome": "Meu Canal",
      "url": "https://www.youtube.com/@meucanal",
      "sobre": "Canal de tutoriais curtos sobre fotografia com celular.",
      "assinatura": "Inscreva-se: https://www.youtube.com/@meucanal",
      "idioma": "pt",
      "categoria": "27",
      "privacy": "public",
      "thumb": {
        "marca": "MEU CANAL",
        "fonte": "",
        "cor_texto": "#ffffff",
        "cor_marca": "#f0e805",
        "cor_destaque": "#f91f06"
      }
    }
  }
}
```

| Campo | O que faz |
|---|---|
| `sobre` | uma frase sobre o canal; o Codex usa para acertar o tom |
| `assinatura` | linha fixa que fecha toda descrição (link do site, inscrição…) |
| `categoria` | id da categoria do YouTube (27 Educação, 28 Ciência e tecnologia, 22 Pessoas e blogs) |
| `thumb.marca` | texto da etiqueta no canto superior esquerdo (vazio = sem etiqueta) |
| `thumb.fonte` | caminho de um `.ttf` (vazio = Montserrat ExtraBold se instalada, senão DejaVu Sans Bold) |
| `codex_modelo` | modelo do Codex (vazio = o padrão da sua conta) |
| `baixador` | comando para baixar links que não são `.mp4` direto; `{url}` e `{outdir}` são trocados |
| `imagem_reserva` | opcional: servidor de imagem local usado se o Codex falhar (`POST {model, prompt, width, height}` → `{"image": base64}`) |

Depois autorize (abre o navegador; entre com a conta dona do canal):

```bash
yt-pubx auth principal --client-secret ~/Downloads/client_secret_XXXX.json
yt-pubx canais
```

Navegador em outra máquina (servidor, acesso remoto)? Depois do **Permitir** a página dá erro de
conexão: copie a URL da barra de endereço, cole no terminal do `yt-pubx auth` e tecle Enter.
O link de autorização também fica em `~/.config/yt-pubx/auth-<canal>.txt`, para copiar sem quebra.

O token fica em `~/.config/yt-pubx/tokens/principal.json` (permissão 600). Para mais canais,
repita: um bloco em `canais` + um `yt-pubx auth <nome>`. O mesmo `client_secret` serve para
todos os canais; cada `auth` é feito logado na conta dona daquele canal (ou escolhendo o canal
de marca na tela do Google).

> Já tem as credenciais guardadas em outro lugar? Em vez do `auth`, coloque no canal
> `"credenciais_cmd": "<comando>"`: um comando que imprime
> `{"client_id": "...", "client_secret": "...", "refresh_token": "..."}`.

## 5. Publicar

```bash
# conferir sem enviar: gera texto e thumb e mostra tudo
yt-pubx publicar video.mp4 --contexto "Do que o vídeo trata + links oficiais" --dry-run

# gostou? publique exatamente o que viu (sem gerar outra arte)
yt-pubx publicar video.mp4 --plano ~/.local/share/yt-pubx/trabalhos/<pasta>/plano.json

# trocar só a frase da thumb
yt-pubx publicar video.mp4 --plano .../plano.json --frase-thumb "Do zero ao ar"

# outro canal, a partir de um link, agendado
yt-pubx publicar https://exemplo.com/video.mp4 --canal segundo --contexto "..." --agendar "2026-12-01 18:00"

# tudo à mão, sem Codex
yt-pubx publicar video.mp4 --title "..." --description "..." --tags "a,b,c" --thumb capa.jpg
```

| Opção | |
|---|---|
| `--contexto`, `--contexto-arquivo`, `--legenda` | matéria-prima para o Codex escrever (a legenda SRT também é enviada) |
| `--title`, `--description`, `--tags` | fixa o que você já tem; o Codex completa o resto |
| `--frase-thumb`, `--cena-thumb` | texto da thumb (2–4 palavras) e a cena da arte |
| `--thumb capa.jpg` / `--thumb-arte arte.png` | thumb pronta / arte pronta (só aplica frase e marca) |
| `--sem-thumb` | não gera nem envia thumb (automático em vídeo vertical/Short) |
| `--privacy public\|unlisted\|private`, `--agendar "AAAA-MM-DD HH:MM"` | visibilidade; agendar sobe privado e o YouTube publica no horário |
| `--canal`, `--idioma`, `--categoria` | sobrepõem o config |
| `--sem-legenda` | usa o SRT só como contexto |
| `--dry-run`, `--plano`, `--manter` | conferir antes; publicar o que foi conferido; guardar o vídeo baixado |

Vídeo vertical curto (até 3 min) vira **Short** automaticamente; ponha `#Shorts` no título se quiser
deixar explícito.

**Saídas:** `~/.local/share/yt-pubx/trabalhos/<data>-<nome>/` (plano.json, thumb.jpg, thumb_arte.png)
e `~/.local/share/yt-pubx/historico.jsonl` (uma linha por publicação).

**Editar um vídeo já publicado** (título, descrição ou tags; o resto fica como está):

```bash
./yt-pubx atualizar https://www.youtube.com/watch?v=XXXXXXXXXXX --canal lives1 --description-arquivo descricao.txt
```

## 6. Usar com um agente (Claude Code, Codex)

Ponha numa instrução do seu agente (CLAUDE.md / AGENTS.md):

> Quando eu pedir para publicar um vídeo no YouTube: junte o contexto (assunto, links oficiais,
> SRT), rode `yt-pubx publicar <video> --contexto "..." --dry-run`, abra a `thumb.jpg` e confira
> se o texto está legível e se título e descrição estão corretos; então publique com
> `--plano <pasta>/plano.json` e me passe o link.

Foi assim que o yt-pubx nasceu: o pedido "publica esses 3 vídeos" virou três dry-runs conferidos,
uma troca de frase na thumb e três publicações com thumb em menos de 5 minutos.

## Problemas comuns

| Mensagem | Causa / saída |
|---|---|
| `redirect_uri_mismatch` | client "Aplicativo da Web" sem o endereço local cadastrado → [docs/autorizar-canal.md](docs/autorizar-canal.md) |
| `single value: access_type` | link copiado quebrado do terminal → abra pelo `~/.config/yt-pubx/auth-<canal>.txt` |
| erro de conexão em `localhost` depois do Permitir | navegador em outra máquina → cole a URL da barra no terminal do `auth` |
| `token OAuth recusado` | token expirado (app em modo Teste: 7 dias) → `yt-pubx auth <canal>` |
| `thumb não aplicada … verify` | canal sem verificação por telefone |
| `legenda não enviada … force-ssl` | token antigo sem o escopo de legendas → `yt-pubx auth` de novo |
| `upload não iniciou (403) quotaExceeded` | cota do dia acabou → amanhã, ou peça aumento |
| vídeo publicado fica privado | projeto de API sem auditoria (ver passo 3) |
| `codex não gerou arte.png` | Codex sem gerador de imagem na sua conta → `--thumb-arte`, `--thumb` ou `imagem_reserva` |

## Licença

MIT. Projeto educacional independente; não é produto do Google, do YouTube nem da OpenAI.
