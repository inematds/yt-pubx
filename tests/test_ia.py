import importlib.machinery,importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
loader=importlib.machinery.SourceFileLoader('publicador',str(ROOT/'yt-pubx'))
spec=importlib.util.spec_from_loader(loader.name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m)
import ia_motor as ia
class Teste(unittest.TestCase):
 def args(self,idioma='pt'):
  return SimpleNamespace(contexto='Ensaio local',contexto_arquivo=None,legenda=None,title=None,description=None,idioma=idioma)
 def dados(self):return {'titulo':'Um teste','descricao':'Descrição do teste','tags':['teste'],'frase_thumb':'UM TESTE','cena_thumb':'Uma tela azul'}
 def test_metadados_pt_nao_traduz(self):
  with patch.object(m,'codex',return_value=json.dumps(self.dados())),patch.object(m.subprocess,'run') as run:
   self.assertEqual(m.gerar_metadados(self.args(),{},'video.mp4',3,'/tmp','legado'),self.dados());run.assert_not_called()
 def test_traducao_central_preserva_cena_e_valida_chaves(self):
  tr={'titulo':'A test','descricao':'Test description','tags':['test'],'frase_thumb':'A TEST'}
  with patch.object(m,'codex',return_value=json.dumps(self.dados())),patch('shutil.which',return_value='tradutor-falso'),patch.object(m.subprocess,'run',return_value=subprocess.CompletedProcess([],0,json.dumps(tr),'')) as run:
   d=m.gerar_metadados(self.args('en'),{},'video.mp4',3,'/tmp','')
   self.assertEqual(d['titulo'],'A test');self.assertEqual(d['cena_thumb'],'Uma tela azul');self.assertEqual(run.call_args.args[0],['tradutor-falso'])
 def test_traducao_invalida_nao_passa(self):
  with patch.object(m,'codex',return_value=json.dumps(self.dados())),patch('shutil.which',return_value='tradutor-falso'),patch.object(m.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'{}','')):
   with self.assertRaises(RuntimeError):m.gerar_metadados(self.args('es'),{},'video.mp4',3,'/tmp','')
 def test_imagem_exige_assinatura_codex(self):
  import copy
  d=copy.deepcopy(ia.carregar());d['etapas']['capa'].update(tipo='api',motor='anthropic',modelo='claude-opus-5-5')
  with self.assertRaisesRegex(ValueError,'capa exige'):ia.validar(d)
if __name__=='__main__':unittest.main()
