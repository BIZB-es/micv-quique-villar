import json, subprocess, sys, tempfile, unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'scripts'/'dry_run.py'

class DryRunTests(unittest.TestCase):
    def invoke(self,text,config):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)
            (p/'source.md').write_text(text,encoding='utf-8')
            (p/'cfg.json').write_text(json.dumps(config),encoding='utf-8')
            result=subprocess.run([sys.executable,str(SCRIPT),'--source',str(p/'source.md'),'--config',str(p/'cfg.json'),'--output',str(p/'out')],capture_output=True,text=True)
            if (p/'out'/'qa-report.json').exists():
                return result,json.loads((p/'out'/'qa-report.json').read_text())
            return result,None
    def base(self):
        return {'run_id':'TEST','source_ref':'fixture','expected_strengths':1,'expected_missions':1,
                'expected_tools':['Obsidian'],'forbidden_names':['CLIENTEX'],
                'required_link_hosts':['entropyme.biz'],'publish':False,
                'human_approval_required':True,'allowed_tools':['filesystem:read']}
    def document(self):
        return '# Demo\n\n## Perfil profesional\nTexto.\n\n## Fortalezas\n1. **Fortaleza.** Texto.\n\n## Experiencia profesional\n- **Misión.** Texto [Enlace](https://entropyme.biz/mision-clientex/).\n\n## Herramientas y entornos\nObsidian\n'
    def test_legacy_slug_is_warning(self):
        r,d=self.invoke(self.document(),self.base())
        self.assertEqual(r.returncode,0)
        self.assertTrue(d['checks']['anonymous_client_names']['pass'])
        self.assertEqual(len(d['checks']['legacy_client_names_in_urls']['warning']),1)
    def test_visible_client_is_fail(self):
        r,d=self.invoke(self.document().replace('Texto.','CLIENTEX operó.',1),self.base())
        self.assertEqual(r.returncode,2)
        self.assertFalse(d['checks']['anonymous_client_names']['pass'])
    def test_publish_refused(self):
        c=self.base();c['publish']=True
        r,d=self.invoke(self.document(),c)
        self.assertNotEqual(r.returncode,0);self.assertIsNone(d)
    def test_source_hash_refused(self):
        c=self.base();c['source_sha256']='0'*64
        r,d=self.invoke(self.document(),c)
        self.assertNotEqual(r.returncode,0);self.assertIsNone(d)

if __name__=='__main__': unittest.main()
