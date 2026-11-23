#!/usr/bin/env python3
"""Minimal offline MiCV harness: immutable input, candidate Markdown/PDF, QA/manifest/checkpoint."""
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def digest(raw): return hashlib.sha256(raw).hexdigest()
def parse_sections(md):
    out = {}
    for match in re.finditer(r'^## (.+)$', md, flags=re.M):
        tail = md.find('\n## ', match.end())
        out[match.group(1)] = md[match.end():(tail if tail >= 0 else len(md))]
    return out

def trim_markup(line):
    t = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', line)
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', t)
    return t.strip()

def collect_missions(sec):
    return [m.group(1).strip() for m in re.finditer(r'^- \*\*(.+?)\.\*\*', sec, flags=re.M)]

def collect_strengths(sec):
    return [m.group(1).strip() for m in re.finditer(r'^\d+\. \*\*(.+?)\.\*\*', sec, flags=re.M)]

def render_pdf(source, dest, label):
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    pdfmetrics.registerFont(TTFont('BIZB',font))
    pdfmetrics.registerFont(TTFont('BIZB-Bold',bold))
    pdfmetrics.registerFontFamily('BIZB', normal='BIZB', bold='BIZB-Bold')
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='B-Title',fontName='BIZB-Bold',fontSize=17,leading=23,spaceAfter=12,textColor=colors.HexColor('#163a52')))
    styles.add(ParagraphStyle(name='B-Head',fontName='BIZB-Bold',fontSize=11,leading=15,spaceBefore=13,spaceAfter=6,textColor=colors.HexColor('#34566b'),keepWithNext=True))
    styles.add(ParagraphStyle(name='B-Sub',fontName='BIZB-Bold',fontSize=9,leading=13,spaceBefore=9,spaceAfter=4,textColor=colors.HexColor('#607080'),keepWithNext=True))
    styles.add(ParagraphStyle(name='B-Text',fontName='BIZB',fontSize=8.3,leading=12,spaceAfter=5))
    styles.add(ParagraphStyle(name='B-Warn',fontName='BIZB-Bold',fontSize=9,leading=13,textColor=colors.HexColor('#a53a31'),spaceAfter=10))
    doc=SimpleDocTemplate(str(dest),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=17*mm)
    flow=[Paragraph(escape(label+' — COPIA DE PRUEBA · NO PUBLICAR'),styles['B-Warn'])]
    for line in source.splitlines():
        if not line.strip(): continue
        if line.startswith('# '): kind='B-Title'; text=line[2:]
        elif line.startswith('## '): kind='B-Head'; text=line[3:]
        elif line.startswith('### '): kind='B-Sub'; text=line[4:]
        else: kind='B-Text'; text=trim_markup(line)
        if line.startswith('**') and line.endswith('**'): text=trim_markup(line)
        if line.startswith('- ') or re.match(r'^\d+\. ',line): text='• '+trim_markup(re.sub(r'^(- |\d+\. )','',line))
        if not text: continue
        flow.append(Paragraph(escape(text),styles[kind]))
    def footer(canvas, doc):
        canvas.saveState();canvas.setFont('BIZB',7)
        canvas.drawRightString(A4[0]-18*mm,11*mm,f'ENSAYO · NO PUBLICAR · {doc.page}')
        canvas.restoreState()
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    src=Path(args.source); out=Path(args.output); cfg=json.loads(Path(args.config).read_text(encoding='utf-8'))
    if cfg.get('publish') is not False or any('remote' in str(x).lower() for x in cfg.get('allowed_tools',[])):
        raise SystemExit('REFUSED: dry-run requires publish=false and local-only tools')
    raw=src.read_bytes(); actual=digest(raw)
    if cfg.get('source_sha256') and cfg['source_sha256']!=actual: raise SystemExit('REFUSED: source hash mismatch')
    text=raw.decode('utf-8'); sections=parse_sections(text)
    ss=collect_strengths(sections.get('Fortalezas',''))
    ms=collect_missions(sections.get('Experiencia profesional',''))
    # Markdown list mission headings may have full stops; preserve exact user-supplied titles.
    urls=re.findall(r'\]\((https?://[^)]+)\)',text)
    public_visible=re.sub(r'\]\(https?://[^)]+\)',']',text)
    checks={
      'six_strengths': {'pass':len(ss)==cfg['expected_strengths'],'actual':len(ss),'expected':cfg['expected_strengths']},
      'seven_missions':{'pass':len(ms)==cfg['expected_missions'],'actual':len(ms),'expected':cfg['expected_missions']},
      'tool_inventory': {'pass':all(t in text for t in cfg.get('expected_tools',[])),'expected':cfg.get('expected_tools',[])},
      'anonymous_client_names': {'pass':not any(re.search(r'(?i)\b'+re.escape(v)+r'\b',public_visible) for v in cfg.get('forbidden_names',[]))},
      'legacy_client_names_in_urls': {'pass':True,'warning': [u for u in urls if any(v.lower() in u.lower() for v in cfg.get('forbidden_names',[]))]},
      'source_links':{'pass':bool(urls) and all(urlparse(u).scheme=='https' and urlparse(u).hostname for u in urls),'count':len(urls)},
      'required_link_hosts':{'pass':all(any(urlparse(u).hostname==h for u in urls) for h in cfg.get('required_link_hosts',[]))},
      'human_gate': {'pass':cfg.get('human_approval_required') is True and cfg.get('publish') is False},
    }
    status='PASS' if all(x['pass'] for x in checks.values()) else 'FAIL'
    out.mkdir(parents=True,exist_ok=True)
    candidate='> **ENSAYO E-001 — COPIA DE PRUEBA. NO PUBLICAR.**\n\n'+text
    (out/'candidate.md').write_text(candidate,encoding='utf-8')
    render_pdf(text,out/'candidate.pdf',cfg['run_id'])
    # Test extraction: ensure PDF carries textual markers, not just a decorative image.
    import fitz
    doc=fitz.open(out/'candidate.pdf'); pdf_text='\n'.join(p.get_text() for p in doc)
    checks['pdf_readable']={'pass': all(x in pdf_text for x in ['Perfil profesional','Fortalezas'] + cfg.get('expected_tools',[])),'pages':len(doc)}
    checks['candidate_no_publish']={'pass':'NO PUBLICAR' in candidate and 'NO PUBLICAR' in pdf_text}
    status='PASS' if all(x['pass'] for x in checks.values()) else 'FAIL'
    report={'run_id':cfg['run_id'],'status':status,'checks':checks,'strength_titles':ss,'mission_titles':ms,'warnings':['Los enlaces se comprobaron sintácticamente, no mediante HTTP.','La web WordPress y las evidencias de cada afirmación requieren revisión separada.', 'Los slugs históricos de algunas URL contienen nombres de clientes aunque no se vean en el texto.']}
    (out/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files={p.name:{'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size} for p in [out/'candidate.md',out/'candidate.pdf',out/'qa-report.json']}
    manifest={'run_id':cfg['run_id'],'skill':'micv-candidatura-sync','mode':'dry-run','source_ref':cfg['source_ref'],'source_sha256':actual,'outputs':files,'status':status,'published':False,'measured_cost_eur':None,'measured_tokens':None}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'checkpoint.md').write_text(f'# Checkpoint {cfg["run_id"]}\n\n- Estado: **{status}**\n- Publicación: **no realizada**\n- Entrada SHA-256: `{actual}`\n- Fortalezas: {len(ss)}; misiones: {len(ms)}; enlaces: {len(urls)}.\n- Próxima acción: revisión humana del reporte, comparativa web/MD/PDF y aprobación explícita antes de publicación.\n',encoding='utf-8')
    print(json.dumps({'status':status,'pages':len(doc),'strengths':len(ss),'missions':len(ms),'links':len(urls),'output':str(out)},ensure_ascii=False))
    return 0 if status=='PASS' else 2
if __name__=='__main__': sys.exit(main())
