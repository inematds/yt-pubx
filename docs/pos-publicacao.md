# Encaminhar após publicar

Cada canal pode definir `pos_publicar` no config local:

```json
{
  "pos_publicar": {
    "comando": ["python3", "/caminho/yt-pubx/hooks/metricool.py"],
    "ambiente": {
      "METRICOOL_PUBLICADOR": "/caminho/publicador/publicar.sh",
      "METRICOOL_MARCA": "minha-marca",
      "METRICOOL_REPO": "conta/repositorio-publico",
      "METRICOOL_REDES": "tiktok,instagram"
    },
    "timeout": 1800
  }
}
```

O comando recebe o caminho de um evento JSON como último argumento. Só roda após o histórico do upload público imediato ser salvo. Não roda em dry-run, uploads privados, não listados ou agendados; não monitora quando um vídeo agendado fica público. Não reenvia o histórico anterior. O adaptador chama um publicador previamente instalado e configurado, mantendo suas validações, recibos e intervalo entre posts.

O estado fica em `~/.local/share/yt-pubx/pos-publicacao/<canal>-<video_id>/`: evento, log e estado. Em erro, a cópia do vídeo permanece. Para retomar uma entrega `pendente`, sem novo upload:

```sh
yt-pubx distribuir VIDEO_ID --canal CANAL
```

Estado `concluido` não executa novamente. Se houver timeout ou interrupção com estado `executando`, a retomada automática é recusada: conferir o recibo e a agenda do destino antes de qualquer reenvio. Não basta reenviar o comando `publicar` para retomar a distribuição.

O publicador Metricool atual aceita vídeo vertical até 180 segundos para Instagram + TikTok (ou até 600 segundos configurando só TikTok). Material incompatível fica pendente, sem corte ou conversão automática. Cada sistema produtor deve evitar chamar o mesmo publicador por fora quando esta integração já estiver habilitada.
