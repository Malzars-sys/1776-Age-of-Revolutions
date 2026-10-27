"""Static regression checks. Writes mission reports only, never gameplay or Git."""
from __future__ import annotations
import collections as C
import copy
import io
import json
import re
import subprocess
import time
import unittest
import econ_alloys_1776 as e


class Alloys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.head_at_start=subprocess.check_output([str(e.GIT),'rev-parse','HEAD'],cwd=e.ROOT,text=True).strip()
        cls.index_at_start=e.sha(e.ROOT/'.git/index')
        cls.b=json.loads((e.OUT/'BASELINE.json').read_text(encoding='utf-8'))
        cls.h=json.loads((e.OUT/'HARDWARE_BASELINE.json').read_text(encoding='utf-8'))
        cls.models={k:e.definitions(v) for k,v in {
            'pms':'common/production_methods','groups':'common/production_method_groups',
            'buildings':'common/buildings','needs':'common/pop_needs',
            'techs':'common/technology/technologies','goods':'common/goods'}.items()}
        cls.prices,cls.wages=e.prices_and_wages()
        cls.external_models=[]

    def n(self,kind,key):return self.models[kind][0][key][0]
    def r(self,key):return e.recipe(self.n('pms',key))
    def c(self,key,**kw):return e.cost(self.r(key),self.prices,self.wages,**kw)

    def test_01_syntax_and_unique_definitions(self):
        for rel in e.OWNED:
            if rel.startswith('common/'):
                with self.subTest(file=rel):self.assertTrue(e.parse((e.ROOT/rel).read_text(encoding='utf-8-sig')))
        for kind,ids in [('pms',e.UTENSILS+[e.BRONZE]),('groups',[e.GROUP])]:
            for key in ids:self.assertNotIn(key,self.models[kind][1])

    def test_02_small_profitable_traditional_production(self):
        r=self.r('pm_basic_smelting_process')
        self.assertEqual(r,dict(inputs=dict(iron=3,copper=4,lead=1,coal=2),outputs=dict(alloys=20),jobs=dict(shopkeepers=100,laborers=2000,machinists=100)))
        self.assertAlmostEqual(1-20/self.b['recipes']['pm_basic_smelting_process']['outputs']['alloys'],2/3)
        for wage in [5,10,12]:
            with self.subTest(wage=wage):self.assertGreater(self.c('pm_basic_smelting_process',labor_wage=wage)['net_before_taxes_subsidies'],0)
        self.assertGreater(self.c('pm_basic_smelting_process',input_factor=1.25)['net_before_taxes_subsidies'],0)
        self.assertEqual(e.vals(self.n('pms','pm_basic_smelting_process'),'unlocking_technologies'),['alloysworking'])

    def test_03_neutral_default_and_factory_attachment(self):
        self.assertEqual(self.r(e.UTENSILS[0]),dict(inputs={},outputs={},jobs={}))
        self.assertEqual(self.n('pms',e.UTENSILS[0]).one('texture'),self.n('pms','pm_no_canal_network').one('texture'))
        self.assertEqual(e.vals(self.n('groups',e.GROUP),'production_methods'),e.UTENSILS)
        self.assertEqual([k for k,(n,p) in self.models['buildings'][0].items() if e.GROUP in e.vals(n,'production_method_groups')],['building_furniture_manufactory'])
        self.assertEqual(e.vals(self.n('buildings','building_furniture_manufactory'),'production_method_groups').count(e.GROUP),1)

    def test_04_increasing_assortment_output_and_efficiency(self):
        rs=[self.r(k) for k in e.UTENSILS[1:]]
        self.assertEqual([len(r['inputs']) for r in rs],[2,3,4,5])
        self.assertEqual([r['outputs'] for r in rs],[{e.HARDWARE:q} for q in [20,40,80,160]])
        ratios=[self.c(k)['value_ratio'] for k in e.UTENSILS[1:]]
        self.assertTrue(all(a<b for a,b in zip(ratios,ratios[1:])))
        self.assertEqual(rs[-1]['inputs'],dict(steel=10,copper=6,lead=4,alloys=10,aluminium=8))
        for key in e.UTENSILS[1:]:
            self.assertGreater(self.c(key)['net_before_taxes_subsidies'],0)
            self.assertGreater(self.c(key,input_factor=1.25)['net_before_taxes_subsidies'],0)
            self.assertGreater(sum(self.r(key)['jobs'].values()),0)
            self.assertNotIn('mercury',self.r(key)['inputs'])
            self.assertGreater(self.r(key)['inputs']['alloys'],0)
            old=self.h['recipes'][key]
            self.assertGreater(sum(self.r(key)['inputs'].values()),sum(old['inputs'].values()))
            self.assertGreater(self.r(key)['outputs'][e.HARDWARE],old['outputs']['furniture'])

    def test_05_valid_inputs_assets_and_scaling(self):
        for key in e.UTENSILS+[e.BRONZE,'pm_basic_smelting_process']:
            n=self.n('pms',key);r=self.r(key)
            for good in set(r['inputs'])|set(r['outputs']):self.assertIn(good,self.prices)
            path=e.scalar(n.one('texture'))
            self.assertTrue((e.ROOT/path).exists() or (e.GAME/path).exists(),path)
            for b in n.children('building_modifiers'):
                for scale in b.children():
                    for field in scale.children():
                        self.assertEqual(scale.key,'level_scaled' if field.key.startswith('building_employment_') else 'workforce_scaled')
        path=e.scalar(self.n('groups',e.GROUP).one('texture'))
        self.assertTrue((e.ROOT/path).exists() or (e.GAME/path).exists())

    def test_06_existing_technology_gates_and_eras(self):
        expected=[([],None),(['organized_workshops','alloysworking'],'era_2'),(['organized_workshops','alloysworking'],'era_2'),
                  (['mechanical_tools','alloysworking'],'era_5'),(['mechanical_tools','bayer_process'],'era_10')]
        for key,(gates,era) in zip(e.UTENSILS,expected):
            self.assertEqual(e.vals(self.n('pms',key),'unlocking_technologies'),gates)
            for gate in gates:self.assertIn(gate,self.models['techs'][0])
            if gates:self.assertIn(era,[self.n('techs',g).one('era') for g in gates])
        self.assertEqual(self.n('techs','alloysworking').one('era'),'era_2')
        self.assertEqual(set(e.vals(self.n('techs','alloysworking'),'unlocking_technologies')),{'shaft_mining','organized_workshops'})
        self.assertEqual(set(e.vals(self.n('pms',e.BRONZE),'unlocking_technologies')),{'alloysworking','standardized_field_artillery'})

    def test_07_bronze_optional_same_cost_and_output(self):
        old=self.r('pm_cannons');new=self.r(e.BRONZE)
        self.assertEqual(new['inputs'],dict(iron=10,hardwood=10,alloys=4))
        self.assertEqual(new['outputs'],old['outputs']);self.assertEqual(new['jobs'],old['jobs'])
        self.assertEqual(self.c(e.BRONZE)['input_cost'],self.c('pm_cannons')['input_cost'])
        self.assertEqual(e.vals(self.n('groups','pmg_foundries'),'production_methods').count(e.BRONZE),1)

    def test_08_only_tiny_household_substitution(self):
        n=self.n('needs','popneed_household_items');entries={e.scalar(v.one('goods')):v for v in n.children('entry')}
        entry=entries['alloys']
        self.assertEqual({k:float(entry.one(k)) for k in ['weight','min_supply_share','max_supply_share']},dict(weight=.02,min_supply_share=.01,max_supply_share=.05))
        self.assertEqual(n.one('default'),'furniture')
        # Native comments: supply-share clamps multiply base weight; not a purchase cap.
        alloy_weight=.02*.05;furniture_floor=float(entries['furniture'].one('weight'))*float(entries['furniture'].one('min_supply_share'))
        self.assertLess(alloy_weight/(alloy_weight+furniture_floor),.01)
        packages=e.definitions('common/buy_packages')[0]
        first=min(int(k.split('_')[1]) for k,(v,p) in packages.items() if k.startswith('wealth_') and any(x.key=='popneed_household_items' for x in e.walk(v.children())))
        self.assertEqual(first,10)
        hardware=entries[e.HARDWARE]
        self.assertEqual({k:float(hardware.one(k)) for k in ['weight','min_supply_share','max_supply_share']},dict(weight=1,min_supply_share=.02,max_supply_share=.35))
        for key,(need,path) in self.models['needs'][0].items():
            if key!='popneed_household_items':self.assertFalse(any(n.one('goods')==e.HARDWARE for n in need.children('entry')))

    def test_09_existing_models_preserved(self):
        allowed={'pms':set(e.UTENSILS[1:]),'groups':set(),'buildings':set(),'needs':{'popneed_household_items'},'techs':set(),'goods':set()}
        added={'goods':{e.HARDWARE}}
        for kind,old in self.h['models'].items():
            current=self.models[kind][0]
            extra=set(current)-set(old)
            self.assertTrue(added.get(kind,set())<=extra,kind)
            for key in extra-added.get(kind,set()):
                path=current[key][1].relative_to(e.ROOT).as_posix()
                self.assertNotIn(path,e.OWNED,(kind,key))
                self.external_models.append(dict(kind=kind,key=key,path=path,change='external addition'))
            self.assertFalse(set(old)-set(current),kind)
            for key,f in old.items():
                if key not in allowed[kind]:
                    if e.fingerprint(current[key][0])!=f:
                        if kind=='pms' and key==e.UTENSILS[0]:
                            neutral=copy.deepcopy(current[key][0])
                            neutral.children('texture')[0].value='"gfx/interface/icons/production_method_icons/no_automation.dds"'
                            self.assertEqual(e.fingerprint(neutral),f,'Only neutral artwork may differ from hardware baseline')
                            continue
                        path=current[key][1].relative_to(e.ROOT).as_posix()
                        self.assertNotIn(path,e.OWNED,(kind,key))
                        self.assertNotIn(kind,{'techs','goods'},(kind,key))
                        self.external_models.append(dict(kind=kind,key=key,path=path,change='external modification'))

    def test_10_shared_objects_have_only_intended_insertions(self):
        for kind,key,remove in [('groups','pmg_foundries',e.BRONZE),('buildings','building_furniture_manufactory',e.GROUP)]:
            n=copy.deepcopy(self.n(kind,key))
            field='production_methods' if kind=='groups' else 'production_method_groups'
            for b in n.children(field):b.value=[v for v in b.children() if v.value!=remove]
            self.assertEqual(e.canonical(n),self.b['raws'][kind][key])
        n=copy.deepcopy(self.n('needs','popneed_household_items'))
        n.value=[v for v in n.children() if not(v.key=='entry' and v.one('goods') in {'alloys',e.HARDWARE})]
        self.assertEqual(e.canonical(n),self.b['raws']['needs']['popneed_household_items'])

    def test_11_secondary_combinations_are_additive(self):
        base_ids=e.vals(self.n('groups','pmg_base_building_furniture_manufactory'),'production_methods')
        luxury_ids=e.vals(self.n('groups','pmg_luxury_building_furniture_manufactory'),'production_methods')
        for base in base_ids:
            for luxury in luxury_ids:
                allowed=e.vals(self.n('pms',luxury),'unlocking_production_methods')
                if allowed and base not in allowed:continue
                for key in e.UTENSILS:
                    with self.subTest(base=base,luxury=luxury,utensil=key):
                        old=sum(self.r(k)['outputs'].get('furniture',0) for k in [base,luxury])
                        self.assertGreaterEqual(old,0)
                        self.assertEqual(self.r(key)['outputs'].get('furniture',0),0)
                        self.assertEqual(self.r(key)['outputs'].get(e.HARDWARE,0),dict(zip(e.UTENSILS,[0,20,40,80,160]))[key])
        for key in ['pm_wohler_deville_process','pm_hall_heroult_process']:
            self.assertGreaterEqual(20+self.r(key)['outputs']['alloys'],0)

    def test_12_localizations_bom_names_no_collisions(self):
        keysets=[]
        for lang in ['french','english']:
            new=e.ROOT/f'localization/{lang}/1776_alloys_utensils_l_{lang}.yml'
            self.assertTrue(new.read_bytes().startswith(b'\xef\xbb\xbf'))
            content=new.read_text(encoding='utf-8-sig');self.assertTrue(content.startswith(f'l_{lang}:'))
            keys=re.findall(r'^ ([^\s:]+):\d* "[^"\n]*"$',content,re.M)
            self.assertEqual(len(keys),31)
            count=C.Counter()
            for path in (e.ROOT/f'localization/{lang}').rglob('*.yml'):
                count.update(re.findall(r'^\s*([^\s:#]+):\d*\s*"',path.read_text(encoding='utf-8-sig'),re.M))
            for k in keys:self.assertEqual(count[k],1,k)
            vanilla='\n'.join(p.read_text(encoding='utf-8-sig') for p in (e.GAME/f'localization/{lang}').rglob('*.yml'))
            for k in keys:self.assertIsNone(re.search(r'^\s*'+re.escape(k)+r':',vanilla,re.M))
            old=e.ROOT/f'localization/{lang}/tech6c5c_aluminium_l_{lang}.yml'
            self.assertTrue(old.read_bytes().startswith(b'\xef\xbb\xbf'))
            self.assertIn("Fabrication traditionnelle d'alliages" if lang=='french' else 'Traditional Alloy Making',old.read_text(encoding='utf-8-sig'))
            before=self.b['originals'][old.relative_to(e.ROOT).as_posix()]
            strip=lambda s:re.sub(r'^ pm_basic_smelting_process(?:_desc)?:[^\n]*','',s,flags=re.M)
            self.assertEqual(strip(before),strip(old.read_text(encoding='utf-8-sig')))
            keysets.append(set(keys))
        self.assertEqual(*keysets)

    def test_13_git_unchanged_external_runtime_audited_separately(self):
        # Other authors are actively editing Ragusa/map data. Report their deltas;
        # do not roll them back or misattribute them to this economic change.
        # Historical HEAD/index may legitimately change between user sessions.
        e.dump('GIT_BASELINE_AUDIT.json',dict(historical_head=self.b['git_head'],current_head=self.head_at_start,historical_index=self.b['git_index'],current_index=self.index_at_start,historical_snapshot_preserved=True,interpretation='Historical drift is recorded separately; this check protects Git during the current test execution.'))
        self.assertEqual(subprocess.check_output([str(e.GIT),'rev-parse','HEAD'],cwd=e.ROOT,text=True).strip(),self.head_at_start)
        self.assertEqual(e.sha(e.ROOT/'.git/index'),self.index_at_start)

    def test_14_early_country_access_without_grants(self):
        profiles={}
        for path in (e.ROOT/'common/history/countries').glob('*.txt'):
            for n in e.walk(e.parse(path.read_text(encoding='utf-8-sig'))):
                if n.key.startswith('c:'):
                    profiles.setdefault(n.key[2:],set()).update(e.scalar(x.value) for x in n.children('add_technology_researched'))
        countries=sorted(k for k,v in profiles.items() if 'alloysworking' in v)
        e.dump('STARTING_ACCESS.json',dict(profiles_with_alloys=countries,access={k:dict(traditional_alloys={'alloysworking'}<=v,copper_brass_utensils={'alloysworking','organized_workshops'}<=v,bronze_artillery={'alloysworking','standardized_field_artillery'}<=v,has_coke='coke_smelting' in v) for k,v in profiles.items() if k in countries}))
        self.assertIn('AUS',countries)
        self.assertTrue({'alloysworking','organized_workshops','standardized_field_artillery'}<=profiles['AUS'])
        self.assertTrue(any('alloysworking' in v and 'coke_smelting' not in v for v in profiles.values()))

    def test_15_full_initial_alloy_factory_costs(self):
        combined={k:C.Counter() for k in ['inputs','outputs','jobs']};selected=[]
        for group in e.vals(self.n('buildings','building_alloys_plant'),'production_method_groups'):
            key=e.vals(self.n('groups',group),'production_methods')[0];selected.append(key)
            for kind,values in self.r(key).items():combined[kind].update(values)
        self.assertEqual(combined['outputs']['alloys'],20)
        cases=[dict(wage=w,**e.cost(combined,self.prices,self.wages,labor_wage=w)) for w in [5,10,12]]
        e.dump('INITIAL_FACTORY_COMBINATION.json',dict(selection='First entries of current PM groups; runtime defaults still to verify',pms=selected,recipe=combined,cases=cases))
        self.assertGreater(cases[1]['net_before_taxes_subsidies'],0)

    def test_16_hardware_is_a_registered_staple_with_transparent_art(self):
        import build_hardware_icon as art
        from PIL import Image
        good=self.n('goods',e.HARDWARE)
        self.assertEqual(good.one('category'),'staple')
        self.assertEqual(good.one('tradeable'),'yes')
        self.assertEqual(float(good.one('cost')),30)
        self.assertNotIn(e.HARDWARE,self.models['goods'][1])
        types,duplicates=e.definitions('common/modifier_type_definitions')
        for side in ['input','output']:
            for op in ['add','mult']:
                key=f'goods_{side}_{e.HARDWARE}_{op}'
                self.assertIn(key,types);self.assertNotIn(key,duplicates)
        icon=e.parse((e.ROOT/'gui/1776_hardware_texticons.gui').read_text(encoding='utf-8'))[0]
        self.assertEqual(icon.one('icon'),e.HARDWARE)
        self.assertEqual(e.scalar(icon.children('iconsize')[0].one('texture')),e.scalar(good.one('texture')))
        target,payload=art.expected()
        self.assertEqual(art.ICON.read_bytes(),payload)
        decoded=Image.open(art.ICON).convert('RGBA')
        self.assertEqual(decoded.size,(256,256))
        self.assertEqual(decoded.tobytes(),target.tobytes())
        source=Image.open(art.SOURCE).convert('RGBA')
        self.assertEqual(source.getpixel((source.width//2,int(source.height*.13)))[3],0)
        for im in [source,decoded]:
            self.assertEqual(im.getchannel('A').getextrema(),(0,255))
            for pt in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)]:self.assertEqual(im.getpixel(pt)[3],0)


def main():
    start=time.perf_counter();stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Alloys))
    legacy=e.legacy_test();e.dump('LEGACY_TEST_AFTER.json',legacy)
    before=json.loads((e.OUT/'LEGACY_TEST_BEFORE.json').read_text(encoding='utf-8'))
    errors=lambda r:[line for line in r['stdout'].splitlines() if line.startswith('- ')]
    regressions=sorted(set(errors(legacy))-set(errors(before)))
    runtime_changed={rel for rel,sha in Alloys.b['files'].items() if e.sha(e.ROOT/rel)!=sha}
    added={p.relative_to(e.ROOT).as_posix() for folder in ['common','localization','map_data','gfx','gui','events'] for p in (e.ROOT/folder).rglob('*') if p.is_file() and p.relative_to(e.ROOT).as_posix() not in Alloys.b['files']}
    concurrent=json.loads((e.OUT/'CONCURRENT_CHANGES.json').read_text(encoding='utf-8'))
    concurrent.update(runtime_changes=sorted(runtime_changed),runtime_additions=sorted(added),unexpected_runtime_changes=sorted((runtime_changed|added)-set(e.OWNED)),git_index_preserved=e.sha(e.ROOT/'.git/index')==Alloys.b['git_index'],git_head_preserved=subprocess.check_output([str(e.GIT),'rev-parse','HEAD'],cwd=e.ROOT,text=True).strip()==Alloys.b['git_head'])
    concurrent.update(external_model_changes=Alloys.external_models,interpretation='Changes outside mission ownership observed during concurrent work; preserved, not certified by economic tests.')
    e.dump('CONCURRENT_CHANGES.json',concurrent)
    e.dump('TEST_RESULTS.json',dict(status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',targeted_tests=result.testsRun,success=result.wasSuccessful(),failures=len(result.failures),errors=len(result.errors),duration_seconds=round(time.perf_counter()-start,3),output=stream.getvalue(),legacy_before_exit=before['exit_code'],legacy_after_exit=legacy['exit_code'],preexisting_errors=errors(before),new_legacy_errors=regressions,external_runtime_changes=concurrent['unexpected_runtime_changes'],runtime_tested=False,human_validated=False))
    revision_changed={rel for rel,sha in Alloys.h['files'].items() if e.sha(e.ROOT/rel)!=sha}
    concurrent.update(hardware_revision_external_changes=sorted((revision_changed|{p for p in added if p not in Alloys.h['files']})-set(e.OWNED)))
    e.dump('CONCURRENT_CHANGES.json',concurrent)
    changed=sorted(((runtime_changed|added)&set(e.OWNED))|{'tools/econ_alloys_1776.py','tools/test_econ_alloys_1776.py','tools/tech6c5c_validate.py','tools/build_hardware_icon.py','workshop_assets/source/aor1776_hardware_transparent.png'})
    changed.extend(p.relative_to(e.ROOT).as_posix() for p in sorted(e.OUT.iterdir()) if p.is_file() and p.name!='FILES_MODIFIED.json')
    e.dump('FILES_MODIFIED.json',dict(scope='Delta since this mission baseline; preserves earlier uncommitted work',status='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION',files=[dict(path=p,sha256=e.sha(e.ROOT/p),kind='report' if p.startswith('docs/') else 'tool' if p.startswith('tools/') else 'gameplay_or_localization') for p in changed]))
    print(stream.getvalue());print('New legacy errors:',regressions)
    raise SystemExit(0 if result.wasSuccessful() and not regressions else 1)


if __name__=='__main__':main()
