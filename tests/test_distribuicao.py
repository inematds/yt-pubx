import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
loader = importlib.machinery.SourceFileLoader('distribuidor', str(ROOT / 'yt-pubx'))
spec = importlib.util.spec_from_loader(loader.name, loader)
m = importlib.util.module_from_spec(spec)
loader.exec_module(m)


class Distribuicao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.video = self.root / 'origem.mp4'
        self.video.write_bytes(b'fixture-video')
        self.publisher = self.root / 'publisher.sh'
        self.publisher.write_text('test "$MARCA" = "marca-teste" || exit 8\n'
                                  'test "$REDES" = "tiktok,instagram" || exit 9\n'
                                  'test "$3" = "teste/repo" || exit 10\n'
                                  'cp "$2" "$2.enviada"\n'
                                  'echo envio >> "$2.contagem"\n'
                                  'test ! -e "$2.falhar"\n')
        self.config = {'pos_publicar': {
            'comando': [sys.executable, str(ROOT / 'hooks/metricool.py')],
            'ambiente': {'METRICOOL_PUBLICADOR': str(self.publisher),
                         'METRICOOL_MARCA': 'marca-teste', 'METRICOOL_REPO': 'teste/repo',
                         'METRICOOL_REDES': 'tiktok,instagram'}}}
        self.folder = self.root / 'pos-publicacao/canal-video123'
        self.state = self.folder / 'estado.json'
        self.patcher = patch.object(m, 'DATA_DIR', str(self.root))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def send(self, status=None, config=None):
        return m.pos_publicar('canal', self.config if config is None else config,
                             'video123', 'https://youtube.test/video123', str(self.video),
                             'Título', 'Descrição', status or {'privacyStatus': 'public'})

    def test_adapter_real_success_and_duplicate(self):
        self.assertTrue(self.send())
        self.assertEqual(json.loads(self.state.read_text())['status'], 'concluido')
        self.assertFalse((self.folder / 'video.mp4').exists())
        self.assertEqual((self.folder / 'legenda.txt.enviada').read_text(), 'Título\n\nDescrição\n')
        self.assertTrue(self.send())
        self.assertEqual((self.folder / 'legenda.txt.contagem').read_text(), 'envio\n')
        self.assertTrue(self.video.exists())

    def test_failure_retains_video_retry_without_upload(self):
        self.folder.mkdir(parents=True)
        flag = self.folder / 'legenda.txt.falhar'
        flag.touch()
        self.assertFalse(self.send())
        self.assertEqual(json.loads(self.state.read_text())['status'], 'pendente')
        self.assertEqual((self.folder / 'video.mp4').read_bytes(), self.video.read_bytes())
        flag.unlink()
        with patch.object(m, 'upload_video') as upload, patch.object(m, 'load_config', return_value={}), \
             patch.object(m, 'canal', return_value=('canal', {})):
            from types import SimpleNamespace
            m.cmd_distribuir(SimpleNamespace(canal='canal', video_id='video123'))
            upload.assert_not_called()
        self.assertEqual(json.loads(self.state.read_text())['status'], 'concluido')

    def test_private_scheduled_and_unconfigured_do_not_forward(self):
        for status in ({'privacyStatus': 'private'}, {'privacyStatus': 'unlisted'},
                       {'privacyStatus': 'public', 'publishAt': '2099-01-01'}):
            self.assertTrue(self.send(status))
        self.assertTrue(self.send(config={}))
        self.assertFalse(self.folder.exists())

    def test_timeout_is_ambiguous_and_never_blindly_retried(self):
        with patch.object(m.subprocess, 'run', side_effect=subprocess.TimeoutExpired('hook', 1)) as run:
            self.assertFalse(self.send())
            self.assertFalse(self.send())
            self.assertEqual(run.call_count, 1)
        self.assertEqual(json.loads(self.state.read_text())['status'], 'executando')
        self.assertTrue((self.folder / 'video.mp4').exists())

    def test_cli_upload_records_history_before_forwarding_and_dry_run_sends_nothing(self):
        history = self.root / 'historico.jsonl'
        args = ['yt-pubx', 'publicar', str(self.video), '--canal', 'canal',
                '--title', 'Título', '--description', 'Descrição', '--sem-thumb']
        def forward(*a):
            self.assertEqual(json.loads(history.read_text())['video_id'], 'video123')
            return True
        with patch.object(m, 'TRABALHOS', str(self.root / 'trabalhos')), \
             patch.object(m, 'HISTORICO', str(history)), \
             patch.object(m, 'load_config', return_value={'canais': {'canal': self.config}}), \
             patch.object(m, 'obter_video', return_value=(str(self.video), False)), \
             patch.object(m, 'duracao', return_value=10), \
             patch.object(m, 'arquivo_ja_publicado', return_value=None), \
             patch.object(m, 'ja_publicado', return_value=None), \
             patch.object(m, 'access_token', return_value='fake'), \
             patch.object(m, 'upload_video', return_value='video123') as upload, \
             patch.object(m, 'pos_publicar', side_effect=forward) as forwarding:
            with patch.object(sys, 'argv', args + ['--dry-run']):
                m.main()
            upload.assert_not_called()
            forwarding.assert_not_called()
            with patch.object(sys, 'argv', args):
                m.main()
            upload.assert_called_once()
            forwarding.assert_called_once()


if __name__ == '__main__':
    unittest.main()
