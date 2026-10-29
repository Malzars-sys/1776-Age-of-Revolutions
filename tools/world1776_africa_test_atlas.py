"""Read-only cartographic test atlas from the current installed game data.

Creates guide artifacts only. No functional writes, gameplay edits or human
attestations. Country labels point to owned pixels, never an inferred capital.
"""
import json,hashlib,textwrap
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from pypdf import PdfReader
import world1776_southern01 as h

ROOT=h.ROOT
OUT=ROOT/'docs/reports/map/WORLD_1776_CLOSURE/AFRICA_GROUPED_TEST_GUIDE_R1'
PDFDIR=ROOT/'output/pdf'
PDF=PDFDIR/'1776_Afrique_parcours_de_verification_R1.pdf'
W,H=2200,1650
INK='#203640';MUTED='#596b70';PAPER='#faf8f2';BLUE='#2e6070';ORANGE='#c65b35';WATER=(213,232,237)
FONT='C:/Windows/Fonts/arial.ttf';BOLD='C:/Windows/Fonts/arialbd.ttf'
def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def write(n,v):(OUT/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def wrap(draw,text,f,width):
 lines=[]
 for paragraph in text.split('\n'):
  line=''
  for word in paragraph.split():
   if line and draw.textlength(line+' '+word,font=f)>width:lines.append(line);line=word
   else:line=(line+' '+word).strip()
  lines.append(line)
 return lines
def paragraph(im,text,xy,width,size=27,color=INK,bold=False,leading=None):
 d=ImageDraw.Draw(im);f=font(size,bold);x,y=xy
 for line in wrap(d,text,f,width):d.text((x,y),line,font=f,fill=color);y+=leading or int(size*1.34)
 return y
def header(title,subtitle,page):
 im=Image.new('RGB',(W,H),PAPER);d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,18),fill=BLUE)
 d.text((65,49),'1776 / TEST AFRICAIN GROUPÉ',font=font(25,True),fill=BLUE)
 d.text((65,96),title,font=font(51,True),fill=INK)
 paragraph(im,subtitle,(68,168),W-136,27,MUTED)
 d.line((65,1560,W-65,1560),fill='#ccd6d5',width=2)
 d.text((65,1584),'Carte des données installées • repères de contrôle, pas frontières historiques certifiées',font=font(23),fill=MUTED)
 d.text((W-164,1584),f'{page} / 5',font=font(24,True),fill=BLUE)
 return im

ZONES=[
 dict(n=1,name='Sénégambie, Mali et Haoussa',where='Côte ouest, puis vers l’intérieur.',anchor=(4050,1780),box=(3660,1690,4350,1900),
      checks=['Au bord de l’Atlantique : Waalo, Baol, Sine et Saloum sont distincts.','Plus à droite : Ségou, Macina, Tombouctou et Gao sont séparés.','Autour de Kano et Katsina : plusieurs royaumes ; pas de Sokoto unifié au départ.'],
      labels=[('WAA','Waalo'),('BAO','Baol'),('SRR','Sine'),('SLU','Saloum'),('SGU','Ségou'),('MSN','Macina'),('TMB','Tombouctou'),('GAO','Gao'),('KTS','Katsina'),('KNN','Kano')]),
 dict(n=2,name='Tchad et vallée du Nil',where='Au sud de l’Égypte ; suivre le fleuve.',anchor=(4690,1710),box=(4300,1430,5010,1925),
      checks=['À l’ouest de Darfour : Ouaddaï, Baguirmi, Fitri et Dar Sila restent distincts.','Le long du Nil : Nubie, Dongola, Shayqiyya, Abdallab et Sennar ont leurs propres territoires.','Cliquer la Nubie : vérifier le lien tributaire avec l’Égypte ; pas d’île de pays créée par un trou de carte.'],
      labels=[('BOR','Bornou'),('WAD','Ouaddaï'),('BGI','Baguirmi'),('BIL','Fitri'),('DLS','Dar Sila'),('DFR','Darfour'),('EGY','Égypte'),('NUB','Nubie'),('DNG','Dongola'),('SHQ','Shayqiyya'),('ABD','Abdallab'),('SNR','Sennar')]),
 dict(n=3,name='Éthiopie et Corne de l’Afrique',where='La pointe de l’Afrique, sous la mer Rouge.',anchor=(5030,1890),box=(4870,1700,5310,2100),
      checks=['Autour de Gondar : Tigré, Godjam et Wollo sont distincts et tributaires de l’empereur.','Plus au sud et à l’est : Choa, Harar, Awsa et Kaffa sont séparés du noyau impérial.','Sur la côte somalie : Mogadiscio/Hiraab et Geledi sont distincts ; pas de grand territoire omanais dans l’intérieur.'],
      labels=[('TGR','Tigré'),('ETH','Gondar / Éthiopie'),('GJM','Godjam'),('WLO','Wollo'),('SHW','Choa'),('HAR','Harar'),('AWS','Awsa'),('KFA','Kaffa'),('HRI','Mogadiscio / Hiraab'),('GLD','Geledi')]),
 dict(n=4,name='Congo et Angola',where='Côte atlantique, au milieu de l’Afrique.',anchor=(4430,2300),box=(4300,2110,4670,2490),
      checks=['Près de l’embouchure du Congo : Kongo, Soyo, Kakongo et Ngoyo sont distincts ; Cabinda n’est pas portugaise.','Au sud : les postes portugais restent reliés à la côte ; Ambriz est hors du Portugal.','Dans l’intérieur : Matamba, Bailundo et Bié sont distincts ; le Kongo n’a pas disparu.'],
      labels=[('KON','Kongo'),('SYO','Soyo'),('KKG','Kakongo'),('NGY','Ngoyo / Cabinda'),('MTM','Matamba'),('MBL','Bailundo'),('BIE','Bié'),('LND','Lunda'),('POR','Portugal / postes côtiers')]),
 dict(n=5,name='Intérieur et Grands Lacs',where='Autour des grands lacs allongés de l’est.',anchor=(4800,2180),box=(4510,2030,4940,2430),
      checks=['Dans le centre : Lunda, Luba, Kuba et Kazembe sont des États centralisés distincts.','Près du lac Victoria : Busoga est séparé du Buganda ; Rwanda et Burundi restent présents.','En diplomatie : Kazembe est indépendant du Lunda ; Kanyok reste tributaire du Luba centralisé.'],
      labels=[('LND','Lunda'),('LBA','Luba'),('KZM','Kazembe'),('KNY','Kanyok'),('KBA','Kuba'),('BUG','Buganda'),('BUS','Busoga'),('RWD','Rwanda'),('BRD','Burundi')]),
 dict(n=6,name='Mozambique',where='Longue côte à l’ouest de Madagascar.',anchor=(4890,2490),box=(4680,2250,5050,2760),
      checks=['Les possessions portugaises sont des postes et zones côtières, pas tout l’arrière-pays.','Inhambane appartient au Portugal ; vers la baie de Maputo, le noyau Tembe reste distinct.','À l’intérieur : Mutapa et Manyika restent présents ; chercher aussi les communautés Makua et Yao.'],
      labels=[('MKU','Makua'),('UYA','Yao'),('MTP','Mutapa'),('MNC','Manyika'),('UTV','Uteve'),('TMP','Tembe / baie de Maputo'),('POR:STATE_LOURENCO_MARQUES','Inhambane (Portugal)')]),
 dict(n=7,name='Afrique australe et Cap',where='Tout en bas du continent.',anchor=(4670,2780),box=(4370,2430,4950,3000),
      checks=['À l’extrémité sud : le Cap reste néerlandais/VOC.','À l’intérieur : communautés de l’Orange, chefferies du Haut-Veld et nguni sont visibles ; pas d’États initiaux Orange, Transvaal, Philippolis ou Waterboer.','Au nord-est : Ngwane existe ; plus au nord, Rozvi existe et Manyika lui est tributaire.'],
      labels=[('DEI','Le Cap / VOC'),('KQO','Communautés de l’Orange'),('BST','Chefferies sotho'),('HVD','Haut-Veld'),('MTB','Chefferies ndébélé'),('NST','Chefferies nguni'),('SWZ','Ngwane'),('MSH','Rozvi')]),
 dict(n=8,name='Madagascar et Comores',where='La grande île à droite de l’Afrique.',anchor=(5180,2545),box=(5010,2300,5320,2745),
      checks=['Au centre de l’île : Antananarivo est un petit noyau ; Ambohimanga et Ambohidratrimo sont séparés.','Sur la côte ouest : Boina au nord et Menabe plus au sud sont distincts.','À la pointe nord : Antankarana est tributaire de Boina. Les Comores, au nord-ouest dans la mer, n’appartiennent pas à Antananarivo.'],
      labels=[('MAD','Antananarivo'),('AVR','Ambohimanga'),('AHI','Ambohidratrimo'),('BOI','Boina'),('MEB','Menabe'),('ATK','Antankarana'),('CMO','Comores')]),
]

def main():
 OUT.mkdir(parents=True,exist_ok=True);PDFDIR.mkdir(parents=True,exist_ok=True)
 sourcepaths=[ROOT/'map_data/provinces.png',ROOT/h.ST]
 for folder in ['common/country_definitions','map_data/state_regions']:
  sourcepaths.extend(h.b.tech.effective(folder))
 sourcehash={str(p):digest(p) for p in sourcepaths}
 riverpath=ROOT/'map_data/rivers.png'
 if not riverpath.exists():riverpath=Path('C:/Games/Victoria 3/game/map_data/rivers.png')
 supplemental={str(riverpath):digest(riverpath)}
 if (OUT/'SUPPLEMENTARY_INPUTS.json').exists():assert json.loads((OUT/'SUPPLEMENTARY_INPUTS.json').read_text('utf8'))==supplemental
 else:write('SUPPLEMENTARY_INPUTS.json',supplemental)
 ident='AFR-20261029-R1-'+sourcehash[str(ROOT/h.ST)][:8]
 if (OUT/'GUIDE_INPUTS.json').exists():
  captured=json.loads((OUT/'GUIDE_INPUTS.json').read_text('utf8'));assert captured['source_sha256']==sourcehash,'Inputs changed: prepare a separate dated guide.'
  if (OUT/'TEST_SHEET.json').exists():assert all(r['status']=='NON_VERIFIE' for r in json.loads((OUT/'TEST_SHEET.json').read_text('utf8'))['tests']),'Do not replace human test observations.'
 else:write('GUIDE_INPUTS.json',dict(id=ident,created_on='2026-10-29',historical_start='1776-01-01',functional_files_changed=0,source_sha256=sourcehash,human_test='NOT_RUN'))
 own=h.prior.m.state_owners(h.raw(ROOT/h.ST));cat=h.b.a.catalog('common/country_definitions')
 tags=sorted({v[-1][1] for v in own.values()});ids={t:i+1 for i,t in enumerate(tags)}
 # Land membership comes from every native state region, including unowned
 # impassable provinces; absence of ownership alone does not imply water.
 lut=np.zeros(1<<24,'int16')
 for n,path in h.b.a.catalog('map_data/state_regions').values():
  if path.name=='99_seas.txt':continue
  for c in h.prior.m.s.ids(n,'provinces'):lut[int(c[1:],16)]=-1
 for c,v in own.items():lut[int(c[1:],16)]=ids[v[-1][1]]
 bmp=np.array(Image.open(ROOT/'map_data/provinces.png').convert('RGB'))
 pack=bmp[:,:,0].astype('uint32')*65536+bmp[:,:,1].astype('uint32')*256+bmp[:,:,2];code=lut[pack]
 riv=np.array(Image.open(riverpath).convert('RGB')).astype('int16');rivermask=(riv[:,:,2]>riv[:,:,0]+20)&(riv[:,:,2]>riv[:,:,1]+10)
 colors=np.zeros((len(tags)+1,3),'uint8');colors[0]=WATER
 for t,i in ids.items():
  try:rgb=np.array(list(map(int,h.prior.m.s.ids(cat[t][0],'color'))))
  except (KeyError,ValueError):rgb=np.array([160,160,145])
  colors[i]=np.clip(rgb*.61+np.array([249,246,236])*.39,0,255)
 refs=[]
 def mapdraw(im,box,rect,labels=None,oceans=None):
  x0,y0,x1,y1=box;rx,ry,rw,rh=rect;scale=min(rw/(x1-x0),rh/(y1-y0));dw,dh=round((x1-x0)*scale),round((y1-y0)*scale);rx+=round((rw-dw)/2);ry+=round((rh-dh)/2)
  a=code[y0:y1,x0:x1];rgb=colors[np.maximum(a,0)];rgb[a<0]=(228,224,207)
  if labels:rgb[rivermask[y0:y1,x0:x1]&(a!=0)]=(90,153,184)
  edge=np.zeros(a.shape,bool);edge[1:]|=a[1:]!=a[:-1];edge[:,1:]|=a[:,1:]!=a[:,:-1];rgb[edge]=(87,103,103)
  img=Image.fromarray(rgb).resize((dw,dh),Image.Resampling.LANCZOS);im.paste(img,(rx,ry));d=ImageDraw.Draw(im)
  def xy(p):return rx+(p[0]-x0)*scale,ry+(p[1]-y0)*scale
  d.rounded_rectangle((rx-1,ry-1,rx+dw+1,ry+dh+1),radius=5,outline='#b9cbd0',width=2)
  placed=[];callouts=[]
  for token,label in labels or []:
   t,_,sid=token.partition(':')
   if t not in ids:continue
   mask=a==ids[t]
   if sid:
    cc=[int(c[1:],16) for c,v in own.items() if v[-1]==[sid,t]];mask &= np.isin(pack[y0:y1,x0:x1],cc)
   yy,xx=np.where(mask)
   if not len(xx):continue
   j=np.argmin((xx-np.median(xx))**2+(yy-np.median(yy))**2);pt=(xx[j]+x0,yy[j]+y0);ax,ay=xy(pt)
   f=font(22,True);lines=wrap(d,label,f,260);lw=max(d.textlength(s,font=f) for s in lines)+18;lh=len(lines)*27+10
   chosen=None
   for offy in [0,-40,40,-75,75,-110,110,-145,145]:
    for offx in [0,-120,120,-230,230]:
     lx=max(rx+7,min(rx+dw-lw-7,ax-lw/2+offx));ly=max(ry+7,min(ry+dh-lh-7,ay-lh/2+offy));r=(lx,ly,lx+lw,ly+lh)
     if not any(r[0]<p[2]+7 and r[2]>p[0]-7 and r[1]<p[3]+6 and r[3]>p[1]-6 for p in placed):chosen=r;break
    if chosen:break
   if chosen is None:chosen=(rx+7,ry+7,rx+7+lw,ry+7+lh)
   placed.append(chosen);lx,ly,ex,ey=chosen
   callouts.append((chosen,ax,ay,lines,f))
   refs.append(dict(page_label=label,TAG=t,owned_pixel=[int(pt[0]),int(pt[1])],state=own.get('x'+format(int(pack[int(pt[1]),int(pt[0])]),'06X'))))
  for chosen,ax,ay,lines,f in callouts:
   lx,ly,ex,ey=chosen;d.line((ax,ay,(lx+ex)/2,(ly+ey)/2),fill=INK,width=2);d.ellipse((ax-4,ay-4,ax+4,ay+4),fill=INK)
  for chosen,ax,ay,lines,f in callouts:
   lx,ly,ex,ey=chosen;d.rounded_rectangle(chosen,radius=7,fill='#ffffff',outline='#9badad',width=1)
   for n,s in enumerate(lines):d.text((lx+9,ly+5+n*27),s,font=f,fill=INK)
  for label,p in oceans or []:
   ax,ay=xy(p);d.text((ax,ay),label,font=font(22),fill=BLUE,stroke_width=1,stroke_fill='#f2f8f8')
  return xy

 # Overview: eight large numbered targets, with a route legend at the right.
 overview=header('Où regarder dans le jeu', 'Nouvelle partie au 1er janvier 1776. Commence en pause ; les numéros renvoient aux vues détaillées.',1)
 xy=mapdraw(overview,(3600,1320,5370,3010),(65,250,1290,1230),oceans=[('Atlantique',(3660,2260)),('Océan Indien',(5145,2850))])
 d=ImageDraw.Draw(overview)
 for z in ZONES:
  x,y=xy(z['anchor']);d.ellipse((x-30,y-30,x+30,y+30),fill=ORANGE,outline='white',width=4);s=str(z['n']);d.text((x-d.textlength(s,font=font(33,True))/2,y-20),s,font=font(33,True),fill='white')
  yy=255+(z['n']-1)*135;d.ellipse((1410,yy,1458,yy+48),fill=ORANGE);d.text((1424,yy+6),str(z['n']),font=font(28,True),fill='white')
  paragraph(overview,z['name'],(1480,yy),650,30,INK,True);paragraph(overview,z['where'],(1480,yy+48),640,25,MUTED)
 d.text((1190,283),'N',font=font(27,True),fill=BLUE);d.line((1200,365,1200,325),fill=BLUE,width=5);d.polygon([(1200,308),(1189,330),(1211,330)],fill=BLUE)
 overview.save(OUT/'01_carte_reperee.png')

 pages=[overview]
 for page,pair,title in [(2,(1,2),'De l’Atlantique au Nil'),(3,(3,5),'De la Corne aux Grands Lacs'),(4,(4,6),'Les deux façades : Congo et Mozambique'),(5,(7,8),'Afrique australe et Madagascar')]:
  im=header(title,'Lis les noms indiqués, puis compare les trois points sous chaque carte. Un nom peut être abrégé dans le jeu.',page);d=ImageDraw.Draw(im)
  for col,n in enumerate(pair):
   z=ZONES[n-1];left=65+col*1080
   d.ellipse((left,242,left+48,290),fill=ORANGE);d.text((left+14,248),str(n),font=font(28,True),fill='white')
   d.text((left+65,242),z['name'],font=font(33,True),fill=INK)
   mapdraw(im,z['box'],(left,314,995,698),z['labels'])
   y=1038
   for i,text in enumerate(z['checks'],1):
    d.rounded_rectangle((left,y+4,left+23,y+27),radius=3,outline=BLUE,width=2)
    y=paragraph(im,text,(left+40,y),940,27,INK,leading=36)+21
  # Tiny Portuguese ports need callouts, rather than misleading centroid labels.
  if page==4:
   paragraph(im,'Les ports portugais sont très petits : zoome davantage si leur couleur est difficile à distinguer.',(65,1494),2050,23,MUTED)
  if page==5:
   paragraph(im,'Antananarivo et ses deux voisins sont des petits territoires contigus : les traits relient chaque nom à sa province.',(65,1494),2050,23,MUTED)
  im.save(OUT/f'{page:02d}_details.png');pages.append(im)

 # The PNGs retain the high-resolution map; the PDF is a convenient five-page
 # handout. Labels/checkboxes are drawing primitives, never purported game UI.
 c=canvas.Canvas(str(PDF),pagesize=landscape(A4));pw,ph=landscape(A4)
 c.setTitle('1776 - Parcours de vérification de l’Afrique');c.setAuthor('1776 Age of Revolutions - guide de test')
 for im in pages:
  s=min(pw/W,ph/H);dw,dh=W*s,H*s;c.drawInlineImage(im,(pw-dw)/2,(ph-dh)/2,width=dw,height=dh);c.showPage()
 c.save()
 tests=[dict(zone=z['n'],name=z['name'],observations=z['checks'],status='NON_VERIFIE',evidence=None) for z in ZONES]
 write('TEST_SHEET.json',dict(version=ident,tests=tests,simulation='NON_VERIFIE',save_reload='NON_VERIFIE',new_human_attestations=0))
 write('LABEL_ANCHORS.json',refs)
 guide=f'''# Parcours de vérification de l’Afrique\n\nGuide du 29 octobre 2026. Version repérée : {ident}. Les cartes montrent les propriétaires réellement présents dans les fichiers au moment de la préparation ; elles ne sont pas un nouvel atlas historique de référence. Aucun fichier de jeu n’est modifié. Les noms sont des repères, pas des positions garanties de capitales.\n\n## Avant de commencer\n\n1. Relance le jeu si le mod était déjà chargé avant les dernières corrections. Crée une nouvelle partie au **1er janvier 1776**. Une ancienne sauvegarde ne permet pas de tester l’installation initiale.\n2. Le mode Observateur convient au tour de carte. Commence en pause et affiche la carte politique.\n3. Repère d’abord la grande île de Madagascar à droite du continent, puis l’extrémité sud où se trouve le Cap. Reviens ensuite au numéro 1 et suis le parcours jusqu’au numéro 8. Le haut des cartes est le nord.\n4. Compare les propriétaires et les noms, pas seulement les couleurs : les couleurs peuvent varier avec les sujets ou le mode de carte. Clique les petits pays pour lire leur nom et leur diplomatie.\n\n'''
 for z in ZONES:
  guide+=f"## {z['n']}. {z['name']}\n\n{z['where']}\n\n"+'\n'.join('- [ ] '+s for s in z['checks'])+'\n\n'
 guide+='''## Ce qu’il faut signaler\n\nSignale un pays attendu qui manque, un propriétaire différent, un nom illisible/une clé de script, un territoire sans propriétaire, une capitale placée dans un pays tiers ou un petit pays coupé par un trou de carte. Pour un lien tributaire, regarde la diplomatie : un simple nom ou une couleur similaire ne prouve pas la relation.\n\nLes grandes zones décentralisées représentent plusieurs communautés : ce n’est pas un bug de n’y voir aucun État centralisé moderne. Le lissage des contours a été reporté ; ne bloque pas ce test sur les seules dents de scie déjà connues. Les marges historiques incertaines (Cap, chefferies, frontières xhosa, etc.) restent celles des rapports ; la conformité à ces cartes ne les transforme pas en frontières historiques certifiées.\n\n## Après le tour en pause\n\nLaisse passer **un mois**, puis sauvegarde et recharge cette sauvegarde. Compare la même date avant et après le rechargement : mêmes propriétaires, noms et relations. Note les pays qui ont changé par une guerre pendant le mois, sans les assimiler automatiquement à un bug d’installation.\n\nSi tu contrôles un pays plutôt que l’Observateur, ajoute un contrôle simple de ses lois et de ses technologies, et essaie de mettre un bâtiment autorisé en construction. Il n’est pas nécessaire de refaire la partie avec chacun des petits pays. Les vérifications de construction/recrutement non faites restent non vérifiées ; ce parcours ne certifie pas la rentabilité ou l’équilibrage militaire.\n\n## Retour à envoyer\n\nTu peux répondre : «1 OK, 2 OK, 3 problème…». Pour chaque problème : numéro de zone, nom du pays ou du lieu, date en jeu, ce que tu vois et une capture assez large pour retrouver la zone. Indique si c’est une nouvelle partie, si le mois a été simulé et si la sauvegarde a été rechargée. Tu n’as pas besoin de connaître le bon tracé historique.\n\nL’absence de défaut visible est un constat de chargement et de carte, pas une validation automatique de tous les critères WORLD. Aucun résultat humain n’est prérempli.\n'''
 (OUT/'PARCOURS.md').write_text(guide,encoding='utf8')
 (OUT/'RETOUR_TEST.txt').write_text(f'''Version du guide : {ident}\nVersion du mod/jeu ou date de lancement :\nNouvelle partie au 1er janvier 1776 :\n1 Sénégal/Mali/Haoussa : non vérifié\n2 Tchad/Nil : non vérifié\n3 Corne : non vérifié\n4 Congo/Angola : non vérifié\n5 Intérieur/Grands Lacs : non vérifié\n6 Mozambique : non vérifié\n7 Afrique australe : non vérifié\n8 Madagascar/Comores : non vérifié\nUn mois simulé : non vérifié\nSauvegarde/rechargement : non vérifié\nLois/technologies/construction éventuellement testées :\nProblèmes (zone, pays, date, description, capture) :\n''',encoding='utf8')
 unchanged=all(digest(Path(p))==v for p,v in {**sourcehash,**supplemental}.items());assert unchanged,'Source changed during guide generation; review before delivery.'
 # Every country callout must land on a pixel owned by that country.
 anchor_ok=all(int(code[r['owned_pixel'][1],r['owned_pixel'][0]])==ids[r['TAG']] for r in refs)
 reader=PdfReader(PDF);assert len(reader.pages)==5 and anchor_ok
 write('VALIDATION.json',dict(status='PASS',sources_unchanged=unchanged,country_callouts_on_owned_pixels=anchor_ok,callout_count=len(refs),pdf_pages=len(reader.pages),overview_zones=8,gameplay_files_written=0,Git_writes=0,vanilla_writes=0,human_tests_recorded=0,visual_review='PENDING'))
 files=list(OUT.glob('*.png'))+[PDF,OUT/'PARCOURS.md',OUT/'RETOUR_TEST.txt',OUT/'TEST_SHEET.json',OUT/'LABEL_ANCHORS.json',OUT/'GUIDE_INPUTS.json']
 write('MANIFEST.json',{str(p.relative_to(ROOT)):digest(p) for p in files})
 print(json.dumps(dict(guide=ident,pdf=str(PDF),overview=str(OUT/'01_carte_reperee.png'),pages=5,callouts=len(refs),validation='PASS; visual review pending'),ensure_ascii=False))

if __name__=='__main__':main()
