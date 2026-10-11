"""Generate a reviewable apply_patch payload; never write gameplay histories.

The historical decisions and demographic assumptions are explicit in MAP2A.
Read-only baseline transformation is also used by the independent inventory checks.
"""
import difflib
import json
from pathlib import Path
import validate_diplomacy_ottoman_1776 as cw
from validate_map2a import ROOT, OUT, HISTORY

def state(raw, sid):
    return next(n for n in cw.walk(cw.parse(raw)) if n.key == 's:'+sid)

def region(raw, sid, tag):
    return next(n for n in state(raw, sid).children() if n.key == 'region_state:'+tag)

def edits(raw, operations):
    for start, end, new in sorted(operations, reverse=True): raw = raw[:start]+new+raw[end:]
    return raw

def append(raw, sid, tag, content):
    matches = [n for n in cw.walk(cw.parse(raw)) if n.key == 's:'+sid]
    if not matches:
        at = cw.parse(raw)[0].end-1
        return edits(raw, [(at,at,'\n\ts:'+sid+' = {\n\t\tregion_state:'+tag+' = {\n'+content+'\n\t\t}\n\t}\n')])
    s = matches[0]
    rs = s.children('region_state:'+tag)
    if rs:
        at = rs[0].end-1
        return edits(raw, [(at,at,'\n'+content+'\n\t\t')])
    at = s.end-1
    return edits(raw, [(at,at,'\n\t\tregion_state:'+tag+' = {\n'+content+'\n\t\t}\n\t')])

def transform(originals):
    result = dict(originals)
    path = HISTORY[0]
    raw = result[path]
    # Upper Silesia is physically six Prussian provinces. Austria's retained
    # Silesian districts lie in the game's Moravia/West Galicia geometries.
    upper = state(raw, 'STATE_UPPER_SILESIA')
    aus = next(n for n in upper.children('create_state') if n.one('country') == 'c:AUS')
    pru = next(n for n in upper.children('create_state') if n.one('country') == 'c:PRU')
    ps = pru.children('owned_provinces')[0]
    body = raw[ps.start:ps.end].replace(' x71E080','').replace(' xF0E080','')
    raw = edits(raw, [(aus.start,aus.end,''),(ps.start,ps.end,body)])
    mora = state(raw,'STATE_MORAVIA').children('create_state')[0].children('owned_provinces')[0]
    raw = edits(raw, [(mora.end-1,mora.end-1,'x71E080 xF0E080 ')])
    wg = state(raw,'STATE_WEST_GALICIA')
    raw = edits(raw, [(wg.end-1,wg.end-1,'\n\t\t# MAP-2A: Teschen retained by Austria; game geometry is West Galicia.\n\t\tcreate_state = {\n\t\t\tcountry = c:AUS\n\t\t\towned_provinces = { x9061E0 }\n\t\t}\n\t')])
    lomb = state(raw,'STATE_LOMBARDY')
    ven = next(n for n in lomb.children('create_state') if n.one('country') == 'c:VEN')
    ps = ven.children('owned_provinces')[0]
    raw = edits(raw, [(ps.start,ps.end,raw[ps.start:ps.end].replace(' x9AC196',''))])
    lomb = state(raw,'STATE_LOMBARDY')
    raw = edits(raw, [(lomb.end-1,lomb.end-1,'\n\t\t# MAP-2A: SWI abstracts the associated Three Leagues, not a modern canton.\n\t\tcreate_state = {\n\t\t\tcountry = c:SWI\n\t\t\towned_provinces = { x9AC196 }\n\t\t}\n\t')])
    result[path] = raw

    path = HISTORY[2]
    raw = result[path]
    ven = region(raw,'STATE_LOMBARDY','VEN')
    ps = ven.children('create_pop')
    assert [p.one('size') for p in ps] == ['483226','81']
    sizes = [p.children('size')[0] for p in ps]
    raw = edits(raw, [(sizes[0].start,sizes[0].end,'size = 478227'),(sizes[1].start,sizes[1].end,'size = 80')])
    raw = raw.replace('# Temporary split by owned provinces (VEN 2/8); regional totals unchanged.',
                      '# MAP-2A: preserve Austrian totals; allocate 5,000 from the former VEN pool to Bormio.\n\t\t# A rounded gameplay allocation informed by 4,832 in the 1807 Bormio aggregate, not a 1776 census.')
    raw = append(raw,'STATE_LOMBARDY','SWI',
                 '\t\t\tcreate_pop = { culture = north_italian size = 4999 }\n\t\t\tcreate_pop = { culture = north_italian religion = jewish size = 1 }')
    result[path] = raw

    path = HISTORY[3]
    raw = result[path]
    au = region(raw,'STATE_UPPER_SILESIA','AUS')
    moravian, teschen = [], []
    # Conservative linguistic allocation of the existing Austrian pool. No
    # claim to a census: Germans mainly Opava, Poles mainly Teschen, Czechs mixed.
    shares = {'north_german':20,'polish':80,'czech':30,'ashkenazi':50}
    for p in au.children('create_pop'):
        count = int(p.one('size')); right = count * shares[p.one('culture')] // 100
        for target, number in ((moravian,count-right),(teschen,right)):
            fragment = raw[p.start:p.end]
            sz = p.children('size')[0]
            fragment = fragment[:sz.start-p.start]+'size = '+str(number)+fragment[sz.end-p.start:]
            target.append('\t\t\t'+fragment)
    raw = edits(raw, [(au.start,au.end,'')])
    raw = append(raw,'STATE_WEST_GALICIA','AUS',
                 '\t\t\t# MAP-2A: Austrian Teschen; conservative split of the existing Austrian Silesian pool.\n'+'\n'.join(teschen))
    result[path] = raw
    result[HISTORY[1]] = append(result[HISTORY[1]],'STATE_MORAVIA','AUS',
                 '\t\t\t# MAP-2A: Austrian Opava/Krnov districts; totals conserved with Teschen.\n'+'\n'.join(moravian))

    # Austrian Upper-Silesian textile declarations move to the newly valid
    # Teschen scope, avoiding new conflicting textile PMs in existing Moravia.
    path = HISTORY[5]
    raw = result[path]
    au = region(raw,'STATE_UPPER_SILESIA','AUS')
    bs = au.children('create_building')
    rail = next(b for b in bs if cw.scalar(b.one('building')) == 'building_railway')
    textile = next(b for b in bs if cw.scalar(b.one('building')) == 'building_textile_mill')
    textile_body = raw[textile.start:textile.end].replace('STATE_UPPER_SILESIA','STATE_WEST_GALICIA')
    assert [n.one('levels') for n in rail.children('add_ownership')[0].children('building')] == ['1']
    rail_body = raw[rail.start:rail.end].replace('STATE_UPPER_SILESIA','STATE_WEST_GALICIA')
    raw = edits(raw, [(au.start,au.end,'')])
    result[path] = append(raw,'STATE_WEST_GALICIA','AUS','\t\t\t'+rail_body+'\n\t\t\t'+textile_body)
    path = HISTORY[6]
    raw = result[path]
    au = region(raw,'STATE_UPPER_SILESIA','AUS')
    textile = au.children('create_building')[0]
    body = raw[textile.start:textile.end].replace('STATE_UPPER_SILESIA','STATE_WEST_GALICIA')
    raw = edits(raw, [(au.start,au.end,'')])
    result[path] = append(raw,'STATE_WEST_GALICIA','AUS','\t\t\t'+body)

    path = HISTORY[-1]
    raw = result[path]
    au = next(n for n in cw.walk(cw.parse(raw)) if n.key == 'c:AUS')
    u = next(n for n in cw.walk(au.children()) if n.key == 'combat_unit' and n.one('state_region') == 's:STATE_UPPER_SILESIA')
    assert u.one('service_type') == 'conscript' and u.one('count') == '1'
    selector = u.children('state_region')[0]
    result[path] = edits(raw, [(selector.start,selector.end,'state_region = s:STATE_WEST_GALICIA')])
    return result

if __name__ == '__main__':
    before = json.loads((OUT/'MAP2A_BASELINE.json').read_text(encoding='utf-8'))['originals']
    after = transform(before)
    lines = ['*** Begin Patch']
    for path in HISTORY:
        if before[path] == after[path]: continue
        assert (ROOT/path).read_text(encoding='utf-8-sig') == before[path], 'Concurrent edit: '+path
        lines.append('*** Update File: '+(ROOT/path).as_posix())
        delta = list(difflib.unified_diff(before[path].splitlines(), after[path].splitlines(), n=3, lineterm=''))[2:]
        if delta[0].startswith('@@ -1,') and (ROOT/path).read_bytes().startswith(b'\xef\xbb\xbf'):
            delta[1] = delta[1][0]+'\ufeff'+delta[1][1:]
        lines += ['@@' if row.startswith('@@') else row for row in delta]
    lines.append('*** End Patch')
    print(json.dumps({'patch':'\n'.join(lines)+'\n'}, ensure_ascii=False))
