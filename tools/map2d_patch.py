"""Generate a narrow apply_patch payload from the saved MAP-2D baseline."""
import json,difflib,sys
from pathlib import Path
from map2a_patch import state,region,edits,append
from map2d_work import ROOT,GAME,OUT,BASE,packed
import validate_diplomacy_ottoman_1776 as cw
from map_1776_audit import values,prov

# Existing RGB abstractions, not exact cadastral boundaries.
TRANSFERS={
 'STATE_BESSARABIA':{'TUR':['x1E1DEF','x23621B','x6BF7B8','xB0E0A0'],'CRI':['x5F2259']},
 'STATE_CRIMEA':{'RUS':['x706060']},
 'STATE_TAURIDA':{'RUS':['x8A09FD']},
 'STATE_CHERSON':{
  'RUS':['x13997A','x29EE58','x3DA304','x3E5AF0','x5BE6ED','x652CE8','x71E061','x726291','x73216A','x89CE7C','x924D7E','x925815','xB285AE','xCC0D93','xE315A3','xF0E0A0','xF60A93','xFD6659','xFDD2CF'],
  'TUR':['x716121','xB02161']},
}
def transform(originals):
    result=dict(originals);path='common/history/states/00_states.txt';raw=result[path]
    for sid,targets in TRANSFERS.items():
        s=state(raw,sid); cr=s.children('create_state')[0];owned=cr.children('owned_provinces')[0]
        moved={v for vs in targets.values() for v in vs}
        keep=[prov(v) for v in values(cr,'owned_provinces') if prov(v) not in moved]
        assert len(keep)+len(moved)==len(values(cr,'owned_provinces'))
        raw=edits(raw,[(owned.start,owned.end,'owned_provinces = { '+' '.join(keep)+' }')])
        s=state(raw,sid);new='\n\t\t# MAP-2D: 1774 treaty exceptions; see the territorial manifest for RGB compromises.\n'
        for tag,vs in targets.items():new+='\t\tcreate_state = { country = c:'+tag+' owned_provinces = { '+' '.join(vs)+' } }\n'
        raw=edits(raw,[(s.end-1,s.end-1,new+'\t')])
    result[path]=raw
    # Preserve every pop's attributes; split only its size, by existing RGB land area.
    # This is a reversible spatial allocation of the inherited pool, not a 1776 census.
    bmp=packed(OUT/'provinces_before.png');poprows=[];allocations={}
    inv=json.loads(BASE.read_text(encoding='utf-8'))['inventory']
    for sid,targets in TRANSFERS.items():
        original_tag='MOL' if sid=='STATE_BESSARABIA' else 'CRI'
        own=[r['key'][0] for r in inv['owners'] if r['key'][1:]==[sid,original_tag]]
        areas={v:int((bmp==int(v[1:],16)).sum()) for v in own};total=sum(areas.values())
        target_areas={tag:sum(areas[v] for v in vs) for tag,vs in targets.items()}
        allocations[sid]={'source':original_tag,'total_land_pixels':total,'target_land_pixels':target_areas,'method':'integer proportional RGB area; remainder stays with original owner'}
        path='common/history/pops/15_russia.txt';raw=result[path];r=region(raw,sid,original_tag);ops=[];bodies={tag:[] for tag in targets}
        for p in r.children('create_pop'):
            count=int(p.one('size'));sz=p.children('size')[0];moved=0
            for tag,area in target_areas.items():
                n=count*area//total;moved+=n
                if n:
                    fragment=raw[p.start:p.end]
                    fragment=fragment[:sz.start-p.start]+'size = '+str(n)+fragment[sz.end-p.start:]
                    bodies[tag].append('\t\t\t'+fragment)
            ops.append((sz.start,sz.end,'size = '+str(count-moved)))
        raw=edits(raw,ops)
        for tag,body in bodies.items():raw=append(raw,sid,tag,'\t\t\t# MAP-2D: redistribution of existing groups; no people created or assimilated.\n'+'\n'.join(body))
        result[path]=raw
    (OUT/'POPULATION_ALLOCATION_METHOD.json').write_text(json.dumps(allocations,indent=2),encoding='utf-8')
    # Distribute only duplicate agricultural declarations. Preserve foreign owners,
    # levels, PMs, reserves and all remaining buildings in their original subdivision.
    path='common/history/buildings/98_build_start_1776_world_redistribution.txt';raw=result[path]
    for sid,src,dest in [('STATE_BESSARABIA','MOL','TUR'),('STATE_CHERSON','CRI','RUS')]:
        r=region(raw,sid,src);bb=r.children('create_building')
        assert {cw.scalar(b.one('building')) for b in bb}=={'building_livestock_ranch','building_wheat_farm'}
        body='\n'.join('\t\t\t'+raw[b.start:b.end] for b in bb if sid!='STATE_BESSARABIA' or cw.scalar(b.one('building'))=='building_livestock_ranch')
        extra='\n'.join('\t\t\t'+raw[b.start:b.end] for b in bb if sid=='STATE_BESSARABIA' and cw.scalar(b.one('building'))=='building_wheat_farm')
        raw=edits(raw,[(r.start,r.end,'')]);raw=append(raw,sid,dest,body)
        if extra:raw=append(raw,sid,'CRI',extra)
    result[path]=raw
    # The AI's voluntary bloc departure uses invite acceptance, not wargoal scores.
    path='common/diplomatic_actions/28_invite_to_power_bloc.txt'
    native=(GAME/path).read_text(encoding='utf-8-sig')
    score=cw.parse(native)[0].children('ai')[0].children('accept_score')[0]
    policy='''
			# MAP-2D: prefer retaining the existing Russian-backed Polish constitution.
			# Only current members, with a guarantee and non-hostile relations. No player lock.
			if = {
				limit = {
					c:PLC ?= this
					c:RUS ?= scope:actor
					is_in_same_power_bloc = scope:actor
					game_date < 1788.2.24
					has_law = law_type:law_oligarchy
					has_treaty_guarantee_independence_with = { TARGET = c:RUS }
					"relations(scope:actor)" > relations_threshold:poor
					NOT = { is_diplomatic_play_enemy_of = c:RUS }
				}
				add = { desc = DIPLOMATIC_ACCEPTANCE_1776_CARDINAL_LAWS value = 150 }
				min = -75 # Vanilla voluntary departure threshold is -100.
			}
		'''
    result[path]=edits(native,[(score.end-1,score.end-1,policy)])
    return {p:t for p,t in result.items() if originals.get(p)!=t}
def make_patch():
    originals=json.loads(BASE.read_text(encoding='utf-8'))['originals'];changed=transform(originals)
    pieces=['*** Begin Patch\n']
    for p,t in changed.items():
        if (ROOT/p).exists():
            before=(ROOT/p).read_text(encoding='utf-8-sig');delta=list(difflib.unified_diff(before.splitlines(True),t.splitlines(True),n=3))
            pieces.append('*** Update File: '+(ROOT/p).as_posix()+'\n')
            for line in delta[2:]:pieces.append('@@\n' if line.startswith('@@') else line)
        else:pieces.append('*** Add File: '+(ROOT/p).as_posix()+'\n'+''.join('+'+line+'\n' for line in t.splitlines()))
    pieces.append('*** End Patch\n');(OUT/'INTEGRATION.patch').write_text(''.join(pieces),encoding='utf-8')
    print('Prepared',len(changed),'history/action files;',sum(len(vs) for ts in TRANSFERS.values() for vs in ts.values()),'province transfers')
if __name__=='__main__':make_patch()
