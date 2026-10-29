"""Explicit WORLD African country replacements and bounded tributary repair.

This patches database entry modes, not the substantive contents of the country
definitions. Old reports/manifests are preserved as historical evidence.
"""
import argparse,json,shutil
from pathlib import Path
import world1776_southern01 as h
import validate_starting_technology_1776 as tech
ROOT=h.ROOT;WORLD=h.LOT.parent;LOT=WORLD/'AFRICA-POLITY-FIX-01'
DIP='common/history/diplomacy/1776_world_interior01.txt'
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']
def dump(n,v):h.save(LOT/n,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(n):return json.loads((LOT/n).read_text('utf-8-sig'))
def delivered():
 rows={r['file']:dict(r) for r in load('FILES_MODIFIED.json')}
 if (LOT/'SYNTAX_REPAIR.json').exists():
  for r in load('SYNTAX_REPAIR.json')['files']:rows[r['file']]['after']=r['after']
 return list(rows.values())
def mode(key):
 if ':' in key:
  a,z=key.split(':',1)
  if a in ['REPLACE','REPLACE_OR_CREATE','TRY_REPLACE','INJECT','TRY_INJECT','INJECT_OR_CREATE']:return a,z
 return 'CREATE',key
def intended():return h.b.a.catalog('common/country_definitions')
def resolve():
 """Model explicit modes; conflicting bare duplicates never silently replace."""
 result={};ignored=[]
 for path in h.b.tech.effective('common/country_definitions'):
  for n in h.b.parse(h.raw(path)):
   m,t=mode(n.key)
   if m=='CREATE' and t in result:ignored.append(dict(TAG=t,file=str(path),kept_source=str(result[t][1])));continue
   if m in ['REPLACE','TRY_REPLACE'] and t not in result:
    if m=='REPLACE':raise AssertionError(('replace_missing_country',t,path))
    continue
   assert m not in ['INJECT','TRY_INJECT','INJECT_OR_CREATE'],'Review field injection semantics if present'
   result[t]=(n,path)
 return result,ignored
def candidates():
 seen={};out=[]
 for path in h.b.tech.effective('common/country_definitions'):
  for n in h.b.parse(h.raw(path)):
   m,t=mode(n.key)
   if t in seen and path.is_relative_to(ROOT) and path.name.startswith('1776_world_') and not any(x in path.name for x in ['balkans','maghreb']) and m=='CREATE':
    out.append(dict(file=path.relative_to(ROOT).as_posix(),TAG=t,previous_source=str(seen[t][1]),previous_type=seen[t][0].one('country_type'),intended_type=n.one('country_type'),capital=n.one('capital')))
   seen[t]=(n,path)
 return out
def pacts():
 rows=[]
 def visit(n,actor=None,path=None):
  if n.key.startswith('c:'):actor=n.key[2:]
  if n.key=='create_diplomatic_pact' and n.one('type')=='tributary':rows.append(dict(overlord=actor,subject=n.one('country').removeprefix('c:'),file=str(path.relative_to(ROOT))))
  for c in n.children():visit(c,actor,path)
 for path in h.b.tech.effective('common/history/diplomacy'):
  if path.is_relative_to(ROOT) and path.name.startswith('1776_world_'):
   for n in h.b.parse(h.raw(path)):visit(n,path=path)
 return rows
def apply():
 LOT.mkdir(exist_ok=True);assert not (LOT/'FILES_MODIFIED.json').exists(),'Already applied'
 plan=candidates();assert len(plan)==49 and len({r['file'] for r in plan})==7,'Reread changed scope'
 dump('PLAN.json',plan);regs,ignored=resolve();snap=tech.collect_snapshot()
 tags=sorted({r['TAG'] for r in plan}|{t for r in pacts() for t in [r['overlord'],r['subject']]})
 dump('TECH_BEFORE.json',[tech.audit_country(t,snap) for t in tags])
 dump('ENTRY_RESOLUTION_BEFORE.json',dict(ignored=ignored,countries={t:dict(type=regs[t][0].one('country_type'),source=str(regs[t][1])) for t in tags}))
 sources=sorted({r['file'] for r in plan}|{DIP});old={r:h.raw(ROOT/r) for r in sources};hashes={r:h.b.a.sha(ROOT/r) for r in sources};out={}
 for rel in sources:
  text=old[rel]
  if rel==DIP:
   n=h.b.one(text,'c:LND');assert len(n.children('create_diplomatic_pact'))==1
   pact=n.children('create_diplomatic_pact')[0];assert pact.one('country')=='c:KZM' and pact.one('type')=='tributary'
   out[rel]=h.b.edits(text,[(pact.start,pact.end,'\n# AFRICA-POLITY-FIX-01: distant Kazembe remains independent; dynastic tribute is not a shared-market subject pact.\n')])
  else:
   ops=[]
   for r in plan:
    if r['file']!=rel:continue
    n=h.b.one(text,r['TAG']);assert text[n.start:n.start+len(r['TAG'])]==r['TAG'];ops.append((n.start,n.start+len(r['TAG']),'REPLACE_OR_CREATE:'+r['TAG']))
   out[rel]=h.b.edits(text,ops)
 h.prior.m.s.g.LOT=LOT
 before=dict(inventory=h.prior.m.s.b4.inventory(),protected=h.prior.m.s.g.protection(),hashes=hashes,pacts=pacts(),historical_start='1776-01-01')
 for text in out.values():h.b.parse(text)
 dump('BEFORE.json',before)
 for r in sources:
  p=LOT/'apply_inputs'/r;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/r,p)
 assert all(h.b.a.sha(ROOT/r)==sha for r,sha in hashes.items()),'Concurrent change; reread'
 for r,t in out.items():
  assert h.b.a.sha(ROOT/r)==hashes[r];h.save(ROOT/r,t,(ROOT/r).read_bytes().startswith(b'\xef\xbb\xbf'))
 dump('FILES_MODIFIED.json',[dict(file=r,before=hashes[r],after=h.b.a.sha(ROOT/r)) for r in sources]);print('Installed:49 explicit replacements in7 definition files; Kazembe pact removed;8 functional files')
def validate():
 checks=[]
 def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
 before=load('BEFORE.json');plan=load('PLAN.json');files=delivered();regs,ignored=resolve();cat=intended()
 for rec in files:
  rel=rec['file'];a=h.raw(LOT/'apply_inputs'/rel);z=h.raw(ROOT/rel);ck('delivered_hash.'+rel,h.b.a.sha(ROOT/rel)==rec['after'])
  if rel!=DIP:
   # Removing the inserted mode prefix must restore the entire original bytes.
   ck('only_entry_modes_changed.'+rel,z.replace('REPLACE_OR_CREATE:','')==a)
   for r in [r for r in plan if r['file']==rel]:
    nn=h.b.one(z,'REPLACE_OR_CREATE:'+r['TAG']);old=h.b.one(a,r['TAG'])
    ck('definition_body_unchanged.'+r['TAG'],z[nn.start:nn.end].replace('REPLACE_OR_CREATE:','',1)==a[old.start:old.end])
    actual,path=regs[r['TAG']];ck('explicit_effective_definition.'+r['TAG'],path==ROOT/rel and actual.one('country_type')==r['intended_type'] and actual.one('capital')==r['capital'])
  else:
   an=h.b.one(a,'c:LND');zn=h.b.one(z,'c:LND');ck('other_diplomacy_preserved',h.b.edits(a,[(an.start,an.end,'<LND>')])==h.b.edits(z,[(zn.start,zn.end,'<LND>')]))
 for r in pacts():
  for role in ['overlord','subject']:ck('nondecentralized_tributary.'+r['overlord']+'.'+r['subject']+'.'+role,regs[r[role]][0].one('country_type')!='decentralized')
 ck('Kazembe_no_world_overlord',not any(r['subject']=='KZM' for r in pacts()))
 ck('Luba_Kanyok_preserved',any(r['overlord']=='LBA' and r['subject']=='KNY' for r in pacts()))
 ck('no_remaining_bare_WORLD_african_duplicates',not candidates())
 now=h.prior.m.s.b4.inventory();ck('world_population',now['world_population']==before['inventory']['world_population']);ck('all_world_RGB_owners',now['owners']==before['inventory']['owners']);ck('Git_identity_index',now['git']==before['inventory']['git'])
 reviewed={}
 if (LOT/'EXTERNAL_COMPOSITION_REVIEW.json').exists():
  review=load('EXTERNAL_COMPOSITION_REVIEW.json');external=json.loads(h.raw(ROOT/review['manifest']))
  for rec in review['files']:
   original=next(r for r in external if r['file']==rec['file'])
   assert original['before_sha256']==before['protected'][rec['file']] and original['after_sha256']==rec['after_sha256']
   reviewed[rec['file']]=rec['after_sha256']
 if (LOT/'PLAYER_TEST_UPDATE.json').exists():
  update=load('PLAYER_TEST_UPDATE.json');rel=update['file'].replace('\\','/');assert update['before']==before['protected'][rel];reviewed[rel]=update['after']
 edited={r['file'] for r in files};outside=[r for r,sha in before['protected'].items() if r not in edited and (not (ROOT/r).exists() or h.b.a.sha(ROOT/r) not in [sha,reviewed.get(r)])];ck('all_other_protected_files_preserved_or_verified_external',not outside,outside)
 snap=tech.collect_snapshot();after=[tech.audit_country(r['TAG'],snap) for r in load('TECH_BEFORE.json')];previous={r['TAG']:r for r in load('TECH_BEFORE.json')};delta=[]
 for r in after:
  old=previous[r['TAG']];a={json.dumps(f,sort_keys=True) for f in old['findings'] if f['priority'] in ['P0','P1']};z={json.dumps(f,sort_keys=True) for f in r['findings'] if f['priority'] in ['P0','P1']};new=[json.loads(x) for x in sorted(z-a)]
  ck('technologies_unchanged.'+r['TAG'],r['technologies']==old['technologies']);ck('no_new_P0_P1.'+r['TAG'],not new,new);delta.append(dict(TAG=r['TAG'],introduced=new,inherited_remaining=[json.loads(x) for x in sorted(a&z)]))
 dump('TECH_AFTER.json',after);dump('TECH_NON_REGRESSION.json',delta)
 # Observed native adjacency, never an invented corridor.
 geo=json.loads((WORLD/'INTERIOR-01/GEOMETRY_CHECK.json').read_text('utf8'));neighbor={r['TAG']:r['neighbors'] for r in geo}
 for t in ['LND','LBA','KZM','KNY']:
  ck('central_core_has_central_neighbor.'+t,any(regs[n][0].one('country_type')!='decentralized' for n in neighbor[t]))
 ck('Kanyok_touches_Luba','LBA' in neighbor['KNY']);ck('Lunda_Kazembe_noncontiguous_preserved','KZM' not in neighbor['LND'])
 result=dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,engine_retest='NOT_RUN',human_success_attested=False,entry_mode_resolution_is_static_model=True)
 dump('VALIDATION.json',result);dump('PACT_AUDIT.json',dict(before=before['pacts'],after=pacts(),country_types={t:regs[t][0].one('country_type') for r in pacts() for t in [r['overlord'],r['subject']]}));dump('CONCURRENT_CHANGES.json',dict(outside_scope_changes=outside,Git_writes=0,vanilla_writes=0,SERG_writes=0,geometry_writes=0,baseline_restored=False))
 print('Validation',result['status'],result['passed'],'/',result['total']);print('Failures',[r for r in checks if not r['passed']]);return result['status']=='PASS'
def report():
 v=load('VALIDATION.json');before=load('BEFORE.json');pop=before['inventory']['world_population']
 h.save(LOT/'REPORT.md',f'''# AFRICA-POLITY-FIX-01 — chargement des statuts et tributaires\n\n29 octobre 2026. IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Correctif autorisé par les signalements du joueur : Kanyok tributaire d'un Luba décentralisé, puis Lunda et Kazembe décentralisés et non contigus. Les captures prouvent le problème signalé, pas un succès après correction ; date en jeu, durée et sauvegarde inconnues.\n\n## Cause et correction\n\nLe vanilla définit LBA/LND/KZM/MSH/MNC décentralisés ; les fichiers WORLD les redéfinissaient sans mode explicite. Le validateur précédent choisissait systématiquement la dernière définition et masquait ce défaut. Les remplacements doivent être explicites avec le mode de base de données prévu par les versions récentes. La correction ajoute REPLACE_OR_CREATE: aux49 redéfinitions africaines préexistantes de7 fichiers WORLD. Le contenu des49 définitions est strictement identique : catégories, cultures, couleurs, capitales et tiers restent les décisions historiques déjà installées. Les nouveaux TAG restent des créations simples. Il ne s'agit pas de centraliser indistinctement les communautés : leurs catégories décentralisées sont également préservées, y compris Luyana, les communautés du Karoo et les chefferies sotho.\n\nLuba, Lunda et Kazembe deviennent donc effectivement déclarés comme États non reconnus centralisés, de même que les autres pouvoirs dont la déclaration était ignorée. Tous les10pactes tributaires WORLD africains conservés ont des acteurs non décentralisés dans le modèle explicite. Les rangs, la diplomatie permise au joueur, les lois effectivement retenues et les budgets demandent une observation moteur ; aucun prestige ni technologie ni armée n'est créé pour forcer leur conformité.\n\nKanyok garde son lien au Luba et le touche déjà. Le pacte Lunda→Kazembe est retiré : Kazembe reste indépendant, sans annexion ni corridor. Une dépendance historique éloignée n'est pas impossible par principe ; sa traduction par le sujet de marché du jeu était ici trop forte et peu adaptée à la demande du joueur. Source historique : Ndaywel è Nziem, UNESCO V ch20 pp651,659-660, PDF local INTERIOR-01/sources/UNESCO_LUBA_LUNDA.pdf réellement relu. La source décrit une royauté structurée, un Kazembe autonome et des tributs attestés notamment dans les années1790 ; elle ne certifie pas le partage économique moteur en1776.\n\n## Conservation et preuves\n\n8 fichiers fonctionnels ciblés :7fichiers de définitions (seules49clés changées) et le seul pacte LND→KZM de la diplomatie INTERIOR-01. Aucun pixel/RGB/frontière, POP, bâtiment/PM, technologie, loi, personnage ou formation militaire modifié. Monde : {pop:,}→{pop:,}, delta0 ; tous les propriétaires RGB inchangés. Les pays des autres chantiers et les versions courantes sont conservés ; pas de Git, vanilla ou suiviSERG écrit. Préimages immédiates et empreintes : apply_inputs/ et FILES_MODIFIED.json. Les anciens reçus ne sont pas écrasés : ce correctif s'applique au-dessus de leur version historique.\n\n{v['passed']}/{v['total']} contrôles statiques, détail VALIDATION.json ; résolution sans remplacement implicite, invariance des corps de définition, audit des pactes, technologies et non-régression, voisinages, conservation des fichiers protégés. La résolution explicite est un modèle statique ; aucun chargement corrigé n'est encore attesté en jeu.\n\nLe test africain groupé reste en cours. La zone5 a un défaut rapporté par le joueur, aucun critère V entier ni succès inventé. WORLD10/320(3,13%) inchangé. Le guide est corrigé : Kazembe doit désormais être indépendant ; Kanyok doit rester tributaire d'un Luba centralisé. Les déclarations modifiées requièrent un redémarrage et une nouvelle partie pour vérifier l'initialisation ; aucun correctif silencieux de la sauvegarde ouverte n'est prétendu.\n''')
 dump('USER_FINDINGS.json',dict(observed_on='2026-10-29',status='USER_REPORTED_PROBLEM',claims=['Kanyok tributary of decentralized Luba','Lunda and Kazembe decentralized','Lunda and Kazembe have no common land border'],screenshots=['C:/Users/simeo/AppData/Local/Temp/codex-clipboard-a2b7eaf7-98d0-4ddc-be40-075333f7ddc6.png','C:/Users/simeo/AppData/Local/Temp/codex-clipboard-94a408c6-117c-4ce3-aa73-a404b73f2c92.png'],game_date=None,new_game_confirmed=None,simulation_duration=None,save_reload_confirmed=None,post_fix_success=False))
 h.save(LOT/'REPRODUCE.md','Python runtime : tools/world1776_africa_polity_fix01.py --validate. Ne pas rejouer --apply. Les anciens validateurs WORLD utilisent une résolution implicite erronée ; les anciens reçus restent historiques, et ce correctif porte sa propre validation. Aucun résultat moteur n’est déduit des statiques.\n')
def tracking():
 assert not (LOT/'TRACKING_PATCHES.json').exists();hashes={n:h.b.a.sha(WORLD/n) for n in TRACK}
 for n in TRACK:p=LOT/'tracking_inputs'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORLD/n,p)
 data=json.loads(h.raw(WORLD/'ROADMAP_STATE.json'));data['lots'].append(dict(id='AFRICA-POLITY-FIX-01',date='2026-10-29',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',country_entry_mode_repairs=49,existing_files_modified=8,territory_changes=0,population_delta=0,removed_pact='LND->KZM',human_problem_reported=True,post_fix_runtime='NOT_RUN',credited_criteria=[],receipt='AFRICA-POLITY-FIX-01/FILES_MODIFIED.json'))
 data['steering_history'].append(data['current_steering']);data['current_steering']=dict(date='2026-10-29',authority='AFRICA-POLITY-FIX-01/USER_FINDINGS.json',last_lot='AFRICA-POLITY-FIX-01',scope='Repair country database replacement modes and remove distant Kazembe subject pact',next_pass='Continue grouped African player test; no automatic new region',runtime_validation_timing='GROUPED_AFRICA',intermediate_player_tests_requested=False,full_V_credit=False)
 assert data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320
 entry='\n\n## AFRICA-POLITY-FIX-01 —29 octobre2026\n\nDéfauts joueur Kanyok/Luba et Lunda/Kazembe enregistrés, sans succès ou durée inventés.49redéfinitions africaines WORLD passent en remplacement explicite, corps identiques ; le validateur précédent masquait les doublons implicites. Pacte lointain LND→KZM retiré, LBA→KNY conservé.8fichiers fonctionnels ciblés, aucune géométrie/population/bâtiment/technologie/armée modifiée. Contrôles VALIDATION.json, application sur versions courantes et préimages ; anciens reçus conservés. Centralisation déclarée des royaumes enfin chargeable, communautés autonomes préservées. Reprise du test africain groupé après correction, aucun autre secteur lancé, WORLD10/320(3,13%) inchangé.\n'
 assert all(h.b.a.sha(WORLD/n)==s for n,s in hashes.items())
 h.save(WORLD/'ROADMAP_STATE.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
 h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'\n\n## AFRICA-POLITY-FIX-01 — chargement à revérifier\n\nSignalement joueur : pays décentralisés avec tributaires ; correction des modes de remplacement installée, succès moteur non attesté. Kazembe désormais indépendant ; Kanyok reste tributaire du Luba centralisé. Les rangs et lois effectives ne sont pas certifiés par un parseur. Frontières et anciennes limites cartographiques inchangées ; poursuite du test africain groupé, pas de nouvelle attestation V.\n')
 h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'\n\n## AFRICA-POLITY-FIX-01 — périmètre\n\nSeulement49préfixes de clés dans7 fichiers country_definitions/1776_world africains, et suppression du seul pacte LND→KZM dans la diplomatie Interior. Aucun corps de définition ou fichier technique partagé modifié. Pas de frontière/pixel/corridor, démographie, graphe TECH, recettes, armée, vanilla, Git ou suiviSERG. PLAN.json et préimages font référence ; les changements concurrents sont conservés.\n')
 h.save(WORLD/'NEXT_ACTION.md','# Prochaine action — test africain groupé en cours\n\nLire AFRICA-POLITY-FIX-01/REPORT.md, USER_FINDINGS.json, PACT_AUDIT.json, VALIDATION.json et FILES_MODIFIED.json. La zone5 présente un défaut observé avant correction : Luba/Lunda/Kazembe décentralisés. Remplacements explicites installés pour les49 déclarations WORLD africaines concernées ; pacte Lunda–Kazembe retiré, Kanyok–Luba maintenu. Aucun territoire déplacé.\n\nContinuer le contrôle africain groupé avec le guide révisé : Kazembe indépendant, royaumes centralisés déclarés. Redémarrage/nouvelle partie nécessaires pour observer cette nouvelle initialisation ; ne pas déclarer l’ancienne sauvegarde réparée ni un succès joueur non reçu. Pas de test supplémentaire par sous-lot, autre région ou lissage lancé automatiquement. WORLD10/320(3,13%),aucun crédit V nouveau.\n')
 con=json.loads(h.raw(WORLD/'CONCURRENT_CHANGES.json'));con['AFRICA-POLITY-FIX-01']=dict(receipt='AFRICA-POLITY-FIX-01/CONCURRENT_CHANGES.json',functional_files=8,entry_mode_repairs=49,geometry_changes=0,population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0);h.save(WORLD/'CONCURRENT_CHANGES.json',json.dumps(con,ensure_ascii=False,indent=2)+'\n')
 dump('TRACKING_PATCHES.json',[dict(file=str((WORLD/n).relative_to(ROOT)),before=hashes[n],after=h.b.a.sha(WORLD/n)) for n in TRACK])
def final():
 v=load('VALIDATION.json');assert v['status']=='PASS'
 data=json.loads(h.raw(WORLD/'ROADMAP_STATE.json'));techcredits=sum(c['status']=='STATIC_VERIFIED' for p in data['phases'] for r in p['subregions'] for c in r['criteria'].values());humans=sum(c['status']=='USER_VALIDATED' for p in data['phases'] for r in p['subregions'] for c in r['criteria'].values());assert techcredits==10 and humans==0
 dump('PROGRESS_CALCULATION.json',dict(technical_verified=techcredits,criteria_total=320,technical_percent=3.13,human_credit=humans,newly_credited=[]))
 dump('FILES_DELIVERED.json',delivered())
 files=[ROOT/r['file'] for r in delivered()]+[LOT/n for n in ['PLAN.json','BEFORE.json','FILES_MODIFIED.json','FILES_DELIVERED.json','SYNTAX_REPAIR.json','ENTRY_RESOLUTION_BEFORE.json','VALIDATION.json','TECH_BEFORE.json','TECH_AFTER.json','TECH_NON_REGRESSION.json','PACT_AUDIT.json','CONCURRENT_CHANGES.json','REPORT.md','USER_FINDINGS.json','REPRODUCE.md','TRACKING_PATCHES.json','PROGRESS_CALCULATION.json','SOURCES.md','EXTERNAL_COMPOSITION_REVIEW.json','PLAYER_TEST_UPDATE.json','AFRICAN_OWNERSHIP_RECHECK.json']]+list((LOT/'sources').glob('*'))+[WORLD/n for n in TRACK]
 dump('DELIVERY_MANIFEST.json',{str(p.relative_to(ROOT)):h.b.a.sha(p) for p in files});print('Final: progress10/320 unchanged; post-fix runtime NOT_RUN')
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['apply','validate','report','tracking','final']:p.add_argument('--'+k,action='store_true')
 a=p.parse_args()
 if a.apply:apply()
 if a.validate and not validate():raise SystemExit(1)
 if a.report:report()
 if a.tracking:tracking()
 if a.final:final()
