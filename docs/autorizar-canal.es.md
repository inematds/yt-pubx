# Autorizar un canal nuevo — paso a paso y sin sustos

[PT](autorizar-canal.md) · [EN](autorizar-canal.en.md) · [ES](autorizar-canal.es.md)

Esta guía es para quienes nunca han usado Google Cloud. Surgió de la autorización real de un canal nuevo (octubre de 2026), que salió mal
varias veces antes de funcionar. Aquí encontrarás cada error que
apareció, qué significa y qué hacer.

## Por qué YouTube pide esta autorización

Publicar un video mediante un programa requiere dos cosas distintas:

| Qué | Para qué sirve | Dónde está |
|---|---|---|
| **Client ID + Client Secret** | le dicen a Google *qué programa* está haciendo la solicitud | el archivo `client_secret_....json` que descargas de Google Cloud |
| **Token de acceso** | indica que *el dueño del canal* autorizó a ese programa a publicar en su nombre | se crea con `yt-pubx auth`, una sola vez |

Tener solo lo primero es como tener la llave del auto sin el permiso del dueño: Google rechaza el envío.
La autorización ocurre cuando tú, con la sesión iniciada en la cuenta dueña del canal, haces clic en **Permitir**.
Después, el token queda guardado y las siguientes publicaciones no te pedirán nada.

## Antes de empezar: revisa estas 4 cosas

1. **Sabes cuál es la cuenta de Google dueña del canal.** Abre el canal en YouTube con la sesión iniciada y fíjate en
   la esquina superior derecha para ver qué correo aparece. Autorizarás con esa cuenta.
2. **La YouTube Data API v3 está habilitada** en el proyecto de Google Cloud (Biblioteca → YouTube Data API v3 → Habilitar).
3. **Tú apareces como usuario de prueba en la pantalla de consentimiento**, o la app está publicada
   (Google Auth Platform → Público → Usuarios de prueba → agregar el correo de la cuenta dueña del canal).
4. **Sabes qué tipo de cliente tienes.** En Credenciales, junto al nombre del cliente, aparece
   "App para computadora" o "Aplicación web". Esto cambia un detalle que se explica más abajo.

## La opción más sencilla: cliente "App para computadora"

Si todavía vas a crear el cliente, elige **App para computadora**. Acepta el retorno en
cualquier puerto local y no requiere registrar ninguna dirección.

```bash
yt-pubx auth meucanal --client-secret ~/Downloads/client_secret_XXXX.json
```

El navegador se abre automáticamente. Inicia sesión con la cuenta dueña del canal, haz clic en **Continuar** y luego en **Permitir**.
Cuando aparezca "yt-pubx: pode fechar esta aba", habrás terminado.

## Si tu cliente es "Aplicación web"

Un cliente web solo acepta volver a una dirección **exactamente igual** a una que hayas registrado. Si la
dirección tiene una letra, una barra o un puerto diferentes, Google muestra `redirect_uri_mismatch`.

1. En Google Cloud, abre **Credenciales → tu cliente → URI de redireccionamiento autorizados**.
2. Haz clic en **+ Agregar URI** y pega `http://localhost:8737/callback` (puede ser otro, siempre que empiece con `http://localhost:`).
3. **Guarda** y espera unos 5 minutos.
4. Descarga de nuevo el JSON del cliente (ahora incluirá esa dirección) y ejecuta:

```bash
yt-pubx auth meucanal --client-secret ~/Downloads/client_secret_XXXX.json
```

yt-pubx lee del JSON la dirección local registrada y la usa exactamente. Si prefieres indicarla manualmente:
`--redirect http://localhost:8737/callback`.

## Cuando el navegador está en otra computadora

Es común cuando yt-pubx se ejecuta en un servidor y tú estás en tu laptop (acceso remoto, SSH).
Después de hacer clic en **Permitir**, Google redirige el navegador a `http://localhost:...`, que no existe en tu
laptop. Aparece **"No se puede acceder a este sitio"** o **"ERR_CONNECTION_REFUSED"**.

**Esto no es un error.** La autorización funcionó y el código está en la barra de direcciones.

1. Haz clic en la barra de direcciones de esa página de error.
2. Copia la URL completa (empieza con `http://localhost:...` y tiene `code=` en medio).
3. Vuelve a la terminal donde `yt-pubx auth` está esperando, pégala y presiona **Enter**.

Listo: yt-pubx termina automáticamente y muestra "Canal ... autorizado".

## Los errores que aparecieron realmente y lo que significan

| Lo que aparece | Qué significa | Qué hacer |
|---|---|---|
| `Error 400: redirect_uri_mismatch` | el cliente es web y la dirección de retorno no está registrada | sección "Si tu cliente es Aplicación web" más arriba |
| `OAuth 2 parameters can only have a single value: access_type` | el enlace se copió **mal** desde la terminal (hay fragmentos repetidos o faltantes) | abre el enlace desde el archivo `~/.config/yt-pubx/auth-<canal>.txt` o haz ctrl+clic en la terminal |
| `Access blocked: ... has not completed the Google verification process` | la cuenta no está en la lista de usuarios de prueba | agrega el correo en Público → Usuarios de prueba |
| Pantalla "Choose an account" sin la cuenta correcta | el navegador no tiene iniciada la sesión de la cuenta dueña del canal | haz clic en **Usar otra cuenta** e inicia sesión con ella |
| `ERR_CONNECTION_REFUSED` / "No se puede acceder a este sitio" después de hacer clic en Permitir | el navegador está en otra máquina | copia la URL de la barra y pégala en la terminal (sección anterior) |
| "Esta URL es de otro enlace" | usaste un enlace de un intento anterior | cada `yt-pubx auth` genera un enlace nuevo; usa el del intento que está en curso |
| `thumb não aplicada … verify` (al publicar) | canal nuevo, sin verificación telefónica | visita <https://www.youtube.com/verify> con la cuenta dueña del canal |

## Tres consejos para ahorrar tiempo

- **Llegar a la pantalla "Choose an account" no demuestra que haya funcionado.** Google solo verifica la dirección
  de retorno después de que eliges la cuenta. Da el proceso por terminado solo cuando aparezca "pode fechar esta aba"
  o "Canal ... autorizado".
- **No cierres el comando `yt-pubx auth` a mitad del proceso.** Cada vez que se ejecuta, crea un enlace nuevo. El código de
  un enlace anterior no sirve en el comando nuevo.
- **Los canales nuevos tienen un límite bajo de publicaciones y no pueden usar miniaturas.** Hasta verificar el teléfono en
  <https://www.youtube.com/verify>, YouTube acepta pocas cargas por día y no aplica miniaturas
  personalizadas. Verifica el teléfono justo después de autorizar.

## Comprueba que funcionó

```bash
yt-pubx canais                 # o canal aparece com "ok"
yt-pubx publicar video.mp4 --canal meucanal --dry-run   # gera texto e thumb sem enviar
```
