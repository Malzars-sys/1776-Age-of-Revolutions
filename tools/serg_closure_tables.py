"""Curated audit tables; reads installed data, writes audit-only JSON/Markdown.

No migration, compiler, country creation or runtime mutation is called here.
The old 94-row inventory is a lead, not an installed-state or historical authority.
"""
from pathlib import Path
import collections, csv, json, re
from serg_global_closure_audit import ROOT,OUT,save
from map_1776_audit import effective
import validate_map2a as qa

V='VALIDÉ EN JEU'; I='INSTALLÉ — NON VALIDÉ'; P='PARTIELLEMENT TRAITÉ'; D='AUDITÉ — BLOQUÉ OU DIFFÉRÉ'; N='NON AUDITÉ'; C='AUDITÉ — CONFORME'
BASE='docs/reports/map/'
W='MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG'
ATT='docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT/RUNTIME_USER_ATTESTATION.json'
def ref(p,needle=None):
    path=ROOT/p
    if not path.exists(): return p+' [NON RETROUVÉ]'
    lines=path.read_text(encoding='utf-8-sig',errors='replace').splitlines()
    line=next((i for i,t in enumerate(lines,1) if needle and needle.lower() in t.lower()),1)
    return p+':'+str(line)

# ID, macro, title, status, native regions (not historical polygons), historical perimeter,
# existing lots/evidence, remaining scope. IDs double as map callouts.
SPECS=[
('A01','A','Holstein royal et exclusion du Schleswig',P,'SCHLESWIG_HOLSTEIN','Holstein impérial; Schleswig extérieur','MAP2Q/REPORT.md','Règlement de 1773 et limites HOL/SCH non reconstruits; Eutin n’est pas tout le Holstein.'),
('A02','A','Eutin et Schwartau, noyaux HLB',V,'SCHLESWIG_HOLSTEIN','Prince-évêché distinct de la ville de Lübeck','MAP2Q/R3/REPORT.md','Chapitre, Ruppersdorf, Neuhof restent ouverts.'),
('A03','A','Villes de Lübeck, Hambourg et Brême',P,'SCHLESWIG_HOLSTEIN ELBE POMERANIA','Villes impériales et possessions séparées, pas les évêchés sécularisés','MAP2K/MAP2K_EXECUTIVE_SUMMARY.md','Pays présents; limites et dépendances suédoises héritées non certifiées historiquement.'),
('A04','A','Wismar–Poel–Neukloster',V,'MECKLENBURG POMERANIA','Possessions impériales suédoises seulement','MAP2N/REPORT.md','Poel regroupée techniquement en Poméranie; Suède entière non impériale.'),
('A05','A','Mecklembourg hors possessions suédoises',N,'MECKLENBURG','Schwerin, Strelitz et juridictions particulières','MAP2M/R9/HRE_REGIONS_PROGRESS.md','Recherche macro R2, pas de contrôle territorial dédié retrouvé.'),
('A06','A','Poméranie impériale, Peene et Wolgast',V,'POMERANIA','Possessions PRU/SWE dans le duché; pas Suède entière','MAP2M/R9/REPORT.md','Peendamm abstrait; frontière politique généralisée acceptée, pas levé cadastral.'),
('A07','A','Brandebourg, Neumark, Magdebourg–Halberstadt',P,'BRANDENBURG ANHALT','Possessions impériales prussiennes, pas Prusse royale extérieure','MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md','Audit macro; frontières Magdebourg/Halberstadt et franges non certifiées RGB par RGB.'),
('A08','A','Hanovre, Brunswick et principautés du Harz',P,'HANNOVER BRUNSWICK ELBE','Branches Brunswick-Lunebourg et possessions impériales du roi britannique','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv','Minden/Osnabrück/Niederstift traités séparément; noyaux restants non reconstruits en détail.'),
('B01','B','Münster, Paderborn, Juliers–Berg : premiers noyaux',V,'WESTPHALIA NORTH_RHINE RUHR','Souverainetés ecclésiastiques et palatines distinctes','MAP2L/RHINE_WESTPHALIA/REPORT.md','Limites et petites juridictions intercalées ouvertes.'),
('B02','B','Osnabrück, Niederstift, Lingen–Tecklenburg',V,'HANNOVER','Osnabrück non annexé au Hanovre/Münster; Niederstift propre à Münster','MAP2L/RHINE_WESTPHALIA_COMPLETION/REPORT.md','Damme-Neuenkirchen, bordures HAN/OLD non certifiées.'),
('B03','B','Minden : correction de 76 cellules',I,'HANNOVER','Possession prussienne de 1776','MAP2L/MINDEN_RAVENSBERG/REPORT.md','Pas de reçu spécifique couvrant ce sous-lot; Ravensberg distinct et différé.'),
('B04','B','Duché de Westphalie et Vest de Cologne',I,'WESTPHALIA','Deux possessions de Cologne, pas toute Westphalie','MAP2L/DUCHY_WESTPHALIA/REPORT.md','84 cellules préservées; reçu spécifique non retrouvé; franges ouvertes.'),
('B05','B','Clèves, Mark, Ravensberg et Gueldre prussienne',P,'NORTH_RHINE RUHR WESTPHALIA RHINELAND','Possessions occidentales de PRU antérieures au XIXe siècle','MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv','Cœurs PRU maintenus; partage Gueldre et bordures non achevés.'),
('B06','B','Lippe et Schaumbourg-Lippe',P,'WESTPHALIA','Comtés distincts; pas titres princiers ultérieurs','MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv','Pays présents, aucune reconstitution complète des frontières retrouvée.'),
('B07','B','Petits comtés, abbayes et Dortmund',D,'WESTPHALIA HANNOVER RUHR','Bentheim, Steinfurt, Rietberg, Corvey, Essen, Werden, ville Dortmund','MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv','Gage de Bentheim à distinguer du titre; pas de pays automatique par abbaye.'),
('B08','B','Emden et noyau côtier de Frise orientale',V,'HANNOVER','Possession prussienne depuis 1744','MAP2O/REPORT.md','319 cellules B; ne certifie pas toute la Frise historique.'),
('B09','B','Frise orientale méridionale et Jever',D,'HANNOVER','Leer/Rheiderland PRU; Jever Anhalt-Zerbst; Kniphausen distinct','MAP2S/JEVER_HISTORICAL_EVIDENCE.md','Jever toujours OLD dans enveloppes candidates; attribution exacte non résolue. MAP2P n’a rien transféré.'),
('C01','C','Rhin central, noyaux palatins et électoraux',V,'BADEN RHINELAND NORTH_RHINE','Neckar/Palatinat distinct de Bavière en 1776','MAP2L/RHINE_CENTRAL/REPORT.md','Validation limitée aux zones inspectées, pas à tous les bailliages.'),
('C02','C','Mayence Rheingau–Bergstraße–Spessart–Tauber',I,'HESSE FRANCONIA BADEN WURTTEMBERG','Possessions mayençaises non assimilées à tout le diocèse','MAP2L/MAINZ_COMPLETION/REPORT.md','Trois couches de noyaux installées; aucune attestation détaillée de l’ensemble retrouvée.'),
('C03','C','Erfurt–Eichsfeld',D,'SAXONY ANHALT','Possessions séparées de Mayence, pas Eichstätt','MAP2L/ERFURT_EICHSFELD/REPORT.md','Translation 7,20 pixels refusée; villes et frontières restent non validées. Aucun nouvel ajustement.'),
('C04','C','Fulda et branches de Nassau installées',V,'HESSE RHINELAND SAXONY','FUL, NAS, NOU, NWB, NSB; provinces distinctes des Provinces-Unies','MAP2W/R2B/REPORT.md','R1/R2A reçu général; R2B explicitement validé. Franges, Hombourg, Hanau, apanages restent ouverts.'),
('C05','C','Hesses, Waldeck, Francfort et juridictions rhénanes restantes',P,'HESSE RHINELAND','Cassel, Darmstadt, Hombourg, Solms, Isembourg, Wittgenstein, Worms/Spire','MAP2W/R2B/UNRESOLVED_R2B.csv','Ne pas convertir tous apanages en souverainetés; temporalités épiscopales à séparer du diocèse et de la ville.'),
('D01','D','Franconie : noyaux principaux et continuation',V,'FRANCONIA BAVARIA','ANS, FBM, WZB, NUR, EIC et fragments de COB','MAP2L/FRANCONIA_CONTINUATION/REPORT.md','Union Ansbach–Bayreuth sous même prince; pas Prusse de 1791. Résidus BAV non certifiés.'),
('D02','D','Hohenlohe, Castell, Wertheim et villes secondaires',D,'FRANCONIA WURTTEMBERG','Branches et villes impériales avant médiatisation','MAP2W/R3/CALIBRATION/REPORT.md','Aucun R3 installé; candidats Langenbourg/Kirchberg retirés, zéro homologue physique accepté.'),
('D03','D','Franges franconiennes et possessions dispersées',P,'FRANCONIA BAVARIA','Limites politiques traversant régions économiques','MAP2L/FRANCONIA/UNRESOLVED.csv','662 cellules BAV était un chiffre initial, pas le résidu actuel après continuations.'),
('E01','E','Souabe : première passe',V,'BADEN WURTTEMBERG BAVARIA','Bade réuni 1771, Wurtemberg, Hohenzollern, Ulm et évêchés','MAP2L/SWABIA/REPORT.md','Noyaux seulement; souveraineté hors noyau non certifiée.'),
('E02','E','Fürstenberg et Ellwangen : continuation',I,'BADEN WURTTEMBERG FRANCONIA','Pays distincts, pas tout domaine spirituel','MAP2L/SWABIA_CONTINUATION/REPORT.md','Noyaux préservés dans tests postérieurs; le reçu FINISH ne valide pas automatiquement toute cette couche.'),
('E03','E','Salem, Waldburg, Constance : finition',V,'BADEN WURTTEMBERG BAVARIA','Quatre branches Waldburg et temporalités ecclésiastiques','MAP2L/SWABIA_FINISH/REPORT.md','Condominats et offices externes ouverts; Constance autrichienne distincte du Hochstift.'),
('E04','E','Villes libres, Weingarten et raccord autrichien',V,'BADEN WURTTEMBERG BAVARIA','Augsbourg/Kempten villes distinctes de leur évêché/abbaye','MAP2L/SWABIA_COMPLETION/REPORT.md','Une cellule chacune autorisée; pas extension automatique à Isny/Lindau/Kaufbeuren.'),
('E05','E','Montbéliard, Oettingen et franges souabes',D,'FRANCHE_COMTE WURTTEMBERG BAVARIA BADEN','Montbéliard vs quatre seigneuries françaises; branches Oettingen','MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv','Aucun transfert de Montbéliard; pas rétroprojection de 1786. Petits territoires et limites autrichiennes ouverts.'),
('F01','F','Passau : noyau politique',V,'BAVARIA','Prince-évêché distinct de BAV/AUS','MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU/REPORT.md','xEDBA00, 40 cellules; périphérie et possessions autrichiennes non reconstituées.'),
('F02','F','Freising : noyau politique',V,'BAVARIA','Hochstift, pas le diocèse',''+W+'/REPORT.md','14 cellules; Burgrain, Werdenfels, bande Ismaning restent C.'),
('F03','F','Ratisbonne : ville et évêché',V,'BAVARIA','Deux juridictions RCI/RBI; pas une seule ville épiscopale',''+W+'/REPORT.md','RCI 2 cellules/713 habitants techniques; RBI 14 cellules. Hohenburg et immunités ouverts.'),
('F04','F','Bavière et enclaves restantes',P,'BAVARIA','Électorat séparé de Palatinat avant décembre 1777','MAP2W/R4/HISTORICAL_INVENTORY.md','Pays BAV préservé; pas preuve globale des résidus, Ortenbourg/Berchtesgaden manquent de représentation distincte.'),
('F05','F','Salzbourg',D,'AUSTRIA BAVARIA TYROL','Erzstift immédiat, non possession habsbourgeoise en 1776','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md','Absence politique distincte confirmée; limites natives et population à établir. Ne pas confondre avec circonscription moderne.'),
('G01','G','Anhalt : quatre principautés',V,'ANHALT','Dessau, Bernbourg, Köthen, Zerbst','MAP2R/REPORT.md','MAP2S arrêt pratique: Rosslau/Barby/Hoym et Jever ne sont pas clos.'),
('G02','G','Saxe et duchés ernestins',V,'SAXONY FRANCONIA','Électorat et duchés de 1776, pas Cobourg-Gotha de 1826','MAP2T/REPORT.md','Noyaux inspectés, pas toutes enclaves et branches.'),
('G03','G','Reuss et Schwarzbourg-Sondershausen',V,'SAXONY ANHALT','Branches juridiquement distinctes, pas Reuss unifié','MAP2U/REPORT.md','Noyaux et enclave septentrionale seulement; franges résiduelles ouvertes.'),
('G04','G','Possessions dispersées de Saxe/Anhalt/Thuringe',P,'SAXONY ANHALT','Condominiums, apanages et enclaves','MAP2U/UNRESOLVED.csv','Ne pas réutiliser listes pré-T/U comme preuve d’absence des nouveaux pays.'),
('H01','H','Bohême',N,'BOHEMIA','Couronne de Bohême dans SERG; pas royaume de Hongrie','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv','Bibliographie macro LOW; pas audit territorial complet retrouvé.'),
('H02','H','Moravie et Silésie autrichienne',P,'MORAVIA WEST_GALICIA','Opava/Teschen impériaux; nom WEST_GALICIA purement technique','MAP2A/MAP2A_EXECUTIVE_SUMMARY.md','Deux doubles propriétaires corrigés et Teschen rescopé; reste de la région non certifié.'),
('H03','H','Silésie prussienne, Glatz et Lusaces',P,'LOWER_SILESIA UPPER_SILESIA SAXONY','Partition 1742/1763, pas acquisitions de 1815','MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/SILESIA_READING.md','Études et maintiens proposés, pas reconstruction complète de la frontière.'),
('H04','H','Autriche, Styrie, Carinthie et Carniole',N,'AUSTRIA STYRIA SLOVENIA','Terres impériales habsbourgeoises; limites avec Hongrie/Croatie distinctes','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv','R2-0133/136/137: inventaire bibliographique seulement; limites natives non homologuées.'),
('H05','H','Tyrol et principautés de Trente/Brixen',P,'TYROL SOUTH_TYROL','Comté habsbourgeois et deux principautés ecclésiastiques impériales','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md','Trente/Brixen sans pays territorial distinct; partage administratif initial ne prouve pas leur souveraineté autrichienne.'),
('H06','H','Autriche antérieure et frontière adriatique',P,'BADEN WURTTEMBERG BAVARIA ISTRIA','Territoires dispersés; Istrie vénitienne non impériale par simple State_ID','MAP2A/MAP2A_EXECUTIVE_SUMMARY.md','Fribourg/Nellenburg/Landvogtei corrigés; Sundgau antérieur vs 1648 et Gorizia/Trieste à examiner séparément.'),
('I01','I','Liège, Stavelot et Pays-Bas autrichiens : noyaux',V,'FLANDERS WALLONIA GELRE','Ensemble bourguignon et deux principautés distinctes','MAP2L/BELGIUM/IMPLEMENTATION.md','Ne valide pas chaque limite de Limbourg, Maastricht ou Bouillon.'),
('I02','I','Luxembourg : intégration à BEO',I,'WALLONIA','Possession habsbourgeoise, pas pays indépendant sous NET','LUX_BEO_INTEGRATION_2026-10-10/REPORT.md','xD001A0 présent BEO; aucun reçu propre à tout le périmètre luxembourgeois.'),
('I03','I','Limbourg, Maastricht, Bouillon et franges belges',P,'WALLONIA FLANDERS GELRE','Condominium et frontières néerlandaises/impériales distincts','MAP2L/BELGIUM/IMPLEMENTATION.md','Petites juridictions ouvertes; souveraineté de Bouillon et Saint-Hubert ne se déduit pas d’un TAG voisin.'),
('J01','J','Milanais–Crémonais et Trois Ligues',I,'LOMBARDY','Milan/Mantoue AUS; Valteline hors SERG sous Trois Ligues','MAP2L/MILAN_CREMONESE/REPORT.md','64 cellules AUS de continuité conservées; autre frontière lombarde non certifiée.'),
('J02','J','Piémont : inclusion impériale limitée',I,'PIEDMONT','Neuf RGB SAR seuls inscrits; pas île de Sardaigne','MAP2L/PIEDMONT/REPORT.md','Appartenance pays entier au bloc ≠ territoire impérial; Savoie/Nice restent non tranchées par ce lot.'),
('J03','J','Savoie, Nice et fiefs ligures',N,'SAVOY PROVENCE PIEDMONT','Statuts impériaux à vérifier territoire par territoire','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv','R1-0013/14/15: dossier macro, pas délimitation et statut impérial entièrement établis.'),
('J04','J','Modène, Parme et Toscane',N,'EMILIA TUSCANY','Principautés présentes; investitures et exclusions pontificales à auditer','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md','MOD/PAR/TUS présents au registre gelé; aucune reconstruction territoriale dédiée retrouvée. Pas toute Italie impériale par défaut.'),
('K01','K','Petites juridictions non cerclées et chevalerie',N,'HESSE FRANCONIA WURTTEMBERG','Chevalerie, fiefs et droits immédiats; pas tous États souverains','MAP2W/R3/HISTORICAL_EVIDENCE.md','Pas d’inventaire de toutes possessions immédiates; portée pratique 1.0 à définir.'),
('K02','K','Liechtenstein et autres exceptions alpines',D,'TYROL SWITZERLAND','Vaduz/Schellenberg immédiats; Suisse et Trois Ligues hors Empire après 1648','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md','Liechtenstein sans représentation distincte; faible surface, décision P2 possible. Pas nouveau pays automatique.'),
]

def build():
    inv=json.loads((OUT/'CURRENT_INVENTORY.json').read_text()); reg=json.loads((OUT/'REGISTRY_CHECKS.json').read_text()); layers=json.loads((OUT/'LAYERS.json').read_text()); counts=json.loads((OUT/'RGB_COUNTS.json').read_text())
    rows=[]
    for id,group,name,status,states,perimeter,evidence,open_ in SPECS:
        evid=BASE+evidence
        if not (ROOT/evid).exists() and id=='I02':
            evid=next((p.relative_to(ROOT).as_posix() for p in (ROOT/BASE/'LUX_BEO_INTEGRATION_2026-10-10').glob('*.md')),evid)
        rows.append(dict(ID=id,Macro_region=group,Secteur=name,Statut=status,Representation_schematique_acceptee='OUI' if status in {V,I} else 'NON ÉTABLI / MIXTE',Regions_techniques=';'.join('STATE_'+s for s in states.split()),Perimetre_historique=perimeter,Preuve=ref(evid),Problemes_ouverts=open_,Portee_validation='Modifications inspectées seulement; pas certification historique' if status==V else 'Pas de validation territoriale exhaustive',Recherche='Macro seulement, insuffisant pour audit territorial' if status==N else 'Dossier historique local retrouvé'))
    save('REGIONAL_DATA.json',rows)
    # Installed country facts, not an engine selection of the visible government.
    facts={t:dict(definition=json.loads(v),history=[],rulers=[],laws=[]) for t,v in inv['countries'].items()}
    for folder in ('countries','characters'):
        for p in effective(ROOT,qa.GAME,'common/history/'+folder):
            raw=p.read_text(encoding='utf-8-sig'); nodes=qa.cw.parse(raw)
            for n in qa.cw.walk(nodes):
                tag=n.key.removeprefix('c:')
                if not n.key.startswith('c:') or tag not in facts:continue
                loc=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else str(p)
                facts[tag]['history'].append(loc+':'+str(raw[:n.start].count('\n')+1))
                facts[tag]['laws']+= [qa.cw.scalar(x.value) for x in n.children('activate_law')]
                for c in n.children('create_character'):
                    if c.one('ruler')=='yes':facts[tag]['rulers'].append({k:c.one(k,'') for k in ('first_name','last_name','birth_date','age','historical','ruler')})
    for t,f in facts.items():
        f['RGBs']=[r['key'][0] for r in inv['owners'] if r['key'][2]==t];f['states']=sorted({r['key'][1] for r in inv['owners'] if r['key'][2]==t})
        f['government_law_declarations']=[x for x in f['laws'] if any(y in x for y in ('monarchy','republic','theocracy','autocracy','oligarchy'))]
    save('COUNTRY_FACTS.json',facts)
    old=list(csv.DictReader((ROOT/BASE/'MAP2W/INVENTORY_1776.csv').open(encoding='utf-8-sig')))
    # Explicit corrections to stale pre-R2/pre-R4 inventory.
    corrections={36:'NWB',37:'NSB',38:'NOU',87:'FSI',88:'PAS',89:'RBI',90:'RCI'}
    selected={
        'KCL':('B01','NORTH_RHINE WESTPHALIA'),'KTR':('C01','RHINELAND'),'KPF':('C01','BADEN RHINELAND RUHR NORTH_RHINE'),
        'WPM':('B01','HANNOVER WESTPHALIA'),'WPD':('B01','WESTPHALIA'),'WPO':('B02','HANNOVER'),'LGE':('I01','WALLONIA FLANDERS'),
        'KMZ':('C02','HESSE FRANCONIA BADEN WURTTEMBERG'),'HEK':('C05','HESSE'),'HES':('C05','HESSE'),'WLD':('C05','HESSE'),'FRM':('C05','HESSE'),
        'NAS':('C04','HESSE'),'NOU':('C04','HESSE'),'NWB':('C04','HESSE'),'NSB':('C04','RHINELAND'),'FUL':('C04','HESSE SAXONY'),
        'ANS':('D01','FRANCONIA BAVARIA'),'WZB':('D01','FRANCONIA'),'FBM':('D01','FRANCONIA BAVARIA'),'NUR':('D01','FRANCONIA BAVARIA'),'EIC':('D01','FRANCONIA BAVARIA'),
        'WUR':('E01','WURTTEMBERG'),'BAD':('E01','BADEN'),'HOH':('E01','WURTTEMBERG'),'HSG':('E01','WURTTEMBERG BADEN'),'SUU':('E01','WURTTEMBERG'),
        'SFU':('E02','BADEN WURTTEMBERG'),'SEW':('E02','WURTTEMBERG FRANCONIA'),'SLM':('E03','BADEN'),'SKC':('E03','BADEN'),'SAG':('E01','BAVARIA'),
        'SKE':('E01','BAVARIA'),'SAC':('E04','BAVARIA'),'SKI':('E04','BAVARIA'),'SRT':('E04','WURTTEMBERG'),'SBI':('E04','WURTTEMBERG'),'SMM':('E04','WURTTEMBERG'),'SRQ':('E04','BADEN'),
        'SWW':('E03','WURTTEMBERG'),'SWF':('E03','WURTTEMBERG'),'SWX':('E03','WURTTEMBERG'),'SWY':('E03','WURTTEMBERG BAVARIA'),
        'BAV':('F04','BAVARIA FRANCONIA'),'PAS':('F01','BAVARIA'),'FSI':('F02','BAVARIA'),'RBI':('F03','BAVARIA'),'RCI':('F03','BAVARIA'),
        'LIP':('B06','WESTPHALIA'),'SCM':('B06','WESTPHALIA')}
    sector={r['ID']:r for r in rows}; entities=[]
    def entity(name,nature,holder,tag,sec,regions,source,historical='Établi pour la juridiction générale; contours non certifiés',rep=None,circle='À qualifier selon juridiction, pas State_ID',membership='Territoire impérial',oldline=None,exact_rgb=None):
        ss=sector[sec]; scope=['STATE_'+s for s in regions.split()]; active=[r['key'][0] for r in inv['owners'] if r['key'][2]==tag and r['key'][1] in scope]
        if exact_rgb is not None:active=[r for r in exact_rgb if any(o['key'][0]==r and o['key'][2]==tag for o in inv['owners'])]
        fact=facts.get(tag,{})
        representation=rep or ('NOYAU DISTINCT — POSSESSIONS OUVERTES' if tag and active else 'DISTINCTION NON REPRÉSENTÉE — DOSSIER À CONFIRMER')
        entities.append(dict(ID=f'J{len(entities)+1:03}',Secteur_ID=sec,Nom_historique=name,Nature_1776=nature,Titulaire_historique_1776=holder,Region_ou_cercle=circle,Appartenance_SERG=membership,TAG_actuel=tag,TAG_defini=tag in facts if tag else False,Proprietaire_actuel=tag if active else 'Non attribuable à la juridiction sans calage',RGB_identifies=';'.join(active),Portee_RGB='Possessions du TAG dans régions techniques indiquées, PAS un tracé certifié de cette juridiction' if active and exact_rgb is None else 'Noyau identifié / aucune limite inventée',Regions_techniques=';'.join(scope),Cellules_bitmap=sum(counts.get(c,0) for c in active),Representation=representation,Statut_couverture=ss['Statut'],Representation_schematique_acceptee=ss['Representation_schematique_acceptee'],Lot_ou_date=ss['Preuve'],Certitude_historique=historical,Certitude_geographique='Noyau politique schématique; pas cadastre' if active and ss['Statut'] in {V,I} else 'Non établie / périphéries ouvertes',Gouvernement_ecrit=';'.join(fact.get('government_law_declarations',[])) or ('Pas de déclaration directe; effets natifs/scripts non développés ici' if fact else 'Sans pays distinct identifié'),Dirigeant_ecrit=json.dumps(fact.get('rulers',[]),ensure_ascii=False),Population_actuelle_TAG_tous_territoires=sum(p['count'] for p in inv['regional_pop'] if p['key'][1]==tag) if tag else None,Problemes_restants=ss['Problemes_ouverts'],Source_historique=source,Preuve_mod=';'.join(fact.get('history',[])[:4]) or 'CURRENT_INVENTORY.json / COUNTRY_FACTS.json : pas de pays territorial distinct identifié',Inventaire_ancien=ref(BASE+'MAP2W/INVENTORY_1776.csv')+' ligne '+str(oldline) if oldline else 'Complément global de cet audit'))
    for number,r in enumerate(old,1):
        tag=corrections.get(number,r['TAG_actuel']); sec,regions=selected.get(tag,('B07','WESTPHALIA'))
        if number in (4,5,6,8):sec='B05';regions={4:'NORTH_RHINE',5:'RUHR WESTPHALIA',6:'WESTPHALIA',8:'RHINELAND NORTH_RHINE'}[number]
        if number==7:sec='B03';regions='HANNOVER'
        if number in (10,11):sec='B04';regions='WESTPHALIA'
        if number in (16,17):sec='B02';regions='HANNOVER'
        if 30<=number<=44 and not tag:sec='C05';regions='HESSE RHINELAND'
        if 51<=number<=57:sec='D02';regions='FRANCONIA WURTTEMBERG'
        if 80<=number<=85:sec='E05';regions='FRANCHE_COMTE WURTTEMBERG BAVARIA'
        if number in (91,92,93):sec='F04';regions='BAVARIA'
        if number==94:sec='F05';regions='AUSTRIA BAVARIA TYROL'
        name=r['Nom_FR'].replace('Wissembourg en Franconie','Weißenburg en Franconie');holder=r['Souverain_1776'];rep=None;source=r['Source_historique']
        if number in (6,16,17):rep='AGREGÉ PRU — IDENTIFICATION EXACTE DU SOUS-TERRITOIRE NON CERTIFIÉE'
        if number==48:rep='AGREGÉ SOUS SOUVERAIN COMMUN ANS — PAS UN PAYS ABSENT'
        if number==31:rep='APANAGE — AUCUN TAG SOUVERAIN AUTOMATIQUE'
        if number in (82,83,84,85,91):rep='ABSTRACTION CONSERVÉE — PAS DE TAG AUTOMATIQUE'
        if number in (87,88,89,90):source=ref(BASE+'MAP2W/R4/HISTORICAL_INVENTORY.md');holder={87:'Ludwig Joseph von Welden',88:'Leopold Ernst von Firmian',89:'Anton Ignaz von Fugger-Weißenhorn',90:'Conseil urbain; titulaire individuel non établi'}[number]
        if number in (92,94):rep='ABSENCE POLITIQUE DISTINCTE CONFIRMÉE';source=ref(BASE+'SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md')
        if number==94:holder='Hieronymus von Colloredo'
        if number in (51,54,55,56,57):rep='ABSENCE POLITIQUE DISTINCTE CONFIRMÉE';source=ref(BASE+'MAP2W/R3/HISTORICAL_EVIDENCE.md')
        if number==54:source='https://www.historisches-lexikon-bayerns.de/Lexikon/Schweinfurt,_Reichsstadt'
        if number==55:source='https://www.historisches-lexikon-bayerns.de/Lexikon/Rothenburg,_Reichsstadt'
        if number in (56,57):source='https://www.historisches-lexikon-bayerns.de/Lexikon/Städte_in_Franken_(Mittelalter/Frühe_Neuzeit)'
        if number==26:rep='ABSENCE POLITIQUE DISTINCTE CONFIRMÉE';source='https://www.dortmund.de/themen/dortmund-historisch/stadtgeschichte/18.-19.-jahrhundert/industriestadt/'
        circle='Franconien' if 45<=number<=57 else 'Souabe' if 58<=number<=85 else 'Bavarois' if number>=86 else 'Westphalien' if number in list(range(4,27)) and number not in (9,10,11) else 'Électoral rhénan' if number in (1,2,3,27) else 'Haut-Rhin / Westphalie selon possession; non homogène'
        nature=r['Nature_1776']
        if number in (35,36,37):nature='principauté distincte, noyau installé'
        if number==38:nature='possessions allemandes distinctes de Nassau-Orange'
        certainty='Établi pour la juridiction générale; contours non certifiés'
        if not tag and rep!='ABSENCE POLITIQUE DISTINCTE CONFIRMÉE':
            certainty='Piste de l’inventaire antérieur; branche, titulaire et souveraineté précise de 1776 non revérifiés ici'
        entity(name,nature,holder,tag,sec,regions,source,historical=certainty,rep=rep,circle=circle,oldline=number+1)
    extras=[
      ('Prince-évêché de Lübeck (Eutin–Schwartau)','principauté épiscopale luthérienne','Friedrich August','HLB','A02','SCHLESWIG_HOLSTEIN','MAP2Q/R3/REPORT.md'),
      ('Ville impériale de Lübeck','ville impériale','Magistrat','LUB','A03','SCHLESWIG_HOLSTEIN POMERANIA','MAP2Q/REPORT.md'),
      ('Hambourg','ville impériale','Sénat','HAM','A03','ELBE','MAP2K/MAP2K_EXECUTIVE_SUMMARY.md'),
      ('Brême','ville impériale','Sénat','BRE','A03','ELBE','MAP2K/MAP2K_EXECUTIVE_SUMMARY.md'),
      ('Holstein royal','duché impérial sous couronne danoise','Christian VII','HOL','A01','SCHLESWIG_HOLSTEIN','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Mecklembourg-Schwerin','duché','Titulaire non revalidé ici','MEC','A05','MECKLENBURG','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Mecklembourg-Strelitz','duché','Titulaire non revalidé ici','MST','A05','MECKLENBURG','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Wismar, Poel, Neukloster','possessions impériales de la couronne suédoise','Gustave III','SWE','A04','MECKLENBURG POMERANIA','MAP2N/REPORT.md'),
      ('Poméranie suédoise','duché impérial','Gustave III','SWE','A06','POMERANIA','MAP2M/R9/REPORT.md'),
      ('Poméranie prussienne','duché impérial','Frédéric II','PRU','A06','POMERANIA','MAP2M/R9/REPORT.md'),
      ('Brandebourg et Neumark','électorat','Frédéric II','PRU','A07','BRANDENBURG','MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md'),
      ('Magdebourg et Halberstadt','possessions prussiennes impériales','Frédéric II','PRU','A07','ANHALT BRUNSWICK','MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md'),
      ('Brunswick-Lunebourg (Hanovre)','électorat','George III','HAN','A08','HANNOVER BRUNSWICK ELBE','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Brunswick-Wolfenbüttel','principauté','Titulaire non revalidé ici','BRA','A08','BRUNSWICK','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Oldenbourg et Delmenhorst','comtés élevés en duché; domaines séparés d’Eutin','Friedrich August','OLD','A08','HANNOVER','MAP2Q/REPORT.md'),
      ('Frise orientale : Emden','comté prussien impérial','Frédéric II','PRU','B08','HANNOVER','MAP2P/REPORT.md'),
      ('Jever','seigneurie sous Anhalt-Zerbst','Friedrich August d’Anhalt-Zerbst','AZR','B09','HANNOVER','MAP2S/JEVER_HISTORICAL_EVIDENCE.md'),
      ('Stavelot-Malmedy','abbaye princière','Titulaire non revalidé ici','STM','I01','WALLONIA','MAP2L/BELGIUM/IMPLEMENTATION.md'),
      ('Pays-Bas autrichiens : Brabant, Flandre, Hainaut, Namur','ensemble de provinces distinctes','Marie-Thérèse','BEO','I01','WALLONIA FLANDERS GELRE','MAP2L/BELGIUM/IMPLEMENTATION.md'),
      ('Luxembourg','duché habsbourgeois','Marie-Thérèse','BEO','I02','WALLONIA','LUX_BEO_INTEGRATION_2026-10-10/REPORT.md'),
      ('Saxe électorale','électorat','Friedrich August III','SAX','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Saxe-Gotha-Altenbourg','duché','Ernst II','GOT','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Saxe-Hildburghausen','duché','Ernst Friedrich III','HIL','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Saxe-Cobourg-Saalfeld','duché','Ernst Friedrich','COB','G02','SAXONY FRANCONIA','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Saxe-Meiningen','duché','Régence; titulaires à relire dans dossier T','MEI','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Saxe-Weimar-Eisenach','deux duchés sous même souverain','Carl August','WEI','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Schwarzbourg-Rudolstadt','principauté','Titulaire à vérifier dans dossier T','SCW','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Schwarzbourg-Sondershausen','principauté','Christian Günther III','SSO','G03','SAXONY ANHALT','MAP2U/HISTORICAL_EVIDENCE.md'),
      ('Reuss-Greiz','comté, pas principauté avant 1778','Heinrich XI','RGZ','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Reuss-Gera','comté','Titulaire à vérifier dans dossier T','RGE','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Reuss-Schleiz','comté','Titulaire à vérifier dans dossier T','RSL','G02','SAXONY','MAP2T/HISTORICAL_EVIDENCE.md'),
      ('Reuss-Lobenstein','comté','Heinrich II','RLO','G03','SAXONY','MAP2U/HISTORICAL_EVIDENCE.md'),
      ('Reuss-Ebersdorf','comté','Heinrich XXIV','REB','G03','SAXONY','MAP2U/HISTORICAL_EVIDENCE.md'),
      ('Anhalt-Dessau','principauté','Leopold Friedrich Franz','ANH','G01','ANHALT','MAP2R/HISTORICAL_EVIDENCE.md'),
      ('Anhalt-Bernbourg','principauté','Friedrich Albrecht','ABG','G01','ANHALT','MAP2R/HISTORICAL_EVIDENCE.md'),
      ('Anhalt-Köthen','principauté','Karl Georg Lebrecht','AKT','G01','ANHALT','MAP2R/HISTORICAL_EVIDENCE.md'),
      ('Anhalt-Zerbst','principauté','Friedrich August','AZR','G01','ANHALT','MAP2R/HISTORICAL_EVIDENCE.md'),
      ('Bohême','royaume électoral','Marie-Thérèse; Joseph II empereur distinct','AUS','H01','BOHEMIA','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Moravie','margraviat de la Couronne de Bohême','Marie-Thérèse','AUS','H02','MORAVIA','MAP2A/MAP2A_EXECUTIVE_SUMMARY.md'),
      ('Silésie autrichienne (Opava/Teschen)','duchés de la Couronne de Bohême','Marie-Thérèse','AUS','H02','MORAVIA WEST_GALICIA','MAP2A/MAP2A_EXECUTIVE_SUMMARY.md'),
      ('Silésie prussienne et Glatz','duchés et comté impériaux sous PRU','Frédéric II','PRU','H03','LOWER_SILESIA UPPER_SILESIA','MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/SILESIA_READING.md'),
      ('Haute et Basse Autriche','archiduchés','Marie-Thérèse','AUS','H04','AUSTRIA','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Styrie','duché','Marie-Thérèse','AUS','H04','STYRIA','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Carinthie','duché; ne correspond pas à un State_ID autonome ici','Marie-Thérèse','AUS','H04','STYRIA TYROL SLOVENIA','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Carniole','duché','Marie-Thérèse','AUS','H04','SLOVENIA','MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Tyrol','comté princier','Marie-Thérèse','AUS','H05','TYROL SOUTH_TYROL','MAP2A/MAP2A_EXECUTIVE_SUMMARY.md'),
      ('Trente','principauté épiscopale','Cristoforo Sizzo de Noris au 1 janvier; ne pas anticiper Thun plus tard en 1776','','H05','SOUTH_TYROL','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Brixen / Bressanone','principauté épiscopale','Titulaire non revalidé ici','','H05','TYROL SOUTH_TYROL','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Autriche antérieure','ensemble territorial dispersé','Marie-Thérèse','AUS','H06','BADEN WURTTEMBERG BAVARIA','MAP2L/SWABIA/REPORT.md'),
      ('Gorizia, Trieste et possessions adriatiques','possessions habsbourgeoises; frontières impériales à auditer','Marie-Thérèse','AUS','H06','ISTRIA','MAP2A/MAP2A_EXECUTIVE_SUMMARY.md'),
      ('Milan et Mantoue','duchés impériaux sous souveraineté habsbourgeoise','Marie-Thérèse','AUS','J01','LOMBARDY','MAP2L/MILAN_CREMONESE/REPORT.md'),
      ('Piémont','principauté dans monarchie sarde','Victor-Amédée III','SAR','J02','PIEDMONT','MAP2L/PIEDMONT/REPORT.md'),
      ('Savoie et Nice','domaines de la monarchie sarde; statut impérial à qualifier','Victor-Amédée III','SAR','J03','SAVOY PROVENCE','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Modène et Reggio','duchés impériaux','Francesco III d’Este','MOD','J04','EMILIA','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Parme et Plaisance','duchés; statut féodal précis à documenter','Ferdinand de Bourbon','PAR','J04','EMILIA','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Toscane','grand-duché; ne pas assimiler à toute Italie impériale','Pietro Leopoldo','TUS','J04','TUSCANY','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Liechtenstein (Vaduz–Schellenberg)','principauté immédiate','Titulaire non revalidé ici','','K02','TYROL SWITZERLAND','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Principauté épiscopale de Hildesheim','principauté ecclésiastique','Titulaire non revalidé ici','','A08','HANNOVER BRUNSWICK','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Goslar','ville impériale; Rammelsberg distinct depuis 1552','Magistrat','','A08','BRUNSWICK HANNOVER','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Quedlinburg','abbaye immédiate; protection prussienne à distinguer de souveraineté','Abbesse non revalidée ici','','A08','ANHALT BRUNSWICK','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('République de Lucques','république; pas principauté napoléonienne','Institutions républicaines','LUC','J04','EMILIA','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('République de Gênes et fiefs ligures','république; statut de chaque fief impérial à qualifier','Institutions républicaines','GEN','J03','PIEDMONT','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv'),
      ('Massa et Carrare','duché et principauté individualisés; dépendance dynastique à arbitrer','Maria Teresa Cybo-Malaspina','','J04','EMILIA TUSCANY','SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md'),
      ('Piombino','principauté distincte de Toscane; souverainetés d’Elbe séparées','Maison Boncompagni-Ludovisi','','J04','TUSCANY','MAP1/inputs/regional_originals/R1_WESTERN_EUROPE_RECOMMENDATIONS.csv'),
    ]
    for name,nature,holder,tag,sec,regions,source in extras:
        rep='ABSENCE POLITIQUE DISTINCTE CONFIRMÉE' if name in ('Trente','Brixen / Bressanone','Principauté épiscopale de Hildesheim','Goslar') else 'ABSTRACTION À ARBITRER — PAS DE TAG AUTOMATIQUE' if not tag else None
        circle={'A':'Bas-Saxon / Haut-Saxon selon territoire','G':'Haut-Saxon','H':'Autrichien; Bohême/Moravie/Silésie hors cercles','I':'Bourguignon ou Westphalien selon principauté','J':'Hors cercles; Savoie à qualifier','K':'Souabe pour Liechtenstein; cas non cerclés distincts'}.get(sec[0],'Westphalien')
        exact=['xF9DCA2'] if sec=='B08' else ['xD001A0'] if sec=='I02' else ['xEDB100','xEDB101','xEDB102','xEDB103','xEDB104','xEDB105'] if sec=='A04' else None
        entity(name,nature,holder,tag,sec,regions,ref(BASE+source),rep=rep,circle=circle,exact_rgb=exact,membership='Portée impériale à qualifier territoire par territoire; pas déduite du TAG' if sec in ('J03','J04') else 'Territoire impérial')
    for r in entities:
        if r['Nom_historique']=='Jever':
            r['Proprietaire_actuel']='OLD dans les enveloppes candidates; intersection historique non résolue'
        if r['Statut_couverture']==N:r['Certitude_historique']='Contexte macro; statut territorial et titulaires non audités de façon suffisante'
        if ' ligne ' in r['Inventaire_ancien']:
            row=r['Inventaire_ancien'].rsplit(' ligne ',1)[1]
            r['Inventaire_ancien']=BASE+'MAP2W/INVENTORY_1776.csv:'+row
        if r['Nom_historique'] in ('Ansbach','Bayreuth'):
            r['Portee_RGB']='Possessions agrégées ANS; cette colonne ne sépare pas les deux margraviats ni leurs populations'
    save('ENTITY_DATA.json',entities)
    print('Regional rows',len(rows),'entity rows',len(entities))
if __name__=='__main__': build()
