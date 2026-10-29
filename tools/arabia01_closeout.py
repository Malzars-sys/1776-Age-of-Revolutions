"""Generate current ARABIA-01 receipts, bounded report and player protocol."""
import collections as C,json,re
from arabia01_install import *

def run():
    v=load('VALIDATION.json');assert v['technical_status']=='PASS_STATIC_ONLY'
    applied=load('APPLIED.json');now=runtime();base=load('PREPARED.json')['world_before'];ours={z['file'] for z in applied['files']}
    for z in applied['files']:assert sha(ROOT/z['file'])==z['after_sha256'],z['file']
    others=[dict(file=r,before=base.get(r),after=now.get(r)) for r in sorted(set(base)|set(now)) if base.get(r)!=now.get(r) and r not in ours]
    dump('CURRENT_RUNTIME_MANIFEST.json',now);dump('CONCURRENT_RUNTIME_DELTA.json',others)
    # Additional independent reference checks: definitions and assets in effective files.
    defs=C.defaultdict(list)
    for p in effective('common/country_definitions'):
        for n in parse(text(p)):defs[n.key].append(str(p))
    flags={n.key:n for p in effective('common/flag_definitions') for n in parse(text(p))}
    coas={n.key:n for p in effective('common/coat_of_arms/coat_of_arms') for n in parse(text(p))}
    checks={}
    for t in ['NEJ','A91','A92']:
        checks[t+'_unique_definition']=len(defs[t])==1
        checks[t+'_flag_defined']=t in flags
        checks[t+'_coa_defined']='aor1776_arabia_'+t.lower() in coas
    checks['solid_pattern_exists']=any((p/'gfx/coat_of_arms/patterns/pattern_solid.tga').exists() for p in [ROOT,GAME])
    nejchars=[]
    for p in effective('common/history/characters'):
        for n in walk(parse(text(p))):
            if n.key=='c:NEJ':nejchars.append(text(p)[n.start:n.end])
    checks['NEJ_1836_templates_absent']=all('NEJ_faisal_al_saud' not in s and 'NEJ_saud_al_saud' not in s for s in nejchars)
    checks['NEJ_1776_named_ruler_present']=any('aor1776_abdulaziz_bin_muhammad_bin_saud' in s for s in nejchars)
    dump('REFERENCE_AUDIT.json',dict(checks=checks,concurrent_runtime_changes=others));assert all(checks.values()),checks
    ps=state_nodes(text(ROOT/PP));pop={}
    for sid in SCOPE:
        pop[sid]={r.key.split(':')[1]:sum(int(p.one('size')) for p in r.children('create_pop')) for r in ps[sid].children()}
    dump('INSTALLED_POP_TOTALS.json',pop)
    inherited=[]
    for z in load('TECH_AFTER.json'):
        if z['TAG'] not in ['NEJ','A91','A92']:
            inherited.append(dict(tag=z['TAG'],findings=z['findings']))
    dump('PREEXISTING_WARNINGS.json',inherited)
    files='\n'.join('- `'+z['file']+'`' for z in applied['files'])
    table='\n'.join('| '+sid+' | '+', '.join(t+' : '+format(n,',').replace(',',' ') for t,n in d.items())+' |' for sid,d in pop.items())
    report=f'''# ARABIA-01 — Première installation territoriale, 1er janvier 1776

**Statut : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Installation du 29 octobre 2026. Aucune validation en jeu réalisée ou attribuée au joueur pour ce lot.

## Résultat installé

- Réactivation de **NEJ, Émirat de Diriyah**, sur cinq provinces du noyau Riyad/Diriyah–Washm–Sudayr. Abdulaziz ben Muhammad ben Saoud remplace les personnages vanilla de 1836 ; l'âge est une approximation à partir de l'année 1720.
- Création de **A91, Banu Khalid**, sur vingt provinces côtières et oasiennes : dix-sept de `STATE_HAIL`, trois de `STATE_NEJD`. Il s'agit du noyau al-Hasa/Qatif, pas d'une certification de toutes les zones d'influence tribale. Souverain personnel non nommé faute de succession suffisamment vérifiée après 1774.
- Création de **A92, Communautés du Qatar**, sur deux provinces de `STATE_ABU_DHABI`. Ensemble décentralisé collectif ; ce n'est ni un État Al Thani ni une conquête de Bahreïn anticipée.
- **BHN** conserve l'île de Bahreïn, sous un nouveau lien de sujet envers **PER**. Le pacte `puppet` sert d'approximation du gouvernorat perse de Nasr al-Madhkur ; ses droits et prélèvements vanilla ne sont pas un traité historique reproduit.
- Les cinq provinces yéménites de Tihama précédemment données à **HDJ** passent à **ZAI**. Le reste du Hedjaz et sa relation ottomane sont préservés, ainsi que Lahj, Mahra, Hadramawt et Oman existants.

Total : **32 transferts de provinces**, deux nouveaux TAGs et un TAG réactivé. Aucun State_ID ni RGB nouveau ; bitmap inchangé. Les nouvelles bannières sont décoratives, pas des drapeaux historiques attestés.

## Population, économie et démarrage

Le stock entier du fichier moyen-oriental reste de **{v['population_before']:,} habitants avant/après**, sans ajout démographique. Toutes les combinaisons culture/religion/statut et leurs effectifs sont conservées à l'échelle de chaque State_ID. La répartition entre propriétaires au Najd et au Qatar est un **choix technique de gameplay**, pas un recensement de 1776 ni une estimation par surface. Voir `POP_REDISTRIBUTION_LEDGER.json`. Les catégories héritées discutables, dont les 231 Bédouins orthodoxes orientaux, n'ont pas été effacées ni présentées comme vérifiées historiquement.

| Région du jeu | Populations initiales après transfert |
| --- | --- |
{table}

Les niveaux des bâtiments civils déjà présents sont conservés dans les deux fichiers qui les déclarent. Le ranch et la route du Najd vont à NEJ, le ranch côtier à A91, la pêche du bloc BHN à A92. Les plantations de café ZAI et HDJ sont fusionnées à trois niveaux pour éviter deux créations concurrentes du même bâtiment ; le port de Tihama est transféré à ZAI. Les participations de propriété suivent les nouveaux détenteurs.

Ajouts explicites : **un port commercial traditionnel A91 et un BHN**, sans chantier naval moderne ; **une unité de conscription irrégulière NEJ et une A91**. Ces deux levées sont des minima de gameplay, pas une mesure des armées de 1776. Aucun habitant n'est ajouté pour les créer. Le recrutement est confié au mécanisme natif, sans caserne dupliquée dans l'histoire civile.

Profils technologiques explicites modestes pour NEJ/A91/A92, sans copie d'un palier industriel. Le commerce caravanier et côtier utilise une variante locale du mercantilisme, limitée à ces TAGs et sans exiger une technologie bancaire postérieure. Les autres lois génériques restent des abstractions du moteur, pas une description exhaustive de leurs institutions historiques.

**Accès au marché, emploi, nourriture et rentabilité ne sont pas certifiés par ces fichiers.** Bahreïn nécessite le contrôle maritime ci-dessous. Les capitaux des portions partagées et les ports secondaires peuvent être déplacés par les choix de hubs du moteur.

## Vérifications exécutées

Commandes : `tools/arabia01.py --plan`, `tools/arabia01_install.py --prepare`, `--apply`, `--repair-profiles`, `--audit`, puis `tools/arabia01_closeout.py`, avec le Python local. Préparation en staging, sauvegarde de chaque préimage et comparaison de toutes les empreintes avant écriture. Pas de restauration générale d'une baseline ancienne.

- **{len(v['checks'])} contrôles ciblés réussis** dans `VALIDATION.json` : les 32 changements correspondent au plan ; les {v['scope_provinces']} provinces des six régions ont chacune un propriétaire ; aucune cellule cible impassable ; noyaux NEJ/A91/A92 connectés par des arêtes de pixels.
- Stock de POPs et niveaux civils conservés ; contenus syntaxiques des régions extérieures identiques aux préimages dans les quatre fichiers partagés.
- NEJ/A91/A92 : `PASS_STATIC_ONLY` pour technologies, recettes, lois demandées et unités. Les premières erreurs détectées sur les nouveaux profils ont été corrigées ; les résultats finaux ne les masquent pas par suppression des contrôles.
- Définitions et références nouvelles, localisation française/anglaise avec BOM et clés uniques, bannières et souverain NEJ contrôlés séparément dans `REFERENCE_AUDIT.json` et `LOCALIZATION_AUDIT.json`.
- Les pays hérités NBB/BHN/ZAI/HDJ gardent des avertissements ou erreurs antérieurs, notamment des demandes de lois avec prérequis absents. `TECH_BEFORE.json`, `TECH_AFTER.json`, `TECH_DELTA.json` et `PREEXISTING_WARNINGS.json` les distinguent : **aucun nouveau signal dans ces pays**. Ce lot ne rend pas l'ensemble du Moyen-Orient techniquement exempt de dette.
- Changements de runtime concurrents hors fichiers de ce lot depuis la préparation : **{len(others)}**, conservés et recensés dans `CONCURRENT_RUNTIME_DELTA.json`. Les travaux africains présents avant la préparation ne sont pas écrasés. Aucun fichier des corrections américaines, du suivi WORLD ou du SERG n'a été édité par ce lot.

Un contrôle statique n'est ni un chargement moteur, ni une validation visuelle, ni une homologation humaine. Les détails de quartiers, les villes historiques supplémentaires et les frontières exactes ne sont pas créés par les repères de l'aperçu.

## Réserves et suite bornée

1. **Koweït** : le RGB natif du port `x00F060`, `STATE_BASRA`, reste IR1. Lorimer p. 1002 le décrit comme dépendant de Bassora en 1775, tout en attestant une chefferie locale Sabah. Le degré de dépendance à traduire en pacte, le partage démographique et le port de Bassora doivent être traités ensemble. Ne pas installer une indépendance pleine sur le seul nom du chef.
2. **Qawasim / Musandam** : le repère de Ras al-Khaimah et Khasab partagent `x0DC972`. Le transfert intégral ferait perdre Musandam à Oman sans preuve. Un découpage de province doit précéder une correction sûre.
3. **Qasim et frontières intérieures** : chronologies contradictoires et contrôle tribal discontinu ; aucune extension saoudienne maximale des années 1780–1810 anticipée. Les enveloppes des provinces restent des approximations.
4. **Oman, Bani Yas, Asir et chefferies méridionales** : les noyaux existants sont conservés ; la granularité tribale et les dépendances ne sont pas déclarées historiquement closes.
5. Démographie fine, équilibre fiscal et militaire, placement de hubs secondaires : réserves ouvertes. Les coordonnées modernes des aperçus ne créent pas de villes accessibles à la recherche interne.

Ce lot ne clôture donc pas la péninsule à 100 %. La prochaine passe territoriale utile est **Koweït et interface du Golfe**, puis le découpage Qawasim/Musandam après correspondance historique plus précise. Aucun dénominateur WORLD ou SERG n'a été modifié pour lui donner des points.

## Fichiers de runtime modifiés ou créés

{files}

Outils et preuves : `tools/arabia01.py`, `tools/arabia01_install.py`, `tools/arabia01_closeout.py` et ce dossier. `PREPARED.json`, `APPLIED.json`, les préimages et les reçus de réparation conservent la trace des versions. Aucun commit, merge, rebase ou push. Vanilla consulté en lecture seule.

## ColGrep local

Un appel exploratoire `C:/Users/simeo/.cargo/bin/colgrep.exe --agent <question de localisation Arabie> .` a été tenté. Échec après environ **1,94 seconde**, au verrou d'index sous `%APPDATA%/colgrep/indices/1776_Age_of_Revolutions_fork-9f9c61cb/.lock`, accès refusé (erreur système 5). Aucune configuration ni intégration modifiée, aucun index reconstruit, aucun modèle installé. Repli sur `rg` et lecture ciblée des dossiers R3 et des dépendances.

**L'exécution du modèle 2B n'est pas confirmée pour cette passe.** Aucun décompte fiable des recherches classiques ou des tokens Codex n'est exposé ; aucune économie de quota n'est revendiquée.
'''
    (OUT/'REPORT.md').write_text(report.replace(f"{v['population_before']:,}",format(v['population_before'],',').replace(',',' ')),encoding='utf8')
    protocol='''# ARABIA-01 — Contrôles dans Victoria 3

Statut initial : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Nouvelle partie au **1er janvier 1776**, mod principal courant. Une ancienne sauvegarde peut conserver ses anciens propriétaires.

1. À la sélection des pays, repérer **Émirat de Diriyah**, **Banu Khalid**, **Communautés du Qatar**, **Bahreïn**, **Yémen/Zaïdites** et le Hedjaz. Utiliser les pays ou les régions Nejd, Hail, Abu Dhabi et Yémen ; ne pas chercher des villes créées uniquement comme repères de documentation. Les noms d'État dynamiques peuvent varier selon leur propriétaire.
2. Vérifier le petit noyau NEJ à Riyad/Diriyah au centre du Najd, A91 le long de Qatif/al-Hasa sur la côte du Golfe, BHN uniquement sur l'île au nord-ouest du Qatar, A92 sur la péninsule. Voir `INSTALLED_ARABIA.png` et les RGB exacts de `PLAN.json`. Ce dessin de travail n'est pas une capture du moteur.
3. NEJ doit avoir Abdulaziz ben Muhammad ben Saoud, sans Faisal de 1836. A91 ne possède pas de chef personnel historiquement certifié ; un personnage généré n'est pas une preuve historique.
4. Vérifier la relation PER → BHN et l'absence d'un Qatar BHN ; le Hedjaz reste dans son lien ottoman existant. Le littoral de Hodeida/Mokha appartient à ZAI, pas HDJ. Contrôler les îlots de frontières à plusieurs niveaux de zoom.
5. Ouvrir les populations des portions : NEJ Nejd 53 000 ; A91 Nejd 29 700 et Hail 61 914 ; NBB Nejd 21 847 ; BHN Abu Dhabi 15 619 ; A92 Abu Dhabi 9 286. Vérifier les catégories d'habitants, pas seulement la somme mondiale. ZAI doit recevoir les 54 060 habitants du littoral sans disparition des autres habitants.
6. Contrôler le ranch et la route de NEJ, le ranch côtier A91, la pêche A92, le café ZAI (3 niveaux), le port yéménite transféré et les deux ports commerciaux ajoutés A91/BHN. Vérifier les propriétaires financiers et l'absence de double plantation. Les doubles déclarations héritées dans les fichiers 08 et 98 ne prouvent pas un double niveau en jeu : contrôler la valeur effectivement chargée.
7. Laisser tourner quelques semaines : marché et port de Bahreïn accessibles depuis la Perse, denrées et prix sans pénurie imputable à une rupture nouvelle ; routes/ports et emplois actifs. Le continent doit permettre des parcours continus dans les noyaux NEJ et A91. Pas de pont de terre vers Bahreïn. Vérifier que les deux levées irrégulières peuvent être mobilisées sans unités ni casernes dupliquées.
8. Sauvegarder puis recharger ; mêmes propriétaires, populations cohérentes après évolution naturelle, relations conservées et absence de crash. Relever les nouvelles erreurs moteur séparément des erreurs préexistantes.

Les réserves Koweït, Qawasim/Musandam et chronologies du Qasim restent ouvertes, même si tous ces contrôles passent. Aucun statut PASS_RUNTIME_USER_VALIDATED ne doit être attribué sans retour explicite du joueur sur la version livrée.
'''
    (OUT/'RUNTIME_PROTOCOL.md').write_text(protocol,encoding='utf8')
    dump('STATUS.json',dict(lot='ARABIA-01',reference_date='1776-01-01',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',technical_status='PASS_STATIC_ONLY',new_technology_profiles='PASS_STATIC_ONLY',historical_closure='OPEN_TARGETED_RESERVES',human_validation=False,engine_test=False,province_transfers=32,scope_provinces=v['scope_provinces'],files=applied['files'],next_action='Kuwait and Gulf dependency interface; Qawasim/Musandam requires a mapped province split. Runtime protocol remains pending.',colgrep=dict(agent_calls=1,failed_before_confirmed_model_execution=True,seconds_approx=1.94,exact_codex_tokens=None)))
    parent=OUT.parent
    (parent/'CURRENT.json').write_text(json.dumps(dict(current_lot='ARABIA-01',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',report='ARABIA-01/REPORT.md',runtime_protocol='ARABIA-01/RUNTIME_PROTOCOL.md',regional_closure=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(checks=len(v['checks']),reference_checks=checks,concurrent_changes=len(others),population=v['population_after'],files=len(applied['files']),status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION')))

if __name__=='__main__':run()
