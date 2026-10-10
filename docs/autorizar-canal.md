# Autorizar um canal novo — passo a passo sem susto

[PT](autorizar-canal.md) · [EN](autorizar-canal.en.md) · [ES](autorizar-canal.es.md)

Este guia é para quem nunca mexeu no Google Cloud. Ele nasceu de uma autorização real de um canal novo (outubro de 2026), que deu errado
várias vezes antes de dar certo. Cada erro que
apareceu está aqui, com o que ele quer dizer e o que fazer.

## Por que o YouTube pede essa autorização

Publicar um vídeo por programa exige duas coisas diferentes:

| O quê | Para que serve | Onde fica |
|---|---|---|
| **Client ID + Client Secret** | dizem ao Google *qual programa* está pedindo | o arquivo `client_secret_....json` que você baixa do Google Cloud |
| **Token de acesso** | diz que *o dono do canal* deixou esse programa publicar por ele | é criado pelo `yt-pubx auth`, uma única vez |

Ter só o primeiro é como ter a chave do carro sem a permissão do dono: o Google recusa o envio.
A autorização é o momento em que você, logado na conta dona do canal, clica em **Permitir**.
Depois disso o token fica guardado e as próximas publicações não pedem nada.

## Antes de começar: confira 4 coisas

1. **Você sabe qual conta Google é a dona do canal.** Abra o canal no YouTube, logado, e veja no
   canto superior direito qual e-mail aparece. É com essa conta que você vai autorizar.
2. **A YouTube Data API v3 está ativada** no projeto do Google Cloud (Biblioteca → YouTube Data API v3 → Ativar).
3. **A tela de consentimento tem você como usuário de teste**, ou o app está publicado
   (Google Auth Platform → Público-alvo → Usuários de teste → adicionar o e-mail da conta dona do canal).
4. **Você sabe o tipo do seu client.** Em Credenciais, ao lado do nome do client, aparece
   "App para computador" ou "Aplicativo da Web". Isso muda um detalhe, explicado abaixo.

## O caminho mais simples: client "App para computador"

Se você ainda vai criar o client, escolha **App para computador**. Ele aceita o retorno em
qualquer porta local e não exige cadastrar endereço nenhum.

```bash
yt-pubx auth meucanal --client-secret ~/Downloads/client_secret_XXXX.json
```

O navegador abre sozinho. Entre com a conta dona do canal, clique em **Continuar** e em **Permitir**.
Quando aparecer "yt-pubx: pode fechar esta aba", acabou.

## Se o seu client é "Aplicativo da Web"

Um client Web só aceita voltar para um endereço **exatamente igual** a um cadastrado nele. Se o
endereço for diferente em uma letra, uma barra ou na porta, o Google mostra `redirect_uri_mismatch`.

1. No Google Cloud, abra **Credenciais → seu client → URIs de redirecionamento autorizados**.
2. Clique em **+ Adicionar URI** e cole `http://localhost:8737/callback` (pode ser outro, desde que comece com `http://localhost:`).
3. **Salve** e espere uns 5 minutos.
4. Baixe o JSON do client de novo (ele passa a trazer esse endereço) e rode:

```bash
yt-pubx auth meucanal --client-secret ~/Downloads/client_secret_XXXX.json
```

O yt-pubx lê o endereço local cadastrado no JSON e usa exatamente ele. Se preferir dizer na mão:
`--redirect http://localhost:8737/callback`.

## Quando o navegador está em outro computador

Comum quando o yt-pubx roda num servidor e você está no seu notebook (acesso remoto, SSH).
Depois do **Permitir**, o Google manda o navegador para `http://localhost:...`, que no seu
notebook não existe. Aparece **"Não é possível acessar esse site"** ou **"ERR_CONNECTION_REFUSED"**.

**Isso não é erro.** A autorização deu certo e o código está na barra de endereço.

1. Clique na barra de endereço dessa página de erro.
2. Copie a URL inteira (começa com `http://localhost:...` e tem `code=` no meio).
3. Volte ao terminal onde o `yt-pubx auth` está esperando, cole e tecle **Enter**.

Pronto: o yt-pubx termina sozinho e mostra "Canal ... autorizado".

## Os erros que apareceram de verdade e o que significam

| O que aparece | O que quer dizer | O que fazer |
|---|---|---|
| `Error 400: redirect_uri_mismatch` | o client é Web e o endereço de retorno não está cadastrado | seção "Se o seu client é Aplicativo da Web" acima |
| `OAuth 2 parameters can only have a single value: access_type` | o link foi copiado **quebrado** do terminal (pedaços repetidos ou faltando) | abra o link pelo arquivo `~/.config/yt-pubx/auth-<canal>.txt`, ou com ctrl+clique no terminal |
| `Access blocked: ... has not completed the Google verification process` | a conta não está na lista de usuários de teste | adicione o e-mail em Público-alvo → Usuários de teste |
| Tela "Choose an account" sem a conta certa | o navegador não está logado na conta dona do canal | clique em **Use another account** e entre com ela |
| `ERR_CONNECTION_REFUSED` / "Não é possível acessar esse site" depois do Permitir | navegador em outra máquina | copie a URL da barra e cole no terminal (seção acima) |
| "Essa URL é de outro link" | você usou um link de uma tentativa anterior | cada `yt-pubx auth` gera um link novo; use o da tentativa que está rodando |
| `thumb não aplicada … verify` (na hora de publicar) | canal novo, sem verificação por telefone | entre em <https://www.youtube.com/verify> com a conta dona do canal |

## Três cuidados que economizam tempo

- **Chegar na tela "Choose an account" não prova que deu certo.** O Google só confere o endereço
  de retorno depois que você escolhe a conta. Só conte vitória com "pode fechar esta aba"
  ou "Canal ... autorizado".
- **Não feche o comando `yt-pubx auth` no meio.** Cada vez que ele roda, cria um link novo. O código de
  um link antigo não serve no comando novo.
- **Canal novo publica com limite baixo e sem capa.** Até verificar o telefone em
  <https://www.youtube.com/verify>, o YouTube aceita poucos uploads por dia e não aplica thumb
  personalizada. Faça a verificação logo depois de autorizar.

## Conferir que funcionou

```bash
yt-pubx canais                 # o canal aparece com "ok"
yt-pubx publicar video.mp4 --canal meucanal --dry-run   # gera texto e thumb sem enviar
```
