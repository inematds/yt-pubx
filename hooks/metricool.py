#!/usr/bin/env python3
"""Adaptador opcional: entrega um evento ao publicador Metricool já configurado.

Publicador, marca e repositório são configuração local, nunca credenciais no código.
O publicador mantém as validações de formato, intervalo e recibo próprias.
"""
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    event_path = Path(sys.argv[1]).resolve()
    event = json.loads(event_path.read_text())
    publisher = Path(os.environ['METRICOOL_PUBLICADOR']).expanduser()
    repo = os.environ['METRICOOL_REPO']
    brand = os.environ['METRICOOL_MARCA']
    if not publisher.is_file():
        raise RuntimeError('publicador Metricool não encontrado')
    caption = event_path.parent / 'legenda.txt'
    # Mesma legenda na retomada: preserva a chave de idempotência do publicador.
    if not caption.exists():
        caption.write_text(event['titulo'] + '\n\n' + event['descricao'] + '\n')
    env = {**os.environ, 'MARCA': brand, 'EXTRA': event['url']}
    if os.environ.get('METRICOOL_REDES'):
        env['REDES'] = os.environ['METRICOOL_REDES']
    result = subprocess.run(['bash', str(publisher), event['video'], str(caption), repo], env=env)
    # Exit 0 do publicador só ocorre com recibo ok ou recibo já existente.
    return result.returncode


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print('Distribuição Metricool pendente:', e, file=sys.stderr)
        sys.exit(2)
