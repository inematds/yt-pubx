# Authorize a new channel — step by step, without the stress

[PT](autorizar-canal.md) · [EN](autorizar-canal.en.md) · [ES](autorizar-canal.es.md)

This guide is for anyone who has never used Google Cloud. It came from a real authorization for a new channel (October 2026), which went wrong
several times before it worked. Every error that
came up is here, along with what it means and what to do.

## Why YouTube asks for this authorization

Publishing a video with a program requires two different things:

| What | What it does | Where it is |
|---|---|---|
| **Client ID + Client Secret** | tell Google *which program* is making the request | the `client_secret_....json` file you download from Google Cloud |
| **Access token** | says that *the channel owner* allowed this program to publish on their behalf | created by `yt-pubx auth`, one time only |

Having only the first is like having the car key without the owner's permission: Google refuses the upload.
Authorization is when you, logged into the account that owns the channel, click **Allow**.
After that, the token is saved and future uploads won't ask for anything.

## Before you start: check 4 things

1. **You know which Google account owns the channel.** Open the channel on YouTube while logged in, and check the
   top-right corner to see which email address is shown. You'll authorize with that account.
2. **The YouTube Data API v3 is enabled** in the Google Cloud project (API Library → YouTube Data API v3 → Enable).
3. **You are listed as a test user on the consent screen**, or the app is published
   (Google Auth Platform → Audience → Test users → add the email address of the account that owns the channel).
4. **You know your client type.** In Credentials, next to the client name, it says
   "Desktop app" or "Web application." This changes one detail, explained below.

## The simplest option: "Desktop app" client

If you still need to create the client, choose **Desktop app**. It accepts the redirect on
any local port and doesn't require you to register any address.

```bash
yt-pubx auth meucanal --client-secret ~/Downloads/client_secret_XXXX.json
```

The browser opens automatically. Sign in with the account that owns the channel, click **Continue** and then **Allow**.
When you see "yt-pubx: you can close this tab", you're done.

## If your client is a "Web application"

A Web client only accepts a redirect to an address that **exactly matches** one registered with it. If the
address differs by one letter, one slash, or the port, Google shows `redirect_uri_mismatch`.

1. In Google Cloud, open **Credentials → your client → Authorized redirect URIs**.
2. Click **+ Add URI** and paste `http://localhost:8737/callback` (you can use another one, as long as it starts with `http://localhost:`).
3. **Save** and wait about 5 minutes.
4. Download the client JSON again (it will now include this address) and run:

```bash
yt-pubx auth meucanal --client-secret ~/Downloads/client_secret_XXXX.json
```

yt-pubx reads the local address registered in the JSON and uses that exact address. If you prefer to specify it manually:
`--redirect http://localhost:8737/callback`.

## When the browser is on another computer

This is common when yt-pubx runs on a server and you're using your laptop (remote access, SSH).
After you click **Allow**, Google sends the browser to `http://localhost:...`, which doesn't exist on your
laptop. You see **"This site can’t be reached"** or **"ERR_CONNECTION_REFUSED"**.

**This is not an error.** Authorization succeeded, and the code is in the address bar.

1. Click the address bar on that error page.
2. Copy the entire URL (it starts with `http://localhost:...` and has `code=` in the middle).
3. Go back to the terminal where `yt-pubx auth` is waiting, paste it, and press **Enter**.

That's it: yt-pubx finishes on its own and shows "Channel ... authorized".

## Errors that actually appeared and what they mean

| What appears | What it means | What to do |
|---|---|---|
| `Error 400: redirect_uri_mismatch` | the client is a Web client and the redirect address isn't registered | see "If your client is a Web application" above |
| `OAuth 2 parameters can only have a single value: access_type` | the link was copied **incorrectly** from the terminal (parts repeated or missing) | open the link from the `~/.config/yt-pubx/auth-<canal>.txt` file, or Ctrl-click it in the terminal |
| `Access blocked: ... has not completed the Google verification process` | the account isn't on the test users list | add the email address under Audience → Test users |
| "Choose an account" screen without the right account | the browser isn't signed in to the account that owns the channel | click **Use another account** and sign in with it |
| `ERR_CONNECTION_REFUSED` / "This site can’t be reached" after clicking Allow | the browser is on another computer | copy the URL from the address bar and paste it into the terminal (see above) |
| "This URL is from a different link" | you used a link from an earlier attempt | each `yt-pubx auth` generates a new link; use the one from the attempt that's currently running |
| `thumb não aplicada … verify` (when publishing) | new channel, not verified by phone | go to <https://www.youtube.com/verify> with the account that owns the channel |

## Three tips that save time

- **Reaching the "Choose an account" screen doesn't prove it worked.** Google checks the redirect address only
  after you select the account. Count it as a success only when you see "you can close this tab"
  or "Channel ... authorized".
- **Don't stop the `yt-pubx auth` command midway.** Every time it runs, it generates a new link. The code from
  an old link won't work with the new command.
- **New channels have a low upload limit and can't use thumbnails.** Until you verify the phone number at
  <https://www.youtube.com/verify>, YouTube accepts only a few uploads per day and won't apply a custom thumbnail.
  Complete verification right after authorizing.

## Check that it worked

```bash
yt-pubx canais                 # the channel appears with "ok"
yt-pubx publicar video.mp4 --canal meucanal --dry-run   # generates text and thumbnail without uploading
```
