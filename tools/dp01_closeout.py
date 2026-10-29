"""Finish DP-01 receipts without modifying another territorial workstream."""
from dp01_install import *
def finish():
 ap=load('APPLIED.json');receipts=[]
 # Clean only the edited region bodies and newly authored files, preserving outside preimages.
 for z in ap['files']:
  rel=z['file'];p=ROOT/rel;assert sha(p)==z['after_sha256'],('Concurrent change',rel)
  raw=text(p);new=raw
  if rel in [ST]+POPS+BUILD:
   patch=[]
   for sid,n in state_nodes(raw).items():
    if sid in SCOPE:
     body=raw[n.start:n.end];clean=re.sub(r'(?m)[\t ]+(?=\r*$)','',body)
     if body!=clean:patch.append((n.start,n.end,clean))
   new=edit(raw,patch)
  elif rel.startswith('common/laws/1776_dp01'):
   # The source law files use legacy CRCRLF; normalise only this newly created local file.
   new=raw.replace('\r\r\n','\n').replace('\r\n','\n');new=re.sub(r'(?m)[\t ]+$','',new)
  if new!=raw:
   before=sha(p);q=OUT/'formatting_preimages'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());p.write_bytes(encoded(p,new));z['after_sha256']=sha(p);receipts.append(dict(file=rel,before_sha256=before,after_sha256=sha(p)))
 dump('FORMATTING_FINISH.json',receipts);dump('APPLIED.json',ap);print('Scoped formatting finished.')
def close():
 v=load('VALIDATION.json');assert v['status']=='PASS_STATIC_ONLY';ap=load('APPLIED.json');base=load('PREPARED.json')['world_before'];now=runtime();ours={z['file'] for z in ap['files']}
 for z in ap['files']:assert sha(ROOT/z['file'])==z['after_sha256'],z['file']
 others=[dict(file=r,before=base.get(r),after=now.get(r)) for r in sorted(set(base)|set(now)) if base.get(r)!=now.get(r) and r not in ours];dump('CONCURRENT_RUNTIME_DELTA.json',others);dump('CURRENT_RUNTIME_MANIFEST.json',now)
 # Source lineage is evidence about the data, not demographic validation for 1776.
 lineage={}
 for rel,sid in [(POPS[0],'STATE_BALUCHISTAN'),(POPS[1],'STATE_HILL_PUNJAB')]:
  p=GAME/rel;ns=state_nodes(text(p));lineage[sid]=dict(vanilla_reference=str(p),vanilla_sha256=sha(p),original_subdivisions=[dict(owner=n.key,cohorts=[dict(culture=scalar(x.one('culture')),religion=scalar(x.one('religion','DEFAULT')),size=int(x.one('size'))) for x in n.children('create_pop')]) for n in ns[sid].children()],current_preimage=str(OUT/'preimages'/rel),meaning='Only cohort ordering/signatures were used to recover merged groups. Current mod counts were retained. These vanilla counts and owners are NOT a census or frontier source for 1776.')
 dump('COHORT_LINEAGE.json',lineage)
 locs=load('CURRENT_LOCATORS.json');dump('HUB_REFERENCE_EVIDENCE.json',[z for z in locs if (z['state'],z['kind']) in [('STATE_BALUCHISTAN','city'),('STATE_BALUCHISTAN','wood'),('STATE_PUNJAB','city'),('STATE_PUNJAB','mine'),('STATE_HILL_PUNJAB','farm'),('STATE_HILL_PUNJAB','wood')]])
 counts=load('POP_LEDGER.json');poptext='\n'.join('| '+z['state']+' | '+', '.join(t['owner']+' : '+format(t['total'],',').replace(',',' ') for t in z['allocations'])+' |' for z in counts)
 filetext='\n'.join('- `'+z['file']+'`' for z in ap['files'])
 report=f'''# DP-01 — Empire durrani et Pendjab au 1er janvier 1776

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — 29 octobre 2026. Aucun test moteur et aucune homologation humaine attribués à cette installation.

## Résultat

La vérification a trouvé des corrections nécessaires. La condition donnée par le joueur pour passer directement à l'Asie centrale (« s'il n'y a pas de changement ») n'est donc pas remplie : **aucun territoire ni pacte kazakh, russe ou d'Asie centrale n'a été modifié**.

- **KAL réactivé**, sans nouveau TAG : noyau Kalat–Sarawan–Jhalawan/Kacchi et ville de Quetta. **Douze provinces** passent de DUR à KAL, dont onze de `STATE_BALUCHISTAN` et une de `STATE_QUETTA`. Pishin (`x1910AD`) reste DUR ; le Gwadar MAK installé antérieurement est conservé. Mir Nasir Khan Ier devient le dirigeant. Son âge exact n'est pas inventé.
- **PTA réactivé** : noyau **Patiala–Sirhind**, trois provinces de `STATE_HILL_PUNJAB`, sous Amar Singh. C'est une enveloppe de gameplay des deux centres, pas la totalité des chefferies cis-Sutlej ni un tracé cadastral. Aucune protection britannique de 1809 n'est anticipée.
- **PAN**, représentation collective préexistante des misls, reçoit **quatre provinces des plaines** autour des hubs Amritsar/Ludhiana et du Doab de Jalandhar. Son nom de confédération et le Jathedar Jassa Singh, déjà présents dans les corrections antérieures, sont conservés. Le détail de tous les misls n'est pas créé.
- **Multan était déjà PAN** ; pas de transfert inventé ni de reconquête durranie de 1780 anticipée. **Kaboul et Timur Shah étaient déjà correctement initialisés** ; ils ne sont pas refaits.
- Les templates vanilla de la cour sikh de 1836 et des deux pays réactivés sont remplacés par l'initialisation de 1776. Le journal de succession des maharajas de 1839 n'est plus ajouté à PAN au lancement de 1776 ; sa définition n'est pas supprimée.
- **Six pointeurs de hubs** sont réalignés sur les locators nommés effectivement présents : Kalat/Sibi, Lahore/Multan, Amritsar/Patiala. Les anciennes références plaçaient notamment le pointeur Kalat sur la côte. Les emplacements des locators, le bitmap et les State_ID ne sont pas déplacés.

Total : **19 provinces transférées**, deux TAGs existants réactivés. Pas de nouveau pays de nom ou de frontière inventé pour remplir les secteurs non résolus.

## Contrôle, suzeraineté et limites de représentation

Le gouvernement local de Kalat est distingué de l'administration directe durranie. Un lien spécifique **DUR → KAL** conserve la suzeraineté nominale, **sans versement régulier**, sans souverain partagé ni incorporation automatique, avec initiatives diplomatiques propres et sujets permis. La participation conditionnelle à certaines expéditions extérieures, décrite par les sources, n'est **pas** reproduite : l'appel automatique à toutes les guerres serait excessif. Marché partagé, protection militaire et rupture effective du pacte doivent être observés en jeu ; un type de sujet natif n'est pas la transcription du traité.

Patiala est représenté par son propriétaire local ; titres accordés par les Durrani et engagements personnels ne sont pas transformés sans preuve en annexion, tribut permanent ou protectorat britannique.

Les coordonnées des aperçus servent uniquement au repérage. Le modèle a treize contrôles et une précision indépendante **non établie** ; certains hubs du Pendjab/Cachemire sont décalés de plusieurs dizaines de pixels. Les transferts retiennent des noyaux nommés et leurs cellules contiguës ; **aucune superposition cadastrale d'une carte de 1776 n'est prétendue**. Les franges restent des approximations de provinces entières.

## Conservation des habitants, bâtiments et forces

Les deux fichiers POPs conservent respectivement **22 545 523** et **190 000 000** habitants. Chaque combinaison culture/religion/statut est conservée par State_ID. Aucun chiffre vanilla n'est réinjecté à la place des valeurs courantes.

La comparaison avec les subdivisions vanilla sert seulement à identifier la provenance de groupes que le mod avait regroupés sous DUR : cohortes KAL et PTA récupérées dans leur ordre courant. **Ce n'est pas une démographie de 1776**. Les 8 010 habitants étiquetés Brahui affectés à la portion de Quetta constituent une répartition technique provisoire explicitement signalée, sans prétendre définir une frontière ethnique.

| Région | Stock courant après réaffectation |
| --- | --- |
{poptext}

Les bâtiments du noyau civil de Kalat suivent KAL. Les cinq niveaux administratifs des collines sont répartis DUR2/PAN2/PTA1, et les deux niveaux de routes PAN1/PTA1. Ranchs, plantations, méthodes de production, réserves et participations sont conservés. Les déclarations du fichier mondial98 restent cohérentes avec les histoires régionales ; aucun niveau civil supplémentaire n'est ajouté.

**Seize unités de conscription existantes** sont réaffectées : huit à PAN, quatre à KAL, quatre à PTA. DUR conserve deux conscriptions dans chacune des deux régions de recrutement concernées. Types, régions et quantités globales sont identiques ; aucune armée permanente, caserne explicite ou population n'est ajoutée pour gonfler les nouveaux pays. Cette répartition technique n'est pas un décompte des armées de 1776.

KAL/PTA ont des profils initiaux explicites et sobres, sans palier industriel copié. Trois variantes de lois limitées à ces pays maintiennent les effets natifs souhaités pour les douanes, la servitude coutumière et, à Patiala, la tolérance des cultes. Elles évitent d'accorder gouvernement constitutionnel ou réseaux scientifiques institutionnalisés pour satisfaire des prérequis tardifs. Ce sont des abstractions du moteur, pas une certification de leurs codes juridiques.

## Vérifications

- **{len(v['checks'])} contrôles statiques ciblés réussis** : changements exactement conformes au plan, unicité des attributions dans les régions concernées, régions et ressources conservées, capitales possédées, cœurs KAL/PTA connectés par arêtes, Pishin et Gwadar témoins, maintien des corrections arabiques.
- Stocks de POPs et niveaux civils conservés, ainsi que types/nombres/régions de recrutement militaire. Les contenus syntaxiques extérieurs aux scopes sont comparés aux préimages actuelles dans les fichiers partagés.
- **KAL et PTA : PASS_STATIC_ONLY** pour technologies, recettes sélectionnées, demandes de lois et unités. **DUR et PAN : erreurs antérieures conservées, aucun nouveau signal**. Les alertes héritées ne sont pas maquillées en réussite générale de l'Asie.
- Paires action/type de sujet et transfert financier nul, caractères de 1776, suppression des templates de 1836, références de hubs, localisation FR/EN avec BOM et clés nouvelles uniques vérifiés.
- {len(others)} changement(s) de runtime hors fichiers du lot constaté(s) depuis la préparation : conservés dans `CONCURRENT_RUNTIME_DELTA.json`, sans attribution à cette passe.

Commandes exécutées : `dp01.py`, `dp01_geography.py`, `dp01_plan.py`, `dp01_install.py --prepare`, `--apply`, `dp01_profile_repair.py`, `dp01_audit.py`, `dp01_closeout.py --finish`, puis nouvel audit et clôture. L'installation contrôle les empreintes avant chaque écriture et conserve les préimages ; aucun ancien fichier partagé n'est restauré globalement.

Ces résultats ne prouvent ni chargement moteur, ni emploi des bâtiments, ni équilibre alimentaire/budgétaire, ni placement des hubs secondaires par le moteur. Voir `RUNTIME_PROTOCOL.md`.

## Réserves ouvertes

1. **Bahawalpur**, les autres chefferies cis-Sutlej et les contours fins de chaque misl restent à cartographier ; les trois provinces PTA ne représentent pas Jind, Nabha et toutes leurs enclaves.
2. **Jammu, Ladakh, Garhwal et autres États des collines** : l'ancien propriétaire DUR de leurs secteurs restants n'est pas historiquement certifié. Le calage courant ne permet pas de transformer ces réserves en frontières précises sans un lot himalayen spécifique.
3. **Makran, Kharan, Las Bela et confins baloutches** : influence, partage de revenus et administration Gichki ne se confondent pas. Pas de transfert uniforme des65 anciennes provinces à Kalat. La présente passe ne clôture pas ces périphéries.
4. **Bactriane, Hazarajat et confins pachtounes** : conserver leur traitement actuel ne démontre pas une administration uniforme de Timur Shah.
5. Répartition démographique locale, ressources par propriétaire d'État partagé, revenus et capacité d'emploi : contrôles approfondis ouverts. Les stocks conservés ne sont pas un recensement validé.

La prochaine étape demandée conditionnellement, **Asie centrale et trois jüz kazakhs**, n'est pas installée ici. Leur état de dépendance envers la Russie devra être vérifié séparément ; le simple serment d'un khan n'établit pas l'administration russe uniforme de tous les jüz.

## Fichiers runtime modifiés ou créés

{filetext}

Outils et preuves dans ce dossier et `tools/dp01*.py`. Aucune écriture dans le vanilla, aucun commit, merge, rebase ou push. Les suivis WORLD/SERG et les reçus américains restent hors mission ; aucun pourcentage de clôture ne leur est attribué.

## ColGrep

Un appel à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent` a été tenté pour localiser les dossiers Durrani/Pendjab et les dépendances. Échec en **1,34 seconde environ**, au verrou de l'index local : accès refusé, erreur système5. Le modèle2B n'est pas confirmé comme exécuté ; repli sur les dossiers R3/R4 connus et `rg`. Aucun réglage, modèle ou index n'a été modifié. Les tokens Codex et une économie comparative fiable ne sont pas disponibles.
'''
 (OUT/'REPORT.md').write_text(report,encoding='utf8')
 protocol='''# DP-01 — Protocole de contrôle en jeu

Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Commencer une **nouvelle partie au 1er janvier 1776**, avec le mod principal courant. Une sauvegarde antérieure ne recharge pas les histoires initiales.

1. À la sélection des pays, trouver **Kalat** et **Patiala**. Le Pendjab doit rester la **confédération des misls**, avec Jassa Singh Ahluwalia/Jathedar ; pas Ranjit Singh de1836. Kalat doit afficher Mir Nasir KhanIer, Patiala Amar Singh. Kaboul et Timur Shah restent durranis.
2. Utiliser `INSTALLED_MAP.png` comme croquis, `PLAN.json` pour les19 RGB exacts. Kalat possède un noyau de12 provinces reliées, de Quetta à Kalat puis vers Khuzdar/Wad et Kacchi ; **Pishin reste DUR**, Gwadar reste MAK. Les repères modernes du croquis ne garantissent pas qu'une ville soit cherchable dans le moteur.
3. Dans les collines du Pendjab : PTA possède trois provinces Patiala/Sirhind ; PAN reçoit les quatre provinces de plaines Amritsar/Ludhiana adjacentes. Multan reste PAN. Ne pas interpréter les secteurs restants comme une validation de l'administration durranie du Ladakh ou des rajas himalayens.
4. Vérifier la relation spécifique DUR → KAL : souverain distinct, aucun prélèvement régulier, diplomatie propre disponible. Vérifier l'accès au marché et la défense réelle, qui ne sont pas prouvés par le script. PTA ne doit pas être sujet britannique.
5. Contrôler les populations des portions : KAL Baloutchistan461912 et Quetta8010 ; PTA collines795451 ; PAN collines1627993. Vérifier les minorités et les esclaves, pas seulement les sommes nationales. Les valeurs sont des stocks techniques conservés, pas des recensements historiques.
6. Contrôler les administrations, routes, ranch et coton transférés ; pas de bâtiment disparu ou de niveaux mondiaux dupliqués. Vérifier le placement des hubs Kalat/Lahore/Multan/Amritsar/Patiala et l'absence de port fictif ou de bâtiment civil dans un pays absent.
7. Vérifier les unités : quatre conscriptions KAL, quatre PTA, huit réaffectées à la formation PAN ; DUR conserve deux dans chacune des deux régions concernées. Mobiliser pour vérifier les centres natifs et les commandants ; ne pas construire de casernes supplémentaires pour compenser un simple délai d'initialisation.
8. Laisser tourner quelques semaines : marchés, nourriture, emplois, budgets et trajets terrestres. Sauvegarder puis recharger. Relever crashs, nouveaux messages d'erreur ou pertes de relations séparément des erreurs déjà présentes.

Aucune durée observée ni validation du joueur n'est encore enregistrée. Un succès de ce protocole ne clôturera pas toutes les réserves himalayennes et baloutches.
'''
 (OUT/'RUNTIME_PROTOCOL.md').write_text(protocol,encoding='utf8')
 dump('STATUS.json',dict(lot='DP-01',reference_date='1776-01-01',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',technical_status='PASS_STATIC_ONLY',runtime_validated=False,historical_closure=False,province_transfers=19,reactivated_tags=['KAL','PTA'],new_population=0,new_units=0,files=ap['files'],central_asia_started=False,conditional_transition='Not taken: Durrani/Punjab corrections were found and installed.',open_reserves=['Himalayan chiefships and Ladakh/Jammu/Garhwal','Bahawalpur and detailed misls/cis-Sutlej boundaries','Makran/Kharan/Las Bela and tributary frontiers','Demography and runtime markets'],colgrep=dict(calls=1,elapsed_seconds_approx=1.34,model_execution_confirmed=False,result='Index lock denied, fallback retrieval')))
 (OUT.parent/'CURRENT.json').write_text(json.dumps(dict(current_lot='DP-01',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',historical_closure=False,report='DP-01/REPORT.md',runtime_protocol='DP-01/RUNTIME_PROTOCOL.md'),indent=2)+'\n',encoding='utf8')
 print(json.dumps(dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',checks=len(v['checks']),transfers=19,concurrent_runtime_changes=len(others),files=len(ap['files']))))
if __name__=='__main__':
 if '--finish' in sys.argv:finish()
 else:close()
