"""Additive B05 evidence and WORLD tracking. No gameplay, SERG or Git writes."""
import ast
import json
import shutil
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
import world1776_balkans05 as b

DATE='2026-10-26'
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def main():
    v=b.load('VALIDATION.json');assert v['status']=='PASS'
    before=b.load('APPLY_BASELINE.json');entry=b.load('BASELINE.json');con=b.load('CONCURRENT_CHANGES.json')
    tech=b.load('TECH_AFTER.json')[0];receipt=b.load('FILES_MODIFIED.json')
    assert not (b.LOT/'DELIVERY_MANIFEST.json').exists(),'Already closed; preserve this receipt.'
    original={name:(b.OUT/name).read_bytes() for name in TRACK}
    for name,data in original.items():
        p=b.LOT/'closeout_inputs'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    def doc(name,text):(b.LOT/name).write_text(text.strip()+'\n',encoding='utf8')
    def append(name,title,text):
        current=(b.OUT/name).read_bytes();assert current==original[name],name+' changed concurrently'
        (b.OUT/name).write_text(current.decode('utf8').rstrip()+'\n\n## '+title+'\n\n'+text.strip()+'\n',encoding='utf8')
    changed=con['entry_to_apply_observed']['SERG_proofs']
    external=[]
    for e in changed:
        dest=b.LOT/'external_reference'/e['file'];dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(b.ROOT/e['file'],dest)
        assert b.b.a.sha(dest)==e['at_apply']==b.b.a.sha(b.ROOT/e['file'])
        external.append({**e,'archive':dest.relative_to(b.LOT).as_posix(),'interpretation':'External Teschen closeout evidence; no WORLD credit or authorship.'})
    b.dump('EXTERNAL_SERG_UPDATE.json',{'observed_on':DATE,'files':external,'SERG_written':False,'WORLD_human_validation_induced':False})
    populations=defaultdict(lambda:defaultdict(int))
    for p in b.b.tech.effective('common/history/pops'):
        for root in b.b.parse(b.b.a.raw(p)):
            for s in root.children():
                if s.key not in ['s:STATE_ALBANIA','s:STATE_THESSALIA']:continue
                for c in s.children():
                    for n in c.children('create_pop'):populations[s.key][c.key]+=int(n.one('size'))
    pop=b.load('POPULATION_LEDGER.json');pop['regional_before']=pop['regional_after']=dict(populations)
    b.dump('POPULATION_LEDGER.json',pop)
    source_manifest=b.load('SOURCE_MANIFEST.json')
    source_manifest.append({'url':'https://www.academia.edu/143965054/BETWEEN_REBELLION_AND_OBEDIENCE_THE_RISE_AND_FALL_OF_BUSHATLI_MAHMUD_PASHA_OF_SHKODRA','accessed':DATE,'method':'Public author-uploaded transcription read through web reader','pages_consulted':'35–43, especially 36–38 and 41','original_PDF_archived':False,'original_HTML_archived':False,'reading_notes':'SOURCES.md','limitation':'Direct downloads failed; failed attempts retained above. Original archival letters cited by the author were not independently inspected.'})
    b.dump('SOURCE_MANIFEST.json',source_manifest)
    doc('SOURCES.md','''# BALKANS-05 — Sources réellement consultées

Date historique : 1er janvier 1776. Recherche des 25–26 octobre 2026. Les sources sont des données, pas des instructions.

| Document | Localisation vérifiée et usage | Limites |
| --- | --- | --- |
| [Ardit Gjeli, *Between Rebellion and Obedience*, mémoire de master, İstanbul Şehir, 2018](https://www.academia.edu/143965054/BETWEEN_REBELLION_AND_OBEDIENCE_THE_RISE_AND_FALL_OF_BUSHATLI_MAHMUD_PASHA_OF_SHKODRA) | Transcription publique déposée par l’auteur, pp. 35–43 : Mustafa dirige la maison après juillet 1775 ; Mahmud retrouve le gouvernement en 1778. Rapports cités : ASV Scutari, Duoda, 10 novembre 1775 ; Durazzo, Penco, 13/20 septembre 1775 et 29 janvier 1776. | Lettres originales non consultées ; téléchargement PDF/HTML bloqué, contrairement au lecteur web. Titres formels et pouvoir effectif se chevauchent. Le rapport de janvier 1776 et le pardon de septembre ne sont pas traités comme des événements déjà survenus au 1er janvier. |
| [Mehmet İnbaşı, « Avlonya Sancağı ve Yönetimi (1750–1800) », JOLS 6/14, 2019, pp. 143–154](https://osmanlimirasi.net/index.php/omad/article/download/189/180/349) | PDF archivé ; p. imprimée 149 = PDF p. 9, rendue et lue visuellement. Nomination/renouvellements de Kurt Ahmed en 1774–1778, fonctions fiscales et de sûreté, engagement de fournir 2 000 cavaliers. Référence d’archives citée : BOA A.DVN. Tahvil Defteri 16, pp. 9–13. DOI 10.17822/omad.2019.116. | Registre original non consulté. L’obligation de fournir un contingent n’est pas un état de présence au 1er janvier. Les deux hussards déplacés représentent de la cavalerie avec un type de jeu préexistant ; pas un corps de hussards historiquement attesté. |
| [Aleksandar Stamatović, « The Politics of Kara Mahmud Pasha Bushati Towards Montenegro in the 1780s », JOLS 9/25, 2022, pp. 485–501](https://osmanlimirasi.net/index.php/omad/article/download/140/135) | PDF archivé ; p. 486 / PDF p. 4 relue. Présente les chronologies concurrentes et les limites des récits anciens. DOI 10.17822/omad.2022.224. | Les campagnes des années 1780 ne prouvent pas la possession de MON en 1776. La chronologie consulaire de Gjeli est retenue pour le chef de maison ; aucune origine Crnojević supposée n’est installée. |
| [Kemal Beydilli, « Tepedelenli Ali Paşa », TDV İslâm Ansiklopedisi, 2011](https://islamansiklopedisi.org.tr/tepedelenli-ali-pasa) | Notice HTML archivée et relue : première nomination à Yanya en 1784–1785 annulée, prise effective mentionnée en janvier 1787. | Cette notice ne dit pas que la prise de Yanya a lieu en 1776, ni en 1788. Elle situe la mort de Kurt Ahmed en 1784, alors qu’İnbaşı relève des renouvellements jusqu’en 1787 : divergence conservée, sans événement de décès inventé. |

Le rendu de contrôle İnbaşı est temporaire dans `.asset-cache/BALKANS-05/inbasi_p09.png`. Les téléchargements réussis, leurs empreintes et les échecs HTTP sont dans SOURCE_MANIFEST.json. Les anciens dossiers MAP1 servent de pistes ; leurs attributions ne remplacent pas le workspace actuel.

## Décision politique et approximation

Scutari et Berat/Avlonya sont des pouvoirs provinciaux enracinés dans leurs alliances, avec des rapports négociés à la Porte. L’appartenance TUR conservée est une représentation agrégée de souveraineté ; elle ne certifie pas une administration centrale uniforme. Deux formations et deux titulaires rendent les maisons visibles. Cette solution n’implémente pas leur autonomie fiscale, leurs conflits internes ni leurs frontières particulières. Aucun TAG national albanais moderne, domaine futur d’Ali ou arrière-pays vénitien inventé.

Les âges 40 et 55 sont des calibrations de génération imposées aux personnages de jeu, non des années de naissance établies. Culture, religion, groupe des propriétaires et idéologie traditionaliste sont des représentations qualitatives, sans bonus personnel ajouté. Les effectifs des deux maisons sont prélevés sur les effectifs techniques antérieurs, pas tirés d’un recensement militaire.
''')
    protected=len(before['gameplay'])-1;serg=len(before['SERG_proofs']);prior=len(before['prior_WORLD_proofs'])
    doc('REPORT.md',f'''# BALKANS-05 — Albanie et Épire ottomanes

Livraison : 26 octobre 2026. Référence : 1er janvier 1776.
Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Recherche régionale : INCOMPLETE. Moteur : NOT_RUN. Nouvelle validation joueur : 0.

## Corrections installées

Deux maisons provinciales deviennent visibles dans les forces ottomanes : **Mustafa Bushati**, chef de la maison de Scutari, et **Ahmed Kurt**, mutasarrıf d’Avlonya. Deux traits d’office sans bonus et leurs textes français/anglais accompagnent les personnages. Les offices représentent leurs fonctions ; les généraux et formations sont une approximation du moteur, pas des gouvernements autonomes complets.

| Formation | Installation | Origine des unités |
| --- | --- | --- |
| Maison de Scutari | Mustafa Bushati, 2 bataillons réguliers d’infanterie irrégulière | Les 2 déjà présents dans l’armée de Roumélie, STATE_ALBANIA |
| Contingent d’Avlonya | Ahmed Kurt, 2 bataillons réguliers de cavalerie du type hussards | 2 des 4 déjà présents dans cette même armée/région ; 2 y restent |

**4 bataillons réaffectés, zéro ajouté ou supprimé.** Tous les effectifs mondiaux par pays, région, type et service sont identiques. Les conscrits, flottes, anciennes formations et affectations des anciens commandants sont conservés. Deux commandants supplémentaires sont créés : leur rémunération éventuelle, la composition de l’armée de cavalerie et leur comportement restent à observer au test groupé ; aucune gratuité budgétaire n’est affirmée.

## Cellules, frontières et populations

**Zéro cellule/RGB changé, zéro nouveau TAG, zéro transfert démographique.** Toutes les attributions existantes sont conservées. Les postes vénitiens B04 — xE8D211 Butrinto, xE8D212 Parga, xE8D213 Prévéza, xE8D214 Vonitsa — ainsi que Cérigo xE8D215, les anciennes Ioniennes, MON, RAG et les passages adriatiques restent identiques. Aucun tracé administratif des maisons n’est prétendu résolu.

| Périmètre technique | Avant | Après |
| --- | ---: | ---: |
| STATE_ALBANIA, portion TUR | 1 073 901 | 1 073 901 |
| STATE_ALBANIA, portion VEN | 500 | 500 |
| STATE_THESSALIA, portion TUR | 958 024 | 958 024 |
| STATE_THESSALIA, portion VEN | 4 700 | 4 700 |
| Monde | 834 936 539 | 834 936 539 |

Ces totaux sont ceux du scénario technique actuel ; cette passe ne les certifie pas comme des dénombrements de 1776. Tous les fichiers de POPs sont identiques, donc leurs ventilations également. Les régions natives ne sont pas assimilées aux limites historiques d’une province ottomane ou de l’Épire.

## Institutions, technologies et économie

L’appartenance TUR est conservée sans nier l’autorité effective des maisons locales. Aucune loi, succession impériale, relation diplomatique, fiscalité provinciale, ressource, bâtiment, recette ou PM n’est changé. L’autorité fiscale, les clans et les autres juridictions d’Épire restent une obligation régionale. Aucun gouvernement futur d’Ali Pacha n’est installé.

Les **23 technologies effectives TUR** sont identiques. L’audit commun avant/après reste FAIL_STATIC avec les mêmes trois observations : technologie de recrutement horse_artillery manquante pour les hussards déjà présents ; avertissement de ressource régionale à Diyarbakır ; profil historique impérial non certifié. L’infanterie irrégulière n’a pas de gate technologique. La réaffectation n’introduit aucun type d’unité ou constat nouveau, mais le recrutement des hussards reste restreint et leur fonctionnement initial n’est pas prouvé. **Aucun crédit T** ni grant automatique pour masquer cette dette.

## Sources et incertitudes

Le choix des titulaires est motivé dans SOURCES.md : travaux de Gjeli fondés sur les rapports consulaires, registre de nominations analysé par İnbaşı, comparaison avec Stamatović et notice TDV d’Ali. La direction effective de Scutari est distinguée du titre nominal. Les juridictions précises, dates de naissance, effectifs réellement présents et recrutement local restent incertains. Âges techniques : Mustafa 40, Ahmed 55 ; pas de naissance prétendument vérifiée. Les 2 000 cavaliers mentionnés par İnbaşı sont une obligation, pas un recensement de garnison. La divergence sur le décès ultérieur d’Ahmed Kurt est conservée.

## Contrôles, concurrence et progression

**{v['passed']}/{v['total']} contrôles statiques réussis**, après correction d’une différence de représentation tuples/listes dans le comparateur de preuves. La première trace 50/52 est conservée dans VALIDATION_RUN01.json ; aucun script du jeu n’a été changé pour résoudre ces deux faux écarts. L’audit technologique impérial reste explicitement en échec hérité, distinct du contrôle de non-régression du lot.

Un seul fichier partagé est retouché dans deux nœuds d’unités ; quatre fichiers spécifiques sont nouveaux. Les {protected} fichiers fonctionnels antérieurs hors patch sont identiques à la capture d’application ; {prior} preuves des lots WORLD précédents sont préservées. Les {serg} preuves SERG présentes à l’application restent identiques. Entre l’entrée de recherche et l’application, {len(changed)} documents SERG avaient évolué avec la clôture externe de Teschen ; copies courantes et empreintes archivées dans EXTERNAL_SERG_UPDATE.json. Aucun crédit humain WORLD n’en découle.

TECH-R1/R2/R3, ECON-ALLOYS/quincaillerie, fortifications/génie et autres travaux concurrents sont préservés. Aucune écriture Git, vanilla ou suivi SERG ; aucune ancienne baseline restaurée.

Seul **S de P1-05** reçoit un point : **10/80 Balkans (12,50 %) ; 10/320 WORLD (3,125 % exacts)**. O/I/D/E/T/R restent partiels, V non commencé. Aucun territoire ni région clos. Prochaine candidate : **BALKANS-06 — Grèce continentale, Péloponnèse et Crète**. Test balkanique groupé à la fin du travail techniquement réalisable ; aucune autre région avant confirmation explicite.
''')
    doc('TEST_MATRIX.md',f'''# B05 — Tests exécutés et limites

- `python tools/validate_starting_technology_1776.py --tag TUR --output .../TECH_BEFORE.json` : sortie 1, FAIL_STATIC, trois constats préexistants.
- `python tools/world1776_balkans05.py --apply` : installation unique bornée avec empreinte immédiatement avant écriture ; refuse une seconde application.
- Même audit vers TECH_AFTER.json : sortie 1, trois constats identiques, aucun nouveau type ou grant.
- `python tools/world1776_balkans05.py --validate` : première exécution 50/52, deux différences tuples/listes dans le comparateur ; preuve brute conservée. Après normalisation JSON du comparateur, **{v['passed']}/{v['total']}**, sortie 0.

Contrôles : reconstruction exacte des cinq fichiers, extérieur de TUR identique, effectifs mondiaux par pays/région/type/service, anciennes formations/personnages/affectations, références, scopes sans collision, traits sans bonus, ressources d’interface natives, clés FR/EN uniques avec BOM, propriétaires et POPs inchangés, empreintes hors lot et anciennes preuves, état Git identique, constats technologiques avant/après identiques.

Limites : aucun moteur lancé, aucune assertion de budget ou de contrôle administratif effectif. Le contrat technologique FAIL_STATIC n’est pas renommé PASS ; son absence d’aggravation est la seule assertion correspondante du lot. Aucun test hérité ni reçu humain n’est réécrit.
''')
    doc('GROUPED_RUNTIME_ITEMS.md','''# B05 — À intégrer au test balkanique final

NOT_RUN ; aucune demande de test intermédiaire, aucune attestation.

1. Nouvelle partie TUR en 1776 : deux formations distinctes, bons noms et titulaires ; traits d’office localisés ; anciens commandants conservés.
2. Comparer le total national, les rattachements STATE_ALBANIA et les réserves ; les quatre bataillons ont changé d’affectation seulement. Observer la formation de cavalerie et les possibilités de regroupement.
3. Vérifier la restriction de recrutement des hussards héritée et leur présence effective ; ne pas confondre recrutement futur et fonctionnement initial. Contrôler coût des deux commandants, mobilisation, entretien et marché pendant un mois.
4. Contrôler les postes vénitiens, Cérigo, RAG et MON comme témoins ; joindre les obligations B01–B04 au protocole consolidé.
5. Sauvegarder/recharger : noms, traits, affectations et effectifs persistants ; relever les erreurs réellement observées.

L’autonomie fiscale, les limites locales et une population historique reconstituée ne sont pas installées par cette représentation. Aucune autre région WORLD avant confirmation du test balkanique groupé.
''')
    state=json.loads(original['ROADMAP_STATE.json']);score=sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values());assert score==9
    region=next(r for r in state['phases'][0]['subregions'] if r['id']=='P1-05')
    remaining={'O':'Frontières conservées ; juridictions provinciales et contrôle fin non clos.','I':'Deux maisons identifiées, représentation par officiers ; autonomie fiscale, autres titulaires et clans incomplets.','D':'Conservation technique démontrée ; démographie historique non reconstituée.','E':'Bâtiments/PM/ressources conservés ; budget des commandants et économie provinciale non simulés.','T':'Trois constats TUR préexistants, dont le gate horse_artillery des hussards ; aucune incompatibilité nouvelle.','R':'Quatre bataillons réaffectés ; effectifs historiques et obligations complètes non certifiés.'}
    for k,reason in remaining.items():region['criteria'][k]={'status':'PARTIAL','evidence':'BALKANS-05/REPORT.md','remaining':reason}
    region['criteria']['S']={'status':'STATIC_VERIFIED','evidence':'BALKANS-05/VALIDATION.json','runtime':'NOT_RUN','scope':'Bounded household representation and conservation only; pre-existing tech debt reported separately, no regional historical closure.'}
    region['criteria']['V']={'status':'NOT_STARTED','evidence':'BALKANS-05/GROUPED_RUNTIME_ITEMS.md','test_timing':'END_OF_BALKANS'}
    state['lots'].append({'id':'BALKANS-05','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','scope':['Scutari household under Mustafa Bushati','Avlonya contingent under Ahmed Kurt','Ottoman framework retained; no territorial transfer'],'runtime':'NOT_RUN','test_timing':'END_OF_BALKANS','files_modified':5,'new_RGBs':0,'new_tags':0,'pixels_recolored':0,'people_transferred':0,'world_population_delta':0,'units_reassigned':4,'new_generals':2,'receipt':'BALKANS-05/FILES_MODIFIED.json','protocol':'BALKANS-05/GROUPED_RUNTIME_ITEMS.md','historical_research_status':'REGION_INCOMPLETE'})
    def percent(n,d):return float((Decimal(n)*100/Decimal(d)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))
    for phase in state['phases']:
        n=sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values());phase['progress']['technical_verified']=n;phase['progress']['technical_percent']=percent(n,phase['progress']['criteria_total'])
    state['progress']['technical_verified']=sum(p['progress']['technical_verified'] for p in state['phases']);state['progress']['technical_percent']=percent(10,320)
    assert state['progress']['technical_verified']==10 and state['progress']['runtime_user_validated']==0
    assert (b.OUT/'ROADMAP_STATE.json').read_bytes()==original['ROADMAP_STATE.json']
    (b.OUT/'ROADMAP_STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    title='BALKANS-05 — '+DATE
    append('ROADMAP.md',title,'Maisons de Scutari et d’Avlonya installées dans le cadre TUR, quatre bataillons réaffectés, aucun changement de carte/POPs. Un seul point S : 10/80 Balkans (12,50 %), 10/320 WORLD (3,125 % exacts ; 3,13 % arrondis), zéro nouvelle validation joueur. T reste partiel : dette de recrutement des hussards préexistante, pas de grant. Rapport BALKANS-05/REPORT.md ; prochaine candidate BALKANS-06 Grèce continentale, Péloponnèse et Crète. Aucune sortie des Balkans sans confirmation du test groupé.')
    append('PROGRESS_HISTORY.md',title,f'Entrée recalculée 9/80 et 9/320. Cinq fichiers fonctionnels : un patch partagé de deux nœuds et quatre nouveaux fichiers propres. Mustafa Bushati à Scutari, Ahmed Kurt à Avlonya ; deux officiers supplémentaires et traits d’office sans bonus. Quatre bataillons existants déplacés depuis Roumélie ; effectifs par pays/région/type/service conservés. Zéro cellule, TAG ou POP transféré ; monde 834 936 539 identique. Pas de domaine futur d’Ali Pacha.\n\n{v["passed"]}/{v["total"]} contrôles statiques, trace initiale 50/52 et correction de sérialisation du comparateur conservées. Audit technologique TUR FAIL_STATIC avant/après, trois constats identiques ; aucun point T. {protected} fichiers fonctionnels hors lot et {prior} preuves WORLD préservés ; {len(changed)} documents SERG externes actualisés avant application, archivés sans validation WORLD induite. Aucune écriture Git/vanilla/SERG.\n\n+1 S de P1-05 seulement : 10/80 (12,50 %), 10/320 (3,125 % exacts), zéro reçu humain nouveau. Institutions et autonomie, démographie, économie et limites fines restent incomplètes. Prochaine candidate B06 ; aucun test intermédiaire ni autre région avant confirmation du test balkanique groupé.')
    append('BLOCKERS.md',title,'Les maisons sont rendues visibles sans simuler une autonomie fiscale ou toutes leurs juridictions. Titres nominaux et autorité effective à Scutari doivent rester distingués ; âges techniques 40/55 non sourcés comme naissances exactes. Contingents repris des données de jeu, pas recensement militaire. Limites, autres titulaires d’Épire, clans, budgets et contrôle effectif ouverts. Dates ultérieures d’Ahmed Kurt divergentes entre İnbaşı et TDV, aucun décès programmé.\n\nTUR : gate horse_artillery des hussards préexistant, avertissement régional cuivre à Diyarbakır et profil historique impérial non certifié. Ni grant commun ni recette retouchés ; pas de point T. Les deux commandants ajoutés et la formation de cavalerie attendent le test groupé. Toutes les obligations B01–B04 restent ouvertes ; aucune validation humaine déduite des tests statiques.')
    append('OWNERSHIP_BOUNDARIES.md',title,'Périmètre d’écriture : dans c:TUR du fichier militaire du Moyen-Orient, seuls le compte des hussards de rumeli_ordusu (4→2) et son nœud de deux fantassins irréguliers sont modifiés. Quatre fichiers propres ajoutent les deux maisons, leurs chefs, deux traits d’office et FR/EN. Aucun autre pays ou officier national modifié ; effectifs par région/type/service conservés.\n\nAucun RGB, souveraineté, POP, bâtiment, PM, technologie, recette, loi ou relation diplomatique écrit. Préserver les postes vénitiens et Cérigo B04, RAG, MON et tous les territoires SERG. Trois preuves SERG avaient changé extérieurement avant application ; référence dans B05/EXTERNAL_SERG_UPDATE.json, aucune écriture de leur suivi.')
    assert (b.OUT/'NEXT_ACTION.md').read_bytes()==original['NEXT_ACTION.md']
    (b.OUT/'NEXT_ACTION.md').write_text('''# Prochaine candidate WORLD — BALKANS-06

**Grèce continentale, Péloponnèse et Crète**, référence 1er janvier 1776, P1-06. B05 installé et vérifié statiquement : BALKANS-05/REPORT.md et DELIVERY_CHECKS.json. Candidate seulement ; ne constitue pas une nouvelle mission automatique.

À la prochaine autorisation, reprendre les juridictions et autorités ottomanes, l’après-Orlov et les troupes albanaises en Morée, les autorités et autonomies locales et les institutions crétoises. Éviter les dirigeants et frontières des indépendances ultérieures. Choisir un lot P0/P1 cohérent à partir du workspace courant, pas d’une baseline ancienne.

Préserver les postes vénitiens B04 et Cérigo, les Ioniennes existantes, les maisons B05, MON/RAG, les interfaces SERG et les travaux TECH/ECON. Relire suivi, preuves, concurrence et empreintes. Aucun Git d’écriture, vanilla ou suivi SERG.

B05 reste incomplet : autonomie fiscale/frontières locales, autres titulaires d’Épire, démographie et budgets ; gate préexistant horse_artillery des hussards. Obligations B01–B04 toujours ouvertes. Aucun point T pour B05.

Progression calculée : **10/80 Balkans (12,50 %) ; 10/320 WORLD (3,125 % exacts, 3,13 % arrondis)** ; zéro nouvelle validation joueur. Seul S de P1-05 est ajouté.

Test joueur groupé à la fin du travail balkanique techniquement réalisable, avec les protocoles B01–B05 et obligations restantes. Aucun test intermédiaire demandé. Aucune autre région avant confirmation explicite ; aucune attestation humaine fictive.
''',encoding='utf8')
    concurrent=json.loads(original['CONCURRENT_CHANGES.json']);concurrent['BALKANS-05']={'receipt':'BALKANS-05/CONCURRENT_CHANGES.json','protected_gameplay_unchanged':protected,'SERG_proofs_unchanged_since_apply':serg,'SERG_external_documents_before_apply':len(changed),'external_receipt':'BALKANS-05/EXTERNAL_SERG_UPDATE.json','prior_WORLD_proofs_unchanged':prior,'SERG_writes':0,'git_writes':0,'vanilla_writes':0,'new_RGBs':0,'world_population_delta':0}
    assert (b.OUT/'CONCURRENT_CHANGES.json').read_bytes()==original['CONCURRENT_CHANGES.json']
    (b.OUT/'CONCURRENT_CHANGES.json').write_text(json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    b.dump('PROGRESS_CALCULATION.json',{'entry':{'Balkans':9,'WORLD':9},'credited':['P1-05/S'],'not_credited':['P1-05/O','P1-05/I','P1-05/D','P1-05/E','P1-05/T','P1-05/R','P1-05/V'],'Balkans':state['phases'][0]['progress'],'WORLD':state['progress'],'rounding':'Decimal ROUND_HALF_UP, two places; WORLD exact 3.125%','human_attestations_created':0})
    checks=[]
    def check(k,value):checks.append({'check':k,'passed':bool(value)})
    for e in receipt:check('receipt.'+e['file'],b.b.a.sha(b.ROOT/e['file'])==e['after'])
    for name in ['world1776_balkans05.py','world1776_balkans05_closeout.py']:
        ast.parse((b.ROOT/'tools'/name).read_text('utf8'));check('python_syntax.'+name,True)
    for e in source_manifest:
        if 'sha256' in e:check('source.'+e['file'],b.b.a.sha(b.LOT/e['file'])==e['sha256'])
    check('static_PASS',v['passed']==v['total'])
    check('technology_FAIL_preserved',tech['status']=='FAIL_STATIC' and len(tech['findings'])==3)
    check('ten_of_320',sum(c['status']=='STATIC_VERIFIED' for p in state['phases'] for r in p['subregions'] for c in r['criteria'].values())==10)
    check('zero_human_credit',state['progress']['runtime_user_validated']==0)
    check('only_Balkans_started',all(p['status']=='NOT_STARTED' for p in state['phases'][1:]))
    check('grouped_gate_preserved',state['phase_transition_gate']['next_region_requires_explicit_user_confirmation'] and not state['phase_transition_gate']['partial_lot_tests_requested'])
    check('population_conserved',pop['world_before']==pop['world_after']==834936539 and pop['all_POP_files_sha256_unchanged'])
    check('Git_identity_unchanged',b.b.a.git_state()==before['inventory']['git'])
    check('SERG_documents_preserved',all(b.b.a.sha(b.ROOT/r)==h for r,h in before['SERG_proofs'].items()))
    check('previous_WORLD_proofs_preserved',all(b.b.a.sha(b.ROOT/r)==h for r,h in before['prior_WORLD_proofs'].items()))
    delivery={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'runtime':'NOT_RUN','human_attestations_created':0}
    b.dump('DELIVERY_CHECKS.json',delivery)
    b.dump('DELIVERY_MANIFEST.json',{'lot':'BALKANS-05','date':DATE,'historical_date':'1776-01-01','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','historical_research_status':'REGION_INCOMPLETE','runtime':'NOT_RUN','functional_files':receipt,'tracking':{n:b.b.a.sha(b.OUT/n) for n in TRACK},'tools':{str(p.relative_to(b.ROOT).as_posix()):b.b.a.sha(p) for p in (b.ROOT/'tools').glob('world1776_balkans05*.py')},'evidence':{p.relative_to(b.LOT).as_posix():b.b.a.sha(p) for p in b.LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'},'tests':{'static':f'{v["passed"]}/{v["total"]}','delivery':f'{delivery["passed"]}/{delivery["total"]}','technology_contract':'FAIL_STATIC_BEFORE_AND_AFTER_SAME_3_FINDINGS'},'human_attestations_created':0})
    print(json.dumps({k:v for k,v in delivery.items() if k!='checks'}));print([c for c in checks if not c['passed']])

if __name__=='__main__':main()
