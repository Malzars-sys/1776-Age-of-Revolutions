"""Additive WORLD-only closeout for the first western Sahel territorial lot."""
import json
from decimal import Decimal, ROUND_HALF_UP
import world1776_sahel01 as s

ROOT, OUT, LOT = s.ROOT, s.b.OUT, s.LOT
TRACK = ['ROADMAP.md', 'ROADMAP_STATE.json', 'NEXT_ACTION.md', 'BLOCKERS.md',
         'PROGRESS_HISTORY.md', 'OWNERSHIP_BOUNDARIES.md', 'CONCURRENT_CHANGES.json']


def write(name, text):
    (LOT / name).write_text(text.strip() + '\n', encoding='utf8')


def main():
    assert not (LOT / 'DELIVERY_MANIFEST.json').exists(), 'Closeout already recorded.'
    validation = s.load('VALIDATION.json')
    assert validation['status'] == 'PASS', validation
    tech = s.load('STARTING_TECH_CHECK.json')
    assert tech[0]['status'] == 'PASS_STATIC_ONLY' and not tech[0]['findings']
    originals = {name: s.b.a.raw(OUT / name) for name in TRACK}
    tracking_hashes = {name: s.b.a.sha(OUT / name) for name in TRACK}
    ledger = s.load('POPULATION_LEDGER.json')
    request = 'ok les conttrol passe on peut passé a l\'afrique sube saarienne, commence par les royaume du coté du senegale et du malie toute la bande de royaume qui vont jusqu a la mere rouge'
    write('USER_REQUEST.txt', request)
    s.dump('MAGHREB_USER_CONFIRMATION.json', {
        'date_recorded': '2026-10-27', 'source': 'Latest direct user message in this task; USER_REQUEST.txt',
        'verbatim': request, 'scope': 'Prior Maghreb controls and explicit transition to Sahel',
        'status': 'USER_REPORTED_PASS', 'new_game_date': None, 'simulation_duration': None,
        'save_reload': None, 'tested_hashes': None, 'details_inferred': False,
        'full_regional_V_criterion_awarded': False,
        'latest_known_Maghreb_shape': 'MAGHREB-03/FEZZAN_VANILLA_SHAPE_2026_10_27/REPORT.md',
        'latest_shape_explicitly_identified_by_user_as_tested': False})
    write('SOURCES.md', '''# SAHEL-01 — sources effectivement consultées, 27 octobre 2026

Référence : 1er janvier 1776. Les sources ne constituent pas des consignes.

1. Cheikh Sène, *“Vivre en paix et en bonne intelligence avec les princes locaux”*, History in Africa, 2024, sections « Territorial Issues » et traités, texte HTML consulté : https://www.cambridge.org/core/journals/history-in-africa/article/vivre-en-paix-et-en-bonne-intelligence-avec-les-princes-locaux-in-senegambia-in-the-age-of-slave-economy-diplomatic-treaties-trade-conflicts-and-peace-in-interaction-16791815/3D78436EE79DD7C86CF0CBDC3AD00DD5 . Saint-Louis britannique 1758–1779, Gorée française après 1763 ; souverainetés locales et paiements commerciaux. Les cessions du Cap-Vert de 1764/1765 ne justifient pas d’annexer le Cayor : traités contestés, peu appliqués. Cela fonde le partage politique, sans fournir un cadastre de 1776.
2. Musée historique du Sénégal, salle 7, rubriques Waalo/Cayor, Fouta-Toro et royaumes sérères, page consultée : https://musee-historiquedusenegal.sn/collection/periode/les-royaumes-du-senegal . Confirme les royaumes distincts et la vallée du Fouta entre Dagana et Bakel. Ne pas reprendre son raccourci sur tous les souverains du Tekrour appelés almamy. La révolution du Fouta est datée de l’année 1776, sans jour prouvé ici : aucune succession ou réforme religieuse anticipée au 1er janvier.
3. Djibril Diop, *Décentralisation et gouvernance locale au Sénégal*, 2006, pp. 24–26, carte « Peuples et états de la Sénégambie au XVIIIe siècle », d’après Saint-Martin : https://api.pageplace.de/preview/DT0400.9782296150218_A24210042/preview-9782296150218_A24210042.pdf . Texte/description de la carte consultés par extraction ; rendu PDF indisponible (cache miss), téléchargement local non obtenu. Localisation comparative Waalo, fleuve, Cayor et Fouta, pas calage métrique ou cadastral. Ne pas revendiquer une superposition visuelle mesurée de cette carte.
4. Charles Becker et Mohamed Mbodj, contribution à *La population du Sénégal*, Charbit/Ndiaye, 1994, passage démographique des comptoirs, extrait indexé consulté : https://ireda.ceped.org/inventaire/ressources/sen-Charbit-Ndiaye-1994_population_Senegal.pdf . Saint-Louis : 4 622 habitants en 1776. PDF complet trop volumineux pour l’outil ; passage précis retrouvé par recherche, pas lecture intégrale revendiquée.
5. Jessica Marie Johnson, thèse, University of Maryland, 2012, tableau 2.2 « Population of Gorée and Saint-Louis, 1685–1810 », extraction tabulaire consultée : https://api.drum.lib.umd.edu/server/api/core/bitstreams/d7609f22-c73a-4dae-8d5b-59cc2566e8fd/content . Gorée 1776 : total 1 569. Seul ce total est repris, pas une nouvelle ventilation ethnique ou servile. PDF complet trop volumineux ; la composition existante du mod reste une dette documentée.
6. Charles Becker et Victor Martin, « Kayor et Baol, royaumes sénégalais et traite des esclaves au XVIIIe siècle », 1975, pp. 270–300, introduction et passages indexés : https://www.persee.fr/doc/outre_0300-9513_1975_num_62_226_1832 . Piste pour le prochain sous-lot des royaumes méridionaux ; aucune frontière Baol installée sur cette seule référence.
7. Pour la file orientale seulement : TDV, « Sokoto », Ahmet Kavas, 2009 : https://islamansiklopedisi.org.tr/sokoto ; califat issu du mouvement de 1804. *General History of Africa*, V, chapitre « The Sudan, 1500–1800 », p. 185, extrait consulté : https://repository.out.ac.tz/407/1/Vol_5._Africa_from_the_Sixteenth_to_the_Eighteenth_Century_editor_B.A.OGOT%28FILEminimizer%29.pdf . Sennar et régence hamaj ; aucune nouvelle frontière soudanaise déduite de cet extrait.

Réutilisation : dossiers MAP1 R7-0119 à R7-0128, R7-0029 et R7-0178/0179, inventaire régional R7. Leurs anciens propriétaires/catalogues sont des pistes, jamais une baseline réinstallée.

Correspondance actuelle : SENEGAL_CELLS.json, SENEGAL_RAW.png et PLAN.json. Les sources distinguent le Waalo autour de Saint-Louis et le Fouta en amont ; trois anciennes provinces FRA de chaque côté donnent une approximation politique cohérente. Les noyaux européens occupent seulement cinq pixels terrestres existants. Saint-Louis suit le locator natif du même nom jusqu’à la mer. Gorée est un point de représentation à la côte du Cap-Vert (3707,1771) : l’île n’est pas séparée à cette résolution. Ce choix n’est ni une île inventée ni une frontière littorale mesurée.

Technologies WAA : interprétation minimale des cultures céréalières, élevage, textile/artisanat et échanges diplomatiques/commerciaux ; six capacités distinctes, aucun tier uniforme, aucun atelier industriel, assurance maritime ou science institutionnalisée attribué. Monarchie et oligarchie représentent sommairement l’autorité du brak et les élites électrices ; titulaires, assemblées et flavor laissés hors de cette passe.
''')
    queue = [
        {'id':'SAHEL-02','scope':'Sénégambie restante, puis interface du haut Sénégal','canonical':['P3-01','P3-02'],
         'territorial_work':['Distinguer Baol, Sine, Saloum et leur interface Cayor/Jolof sans rétroprojeter les unions ultérieures.', 'Vérifier le classement décentralisé des royaumes CAY/JLF/BND/KBU ; modifier le statut politique si sourcé, pas leurs personnages.', 'Gambie : SIL est une administration coloniale tardive ; relever les forts et souverainetés riveraines avant de remplacer ses deux provinces.', 'Vérifier Boundou, Galam et Kaabu sur les provinces existantes.'], 'status':'OPEN_NOT_INSTALLED'},
        {'id':'SAHEL-03','scope':'Ségou, Kaarta, Macina et Tombouctou','canonical':['P3-02'],
         'territorial_work':['Ségou et Kaarta existent déjà : pas de fusion par commodité.', 'Le MSN actuel couvre 41 provinces en EASTERN_MALI et 24 en TIMBUKTU ; distinguer autorités peules pré-Diina, influence bambara, Arma et Touaregs. Ne pas donner tout MSN à Ségou.', 'Identifier Djenné, delta intérieur et Sikasso ; le hub de EASTERN_MALI est Sikasso, pas une preuve de possession de tout le Macina.'], 'status':'OPEN_NOT_INSTALLED'},
        {'id':'SAHEL-04','scope':'Boucle du Niger, Aïr et interface mossi','canonical':['P3-02','P3-04'],
         'territorial_work':['Contrôler les ensembles AIR/DIN/AJJ/TBI et MOS avec sources datées ; ne pas confondre ethnonymes et États.'], 'status':'OPEN_NOT_INSTALLED'},
        {'id':'SAHEL-05','scope':'Royaumes haoussa avant le califat de Sokoto','canonical':['P3-04'],
         'territorial_work':['SOK possède 159 provinces dans cinq régions : califat de 1804 anachronique en 1776.', 'Délimiter les royaumes attestés (Gobir déjà HAU, Kano, Katsina, Zazzau, etc.) avec géométrie locale ; aucun partage par rectangles ou distances aux capitales.'], 'status':'OPEN_NOT_INSTALLED'},
        {'id':'SAHEL-06','scope':'Bornou, Baguirmi, Ouaddai et Darfour','canonical':['P3-04','P3-06'],
         'territorial_work':['Pays déjà présents ; contrôler leur extension en 1776 et les confins du Tchad avant tout transfert.'], 'status':'OPEN_NOT_INSTALLED'},
        {'id':'SAHEL-07','scope':'Kordofan, vallée du Nil, Sennar et débouchés de mer Rouge','canonical':['P3-06','interface R3'],
         'territorial_work':['SD1 reste décentralisé sur Kordofan, Nil Bleu et une grande part de Dongola/Érythrée : restaurer les pouvoirs attestés, notamment le sultanat Funj et ses autonomies, sans unifier tout le Soudan.', 'Préserver et vérifier les ports ottomans et les interfaces éthiopiennes ; ne pas anticiper la conquête égyptienne de 1821.'], 'status':'OPEN_NOT_INSTALLED'}]
    s.dump('TERRITORIAL_QUEUE.json', {'authorized_by':'USER_REQUEST.txt','direction':'WEST_TO_EAST_SENEGAL_MALI_RED_SEA',
           'not_authorized_by_this_route':['Congo','Southern Africa','Madagascar'], 'next':'SAHEL-02', 'lots':queue})
    write('GROUPED_RUNTIME_ITEMS.md', '''# Contrôle à regrouper avec les autres lots du Sahel

Statut de SAHEL-01 : NOT_RUN. Aucun test intermédiaire demandé.

Lors du contrôle groupé : nouvelle partie au 1er janvier 1776 ; constater Waalo indépendant, continuité du Fouta élargi, Saint-Louis GBR et point français du Cap-Vert. Vérifier que le brak généré, la capitale et les lois de WAA chargent ; contrôler populations 62 889 WAA, 157 264 FTR, 4 622 GBR et 1 569 FRA. Observer l’accès maritime des petits noyaux, les hubs générés et les centres de commerce français hérités. Simuler puis sauvegarder/recharger à la fin du contrôle groupé ; ne pas déclarer ces étapes exécutées avant reçu utilisateur.

Témoins : possessions espagnoles/Gibraltar, Siwa reliée à l’Égypte, contour actuel du Fezzan, zones SERG et installations américaines concurrentes. Les autres secteurs sahéliens ne sont pas déclarés corrigés par ce premier lot.
''')
    write('REPORT.md', f'''# SAHEL-01 — Nord de la Sénégambie

Date de référence : 1er janvier 1776. Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Premier lot borné de la bande Sénégal/Mali–mer Rouge, **pas clôture de toute la bande**. Le joueur a déclaré les contrôles du Maghreb passés et autorise cette transition ; reçu limité dans MAGHREB_USER_CONFIRMATION.json, sans durée ni version testée inventée.

## Corrections installées

- Waalo (WAA), pays indépendant non reconnu, restauré sur xEF30C0 (hors noyau côtier), xA80844 et x3A5023, auparavant français.
- Fouta-Toro (FTR) reçoit x267B18, x329831 et x339E4C, auparavant français. Ses trois provinces antérieures restent intactes. Aucune révolution de 1776 datée artificiellement au 1er janvier.
- Saint-Louis britannique : quatre pixels terrestres (3719–3722,1734), nouveau xE8D241, incluant le locator natif de la ville et un débouché côtier. Pas d’annexion britannique du Waalo.
- Gorée française : xE8D242, un pixel à (3707,1771), prélevé sur le parent côtier CAY xBCFFB5. **Proxy politique côtier** : l’île distincte n’existe pas dans le bitmap natif. Aucun pixel marin changé en terre, aucune grande cession du Cap-Vert déduite de traités de papier. Parent CAY conservé.

Géométrie : cinq pixels recolorés, deux RGB nouveaux, six provinces réattribuées. États administratifs natifs, ressources, terrains des parents, modèles de hubs et reste du bitmap conservés. Le contour Waalo/Fouta suit les provinces disponibles : approximation politique, pas cadastre exact. Les limites des royaumes au sud restent ouvertes.

## Populations et données nécessaires

Monde **{ledger['world_before']:,} → {ledger['world_after']:,}**, delta zéro. Ancien pool FRA Sénégal : 131 968. Répartition installée : FRA/Gorée 1 569 ; GBR/Saint-Louis 4 622 ; WAA 62 889 ; ajout FTR 62 888, soit FTR final 157 264. Toutes les identités de cohortes culture/religion/statut servile du pool sont conservées à l’unité à l’échelle globale. Aucun habitant ajouté ou supprimé.

Les deux totaux de comptoirs sont des observations de 1776. La ventilation des cohortes est héritée, non un recensement ethnique ou servile corrigé. Le résidu partagé entre les deux groupes de trois provinces est une allocation technique explicite, pas une estimation historique nouvelle de densité. Cette démographie reste incertaine.

WAA : monarchie/oligarchie comme représentation minimale du brak et des élites électrices ; aucun dirigeant historique inventé, aucun événement/trait/flavor ajouté. Six technologies rurales, artisanales et d’échanges explicites, dépendances valides. Loi de coutumes commerciales propre à WAA, recette strictement identique au mercantilisme courant, disponibilité via relations internationales ; évite d’attribuer l’assurance maritime pour débloquer des droits commerciaux. Aucun graphe TECH ou recette ECON commun modifié. Aucun bâtiment/PM/unité nouveau ; les centres de commerce français hérités restent dans la portion française.

## Sources, incertitudes et contrôles

SOURCES.md distingue textes consultés, extraits indexés et rendu cartographique indisponible. La date de souveraineté est étayée ; le contour de l’île et la délimitation cadastrale ne sont pas certifiés.

**{validation['passed']}/{validation['total']} contrôles statiques** : patch exact des nœuds Sénégal et composition contrôlée de deux modifications américaines indépendantes, propriétaires uniques, seulement cinq pixels terrestres, pays continus, population et cohortes conservées, index Git inchangé et preuves antérieures préservées. Profil WAA : PASS_STATIC_ONLY, six technologies, aucun constat. Aucun lancement moteur par l’agent. Protocole groupé, aucune demande de test intermédiaire.

Concurrence : trois fichiers avaient évolué depuis le premier relevé (états, populations et régions d’Amérique du Nord). Pendant les vérifications, le même chantier a transféré xBA821E de QPW à LOU et retiré une revendication USA au Texas. Le premier contrôle strict (39/42) est archivé dans VALIDATION_RUN01_CONCURRENT.json ; ses trois écarts correspondent à ces changements externes, pas à un échec du Sénégal. EXTERNAL_COMPOSITION_REVIEW.json rapproche les deux nœuds des reçus américains et conserve leurs versions exactes. Le contrôle courant utilise cette composition explicitement bornée. Application sur les versions courantes, pas sur la première baseline. Le contour Fezzan de 78 provinces demandé séparément est préservé, ainsi que Siwa, Gibraltar, Balkans, SERG, TECH-R1/R2/R3 et ECON. Aucune opération Git d’écriture, aucun suivi SERG ou vanilla écrit.

## Suite

Inventaire courant de 22 régions dans SAHEL_BELT_INVENTORY.json. TERRITORIAL_QUEUE.json ordonne les royaumes sénégambiens restants, Mali/Tombouctou, Niger, pays haoussa, bassin du Tchad/Darfour puis Nil/mer Rouge. Les gros ensembles MSN/SOK/SD1 restent des corrections à étudier et installer, pas des régions déjà validées. Travail exclusivement territorial ; personnages et raffinements de bâtiments différés.

P3-01 reste partiel : aucun critère régional entier crédité. WORLD reste **10/320, 3,13 %** selon le dénominateur historique, qui inclut des domaines désormais différés. Ce chiffre ne mesure pas le nombre de frontières corrigées.
''')

    state = json.loads(originals['ROADMAP_STATE.json'])
    previous = dict(state['current_steering'])
    state.setdefault('steering_history', []).append(previous)
    state['current_phase'] = 'P3'
    p3 = next(p for p in state['phases'] if p['id'] == 'P3')
    p3['status'] = 'IN_PROGRESS_TERRITORIAL_CARTOGRAPHY_ONLY'
    p4 = next(p for p in state['phases'] if p['id'] == 'P4')
    p4['status'] = 'CARTOGRAPHIC_PASS_USER_REPORTED_CONTROLS_PASSED'
    p4['reported_validation'] = 'SAHEL-01/MAGHREB_USER_CONFIRMATION.json'
    region = next(r for r in p3['subregions'] if r['id'] == 'P3-01')
    for code in ['O','I','D','E','T','R','S']:
        region['criteria'][code]['status'] = 'PARTIAL'
        region['criteria'][code]['evidence'] = 'SAHEL-01/REPORT.md'
        region['criteria'][code]['remaining'] = 'Regional obligations outside the bounded northern Senegal core remain open; no whole criterion credit.'
    region['criteria']['V']['status'] = 'NOT_STARTED'
    region['criteria']['V']['evidence'] = 'SAHEL-01/GROUPED_RUNTIME_ITEMS.md'
    state['current_steering'] = {'date':'2026-10-27','scope':'Territorial Sahel belt, Senegal/Mali to Red Sea',
        'authority':'SAHEL-01/USER_REQUEST.txt','first_lot':'SAHEL-01 northern Senegambia',
        'next_pass':'SAHEL-02 remaining Senegambian kingdoms, then Mali',
        'intermediate_player_tests_requested':False,'runtime_validation_timing':'GROUPED_SAHEL',
        'Maghreb_user_report':'SAHEL-01/MAGHREB_USER_CONFIRMATION.json','full_V_credit':False}
    state['phase_transition_gate'].update(authorized_next_phase='P3', explicit_transition_authorized=True,
        source='Direct user message, 2026-10-27, SAHEL-01/USER_REQUEST.txt',
        rule='User reports prior Maghreb controls passed and explicitly requests Senegal/Mali to Red Sea. Territorial scope retained.',
        authorization_is_runtime_validation=False, runtime_validation_timing='GROUPED_SAHEL')
    state['lots'].append({'id':'SAHEL-01','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        'scope':['Northern Senegambia: Waalo / upstream Futa Toro / Saint-Louis and Goree coastal points'],
        'runtime':'NOT_RUN','files_modified':len(s.load('FILES_MODIFIED.json')),'new_RGBs':2,'pixels_recolored':5,
        'new_tags':['WAA'],'world_population_delta':0,'receipt':'SAHEL-01/FILES_MODIFIED.json','credited_criteria':[]})
    for phase in state['phases']:
        count = sum(c['status']=='STATIC_VERIFIED' for r in phase['subregions'] for c in r['criteria'].values())
        phase['progress']['technical_verified'] = count
        phase['progress']['technical_percent'] = float((Decimal(count)*100/Decimal(phase['progress']['criteria_total'])).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
    score = sum(p['progress']['technical_verified'] for p in state['phases'])
    assert score == 10 and state['progress']['criteria_total'] == 320 and state['progress']['runtime_user_validated'] == 0
    state['progress']['technical_verified'] = score
    state['progress']['technical_percent'] = float((Decimal(score)*100/320).quantize(Decimal('.01'), rounding=ROUND_HALF_UP))
    updated = {'ROADMAP_STATE.json':json.dumps(state,ensure_ascii=False,indent=2)+'\n'}
    heading = '\n\n## SAHEL-01 — 27 octobre 2026\n\n'
    short = f'''Confirmation directe : contrôles antérieurs du Maghreb déclarés passés ; détails de durée/version/sauvegarde non fournis, aucun critère V entier inventé. Transition P4→P3 autorisée. Premier lot territorial installé au nord du Sénégal : Waalo WAA, trois provinces au Fouta, petits noyaux Saint-Louis GBR et Gorée FRA. Cinq pixels, deux RGB, population mondiale inchangée à {ledger['world_after']:,}. {validation['passed']}/{validation['total']} statiques, profil WAA PASS_STATIC_ONLY. Suite : Sénégambie restante et Mali, puis Niger/Haoussa/Tchad/Nil jusqu’à la mer Rouge. Aucun flavor, aucun point régional supplémentaire ; WORLD 10/320 (3,13 %). Rapport SAHEL-01/REPORT.md. Les versions américaines et le contour Fezzan de 78 provinces sont conservés.'''
    updated['ROADMAP.md'] = originals['ROADMAP.md'].rstrip() + heading + short + '\n'
    updated['PROGRESS_HISTORY.md'] = originals['PROGRESS_HISTORY.md'].rstrip() + heading + short + '\n'
    updated['BLOCKERS.md'] = originals['BLOCKERS.md'].rstrip() + heading + '''Gorée est un proxy côtier d’un pixel, pas une île physiquement séparée. Tracé Waalo/Fouta par provinces natives, répartition de population résiduelle technique et composition des cohortes héritée. Capitales/hubs générés, lois et budgets du nouveau WAA à observer au contrôle groupé, sans demande intermédiaire. Les royaumes au sud, l’administration SIL en Gambie, MSN au Mali, SOK avant 1804 et SD1/Funj restent ouverts dans SAHEL-01/TERRITORIAL_QUEUE.json. Aucun de ces constats n’autorise un partage arbitraire. Le reçu Maghreb borne les mots réellement prononcés ; durée/version/sauvegarde non attestées.\n'''
    updated['OWNERSHIP_BOUNDARIES.md'] = originals['OWNERSHIP_BOUNDARIES.md'].rstrip() + heading + '''Seuls nœuds STATE_SENEGAL des historiques d’états/POPs et de la région native, cinq pixels existants et deux terrains hérités. Six fichiers nouveaux propres à WAA (définition, histoire, effet, loi et FR/EN). Aucun autre pays, région, ressource, hub, recette ou territoire SERG écrit. 00_states courant composé sur le contour Fezzan de 78 provinces et les changements américains présents, y compris la retouche Arkansas/Texas survenue après notre application ; reçus et version exacte archivés dans EXTERNAL_COMPOSITION_REVIEW.json. Aucune restauration d’une baseline antérieure. Le corridor autorisé traverse P3-01/02/04/06 et ses interfaces R3 ; aucune autre région subsaharienne lancée par cette demande.\n'''
    updated['NEXT_ACTION.md'] = '''# Prochaine passe — SAHEL-02, royaumes sénégambiens restants, puis Mali

Le joueur déclare les contrôles du Maghreb passés et autorise la bande Sénégal/Mali–mer Rouge. Reçu limité : SAHEL-01/MAGHREB_USER_CONFIRMATION.json. Ne pas lui redemander cette autorisation ; ne pas inventer de durée ou de sauvegarde testée.

SAHEL-01 installé et contrôlé : Waalo indépendant, extension amont du Fouta-Toro, noyau britannique de Saint-Louis et proxy côtier français de Gorée. Lire SAHEL-01/REPORT.md, PLAN.json, VALIDATION.json et TERRITORIAL_QUEUE.json avant toute suite. Premier lot borné, aucune clôture de P3-01 ou de tout le Sahel.

Traiter les frontières des royaumes sénégambiens restants (Baol, Sine/Saloum, Cayor/Jolof, Boundou/Galam/Kaabu et Gambie) en conservant ce noyau ; reprendre ensuite Ségou–Kaarta–Macina/Tombouctou. Continuer vers Niger/Aïr, royaumes haoussa avant Sokoto, Tchad/Darfour puis Sennar/Nil/mer Rouge selon la file. Pas d’annexion globale de MSN à Ségou, de partage arbitraire de SOK ou d’unification de SD1.

Frontières et souverainetés uniquement. Personnages, refinements de bâtiments et flavor différés. Préserver Maghreb/Gibraltar, Siwa, contour Fezzan actuel, Balkans, SERG, TECH-R1/R2/R3, ECON et Amérique du Nord concurrente ; patchs ciblés sur versions courantes. Pour tout nouveau TAG : profil initial explicite, dépendances et compatibilité contrôlés. Population et cohortes à tracer.

Contrôles joueur regroupés pour les lots du Sahel, aucune demande intermédiaire. Protocole SAHEL-01/GROUPED_RUNTIME_ITEMS.md ; nouveau lot NOT_RUN. WORLD reste 10/320, 3,13 %, sans crédit pour un noyau régional partiel.
'''
    concurrent = json.loads(originals['CONCURRENT_CHANGES.json'])
    concurrent['SAHEL-01'] = {'receipt':'SAHEL-01/CONCURRENT_CHANGES.json','external_review':'SAHEL-01/EXTERNAL_REVIEW.json',
        'functional_files_modified':len(s.load('FILES_MODIFIED.json')),'new_RGBs':2,'pixels_recolored':5,
        'world_population_delta':0,'Git_writes':0,'SERG_writes':0,'vanilla_writes':0}
    updated['CONCURRENT_CHANGES.json'] = json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n'
    assert all(s.b.a.sha(OUT/name)==h for name,h in tracking_hashes.items()), 'WORLD tracking changed concurrently: reread.'
    for name, text in updated.items():
        target = OUT/name
        snapshot = LOT/'tracking_inputs'/name
        snapshot.parent.mkdir(parents=True,exist_ok=True)
        snapshot.write_bytes(target.read_bytes())
        target.write_text(text,encoding='utf8')
    s.dump('PROGRESS_CALCULATION.json', {'credited':[],'WORLD':state['progress'],'P3':p3['progress'],
        'reason':'Only northern Senegal subset; no whole regional criterion cleared. User report does not attest required full V details.',
        'human_report_recorded':True,'full_regional_human_validation_created':False})
    s.dump('DELIVERY_MANIFEST.json', {'lot':'SAHEL-01','date':'2026-10-27','status':'IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',
        'runtime':'NOT_RUN','files':s.load('FILES_MODIFIED.json'),'tracking':{n:s.b.a.sha(OUT/n) for n in TRACK},
        'checks':{'static':f"{validation['passed']}/{validation['total']}",'WAA_starting_knowledge':tech[0]['status']},
        'evidence':{p.relative_to(LOT).as_posix():s.b.a.sha(p) for p in LOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'}})
    print(json.dumps({'lot':'SAHEL-01','static':validation['passed'],'total':validation['total'],'tech':tech[0]['status'],'WORLD':state['progress']},ensure_ascii=False))


if __name__ == '__main__': main()
