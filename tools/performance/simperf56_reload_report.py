"""Build the follow-up report from completed measurements, never placeholders."""
from pathlib import Path
from datetime import datetime,timezone
import csv,json,re
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'docs/reports/performance/INITIAL_SIMULATION_ISSUE56_2026_11_17'
ROUND=REPORT/'RELOAD_EXPERIMENT_2026_11_17'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
data={name:load(ROUND/file) for name,file in {'MATURE1':'MATURE_BEFORE_RESTART.json','RELOAD1':'RELOAD1_RESULTS.json','RELOAD2':'RELOAD2_RESULTS.json','INIT_REF1':'INIT_REF1_RESULTS.json','INFRA_M0':'INFRA_M0_RESULTS.json'}.items()}
save=load(ROUND/'MATURE_SAVE.json');variant=load(ROUND/'INFRA_MONTHLY_VARIANT.json');audit=load(ROUND/'PRESERVATION_AFTER.json')
assert len({d['executable_sha256'] for d in data.values()})==1
assert len({d['settings_sha256'] for d in data.values()})==1
assert all(d['heartbeat_sequence_consecutive'] for d in data.values())
rows=[]
for trial,record in data.items():
    for w in record['heartbeat_windows']:
        if w['window'].startswith('SAVED_PLUS_'):
            rows.append(dict(trial=trial,window=w['window'],start_date=w['start']['date_raw'],end_date=w['end']['date_raw'],simulated_days=w['simulated_days'],wall_seconds=w['wall_seconds'],days_per_second=w['days_per_second'],cpu_machine_percent_approx=w['cpu_machine_percent_approx'],working_set_mib_mean=w['working_set_mib_mean'],clock_error_bound_seconds=1))
def point(trial,offset,length):return next(r for r in rows if r['trial']==trial and r['window']==f'SAVED_PLUS_{offset}_{length}')
def fr(value,digits=1):return f'{value:.{digits}f}'.replace('.',',')
def seconds(trial,offset,length):return fr(point(trial,offset,length)['wall_seconds'],0)+' s'
run=Path(data['INFRA_M0']['run']);traces=[]
for p in (run/'logs').glob('debug*.log'):
    traces.extend(line for line in p.read_text(encoding='utf-8-sig',errors='replace').splitlines() if 'SIM56|DIAG|INFRA_MONTHLY_BYPASSED' in line)
assert traces,'No runtime proof of the monthly bypass: investigate before reporting.'
source=Path(save['path']);import hashlib
assert hashlib.sha256(source.read_bytes()).hexdigest()==save['save_sha256']
for group in ('runtime','normal_profile','git_index','steam_executable','protected_diplomacy','earlier_evidence','existing_performance_tools'):
    assert not audit['groups'][group]['changes'],f'Preservation difference: {group}'
core_table='\n'.join('| '+label+' | '+' | '.join(seconds(t,0,n) for n in (14,28,56))+' |' for t,label in [('MATURE1','Sans redémarrage'),('RELOAD1','Nouveau processus 1'),('RELOAD2','Nouveau processus 2')])
stages='\n'.join('| '+f'J+{offset+1} à J+{offset+15}'+' | '+' | '.join(seconds(t,offset,14) for t in ('MATURE1','RELOAD1','RELOAD2'))+' |' for offset in (0,14,28,42,56,70,84,98))
resources='\n'.join('| '+t+' | '+fr(point(t,0,56)['days_per_second'],3)+' | '+fr(point(t,0,56)['cpu_machine_percent_approx'])+' % | '+fr(point(t,0,56)['working_set_mib_mean']/1024,2)+' |' for t in data)
infra_table='\n'.join('| '+str(n)+' jours | '+seconds('INIT_REF1',0,n)+' | '+seconds('INFRA_M0',0,n)+' |' for n in (14,28,56))
ref=point('INIT_REF1',0,56)['wall_seconds'];off=point('INFRA_M0',0,56)['wall_seconds'];gain=100*(ref-off)/ref
diagnosis=(f'Le retrait mensuel donne un écart de {fr(gain)} % sur les 56 premiers jours. Cette unique ablation ne suffit pas à valider un petit gain ni une optimisation équivalente. Elle ne supprime pas la forte phase lente initiale.' if abs(gain)<10 else f'Un signal de {fr(gain)} % est observé sur les 56 premiers jours. Il faut le répéter dans l’ordre inverse avant de l’attribuer avec confiance ; le retrait modifie aussi les décisions et l’évolution économique, pas seulement le coût direct du code.')
if off>=ref:
    diagnosis=f'Aucun gain net observé : {fr(off,0)} secondes avec ablation contre {fr(ref,0)} pour le témoin sur 56 jours, soit {fr(100*(off-ref)/ref)} % de temps supplémentaire dans cette prise. Cette unique comparaison ne démontre pas une aggravation fiable de quelques pour cent. Elle ne soutient pas la suppression de ce contrôleur comme solution à la forte lenteur initiale.'
text=f'''# Issue 56 — rechargement d’un monde mature et contrôle mensuel régional

17 novembre 2026. Rapport de suivi du bilan initial, conservé sans réécriture.
Référence : main `bd776919f625016cb9e63b2359cc04796c681ef5`.
Issue : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56.

## Conclusion du contrôle prioritaire

**Le ralentissement fort du début de campagne ne revient pas dans les deux rechargements testés du monde mature.** Le processus a été entièrement fermé entre chaque passage. Les mêmes dates simulées et la même sauvegarde sont comparées ; il ne s’agit pas d’une comparaison de démarrages du programme.

| Passage | 14 jours | 28 jours | 56 jours |
|---|---:|---:|---:|
{core_table}

Les premières fenêtres restent dans le même ordre de grandeur que les suivantes. Il n’apparaît pas ici de phase lente transitoire longue après chargement, ni de ralentissement persistant comparable aux premiers mois de 1776. Ce constat porte sur les journées complètes mesurées après la reprise : **le premier jour partiel, la préparation en pause, la durée de chargement et les effets plus courts ne sont pas évalués par ces fenêtres**.

Un contrôle positif contemporain recharge ensuite le monde initial de 1776 : {seconds('INIT_REF1',0,14)} pour les 14 premiers jours et {seconds('INIT_REF1',0,56)} pour 56 jours. Le monde initial reste donc nettement plus lent alors que les fichiers et shaders ont déjà été utilisés pendant les essais. Le simple redémarrage d’un processus ne suffit pas à reproduire cette lenteur dans le monde mature.

Cela oriente vers une propriété persistante du scénario initial et de son évolution : état économique, emploi, marchés, priorités/files IA, situation militaire ou diplomatique, variables temporaires, conditions de date, données ou caches sérialisés. **Cela ne prouve pas que l’économie ou une fonction IA précise est la cause.** Des caches de fichiers et de shaders sont conservés ; ce test n’est pas un redémarrage du PC avec purge de tous les caches.

## Sauvegarde, environnement et indépendance des processus

- Monde créé dans MATURE1 depuis la sauvegarde commune France 1776, puis simulé sans choix d’événement à vitesse 5.
- Sauvegarde mature réelle : **21 avril 1777** (`{save['saved_date']}`), environ seize mois après le départ, {format(save['bytes'],',').replace(',',' ')} octets. La phase lente avait disparu : fenêtre de janvier 1777 à 7 secondes pour 14 jours.
- Fichier : `{source.name}` ; version vérifiée **{save['version']}** ; SHA256 `{save['save_sha256']}`. Le fichier est conservé intact et toutes ses copies vérifiées.
- Après sauvegarde, reprise sans redémarrage pour mesurer DAY S+1 puis les 14/28/56 jours suivants, et les tranches ultérieures. Les pauses de sauvegarde se trouvent avant S+1.
- Fermeture complète du processus MATURE1 (PID16504), puis nouveaux processus RELOAD1 (PID32668) et RELOAD2 (PID30228), sans chevauchement. Les journaux LAUNCH/EXIT sont archivés et la disparition des fenêtres a été contrôlée.
- Même Steam **Victoria 3 1.15.1 sans DLC de gameplay**, même runtime figé, COMPACT, paramètres et sondes. L’installation locale 1.15.0 avec DLC est restée distincte et n’a pas été utilisée.
- Réglages initiaux SHA256 `{data['MATURE1']['settings_sha256']}` ; exécutable SHA256 `{data['MATURE1']['executable_sha256']}`.
- Vue carte France harmonisée en passant par Menu puis Reprendre, sans choisir d’option d’événement. Vitesse 5 avant chaque reprise. Quelques expirations de capture graphique ont été résolues avant mesure par réinitialisation du contrôleur et nouvelle observation ; aucun clic aveugle n’a servi à poursuivre.

## Persistance sur les tranches suivantes

J correspond au jour de sauvegarde S ; la première borne est S+1. Chaque ligne mesure 14 jours entiers aux mêmes dates dans les trois passages.

| Tranche | Sans redémarrage | Rechargement 1 | Rechargement 2 |
|---|---:|---:|---:|
{stages}

Les 56 jours suivants, au-delà de la première fenêtre de 56 jours, prennent {seconds('MATURE1',56,56)}, {seconds('RELOAD1',56,56)} et {seconds('RELOAD2',56,56)}. Il n’y a pas de retour d’une phase de plusieurs mois à environ trois fois le temps initial mature.

## CPU et RAM

Pour les 56 premiers jours de chaque contexte, CPU sur l’ensemble des 16 processeurs logiques et RAM en Gio de working set résident moyen :

| Passage | Jours simulés/s | CPU processus | RAM résidente (Gio) |
|---|---:|---:|---:|
{resources}

Le working set diffère fortement entre processus. Il dépend de la résidence des pages et de Windows ; il ne représente pas toute l’allocation privée et ne démontre pas une cause mémoire. Les applications tierces, la mémoire globale, les fréquences CPU/GPU et le premier plan ne sont pas entièrement contrôlés. Les petits écarts de quelques pour cent ne sont pas présentés comme des gains certains. Aucun FPS moyen fiable n’a été collecté.

## Expérience suivante choisie et exécutée : IA régionale mensuelle seule

Le monde mature reste rapide après redémarrage, tandis que le monde initial rechargé reste lent. L’expérience suivante vise donc un travail périodique dans cet état initial, en priorité le contrôleur mensuel d’infrastructures régional. INIT_REF1 et INFRA_M0 repartent du même fichier initial, SHA256 `387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2`.

Une seule différence de runtime : `{variant['changed_files'][0]}`. Seul le corps du child `aor1776_ai_regional_infrastructure_monthly` est retiré. Le hook natif et ses autres enfants, l’initialisation régionale, le HRE quotidien et mensuel, la carte, les pays, les lois, la technologie et l’histoire restent inchangés dans les fichiers.

Source SHA256 `{variant['source_sha256']}` ; diagnostic `{variant['diagnostic_sha256']}`. **{len(traces)} traces de bypass mensuel ont été effectivement observées**, en plus de la vérification du montage et des empreintes. Le coût de ces traces est inclus.

| Intervalle initial | Témoin contemporain | Mensuel régional désactivé |
|---|---:|---:|
{infra_table}

{diagnosis}

Le coût net comprend les conséquences des décisions retirées ; il ne s’agit pas d’un profil CPU interne de cette seule fonction. L’ablation n’est **pas** une correction préservant le gameplay. Elle n’est ni intégrée, ni fusionnée, ni proposée comme optimisation prête à installer.

L’initialisation régionale avait déjà été appliquée avant la sauvegarde initiale commune. Ce test ne retire que son activité mensuelle ultérieure ; il n’exonère ni cette initialisation ni ses conséquences persistantes. Pour isoler l’initialisation elle-même, il faudrait une comparaison dédiée de nouvelles campagnes, et non désactiver son hook en rechargeant une sauvegarde où ses effets sont déjà présents.

## Incertitudes et portée

Les bornes sont les timestamps natifs HH:mm:ss des logs, avec erreur de résolution inférieure à une seconde sur une différence. Les arrivées des lignes sont tamponnées et ne servent jamais de chronomètre. Les fichiers WINDOW d’arrivée restent des diagnostics provisoires ; seuls les résultats d’analyse native sont utilisés.

CPU cumulé et working set sont suivis à 500 ms puis alignés sur les bornes UTC (Paris UTC+1 en novembre 2026). Aucun CPU de démarrage, compilation de shaders ou menu n’est attribué à une fenêtre de simulation. Le calendrier moteur compte 365 jours ; les sondes vérifient la continuité des dates. Les contrôles n’ont pas le pouvoir statistique de certifier un petit effet et ne séparent pas l’ensemble des mécanismes persistants. Les décisions IA peuvent diverger après rechargement malgré le même point de départ.

Les essais sont en mode debug et comportent les mêmes sondes DAY. L’alerte de métadonnée commune et les erreurs héritées restent à distinguer des nouvelles erreurs éventuelles du diagnostic. Cette étude ne valide pas les performances de l’autre installation 1.15.0 avec DLC.

## Prochaines étapes recommandées

1. Isoler **le child mensuel HRE seul**, dans une autre copie depuis la sauvegarde initiale, en gardant les routines quotidiennes et le contrôleur régional normal. La précédente ablation quotidienne n’exonère pas tout le HRE. Ne pas combiner les deux suppressions.
2. Si le contrôle régional donne un signal reproductible, distinguer les tris d’États, remises à zéro de variables, invalidations et choix de PM ; chercher ensuite seulement une réduction équivalente de calculs. Une répétition dans l’ordre inverse est nécessaire pour les petits écarts.
3. Si les contrôles scriptés n’expliquent pas l’écart, profiler les traitements natifs IA/emploi/marchés et les files ou données persistantes du départ. Examiner aussi les conditions de date et les variables à durée limitée. Le rechargement rapide ne prouve pas une initialisation économique précise.
4. Une série 1.15.0 avec DLC doit rester séparée. Aucune suppression artificielle de pays, POP ou contenu historique pour obtenir un meilleur chiffre.

## Préservation et fichiers produits

Audit final : {audit['groups']['runtime']['unchanged']}/{audit['groups']['runtime']['checked']} fichiers runtime normaux identiques ; {audit['groups']['normal_profile']['unchanged']}/{audit['groups']['normal_profile']['checked']} fichiers suivis du profil et des sauvegardes normaux identiques ; trois fichiers Russie–Kazakh, index Git et exécutable inchangés. Les {audit['groups']['earlier_evidence']['checked']} preuves antérieures protégées sont conservées. L’analyseur préparé a reçu un argument facultatif d’ancres DAY ; sa version précédente exacte est archivée et la régression des anciennes mesures vérifiée. Aucun travail préexistant n’a été supprimé.

La configuration de préparation est étendue par profils uniques avec archivage avant chaque ajout. Aucun Git d’écriture, aucun commit/push/fusion, aucune modification des installations normales ni du mod principal. Les diagnostics sont exclusivement dans le laboratoire Temp.

Preuves : `MATURE_SAVE.json`, profils, LAUNCH/EXIT et logs par passage ; `MATURE_BEFORE_RESTART.json`, `RELOAD1_RESULTS.json`, `RELOAD2_RESULTS.json`, `INIT_REF1_RESULTS.json`, `INFRA_M0_RESULTS.json`, `MEASUREMENTS.csv`, `INFRA_MONTHLY_VARIANT.json`, audit avant/après et protocole. La sauvegarde mature est désormais disponible pour répéter les contrôles sans refaire toute l’année.

**Statut : contrôle de rechargement exécuté et répété ; l’enquête sur la cause initiale reste ouverte. Aucun correctif de production validé.**
'''
with (ROUND/'REPORT_FR.md').open('x',encoding='utf-8') as out:out.write(text)
with (ROUND/'MEASUREMENTS.csv').open('x',encoding='utf-8-sig',newline='') as out:
    writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
summary=dict(utc=datetime.now(timezone.utc).isoformat(),mature_save=save,core_results={t:{str(n):point(t,0,n)['wall_seconds'] for n in (14,28,56)} for t in data},infra_56day_wall_time_delta_percent=-gain,infra_56day_time_reduction_percent=gain,infra_trace_count=len(traces),production_patch=False,issue_state_recommended='open',report_sha256=hashlib.sha256((ROUND/'REPORT_FR.md').read_bytes()).hexdigest())
with (ROUND/'SUMMARY.json').open('x',encoding='utf-8') as out:json.dump(summary,out,indent=2,ensure_ascii=False)
print(json.dumps(summary,indent=2,ensure_ascii=False))
