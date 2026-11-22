#!/usr/bin/env python3
"""Wektorowe drzewo oraz czytelny katalog kart i powiazan w jednym PDF."""
import html
import os
from pathlib import Path
import tempfile

# ReportLab jest opcjonalny: zwykly eksport HTML go nie wymaga.
try:
 from reportlab.lib.colors import HexColor
 from reportlab.lib.pagesizes import A4,landscape
 from reportlab.lib.styles import ParagraphStyle
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.platypus import BaseDocTemplate, Flowable, Frame, KeepTogether, NextPageTemplate, PageBreak, PageTemplate, Paragraph,LongTable,TableStyle
except ImportError as exc:
 raise ImportError('PDF export requires ReportLab. Run this command with a Python environment containing reportlab.') from exc

TYPES=['goal','signal','opportunity','idea','experiment','result','decision']
COLORS={'goal':('#FFFBF0','#FFE49A','#E7C864'),'signal':('#F3FAFF','#D4ECFF','#99C8ED'),'opportunity':('#F0FFF2','#D0F3D4','#98CDA1'),'idea':('#F8F4FF','#E3D8FF','#BBA3EA'),'experiment':('#FFF7EF','#FFD8B2','#EAB785'),'result':('#F7F7F7','#EAEAEA','#C9C9C9'),'decision':('#F7F7F7','#EAEAEA','#C9C9C9')}
LABELS={
 'en':dict(pdf_legend='Solid dark frame: selected path. Dashed frame: recommendation.',pdf_download='Download PDF',pdf_title='Tree and relationship guide',pdf_overview='Full tree',pdf_guide='Cards and relationships',pdf_counts='Contents',pdf_reading='How to read this document',pdf_reading_body='The next page contains the complete vector tree. Zoom in or click a card to jump to its readable description. The following pages explain the connections visible in the tree using card IDs and full titles.',pdf_context_note='Goal-to-signal lines provide goal context; they do not prove that an idea or test will achieve the outcome.',pdf_status='Status',pdf_incoming='Preceding cards',pdf_outgoing='Connects to',pdf_none='No outgoing connection recorded.',pdf_source='Open full description and sources',pdf_path='Selected cards',pdf_description='Description',pdf_revision='Revision',pdf_page='Page',pdf_evidence='supports this opportunity',pdf_context='provides context for this signal',pdf_structural='continues to',pdf_gap='No direct opportunity link recorded; the signal is retained for review.'),
 'pl':dict(pdf_legend='Ciemna ciągła ramka: wybrana ścieżka. Ramka przerywana: rekomendacja.',pdf_download='Pobierz PDF',pdf_title='Drzewko i opis powiązań',pdf_overview='Pełne drzewko',pdf_guide='Karty i powiązania',pdf_counts='Zawartość',pdf_reading='Jak czytać ten dokument',pdf_reading_body='Na następnej stronie znajduje się pełne drzewko wektorowe. Można je powiększać, a kliknięcie karty przenosi do jej czytelnego opisu. Kolejne strony objaśniają połączenia widoczne na drzewku, podając ID i pełne tytuły kart.',pdf_context_note='Linie Cel - Sygnały pokazują kontekst celu; nie dowodzą, że pomysł lub test doprowadzi do jego osiągnięcia.',pdf_status='Status',pdf_incoming='Poprzedzające karty',pdf_outgoing='Łączy się z',pdf_none='Nie zapisano dalszego połączenia.',pdf_source='Otwórz pełny opis i źródła',pdf_path='Wybrane karty',pdf_description='Opis',pdf_revision='Rewizja',pdf_page='Strona',pdf_evidence='wspiera tę szansę',pdf_context='stanowi kontekst tego sygnału',pdf_structural='prowadzi do',pdf_gap='Nie zapisano bezpośredniego powiązania z szansą; sygnał pozostaje do przeglądu.')}


def labels(data):
 return {**LABELS.get(data['language'],LABELS['en']),**{k:v for k,v in data['ui'].items() if k.startswith('pdf_')}}


def register_fonts(font_path=None):
 if font_path:
  regular=Path(font_path);bold=regular
 else:
  candidates=[(Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/System/Library/Fonts/Supplemental/Arial Bold.ttf')),(Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')),(Path('/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf'),Path('/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf')),(Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/arial.ttf',Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/arialbd.ttf')]
  pair=next(((a,b) for a,b in candidates if a.is_file()),None)
  if pair is None:raise ValueError('No suitable TTF font found. Supply --pdf-font /path/to/font.ttf with the characters used in this cycle.')
  regular,bold=pair
 if not regular.is_file():raise ValueError('PDF font does not exist: '+str(regular))
 pdfmetrics.registerFont(TTFont('Supersprint',str(regular)))
 pdfmetrics.registerFont(TTFont('SupersprintBold',str(bold if bold.is_file() else regular)))
 pdfmetrics.registerFontFamily('Supersprint',normal='Supersprint',bold='SupersprintBold',italic='Supersprint',boldItalic='SupersprintBold')


def escaped(value):
 return html.escape(str(value).replace('—','-').replace('–','-').replace('‑','-'),quote=True).replace('\r','').replace('\n','<br/>')


def styles():
 return dict(body=ParagraphStyle('body',fontName='Supersprint',fontSize=10,leading=14,textColor=HexColor('#292929'),spaceAfter=8,splitLongWords=True),small=ParagraphStyle('small',fontName='Supersprint',fontSize=8.5,leading=12,textColor=HexColor('#5D5D5D'),spaceAfter=7),title=ParagraphStyle('title',fontName='SupersprintBold',fontSize=27,leading=33,spaceAfter=16,textColor=HexColor('#292929')),section=ParagraphStyle('section',fontName='SupersprintBold',fontSize=19,leading=25,spaceAfter=14,textColor=HexColor('#292929'),keepWithNext=True),heading=ParagraphStyle('heading',fontName='SupersprintBold',fontSize=12,leading=16,spaceBefore=10,spaceAfter=7,textColor=HexColor('#292929'),keepWithNext=True),mapping=ParagraphStyle('mapping',fontName='Supersprint',fontSize=9.5,leading=13.5,leftIndent=12,spaceAfter=7,textColor=HexColor('#292929'),splitLongWords=True))


def card_content(node,width):
 body=ParagraphStyle('tree-body',fontName='Supersprint',fontSize=13,leading=18,textColor=HexColor('#5D5D5D'),splitLongWords=True)
 title=ParagraphStyle('tree-title',fontName='SupersprintBold',fontSize=14,leading=19,textColor=HexColor('#292929'),spaceAfter=8,splitLongWords=True)
 meta=ParagraphStyle('tree-meta',fontName='Supersprint',fontSize=12,leading=16,textColor=HexColor('#5D5D5D'),splitLongWords=True)
 parts=[(Paragraph(escaped(node['id']),meta),10),(Paragraph(escaped(node['title']),title),8)]
 summary=node['summary'] or node.get('card',{}).get('hypothesis','')
 if summary:parts.append((Paragraph(escaped(summary),body),14))
 parts.append((Paragraph(escaped(node['status_label']),meta),0))
 measured=[]
 for paragraph,gap in parts:
  _,height=paragraph.wrap(width-36,100000)
  measured.append((paragraph,height,gap))
 return measured,max(155,36+sum(h+gap for _,h,gap in measured))


def layout_tree(nodes,edges):
 """Ten sam porzadek, rodzice i odstepy co w widoku HTML; wysokosci mierzy PDF."""
 positions={};children={n['id']:[] for n in nodes};parent={};main=[n for n in nodes if n['type'] not in ['goal','signal']]
 main_ids={n['id'] for n in main};stage={n['id']:TYPES.index(n['type']) for n in nodes}
 for e in edges:
  a,b=e['source'],e['target']
  if e['evidence'] or a not in main_ids or b not in main_ids or stage[a]>=stage[b] or b in parent:continue
  children[a].append(b);parent[b]=a
 order={n['id']:i for i,n in enumerate(nodes)}
 for items in children.values():items.sort(key=order.get)
 def branch(id):
  if not children[id]:return {id:0},-140,140
  placed=[];cursor=0
  for child in children[id]:
   coords,lo,hi=branch(child);shift=cursor-lo;placed.append((coords,lo,hi,shift));cursor=hi+shift+36
  center=(placed[0][3]+placed[-1][3])/2;coords={id:0};lo=-140;hi=140
  for sub,left,right,offset in placed:
   shift=offset-center;coords.update({k:x+shift for k,x in sub.items()});lo=min(lo,left+shift);hi=max(hi,right+shift)
  return coords,lo,hi
 centers={};cursor=0
 for n in main:
  if n['id'] in parent:continue
  coords,lo,hi=branch(n['id']);offset=cursor-lo;centers.update({k:x+offset for k,x in coords.items()});cursor=hi+offset+72
 branch_width=max(0,cursor-72)
 independent=[sum(280 for n in nodes if n['type']==kind)+max(0,sum(n['type']==kind for n in nodes)-1)*36 for kind in ['goal','signal']]
 width=max(280,branch_width,*independent)+48;top=48;lanes=[];measured={n['id']:card_content(n,280) for n in nodes}
 for kind in TYPES:
  items=[n for n in nodes if n['type']==kind]
  if not items:continue
  height=64+max(measured[n['id']][1] for n in items)+24
  lanes.append(dict(kind=kind,top=top,height=height));row_width=len(items)*280+(len(items)-1)*36;left=(width-row_width)/2
  for n in items:
   x=left if kind in ['goal','signal'] else (width-branch_width)/2+centers[n['id']]-140
   positions[n['id']]=dict(left=x,top=top+64,width=280,height=measured[n['id']][1],stage=TYPES.index(kind));left+=316
  top+=height+80
 return dict(positions=positions,lanes=lanes,width=width,height=top-80+48 if lanes else 180,measured=measured)


class Tree(Flowable):
 def __init__(self,data,layout,anchors,register_goals=False,output=None):
  super().__init__();self.data=data;self.layout=layout;self.anchors=anchors;self.edges=[e for e in data['edges'] if e['visible']];self.gutter=32+len(self.edges)*3;self.width=layout['width']+self.gutter*2;self.height=layout['height'];self.register_goals=register_goals;self.output=Path(output) if output else None
 def draw(self):
  c=self.canv;layout=self.layout;h=self.height;ox=self.gutter
  if not self.data['nodes']:
   c.setFillColor(HexColor('#5D5D5D'));c.setFont('Supersprint',12);c.drawString(ox,100,self.data['ui']['empty'])
  for lane in layout['lanes']:
   bg,_,line=COLORS[lane['kind']];c.setFillColor(HexColor(bg));c.setStrokeColor(HexColor(line));c.setLineWidth(.6);c.roundRect(ox,h-lane['top']-lane['height'],layout['width'],lane['height'],12,fill=1,stroke=1);c.setFillColor(HexColor('#292929'));c.setFont('SupersprintBold',12);c.drawString(ox+24,h-lane['top']-32,self.data['ui'][lane['kind']])
  stages={TYPES.index(lane['kind']):lane for lane in layout['lanes']}
  for index,e in enumerate(self.edges):
   a,b=(layout['positions'][e[k]] for k in ['source','target']);sx=a['left']+140+ox;tx=b['left']+140+ox;sy=a['top']+a['height'];ty=b['top']
   if b['stage']==a['stage']+1:
    sources=list(dict.fromkeys(edge['source'] for edge in self.edges if layout['positions'][edge['source']]['stage']==a['stage']));middle=stages[a['stage']]['top']+stages[a['stage']]['height']+16+48*(sources.index(e['source'])+.5)/len(sources);points=[(sx,sy),(sx,middle),(tx,middle),(tx,ty)]
   else:
    exit=stages[a['stage']]['top']+stages[a['stage']]['height']+18+(index%8)*3;entry=stages[b['stage']]['top']-18-(index%8)*3;side=ox-16-index*3;points=[(sx,sy),(sx,exit),(side,exit),(side,entry),(tx,entry),(tx,ty)]
   c.setStrokeColor(HexColor('#292929' if e['on_path'] else '#8795A3'));c.setLineWidth(3 if e['on_path'] else 1.4);c.setDash(4,5) if e['evidence'] else c.setDash();c.setLineJoin(1);path=c.beginPath();path.moveTo(points[0][0],h-points[0][1])
   for x,y in points[1:]:path.lineTo(x,h-y)
   c.drawPath(path);c.setDash()
  for n in self.data['nodes']:
   p=layout['positions'][n['id']];x=p['left']+ox;y=h-p['top']-p['height'];_,fill,border=COLORS[n['type']];c.setFillColor(HexColor(fill));c.setStrokeColor(HexColor('#292929' if n['on_path'] else '#5D5D5D' if n['recommended'] else border));c.setLineWidth(3 if n['on_path'] else 2 if n['recommended'] else .8)
   if n['recommended'] and not n['on_path']:c.setDash(5,4)
   c.roundRect(x,y,p['width'],p['height'],16,fill=1,stroke=1);c.setDash();cursor=y+p['height']-18
   for paragraph,ph,gap in layout['measured'][n['id']][0]:paragraph.drawOn(c,x+18,cursor-ph);cursor-=ph+gap
   if self.register_goals and n['type']=='goal':
    c.bookmarkHorizontal(self.anchors[n['id']],x,y+p['height'])
    if n.get('link'):
     uri=n['link'] if n['link'].startswith(('http://','https://')) else (self.output.parent/n['link']).resolve().as_uri();c.linkURL(uri,(x,y,x+p['width'],y+p['height']),relative=1,thickness=0)
   else:c.linkRect('',self.anchors[n['id']],(x,y,x+p['width'],y+p['height']),relative=1,thickness=0)


def write_full_pdf(data,output,font_path=None):
 register_fonts(font_path);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);ui=data['ui'];text=labels(data);style=styles();by_id={n['id']:n for n in data['nodes']};anchors={n['id']:f'node_{i}' for i,n in enumerate(data['nodes'])};edges=[e for e in data['edges'] if e['visible']];layout=layout_tree(data['nodes'],edges);tree=Tree(data,layout,anchors)
 def p(value,kind='body'):return Paragraph(escaped(value),style[kind])
 def ref(id,full=True):
  node=by_id[id];return f'<link href="#{anchors[id]}" color="#292929"><b>{escaped(id)}</b></link>'+(' - '+escaped(node['title']) if full else '')
 def footer(canvas,doc):
  canvas.saveState();w,h=canvas._pagesize;canvas.setFont('Supersprint',8);canvas.setFillColor(HexColor('#5D5D5D'));canvas.drawString(36,22,f'{data["project_context"]["product"]} | {text["pdf_revision"]} {data["revision"]}');canvas.drawRightString(w-36,22,f'{text["pdf_page"]} {doc.page}');canvas.restoreState()
 def tree_header(canvas,doc):
  footer(canvas,doc);canvas.saveState();canvas.setFont('SupersprintBold',20);canvas.setFillColor(HexColor('#292929'));canvas.drawString(26,canvas._pagesize[1]-30,text['pdf_overview']+' | '+data['project_context']['product']);canvas.restoreState()
 story=[p(ui['title'],'title'),p(data['project_context']['product'],'section'),p(text['pdf_title']),p(f'{text["pdf_revision"]} {data["revision"]} | {ui["stage"]}: {ui.get(data["stage"],data["stage"])}','small')]
 for key in ['description','audience','outcome']:
  story.extend([p(ui[key],'heading'),p(data['project_context'][key])])
 if data['project_context'].get('checkpoint'):story.append(p(data['project_context']['checkpoint'],'small'))
 story.append(p(text['pdf_counts'],'heading'))
 story.append(p(' | '.join(f'{ui[k]}: {sum(n["type"]==k for n in data["nodes"])}' for k in TYPES if any(n['type']==k for n in data['nodes']))))
 story.extend([p(text['pdf_reading'],'heading'),p(text['pdf_reading_body']),p(text['pdf_context_note'],'small'),p(text['pdf_legend'],'small')])
 selected=[n for n in data['nodes'] if n['selected']]
 if selected:
  story.append(p(text['pdf_path'],'heading'))
  for n in selected:story.append(Paragraph(ref(n['id']),style['mapping']))
 story.extend([NextPageTemplate('tree'),PageBreak(),tree,NextPageTemplate('normal'),PageBreak(),p(text['pdf_guide'],'title')])
 if not data['nodes']:story.append(p(ui['empty']))
 for kind in TYPES:
  items=[n for n in data['nodes'] if n['type']==kind]
  if not items:continue
  for node_index,n in enumerate(items):
   card_start=len(story)
   if node_index==0:story.append(p(ui[kind],'section'))
   heading=Paragraph(f'<a name="{anchors[n["id"]]}"/>{escaped(n["id"])} - {escaped(n["title"])}',style['heading'])
   status=n['status_label']+(' | '+ui['recommended'] if n['recommended'] else '')
   story.extend([heading,p(text['pdf_status']+': '+status,'small')])
   if n['summary']:story.append(p(n['summary']))
   for block in n['preview_blocks']:
    if not block['body'] or (not block.get('label') and block['body']==n['summary']):continue
    if block.get('label'):story.append(Paragraph('<b>'+escaped(block['label'])+'</b>',style['body']))
    story.append(p(block['body']))
   incoming=[e for e in edges if e['target']==n['id']];outgoing=[e for e in edges if e['source']==n['id']]
   if incoming:story.append(Paragraph(escaped(text['pdf_incoming'])+': '+', '.join(ref(e['source'],False) for e in incoming),style['small']))
   story.append(p(text['pdf_outgoing'],'heading'))
   if not outgoing:story.append(p(text['pdf_gap'] if kind=='signal' else text['pdf_none'],'small'))
   for e in outgoing:
    relation=text['pdf_context'] if e['type']=='context' else text['pdf_evidence'] if kind=='signal' else text['pdf_structural']
    story.append(Paragraph(ref(e['source'],False)+' '+escaped(relation)+' '+ref(e['target']),style['mapping']))
   if n.get('link'):
    raw=n.get('artifact_path') or n.get('source_path') or n['link'];link=n['link'];uri=link if link.startswith(('http://','https://')) else (output.parent/link).resolve().as_uri()
    story.append(Paragraph(f'<link href="{html.escape(uri,quote=True)}" color="#292929">{escaped(text["pdf_source"])}</link><br/>'+escaped(raw),style['small']))
   block=story[card_start:];del story[card_start:]
   block_height=sum(f.wrap(A4[0]-72,100000)[1]+f.getSpaceBefore()+f.getSpaceAfter() for f in block)
   if block_height<=A4[1]-100:story.append(KeepTogether(block))
   else:story.extend(block)
 tree_size=(tree.width+52,tree.height+100)
 if max(tree_size)>14400:raise ValueError('Tree exceeds the portable PDF page-size limit. Split the cycle into smaller projections before exporting PDF.')
 fd,tmp=tempfile.mkstemp(prefix='.supersprint-',suffix='.pdf',dir=output.parent);os.close(fd)
 try:
  doc=BaseDocTemplate(tmp,pagesize=A4,leftMargin=36,rightMargin=36,topMargin=42,bottomMargin=42,title=data['project_context']['product']+' - '+text['pdf_title'],author='Supersprint')
  doc.addPageTemplates([PageTemplate(id='normal',frames=Frame(36,42,A4[0]-72,A4[1]-84,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=footer,pagesize=A4),PageTemplate(id='tree',frames=Frame(26,46,tree.width+1,tree.height+1,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=tree_header,pagesize=tree_size)])
  doc.build(story);os.replace(tmp,output)
 except Exception:
  Path(tmp).unlink(missing_ok=True);raise
 return dict(nodes=len(data['nodes']),visible_edges=len(edges),tree_page_size=list(tree_size))

COMPACT={
 'en':dict(title='Cycle map',note='Original tree with full cards. Click a card to find its mappings in the register on the following pages.',reading='Mappings: preceding IDs > this card > following IDs. A dash means no recorded link. Click an ID in the register to open its source.',content='Card / description',mapping='Mappings',common_status='Status for all cards',tests='Tests',signal_gap='A mapping ending with - has no direct opportunity link.',pdf_all='Complete card register',summary='Descriptions and test protocols remain available through the source links.',limit='The compact map would require text smaller than 9 pt. Use --pdf-layout full or prepare a smaller projection.'),
 'pl':dict(title='Mapa cyklu',note='Oryginalne drzewko z pełnymi kartami. Kliknięcie karty prowadzi do jej wiersza w rejestrze powiązań.',reading='Powiązania: poprzedzające ID > ta karta > kolejne ID. Znak - oznacza brak zapisanej relacji. Kliknięcie ID w rejestrze otwiera źródło.',content='Karta / opis',mapping='Powiązania',common_status='Status wszystkich kart',tests='Testy',signal_gap='Wpis zakończony znakiem - nie ma bezpośredniego powiązania z szansą.',pdf_all='Rejestr wszystkich kart',summary='Rozwinięte opisy i protokoły testów pozostają dostępne przez odnośniki do źródeł.',limit='Mapa wymagałaby tekstu mniejszego niż 9 pkt. Użyj --pdf-layout full albo przygotuj mniejszą projekcję.')}


def compact_labels(data):
 return {**COMPACT.get(data['language'],COMPACT['en']),**{k.removeprefix('pdf_compact_'):v for k,v in data['ui'].items() if k.startswith('pdf_compact_')}}


def mapping_ids(data,id):
 edges=[e for e in data['edges'] if e['visible']]
 return list(dict.fromkeys(e['source'] for e in edges if e['target']==id)),list(dict.fromkeys(e['target'] for e in edges if e['source']==id))


def write_compact_pdf(data,output,font_path=None):
 register_fonts(font_path);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True);ui=data['ui'];text=labels(data);words=compact_labels(data);anchors={n['id']:f'node_{i}' for i,n in enumerate(data['nodes'])};normal=landscape(A4);width=normal[0]-64
 style=styles();style['body'].fontSize=10;style['body'].leading=14
 cell=ParagraphStyle('cell',fontName='Supersprint',fontSize=10,leading=13,textColor=HexColor('#292929'),splitLongWords=True)
 header=ParagraphStyle('cell-head',fontName='SupersprintBold',fontSize=9,leading=12,textColor=HexColor('#292929'))
 link_style=ParagraphStyle('cell-map',fontName='Supersprint',fontSize=9.5,leading=14,textColor=HexColor('#292929'))
 def p(value,kind='body'):return Paragraph(escaped(value),style[kind])
 def ref(id):return f'<link href="#{anchors[id]}" color="#292929"><b>{escaped(id)}</b></link>'
 def footer(c,doc):
  c.saveState();w,h=c._pagesize;c.setFillColor(HexColor('#5D5D5D'));c.setFont('Supersprint',8);c.drawString(32,18,f'{data["project_context"]["product"]} | {text["pdf_revision"]} {data["revision"]}');c.drawRightString(w-32,18,f'{text["pdf_page"]} {doc.page}');c.restoreState()
 layout=layout_tree(data['nodes'],[e for e in data['edges'] if e['visible']])
 tree=Tree(data,layout,anchors,register_goals=True,output=output);overview=(tree.width+64,tree.height+220)
 if max(overview)>14400:raise ValueError('Tree exceeds the portable PDF page-size limit. Split the cycle into smaller projections before exporting PDF.')
 story=[p(data['project_context']['product']+' | '+words['title'],'title'),p(ui['stage']+': '+ui.get(data['stage'],data['stage'])+(' | '+data['project_context']['checkpoint'] if data['project_context'].get('checkpoint') else ''),'small'),p(words['note'],'small'),p(text['pdf_legend'],'small'),p(text['pdf_context_note'],'small')]
 if data['nodes']:story.append(tree)
 else:story.extend([p(ui['empty']),p(data['project_context']['outcome'])])
 story.extend([NextPageTemplate('normal'),PageBreak()])
 section_count=0
 for kind in TYPES:
  if kind=='goal':continue
  items=[n for n in data['nodes'] if n['type']==kind]
  if not items:continue
  if section_count:story.append(PageBreak())
  section_count+=1
  story.append(p(ui[kind],'section'));story.append(p(words['reading'],'small'))
  statuses=list(dict.fromkeys(n['status_label'] for n in items));common=len(statuses)==1
  if common:story.append(p(words['common_status']+': '+statuses[0],'small'))
  if kind=='signal':story.append(p(words['signal_gap'],'small'))
  rows=[[Paragraph(escaped('ID'),header),Paragraph(escaped(ui[kind]),header),Paragraph(escaped(words['mapping']),header)]]
  for n in items:
   incoming,outgoing=mapping_ids(data,n['id']);parts=[]
   if incoming:parts.append(', '.join(ref(id) for id in incoming))
   parts.append(ref(n['id']))
   if outgoing:parts.append(', '.join(ref(id) for id in outgoing))
   elif n['type']=='signal':parts.append('-')
   mapping=' &gt; '.join(parts)
   status=n['status_label']+(' | '+ui['recommended'] if n['recommended'] else '')
   title=escaped(n['title'])
   if not common or n['selected'] or n['recommended']:title+='<br/><font size="8.5" color="#5D5D5D">'+escaped(status)+'</font>'
   source=n.get('link');source_markup=escaped(n['id'])
   if source:
    uri=source if source.startswith(('http://','https://')) else (output.parent/source).resolve().as_uri();source_markup=f'<link href="{html.escape(uri,quote=True)}" color="#292929">{source_markup}</link>'
   rows.append([Paragraph(f'<a name="{anchors[n["id"]]}"/><b>{source_markup}</b>',cell),Paragraph(title,cell),Paragraph(mapping,link_style)])
  table=LongTable(rows,colWidths=[58,width-288,230],repeatRows=1,hAlign='LEFT')
  commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('BACKGROUND',(0,0),(-1,0),HexColor(COLORS[kind][1])),('LINEBELOW',(0,0),(-1,0),.7,HexColor(COLORS[kind][2])),('LINEBELOW',(0,1),(-1,-1),.35,HexColor('#DDDDDD'))]
  for i,n in enumerate(items,1):
   if n['selected']:commands.extend([('BACKGROUND',(0,i),(-1,i),HexColor(COLORS[kind][0])),('LINEBEFORE',(0,i),(0,i),2,HexColor('#292929'))])
  table.setStyle(TableStyle(commands));story.append(table)
 if not section_count:story.append(p(ui['empty']))
 fd,tmp=tempfile.mkstemp(prefix='.supersprint-',suffix='.pdf',dir=output.parent);os.close(fd)
 try:
  doc=BaseDocTemplate(tmp,pagesize=overview,title=data['project_context']['product']+' - '+words['title'],author='Supersprint')
  doc.addPageTemplates([PageTemplate(id='map',frames=Frame(32,32,overview[0]-64,overview[1]-64,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=footer,pagesize=overview),PageTemplate(id='normal',frames=Frame(32,32,width,normal[1]-64,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=footer,pagesize=normal)])
  doc.build(story);os.replace(tmp,output)
 except Exception:
  Path(tmp).unlink(missing_ok=True);raise
 return dict(nodes=len(data['nodes']),visible_edges=sum(e['visible'] for e in data['edges']),layout='compact')


def write_pdf(data,output,font_path=None,layout='compact'):
 if layout not in ['compact','full']:raise ValueError('Unknown PDF layout: '+str(layout))
 return (write_compact_pdf if layout=='compact' else write_full_pdf)(data,output,font_path)
