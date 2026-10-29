"""Global starting-ruler layer: private files, conservative research, static checks.

--install captures the current workspace and adds only four new gameplay files.
--validate does not edit gameplay. No Git writes and no vanilla writes.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse, hashlib, json, re
import audit_anzin_regional_infrastructure as a
import audit_starting_tech_1776 as tech
from validate_diplomacy_ottoman_1776 import parse, walk, scalar, normalized
from localization_duplicate_audit import entries
import world1776_balkans04 as b4
import world1776_nordic01 as nordic

ROOT = a.ROOT
OUT = ROOT / 'docs/reports/characters/WORLD_RULERS_1776_R1'
PREFIX = 'aor1776_wr1'
FILES = ['common/character_templates/1776_world_rulers_r1.txt',
         'common/history/characters/zz_1776_world_rulers_r1.txt'] + [
         f'localization/{lang}/1776_world_rulers_r1_l_{lang}.yml' for lang in ['french','english']]

def save(name, value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def load(name):
    return json.loads((OUT/name).read_text(encoding='utf8'))

def label(path):
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else 'VANILLA:'+path.relative_to(a.GAME).as_posix()

def inventory():
    countries = a.catalog('common/country_definitions')
    active = defaultdict(set)
    for n in walk(parse(a.raw(ROOT/'common/history/states/00_states.txt'))):
        if n.key.startswith('s:STATE_'):
            for st in n.children('create_state'):
                owner = st.one('country')
                if owner: active[owner.removeprefix('c:')].add(n.key[2:])
    templates = a.catalog('common/character_templates')
    unresolved = []
    def resolve(n, seen=()):
        result = {}
        parent = n.one('template')
        if parent and parent not in templates:
            # Existing suppressed vanilla templates are evidence of debt, not
            # permission to restore 1836 characters during a 1776 ruler pass.
            result['unresolved_template'] = parent
        elif parent:
            assert parent not in seen, ('template cycle', parent)
            result.update(resolve(templates[parent][0], seen+(parent,)))
        result.update({x.key:scalar(x.value) for x in n.children() if not isinstance(x.value,list)})
        return result
    rulers = defaultdict(list)
    executives = []
    unions = {}
    def visit(nodes, country, path, mode):
        for n in nodes:
            ctx = n.key[2:] if n.key.startswith('c:') else country
            if n.key=='create_character' and ctx:
                fields = resolve(n)
                if fields.get('unresolved_template'):
                    unresolved.append(dict(country=ctx,file=label(path),template=fields['unresolved_template']))
                if fields.get('ruler')=='yes' or fields.get('role')=='ruler':
                    rulers[ctx].append(dict(file=label(path),line=a.raw(path)[:n.start].count('\n')+1,**fields))
                if fields.get('company') and fields.get('historical')=='yes':
                    executives.append(dict(country=ctx,file=label(path),**fields))
            if mode=='diplomacy' and ctx and n.key=='create_diplomatic_pact' and n.one('type')=='personal_union':
                unions[n.one('country').removeprefix('c:')]=dict(overlord=ctx,file=label(path))
            visit(n.children(), ctx, path, mode)
    for folder in ['characters','military_formations','countries','diplomacy']:
        for path in tech.effective('common/history/'+folder):
            visit(parse(a.raw(path)),None,path,folder)
    names = entries('french')
    initial = {x['TAG']:x for x in load('INVENTORY_WITH_NAMES.json')}
    rows = []
    for tag, states in sorted(active.items()):
        n = countries[tag][0]
        rs = rulers[tag]
        name = initial.get(tag,{}).get('name') or (names[tag][-1][2] if tag in names else tag)
        rows.append(dict(TAG=tag,name=name,kind=n.one('country_type'),cultures=a.ids(n,'cultures'),
                         states=sorted(states),rulers=rs,status='HAS_SCRIPTED_HISTORICAL_RULER' if any(
                         r.get('historical')=='yes' for r in rs) else 'SCRIPTED_UNCERTIFIED_RULER' if rs else 'NO_SCRIPTED_RULER'))
    return dict(countries=rows,unions=unions,executives=executives,unresolved_templates=unresolved)

def texts(profiles):
    templates=['# WORLD RULERS R1. Research and uncertainty: docs/reports/characters/WORLD_RULERS_1776_R1/',
               '# Birth year alone uses an approximate age; no invented exact birthday.',
               '# IG / ideology / vanilla traits are explicit gameplay interpretations.']
    history=['# Deterministic historical identities; existing historical characters remain untouched.','CHARACTERS = {']
    loc={lang:['l_'+lang+':',f' {PREFIX}_empty:0 ""'] for lang in ['french','english']}
    for p in profiles:
        key=PREFIX+'_'+p['TAG'].lower()
        templates += [f'\n# {p["TAG"]}: sources '+', '.join(p['source_ids']),key+' = {',
          f' first_name = {key}_name', f' last_name = {PREFIX}_empty', ' historical = yes',
          ' ruler = yes', ' culture = cu:'+p['culture'], ' female = '+('yes' if p['female'] else 'no'),
          ' interest_group = '+p['interest_group'], ' ideology = '+p['ideology']]
        if p['religion']: templates.append(' religion = rel:'+p['religion'])
        if p['age'] is not None: templates += [' # Generation estimate from the sourced year/range, not an archival birthday.',f' age = {p["age"]}']
        else: templates.append(' # Birth and age unknown: leave native age generation in place.')
        templates += [' traits = { '+' '.join(p['traits'])+' }',' trait_generation = { }','}']
        history.append(' c:'+p['TAG']+' ?= { create_character = { template = '+key+' } }')
        name=p['full_name']
        for lang in loc:
            if lang=='english': name_en=name.replace(' de Waldburg',' von Waldburg')
            else: name_en=name
            loc[lang].append(f' {key}_name:0 "{name_en}"')
    history += ['}']
    return {FILES[0]:'\n'.join(templates)+'\n',FILES[1]:'\n'.join(history)+'\n',
            **{FILES[2+i]:'\n'.join(loc[lang])+'\n' for i,lang in enumerate(['french','english'])}}

OVERRIDES = {
 'RAG':('DEFER_EXACT_OFFICEHOLDER','Le recteur change mensuellement ; identité exacte de janvier1776 non établie. Placeholder procédural explicitement conservé. Voir BALKANS-02.'),
 'KHR':('DEFER_SOURCE_GAP','Le souverain exact du noyau Kharan n’est pas établi dans les preuves DP ; ne pas transformer un nom de lignée en individu.'),
 'MAK':('DEFER_SOURCE_GAP','Le titulaire exact du Makran en janvier1776 n’est pas établi dans les preuves DP ; personnage procédural conservé.'),
 'HAR':('DEFER_CONFLICT','Les listes consultées divergent entre Ahmad ibn Abi Bakr et Muhammad ibn Yusuf pour1755–1782. Aucune fusion de noms ; édition primaire à consulter.'),
 'TGR':('DEFER_CONFLICT','Mikael Sehul est donné mort en1775 dans une notice et en1777/78/80 dans d’autres ; son statut après1772 est discuté. Ne pas certifier sa présence au1er janvier1776.'),
 'GJA':('DEFER_CONFLICT','Akopyan, ONS197, donne Muhammad Hasan1760–1780 ; des listes distinguent un frère Muhammad1768–1780. L’identité exacte n’est pas suffisamment réconciliée.'),
 'SRV':('DEFER_AUTHORITY','Aghasi et Muhammad Said : pouvoir conjoint, captivité et domination de Quba nécessitent une chronologie précise ; pas de double titulaire supposé.'),
 'ABK':('DEFER_SOURCE_GAP','Zurab Shervashidze est une piste plausible ; seule une notice dérivée a été retrouvée, sans passage primaire suffisamment vérifié.'),
 'NAK':('DEFER_SOURCE_GAP','Vali Quli1773–1781 est une piste de liste compilée ; identité non confirmée par une source assez étayée dans cette passe.'),
 'TAL':('DEFER_SOURCE_GAP','Qara Khan / Jamal al-Din : titres et bornes diffèrent selon les listes ; passage biographique primaire non recoupé.'),
 'ARK':('DEFER_SOURCE_GAP','Sanda Thumana1774–1777 est la piste correcte, et non Sanda WimalaII1777 ; les listes remontent à une chronique non directement vérifiée. Pas de naissance copiée.'),
 'URT':('DEFER_TRANSITION','Sceaux de Fazil Biy en1770/71 et activité de son fils Khudoyar plus tard : date de transmission antérieure ou postérieure à janvier1776 non établie.'),
 'QTG':('DEFER_SOURCE_GAP','Karategin : pas de titulaire individuel de1776 étayé dans les sources consultées ; ne pas rétroprojeter les begs du XIXe siècle.'),
 'KLB':('DEFER_SOURCE_GAP','Kulob : titulaire individuel de1776 non établi ; généalogies tardives insuffisantes.'),
 'LBA':('DEFER_CONFLICT','Chronologies orales d’Ilunga Sungu, Kasongo Lukenge et de la succession1775 divergentes ; ne pas utiliser Kumwimba Ngombe plus tardif.'),
 'LND':('DEFER_TRANSITION','Succession Nawej Muteba/Cikombe vers1775 non assez recoupée. Les titres Mwant Yav ne fournissent pas seuls une identité.'),
 'BMB':('DEFER_CHRONOLOGY','Les listes orales bemba présentent télescopages et divergences (Roberts, Chronology of the Bemba). Titulaire exact de1776 non certifié.'),
 'FTR':('DEFER_TRANSITION','Révolution au FoutaToro au cours de1776 : ne pas placer automatiquement AbdulKader Kane ou Sulayman Baal au pouvoir le1er janvier.'),
 'HAU':('DEFER_CONFLICT','Gobir : les pistes distinguent Dan Gudi1770–1777 de Yakuba1795–1801 ; ne pas installer Yakuba ou Bawa trop tôt sur une liste mal alignée.'),
 'KEB':('DEFER_SOURCE_GAP','Kebbi : Sulemana1775–1803 est la piste, pas son fils Muhammadu Hodi1803–1826. Liste primaire non vérifiée dans cette passe.'),
 'KTS':('DEFER_TRANSITION','Katsina : transition située en1776 dans les listes ; pas de jour ni chronologie primaire suffisante pour sélectionner le titulaire initial.'),
 'ZAZ':('DEFER_SOURCE_GAP','Zazzau : Yamusa est une piste de listes, mais les passages scientifiques consultés n’établissent pas assez sûrement le titulaire du départ.'),
 'DAU':('DEFER_SOURCE_GAP','Daura : pas de chronologie personnelle de1776 suffisamment recoupée dans les sources consultées.'),
 'NUP':('DEFER_SOURCE_GAP','Nupe : Iysa est une piste, mais l’année et le titulaire doivent être recoupés dans une histoire dynastique avant ajout.'),
 'A91':('DEFER_TRANSITION','BanuKhalid : successions et coups de1774–1775 entre héritiers d’Urayir non assez recoupés ; ne pas nommer un individu sur simple mémoire.'),
 'AWS':('DEFER_CONFLICT','Aussa : listes divergentes sur le nom/patronyme du successeur de Kadhafo (1749–1779). Pas d’assimilation automatique d’un nom dynastique au souverain.'),
 'SNR':('DEFER_TRANSITION','Sennar : BadiV/AdlanII, succession située en1776, date précise non établie ; pas de permutation au1er janvier par convention.'),
 'SLQ':('DEFER_SOURCE_GAP','Shilluk : Kudit wad Okon1770–1780 est une piste de tableau communautaire ; les passages scientifiques dépouillés ne corroborent pas précisément cette séquence.'),
 'TQL':('DEFER_SOURCE_GAP','Taqali : Ismail est une piste ; source précise de sa période de règne non vérifiée dans cette passe.'),
 'FZN':('DEFER_SOURCE_GAP','Fezzan : dynastie AwladMuhammad établie, mais porteur individuel du titre au1er janvier1776 non identifié ; ne pas utiliser un souverain mentionné en1807.'),
 'WAA':('DEFER_SOURCE_GAP','Waalo : succession après Naatago Aram et guerre civile ; les extraits consultés de Barry ne certifient pas un brak unique pour janvier1776.'),
 'JLF':('DEFER_SOURCE_GAP','Jolof : noms Birayamb/Biram Yamb renvoient à plusieurs périodes ; aucune équivalence personnelle forcée.'),
 'XIN':('DEFER_APPOINTMENT','Ili : poste impérial de général, pas un nouveau souverain héréditaire ; titulaire exact du1er janvier1776 à vérifier dans les registres de nominations Qing.'),
 'MGL':('DEFER_APPOINTMENT','Uliastai : nominations et homonymies des princes Qing à vérifier avant attribution ; aucune indépendance ajoutée.'),
 'YUN':('DEFER_APPOINTMENT','Yungui : pas de vice-roi nommé sans registre exact ; Li Shiyao de1777 ne doit pas être projeté en1776.'),
 'SHS':('DEFER_COLLECTIVE','Ensemble shan composé de plusieurs autorités ; aucun saopha d’un seul État attribué à toute la fédération.'),
 'LAN':('DEFER_COLLECTIVE','Communautés minières de Mandor : ne pas installer le fondateur de Lanfang1777 comme souverain unique en1776.'),
 'ALK':('DEFER_COLLECTIVE','Comptoirs russes d’Alaska : pas de chef unique de la future Compagnie russo-américaine rétroprojeté en1776.'),
 'HWA':('DEFER_COLLECTIVE','Îles occidentales d’Hawaï : plusieurs chefferies ; la présence de Kamakahelei à Kauai ne suffit pas à lui donner toutes les îles du TAG.'),
 'IRO':('DEFER_COLLECTIVE','Six Nations : Joseph Brant n’est pas un monarque de toute la confédération ; pas d’autorité pantribale fabriquée.'),
 'CKS':('DEFER_COLLECTIVE','Chefs chickasaws concurrents et compétences réparties ; ne pas attribuer au seul Piomingo un pouvoir unique non établi.'),
 'CTW':('DEFER_COLLECTIVE','Choctaws : chefs de divisions distinctes ; Franchimastabe d’une division ne devient pas chef de tout le TAG.'),
}

def decisions(inv, installed):
    prior = load('PRIOR_POLITY_PROFILES.json')
    installed = {p['TAG']:p for p in installed}
    companies = {'BIC':'BIC_john_harrison','DEI':'DEI_egbert_de_vrij_temminck','HBC':'CLEANUP2C1B_HBC_sir_bibye_lake_jr'}
    result=[]
    for r in inv['countries']:
        tag=r['TAG'];entry=dict(r)
        if tag in installed:
            status='HISTORICAL_RULER_INSTALLED_R1';reason=installed[tag]['full_name'];refs=installed[tag]['source_ids']
        elif r['status']=='HAS_SCRIPTED_HISTORICAL_RULER':
            status='PRESERVE_EXISTING_SCRIPTED_HISTORICAL_RULER';reason='Personnage déjà explicitement historique dans les scripts courants ; cette passe ne réaudite pas sa biographie.';refs=[]
        elif tag in inv['unions']:
            status='COVERED_PERSONAL_UNION';reason='Souverain partagé avec '+inv['unions'][tag]['overlord']+' ; use_overlord_ruler=yes dans le type natif. Aucun second personnage.';refs=[inv['unions'][tag]['file']]
        elif tag in companies:
            matching=[e for e in inv['executives'] if e.get('template')==companies[tag]]
            assert len(matching)==1,(tag,matching)
            status='COVERED_COMPANY_EXECUTIVE';reason='Responsable historique de la compagnie déjà créé par le modèle '+companies[tag]+' dans le pays propriétaire. Pas de monarque ajouté.';refs=[matching[0]['file']]
        else:
            status,reason=OVERRIDES.get(tag,('DEFER_NO_VERIFIED_REPRESENTATIVE' if r['kind']=='decentralized' else 'DEFER_SOURCE_GAP',
                 'Aucun représentant individuel couvrant ce TAG au1er janvier1776 suffisamment établi par les sources consultées. La catégorie décentralisée ne prouve pas l’absence de chefs : aucun chef local n’est étendu à tout l’ensemble.' if r['kind']=='decentralized' else
                 'Le dépouillement des recherches antérieures et des sources régionales consultées ne permet pas de certifier un titulaire individuel au1er janvier1776. Recherches ciblées supplémentaires possibles ; aucune affirmation d’absence historique de dirigeant.'))
            refs=['PRIOR_POLITY_PROFILES.json:'+tag] if tag in prior else ['research/ (périmètre des recherches, aucune preuve négative exhaustive)']
        entry.update(decision=status,reason=reason,evidence=refs)
        if tag in prior: entry['prior_polity_context']=prior[tag].get('basis')
        result.append(entry)
    return result

def capture_native():
    folders=['common/character_templates','common/character_traits','common/history/characters','common/subject_types']
    return {p.relative_to(a.GAME).as_posix():a.sha(p) for f in folders for p in (a.GAME/f).rglob('*') if p.is_file()}

def install():
    assert not (OUT/'APPLY_BASELINE.json').exists(), 'Already installed; validate instead.'
    assert all(not (ROOT/r).exists() for r in FILES), 'Private path already exists; inspect without overwriting.'
    inv=inventory();profiles=load('CURATED_PROFILES.json');rows={r['TAG']:r for r in inv['countries']}
    for p in profiles:
        assert p['TAG'] in rows
        assert not rows[p['TAG']]['rulers'], ('Concurrent or inherited character now present',p['TAG'],rows[p['TAG']]['rulers'])
        assert p['TAG'] not in inv['unions'], ('Shared sovereign',p['TAG'])
    current=nordic.hashes()
    baseline=dict(utc=datetime.now(timezone.utc).isoformat(),inventory=inv,protected=current,
                  native=capture_native(),world=b4.inventory(),planned_new=FILES,
                  profiles_sha256=a.sha(OUT/'CURATED_PROFILES.json'),sources_sha256=a.sha(OUT/'SOURCES.json'))
    save('APPLY_BASELINE.json',baseline)
    # Check again immediately before mutations; never restore old shared contents.
    assert nordic.hashes()==current, 'Workspace evolved during capture; review before installation.'
    for rel,text in texts(profiles).items():
        p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('x',encoding='utf-8-sig' if p.suffix=='.yml' else 'utf8',newline='\n') as f:f.write(text)
    save('INSTALLED.json',dict(utc=datetime.now(timezone.utc).isoformat(),files={r:a.sha(ROOT/r) for r in FILES},
                              countries=[p['TAG'] for p in profiles],status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'))
    print('Installed',len(profiles),'ruler profiles in',len(FILES),'new private files.')

def validate():
    baseline=load('APPLY_BASELINE.json');profiles=load('CURATED_PROFILES.json');sources=load('SOURCES.json');inv=inventory()
    rows={r['TAG']:r for r in inv['countries']};checks=[]
    def check(name, condition, detail=None):
        checks.append(dict(name=name,passed=bool(condition),detail=detail))
    expected=texts(profiles)
    for rel,text in expected.items():
        check('installed_content:'+rel,a.raw(ROOT/rel)==text)
        if rel.endswith('.txt'):check('parse:'+rel,bool(parse(a.raw(ROOT/rel))))
    cats={c:a.catalog('common/'+c) for c in ['character_templates','cultures','religions','interest_groups','ideologies']}
    vanilla_traits={n.key:n for p in (a.GAME/'common/character_traits').glob('*.txt') for n in parse(a.raw(p)) if isinstance(n.value,list)}
    mod_traits=a.catalog('common/character_traits')
    loc={lang:entries(lang) for lang in ['french','english']}
    native_loc={lang:entries(lang,root=a.GAME/'localization') for lang in ['french','english']}
    for lang in loc:
        check('bom:'+lang,(ROOT/FILES[2+['french','english'].index(lang)]).read_bytes().startswith(b'\xef\xbb\xbf'))
    for p in profiles:
        tag=p['TAG'];rs=rows[tag]['rulers'];key=PREFIX+'_'+tag.lower();node=cats['character_templates'][key][0]
        check(tag+':one_historical_ruler',len(rs)==1 and rs[0]['historical']=='yes')
        check(tag+':culture',p['culture'] in cats['cultures'])
        check(tag+':religion',p['religion'] is None or p['religion'] in cats['religions'])
        check(tag+':IG',p['interest_group'] in cats['interest_groups'])
        check(tag+':ideology',p['ideology'] in cats['ideologies'])
        check(tag+':birth_precision',node.one('birth_date') is None and (node.one('age')==str(p['age']) if p['age'] is not None else node.one('age') is None))
        check(tag+':birthplace_not_faked',all(node.one(x) is None for x in ['birth_place','birth_location','born_in']))
        check(tag+':no_random_traits',len(node.children('trait_generation'))==1 and node.children('trait_generation')[0].value==[])
        check(tag+':no_extra_roles',all(node.one(x) is None for x in ['general','admiral','heir','ig_leader']))
        check(tag+':traits_vanilla',all(t in vanilla_traits for t in p['traits']))
        # Node objects carry source offsets: compare parsed semantics, not file
        # positions or whitespace. The initial false failures remain archived.
        check(tag+':traits_effective_unchanged',all(normalized([mod_traits[t][0]])==normalized([vanilla_traits[t]]) for t in p['traits']))
        check(tag+':sources',all(s in sources and sources[s]['consulted'] and sources[s]['locator'] for s in p['source_ids']))
        check(tag+':documented_choices',bool(p['traits_basis'] and p['interest_group_basis'] and p['uncertainties']))
        for lang in loc:
            k=key+'_name'
            check(tag+':localization_'+lang,len(loc[lang].get(k,[]))==1 and k not in native_loc[lang])
    old={r['TAG']:r for r in baseline['inventory']['countries']}
    selected={p['TAG'] for p in profiles}
    changed_existing=[]
    for tag,r in old.items():
        if tag not in selected and rows.get(tag,{}).get('rulers')!=r['rulers']:changed_existing.append(tag)
    check('existing_rulers_preserved',not changed_existing,changed_existing)
    check('active_TAGs_preserved',set(old)==set(rows))
    check('inherited_unresolved_templates_not_increased',inv['unresolved_templates']==baseline['inventory']['unresolved_templates'],inv['unresolved_templates'])
    now=nordic.hashes();delta={r:dict(before=h,after=now.get(r)) for r,h in baseline['protected'].items() if now.get(r)!=h}
    unexpected_new=sorted(set(now)-set(baseline['protected'])-set(FILES))
    check('preexisting_gameplay_and_SERG_files_unchanged',not delta,delta)
    check('only_four_new_gameplay_files',not unexpected_new,unexpected_new)
    check('canonical_vanilla_unchanged',capture_native()==baseline['native'])
    world=b4.inventory()
    check('world_population_conserved',world['world_population']==baseline['world']['world_population'],[baseline['world']['world_population'],world['world_population']])
    check('province_owners_conserved',world['owners']==baseline['world']['owners'])
    check('git_HEAD_branch_index_unchanged',world['git']==baseline['world']['git'])
    check('research_profiles_unchanged_since_install',a.sha(OUT/'CURATED_PROFILES.json')==baseline['profiles_sha256'])
    dec=decisions(inv,profiles);save('COUNTRY_DECISIONS.json',dec)
    check('global_decisions_complete',len(dec)==len(rows) and len({r['TAG'] for r in dec})==len(rows))
    for tag,u in inv['unions'].items():
        if tag in rows and not rows[tag]['rulers']:
            check('union_inherits_historical:'+tag,any(r.get('historical')=='yes' for r in rows.get(u['overlord'],{}).get('rulers',[])))
    tally=Counter(r['decision'] for r in dec)
    result=dict(status='PASS_STATIC' if all(c['passed'] for c in checks) else 'FAIL_STATIC',
                utc=datetime.now(timezone.utc).isoformat(),checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
                countries=len(rows),installed=len(profiles),distinct_people=len({p['full_name'] for p in profiles}),decisions=dict(tally),
                world_population_before=baseline['world']['world_population'],world_population_after=world['world_population'],
                runtime='NOT_RUN',human_validation='NONE_ADDED',files={r:a.sha(ROOT/r) for r in FILES},
                concurrent_delta=delta,unexpected_new=unexpected_new)
    save('STATIC_CHECKS.json',result)
    reports(profiles,sources,dec,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['checks','files']},ensure_ascii=False,indent=2))
    if result['status']!='PASS_STATIC':
        print(json.dumps([c for c in checks if not c['passed']],ensure_ascii=False,indent=2));raise SystemExit(1)

def reports(profiles,sources,dec,result):
    translations=entries('french',root=a.GAME/'localization')
    translations.update(entries('french'))
    def readable(key):
        return translations[key][-1][2] if key in translations else key
    def prose(s):
        # Human prose only: never apply this to URLs, IDs, or game scripts.
        return re.sub(r'(?<=[A-Za-zÀ-ÿ])(?=\d)|(?<=\d)(?=[A-Za-zÀ-ÿ])',' ',s)
    profiles=[{k:prose(v) if k in ['office','tenure','historical_fact','birth','birthplace','uncertainties','traits_basis','interest_group_basis','ideology_basis'] else v
               for k,v in p.items()} for p in profiles]
    intro=['# Fiches des dirigeants ajoutés — 1er janvier 1776','',
        'Les identités et fonctions sont sourcées. Les traits, groupes d’intérêt et idéologies sont des interprétations de gameplay explicitement séparées des faits. Aucun trait nouveau n’est créé.',
        'Une année connue donne seulement un âge estimé. Quand la naissance est inconnue, le champ est omis : tout âge affiché par le moteur sera procédural, pas une date historique certifiée. Les lieux figurent dans ces fiches ; aucun champ moteur non pris en charge n’a été inventé.',
        'Les cultures utilisent le catalogue actuel du mod. Une religion imposée représente le contexte documenté du pouvoir ou son proxy existant, sauf baptême individuel explicitement attesté ; elle ne certifie pas des pratiques privées. Pour les confessions non établies signalées, la génération native reste active.',
        'Les portraits/DNA restent générés. Les fins de règne ci-dessous sont documentaires : aucun décès futur ou changement de loi n’est imposé. Fonction dans le moteur : dirigeant seulement, sans nomination automatique comme général ou chef de groupe d’intérêt.','']
    for p in profiles:
        intro += [f'## {p["TAG"]} — {p["full_name"]}','',
          f'- Fonction historique : {p["office"]}. Période : {p["tenure"]}.',
          '- Fait établi : '+p['historical_fact'],
          '- Naissance : '+p['birth']+'. Lieu : '+p['birthplace']+'.',
          '- Âge de génération : '+(str(p['age'])+' ans, estimation explicitement non exacte.' if p['age'] is not None else 'non renseigné ; valeur native éventuelle non historique.'),
          '- Culture dans le moteur : `'+p['culture']+'`. Religion : '+('`'+p['religion']+'` (contexte/proxy, sauf attestation individuelle citée).' if p['religion'] else 'non spécifiée, non certifiée historiquement.'),
          '- Groupe : '+readable(p['interest_group'])+' (`'+p['interest_group']+'`). '+p['interest_group_basis'],
          '- Idéologie : '+readable(p['ideology'])+' (`'+p['ideology']+'`). '+p['ideology_basis'],
          '- Traits vanilla : '+', '.join(readable(t)+' (`'+t+'`)' for t in p['traits'])+'. '+p['traits_basis'],
          '- Limites : '+p['uncertainties'],
          '- Sources : '+', '.join('['+s+' — '+sources[s]['title']+']('+sources[s]['url']+')' for s in p['source_ids'])+'.','']
    (OUT/'FICHES_DIRIGEANTS.md').write_text('\n'.join(intro),encoding='utf8')
    s=['# Sources et portée réelle des consultations','',
       'Consultations de cette passe : 29 octobre 2026. Les dates de publication signalées par les moteurs ne sont pas utilisées comme dates des événements. Les archives JSON conservent résultats, URLs et limites de lecture ; elles ne constituent pas une validation du contenu par le moteur du jeu.','']
    for key,v in sources.items():
        s += ['## '+key+' — '+v['title'],'',v['url'],'','Localisation : '+v['locator']+'.','',v['consulted'],'']
    (OUT/'SOURCES.md').write_text('\n'.join(s),encoding='utf8')
    d=['# Registre global des décisions','',f'{len(dec)} pays actifs inventoriés. Chaque ligne a sa décision ; le JSON donne également les fichiers et personnages existants. « Non établi » ne signifie jamais « aucun dirigeant n’existait ». La recherche est bornée aux documents réellement consultés et n’est pas un dépouillement exhaustif de toutes les archives mondiales.','',
       '| TAG | Pays | Décision | Justification |','| --- | --- | --- | --- |']
    for r in dec:
        d.append('| '+' | '.join((prose(str(r[k])) if k=='reason' else str(r[k])).replace('|','/').replace('\n',' ') for k in ['TAG','name','decision','reason'])+' |')
    (OUT/'DECISIONS.md').write_text('\n'.join(d)+'\n',encoding='utf8')
    summary=['# WORLD RULERS 1776 R1 — livraison','',
       'Statut : '+('IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' if result['status']=='PASS_STATIC' else 'STATIC_VALIDATION_FAILED')+'.',
       f'{result["installed"]} pays reçoivent un dirigeant historique, représentant {result["distinct_people"]} personnes distinctes. Cayor et Baol partagent le même titulaire dans deux représentations techniques, sans modifier leur relation diplomatique.',
       f'{result["countries"]} pays actifs ont une décision traçable. Les personnages déjà marqués historiques sont préservés, sans nouvelle certification de leur biographie. Les souverains d’unions personnelles et les responsables historiques de compagnies sont distingués des lacunes.',
       '', '| Décision | Pays |','| --- | ---: |']
    summary += [f'| {k} | {v} |' for k,v in sorted(result['decisions'].items())]
    summary += ['',f'Contrôles statiques : {result["passed"]}/{result["total"]}. Chargement moteur, rendu, chronologie après simulation : NON TESTÉS. Aucun reçu humain créé.',
      f'Population mondiale : {result["world_population_before"]} → {result["world_population_after"]}. Aucune cellule/RGB, frontière, ressource, bâtiment, recette, technologie ou loi modifiée. Quatre fichiers fonctionnels nouveaux, aucune réécriture de fichier partagé.',
      'Préservation vérifiée par empreintes : fichiers fonctionnels préexistants, suivi SERG, références vanilla consultées, HEAD/branche/index Git. Les travaux Durrani, TECH, ECON, Amériques et autres ajouts présents à la capture d’installation sont conservés. Les évolutions antérieures à cette capture sont distinguées dans la comparaison des inventaires.',
      '', 'Fichiers : `FICHES_DIRIGEANTS.md`, `SOURCES.md`, `DECISIONS.md`, `COUNTRY_DECISIONS.json`, `STATIC_CHECKS.json`, `APPLY_BASELINE.json`, `INSTALLED.json`.',
      '', 'Protocole de contrôle en jeu : nouvelle partie au 1er janvier 1776, inspecter notamment Boina (Ravahiny), Shewa, Choughnan, Chaki, Cayor/Baol et les quatre Waldburg ; vérifier noms, traits, IG et absence de second dirigeant dans les unions/compagnies. Les personnages de Tonga et des Cherokees gardent un pays de type décentralisé : vérifier aussi leur disponibilité dans les vues de personnages, sans conclure de la seule syntaxe à un affichage natif garanti. Sauvegarder/recharger et vérifier la persistance. Aucun test intermédiaire d’une région territoriale n’est requis par cette livraison.',
      '', 'Lieux de naissance : un seul lieu probable recoupé ici (Chota pour Oconostota), explicitement non certain ; les autres restent inconnus. Les sources retenues ne donnent aucune nouvelle date de naissance complète assez sûre ; aucune date fictive n’a été introduite pour remplir les fiches.',
      '', 'Prochaine action : vérification des personnages livrés dans une nouvelle partie ; les dossiers différés restent documentés, sans création d’identité de remplacement. Aucune autre région territoriale n’est lancée.','']
    summary += ['Le premier contrôle des traits a produit 27 faux écarts, car il comparait aussi des positions de texte. La comparaison corrigée porte sur les définitions analysées, strictement identiques au vanilla. L’exécution initiale est conservée dans STATIC_CHECKS_INITIAL_FAILED.json ; aucun trait n’a été modifié pour satisfaire le test.',
                'L’inventaire VFS détecte aussi 25 références héritées à des modèles vanilla supprimés (notamment personnages de1836). Elles étaient présentes avant cette installation et ne sont pas réintroduites. Voir APPLY_BASELINE.json, inventory.unresolved_templates : dette antérieure distinguée des nouveaux personnages.','']
    (OUT/'REPORT.md').write_text('\n'.join(summary),encoding='utf8')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--install',action='store_true');ap.add_argument('--validate',action='store_true');args=ap.parse_args()
    if args.install:install()
    if args.validate:validate()
