"""Read-only Malagasy political screening. Writes only its audit and WORLD tracking."""
import argparse,json,shutil
from collections import Counter
from datetime import datetime,timezone
import world1776_interior01 as h
import world1776_sahel0205_closeout as poptool

ROOT=h.ROOT
WORLD=h.LOT.parent
LOT=WORLD/'MADAGASCAR-01-AUDIT'
SID=['STATE_NORTH_MADAGASCAR','STATE_SOUTH_MADAGASCAR']
TRACK=['ROADMAP.md','ROADMAP_STATE.json','NEXT_ACTION.md','BLOCKERS.md','PROGRESS_HISTORY.md','OWNERSHIP_BOUNDARIES.md','CONCURRENT_CHANGES.json']

def read(p):return json.loads(p.read_text('utf-8-sig'))
def doc(name,text):h.save(LOT/name,text)
def dump(name,data):doc(name,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(p):return h.b.a.sha(p)

def protected():
    paths=[]
    for folder in ['common','events','gui','localization','map_data','gfx/map/map_object_data']:
        paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.txt','.yml','.gui','.json','.png'])
    return {p.relative_to(ROOT).as_posix():sha(p) for p in paths}

def snapshot():
    text=h.raw(ROOT/h.ST);own=h.prior.m.state_owners(text)
    regions=h.b.a.catalog('map_data/state_regions');countries=h.b.a.catalog('common/country_definitions')
    n,p=countries['MAD'];pops=Counter()
    for path in h.b.tech.effective('common/history/pops'):pops.update(poptool.portions(h.raw(path)))
    states=[]
    for s in SID:
        r,path=regions[s];colors=h.prior.m.s.ids(r,'provinces')
        states.append(dict(state=s,native_RGBs=colors,native_unique_count=len(set(colors)),owners={c:own.get(c,[]) for c in colors},population={t:v for (ss,t),v in pops.items() if ss==s},state_node=text[h.b.one(text,'s:'+s).start:h.b.one(text,'s:'+s).end]))
    return dict(captured_utc=datetime.now(timezone.utc).isoformat(),historical_date='1776-01-01',country=dict(TAG='MAD',source=str(p),definition=h.raw(p)[n.start:n.end],country_type=n.one('country_type'),capital=n.one('capital'),tier=n.one('tier')),states=states,world_population=sum(pops.values()),madagascar_population=sum(v for (s,t),v in pops.items() if s in SID),functional_hashes=protected(),country_history_sha256=sha(ROOT/'common/history/countries/mad - madagascar.txt'),dynamic_name_sha256=sha(ROOT/'common/dynamic_country_names/00_dynamic_country_names.txt'))

def audit():
    assert not (LOT/'BASELINE.json').exists(),'Audit already captured; inspect existing proof.'
    LOT.mkdir(parents=True,exist_ok=True);before=snapshot();dump('BASELINE.json',before)
    for name in TRACK:
        src=WORLD/name;dest=LOT/'tracking_inputs'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    findings=[dict(id='M01',priority='P0_HISTORICAL_TERRITORIAL',finding='One MAD owner for all122 native provinces; unified island inappropriate for1776.',mapping_status='NOT_INSTALLED'),dict(id='M02',priority='P1_HISTORICAL_TERRITORIAL',finding='Imerina royal centres must be distinguished before later consolidation.',mapping_status='NATIVE_RGB_MAPPING_REQUIRED'),dict(id='M03',priority='P1_POLITICAL_CLASSIFICATION',finding='Separate organised royal states from autonomous communities; no blanket decentralisation.',mapping_status='REGIONAL_AUTHORITY_REVIEW_REQUIRED'),dict(id='M04',priority='P1_HISTORICAL_MODEL',finding='Tributary reach is not direct provincial administration.',mapping_status='DEPENDENCY_AND_COURT_REVIEW_REQUIRED')]
    dump('FINDINGS.json',dict(status='AUDIT_COMPLETE_TERRITORIAL_WORK_REMAINS',findings=findings,new_RGBs=0,territorial_transfers=0,functional_writes=0,new_human_validation=False))
    doc('REPORT.md',f'''# MADAGASCAR-01-AUDIT — contrôle demandé avant l'Afrique australe

28 octobre2026 ; référence1janvier1776. **AUDIT_COMPLETE_TERRITORIAL_WORK_REMAINS**. Audit documentaire et des scripts, aucune correction territoriale installée.

## État réel du mod

Les deux régions moteur sont attribuées intégralement à **MAD** : **60 provinces au nord et62 au sud,122 RGB uniques**. La définition effective héritée du vanilla est `unrecognized`, `kingdom`, culture `malagasy`, capitale NORTH_MADAGASCAR. Ce type est un État organisé dans le moteur ; il ne signifie pas reconnaissance internationale. Le nom dynamique du mod utilise `dyn_c_merina_kingdom`, traduit en français natif par «Royaume Mérina», lorsque ses conditions monarchiques sont remplies. Le rendu en jeu n'a pas été observé ici.

## Conclusion historique

Le nom à employer est **merina / Imerina**, non Médina. En1776, l'Imerina reste partagée entre cours rivales, notamment Ambohimanga, Antananarivo et Ambohidratrimo. Boina et Menabe sont d'autres royaumes ; les formations betsileo demandent leur propre examen, notamment l'ascendant d'Isandra. Les Tsimihety offrent au contraire un cas de communautés sans royaume centralisé. Sources : Kent p.923,944–951 ; Berg1988, extrait public.

Le défaut certain est donc l'**unification de toute l'île sous MAD**. La proportion exacte à classer décentralisée n'est pas établie : il faut restaurer plusieurs pouvoirs organisés et les autonomies locales, pas décentraliser indistinctement tous les territoires extérieurs à l'Imerina. Les dates d'accession/conquête divergent selon les études ; aucune date précise ni généalogie nouvelle n'est installée.

## Travail territorial à préparer

FINDINGS.json énumère quatre problèmes. Délimiter les noyaux royaux et les communautés depuis les cellules actuelles ; vérifier droits tributaires, contrôle effectif et autonomie avant tout pacte. Examiner séparément l'interface betsimisaraka et les établissements européens en1776. Une carte ethnique ou une liste de dynasties ne vaut pas découpage cadastral daté. Aucun nouveau TAG ou RGB proposé comme déjà validé. Respecter la règle d'absence de nouvelle enclave centralisée ; ne pas inventer de corridor pour forcer la continuité.

## Données et contrôles

Population native du périmètre : **{before['madagascar_population']:,}** ; monde : **{before['world_population']:,}**. Aucune population transférée, aucun bâtiment, PM, profil technologique, personnage, pacte ou localisation fonctionnelle écrit. Tous les RGB et blocs lus sont conservés dans BASELINE.json avec empreintes. VALIDATION.json vérifie les références natives, les attributions et l'absence de modification pendant l'audit ; ce n'est ni un chargement moteur ni une validation historique des frontières.

Git, vanilla et suiviSERG non écrits. Les travaux INTERIOR-01, Congo, Corne, TECH/ECON, SERG et américains restent dans leur version courante. Les modifications extérieures éventuellement survenues pendant l'audit sont seulement consignées, jamais annulées. WORLD demeure10/320(3,13%), aucun point entier ni reçu humain.

**Prochaine action : correction cartographique de Madagascar depuis cet audit, avant la reprise de l'Afrique australe.** Le contrôle demandé est terminé ; les nouveaux propriétaires précis restent à installer dans une passe territoriale.
''')
    doc('SOURCES.md','''# Sources effectivement consultées

- R.K.Kent, «Madagascar et les îles de l'océan Indien», Histoire générale de l'Afrique,V, ch.28,p.921–967. [PDF public](https://bokundoli.org/wp-content/uploads/2021/12/T5-30.pdf). Texte consulté par l'outil web : p.921–923,944–951,959. Pas de lecture intégrale revendiquée ; téléchargement local échoué, aucune copie PDF locale. Carte28.1 ethnique signalée dans le texte, pas examinée ni utilisée comme frontière.
- Gerald M.Berg, «Sacred Acquisition: Andrianampoinimerina at Ambohimanga,1777–1790», Journal of African History29(2),1988,p.191–211, [extrait sur Cambridge](https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/sacred-acquisition-andrianampoinimerina-at-ambohimanga-17771790/EBA65FD0322C0EA8D5B77EBE801598F8). Extrait lu, article intégral non consulté. Sa chronologie du pouvoir à Ambohimanga diffère des datations simplifiées ; aucun souverain daté artificiellement.
- [UNESCO/ICOMOS,évaluation Ambohimanga2001](https://whc.unesco.org/document/1118) et [fiche patrimoniale](https://whc.unesco.org/en/list/950/), passages historiques consultés ; portée monumentale, pas carte des juridictions1776.
- [Ellis2007,notice de l'African Studies Centre Leiden](https://www.ascleiden.nl/publications/tom-and-toakafo-betsimisaraka-kingdom-and-state-formation-madagascar-c1715-1750) : bibliographie seulement ; article intégral non lu, aucune frontière1776 tirée du seul titre1715–1750.
- [Larousse](https://www.larousse.fr/encyclopedie/divers/Madagascar_histoire/187014), synthèse ouverte : corroboration générale seulement. La chronologie imprimée comporte une incohérence avec la succession Radama ; pas de date ou de titulaire installé depuis cette notice.
- MAP1, dossiers R7-0111 et0144 : pistes héritées relues, anciens propriétaires/RGB non utilisés comme vérité courante. Les122cellules sont recomptées dans le workspace réel.
''')
    doc('USER_REQUEST.txt',"«Non, avant de parler de l'Afrique australe, vérifie le royaume de Médina, si tant est qu'il s'appelait comme ça à l'époque. Je crois qu'une trop grande partie de Madagascar est centralisée.»\nPortée de cette passe : vérification et audit ; aucun partage territorial précis demandé ou installé.\n")
    validate()

def validate():
    before=read(LOT/'BASELINE.json');now=snapshot();checks=[]
    def ck(k,v):checks.append(dict(check=k,passed=bool(v)))
    colors=[c for r in now['states'] for c in r['native_RGBs']]
    ck('native_60_north_62_south', [r['native_unique_count'] for r in now['states']]==[60,62])
    ck('122_distinct_native_RGBs',len(colors)==len(set(colors))==122)
    ck('current_single_owner_MAD',all(v==[[r['state'],'MAD']] for r in now['states'] for v in r['owners'].values()))
    ck('organised_unrecognized_kingdom',now['country']['country_type']=='unrecognized' and now['country']['tier']=='kingdom')
    ck('all_Madagascar_nodes_preserved',now['states']==before['states'])
    ck('population_world_unchanged',now['world_population']==before['world_population'])
    ck('population_Madagascar_unchanged',now['madagascar_population']==before['madagascar_population'])
    ck('national_definition_unchanged',now['country']==before['country'])
    ck('national_history_unchanged',now['country_history_sha256']==before['country_history_sha256'])
    ck('dynamic_name_unchanged',now['dynamic_name_sha256']==before['dynamic_name_sha256'])
    external=[dict(file=r,before=v,after=now['functional_hashes'].get(r)) for r,v in before['functional_hashes'].items() if now['functional_hashes'].get(r)!=v]
    dump('CONCURRENT_CHANGES.json',dict(observed_external_changes=external,functional_writes_by_this_audit=0,Git_writes=0,vanilla_writes=0,SERG_writes=0,old_baseline_restored=False))
    dump('VALIDATION.json',dict(status='PASS' if all(r['passed'] for r in checks) else 'FAIL',passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,scope='Read-only audit integrity, not historical or runtime acceptance',automated_engine_test=False,human_validated=False))
    assert all(r['passed'] for r in checks)
    print('Audit integrity PASS',len(checks),'checks;',len(external),'external file changes observed; no functional writes.')

def tracking():
    assert not (LOT/'TRACKING_PATCHES.json').exists(),'Tracking already updated.'
    versions={n:sha(WORLD/n) for n in TRACK};data=read(WORLD/'ROADMAP_STATE.json')
    assert not any(r['id']=='MADAGASCAR-01-AUDIT' for r in data['lots'])
    assert data['progress']['technical_verified']==10 and data['progress']['criteria_total']==320
    data['lots'].append(dict(id='MADAGASCAR-01-AUDIT',date='2026-10-28',status='AUDIT_COMPLETE_TERRITORIAL_WORK_REMAINS',functional_writes=0,native_RGBs_reviewed=122,territorial_findings=4,receipt='MADAGASCAR-01-AUDIT/VALIDATION.json',credited_criteria=[],runtime='NOT_RUN'))
    data['steering_history'].append(data['current_steering']);data['current_steering']=dict(date='2026-10-28',authority='MADAGASCAR-01-AUDIT/USER_REQUEST.txt',last_lot='MADAGASCAR-01-AUDIT',scope='Madagascar review requested before southern Africa; audit complete, territorial correction pending',next_pass='Resolve Malagasy political fragmentation and map native royal cores before resuming southern Africa',cosmetic_smoothing_deferred=True,runtime_validation_timing='GROUPED_AFRICA',intermediate_player_tests_requested=False,full_V_credit=False)
    for phase in data['phases']:
        for r in phase['subregions']:
            if r['id']=='P3-09':r['criteria']['O'].update(status='PARTIAL',evidence='MADAGASCAR-01-AUDIT/REPORT.md',remaining='Unified MAD assignment confirmed anachronistic; royal/communal native-cell mapping and corrections not installed. No whole criterion credited.')
    count=sum(c['status']=='STATIC_VERIFIED' for p in data['phases'] for r in p['subregions'] for c in r['criteria'].values());assert count==10
    entry='\n\n## MADAGASCAR-01-AUDIT —28octobre2026\n\nConsigne directe : vérifier Madagascar avant l’Afrique australe. Audit achevé,4problèmes territoriaux/classification documentés ;122RGB examinés,aucun transfert ni écriture fonctionnelle. Noms dynamiques et populations lus sur version courante, preuves MADAGASCAR-01-AUDIT/REPORT.md et VALIDATION.json. Corrections cartographiques encore à installer, frontière précise non certifiée. Aucun point entier ni reçu humain ; WORLD10/320(3,13%). Suite australe différée derrière ce point.\n'
    assert all(sha(WORLD/n)==v for n,v in versions.items())
    h.save(WORLD/'ROADMAP_STATE.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    for n in ['ROADMAP.md','PROGRESS_HISTORY.md']:h.save(WORLD/n,h.raw(WORLD/n).rstrip()+entry)
    h.save(WORLD/'BLOCKERS.md',h.raw(WORLD/'BLOCKERS.md').rstrip()+'\n\n## Madagascar — audit28octobre2026\n\nM01–M04 dans MADAGASCAR-01-AUDIT/FINDINGS.json. Le découpage politique précis et les différences d’autonomie restent à installer. Pas de passage à l’Afrique australe sur la seule base du précédent NEXT_ACTION ; suivre la nouvelle consigne directe. Aucun nouveau test moteur/joueur ni crédit.\n')
    h.save(WORLD/'OWNERSHIP_BOUNDARIES.md',h.raw(WORLD/'OWNERSHIP_BOUNDARIES.md').rstrip()+'\n\n## MADAGASCAR-01-AUDIT\n\nLecture seule des deux nœuds NORTH/SOUTH_MADAGASCAR, de MAD, de ses POP et de son nom dynamique. Aucune cellule, POP, technologie, loi, bâtiment, personnage, localisation ou relation écrit. Seuls les rapports de ce lot et le suivi WORLD sont actualisés. SERG/TECH/ECON/Amériques et lots africains conservés.\n')
    h.save(WORLD/'NEXT_ACTION.md','# Prochaine action — après MADAGASCAR-01-AUDIT\n\nAudit demandé avant l’Afrique australe achevé : lire MADAGASCAR-01-AUDIT/REPORT.md, SOURCES.md, BASELINE.json, FINDINGS.json et VALIDATION.json. Aucune correction fonctionnelle installée par l’audit. Préparer la restauration territoriale de Madagascar en distinguant pouvoirs organisés et communautés autonomes ; établir les correspondances RGB à partir des noyaux historiques, sans frontière arbitraire.\n\nL’Afrique australe/VOC vient ensuite. Préserver INTERIOR-01 et les autres lots, TECH/ECON, SERG et Amériques ; aucune ancienne baseline à réinstaller. Aucun flavor ni lissage cosmétique lancé. Tests africains groupés, aucun test intermédiaire demandé ni reçu humain ajouté. WORLD10/320(3,13%).\n')
    concurrent=read(WORLD/'CONCURRENT_CHANGES.json');concurrent['MADAGASCAR-01-AUDIT']=dict(receipt='MADAGASCAR-01-AUDIT/CONCURRENT_CHANGES.json',functional_writes=0,territorial_transfers=0,world_population_delta=0,Git_writes=0,vanilla_writes=0,SERG_writes=0)
    h.save(WORLD/'CONCURRENT_CHANGES.json',json.dumps(concurrent,ensure_ascii=False,indent=2)+'\n')
    dump('TRACKING_PATCHES.json',[dict(file=n,before=versions[n],after=sha(WORLD/n)) for n in TRACK])

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for k in ['audit','validate','tracking']:parser.add_argument('--'+k,action='store_true')
    a=parser.parse_args()
    if a.audit:audit()
    if a.tracking:tracking()
    if a.validate:validate()
