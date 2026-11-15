# Tipo, motor, modelo e esforço por etapa

Configuração ativa: `~/.config/yt-pubx/ia.yaml`. Exemplo portátil sem credenciais no repo: `ia.exemplo.yaml`. Metadados podem usar assinatura Claude/Codex ou APIs Anthropic/OpenAI/OpenRouter autorizadas; todas as APIs começam desativadas. Capa exige Codex/image_gen por assinatura. Sem fallback pago. A configuração antiga codex_modelo foi substituída pela seleção explícita de cada etapa no novo arquivo.

```bash
python3 ia_motor.py ver
python3 ia_motor.py configurar metadados --tipo assinatura --motor claude --modelo claude-opus-5-5 --esforco medium
python3 ia_motor.py configurar metadados --tipo assinatura --motor codex --modelo gpt-6.1-sol --esforco medium
```

O cron/publicador lê a configuração em cada chamada. Mudar o arquivo vale para os publicadores que chamam yt-pubx (clima e filas inclusive); canais, tokens, histórico e prevenção de duplicatas são preservados. Nenhuma conta é configurada no repo. Para instalação nova copie ia.exemplo.yaml para sua pasta de configuração antes de personalizar. API não autorizada falha antes de ler a chave. Valores de credenciais nunca entram no YAML, argumentos ou telemetria.

Metadados são criados em PT; canais de outros idiomas passam pelo inema-traduz pela assinatura. A tradução não troca junto com o gerador e é validada antes de publicar.
