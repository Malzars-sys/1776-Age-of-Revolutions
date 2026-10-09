"""Read-only PM/PMG colour triage. Derived reports stay in ignored .asset-cache.

Resolve REPLACE_OR_CREATE keys and installed-game fallback. A pixel heuristic
flags candidates for visual review; it never authorises edits or claims engine QA.
"""
import argparse
from collections import Counter
import colorsys
import json
from pathlib import Path
import struct
from PIL import Image

import asset4_style_reference_audit as art


def catalog(folder, native=False):
    return {k.removeprefix('REPLACE_OR_CREATE:'): v
            for k, v in art.catalog(folder, native).items()}


def palette(path):
    counts = Counter()
    data = path.read_bytes()
    # Native BGRA8 sRGB DX10 (91) is uncompressed; read its top mip directly.
    if data[84:88] == b'DX10' and struct.unpack_from('<I', data, 128)[0] in (87, 91):
        h, w = struct.unpack_from('<II', data, 12)
        im = Image.frombytes('RGBA', (w, h), data[148:148+w*h*4], 'raw', 'BGRA')
    else:
        im = art.decode(path)
    im.thumbnail((104, 104))
    for r, g, b, alpha in im.get_flattened_data():
        if alpha < 160:
            continue
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if v < 0.25:
            continue  # outlines are not the field palette
        h *= 360
        if s < 0.18:
            kind = 'white'
        elif h < 18 or h >= 345:
            kind = 'red'
        elif h < 65:
            kind = 'ochre'
        elif h < 140:
            kind = 'green'
        elif h < 185:
            kind = 'teal'
        elif h < 255:
            kind = 'blue'
        else:
            kind = 'purple'
        counts[kind] += alpha / 255 * v
    total = sum(counts.values())
    return ({k: round(v / total, 3) for k, v in counts.most_common()}
            if total else {})


def audit():
    rules = json.loads((art.ROOT / 'docs/reports/assets/pm_palette_rules.json').read_text())
    groups = catalog('common/production_method_groups')
    pms = catalog('common/production_methods')
    native_pms = catalog('common/production_methods', True)
    native_groups = catalog('common/production_method_groups', True)
    buildings = catalog('common/buildings')
    used = {g for t, _ in buildings.values()
            for g in art.field(t, 'production_method_groups', [])}
    decoded, rows = {}, []
    for key, (tokens, source) in sorted(groups.items()):
        if key not in used:
            continue
        members = [pm for pm in art.field(tokens, 'production_methods', []) if pm in pms]
        if not source.is_relative_to(art.ROOT) and not any(pms[pm][1].is_relative_to(art.ROOT) for pm in members):
            continue
        group_texture = art.field(tokens, 'texture')
        family = rules['group_overrides'].get(key) or rules['native_group_textures'].get(Path(group_texture).name)
        override = next((v for prefix,v in rules.get('group_prefixes',{}).items() if key.startswith(prefix)), None)
        if override:
            family = override
        # An absent texture is only inherited when the installed PMG supplies it.
        if not family:
            native = native_groups.get(key)
            if native:
                family = rules['native_group_textures'].get(Path(art.field(native[0], 'texture')).name)
        expected = rules['families'][family]['palette'] if family else None
        details = []
        for pm in members:
            t, file = pms[pm]
            if not file.is_relative_to(art.ROOT):
                continue
            tex = art.field(t, 'texture')
            protected = ('copper' in key or 'copper' in pm or 'copper' in file.name or
                         file.name == '24_tech8c_research_laboratory.txt')
            path = art.resolve(tex)
            if protected:
                state, observed = 'PROTECTED', {}
            elif not path or 'error_' in tex:
                state, observed = 'PLACEHOLDER_OR_MISSING', {}
            else:
                if path not in decoded:
                    decoded[path] = palette(path)
                observed = decoded[path]
                state = ('UNKNOWN_GROUP_PALETTE' if not expected else
                         'COLOUR_REVIEW' if observed.get(expected, 0) < 0.60 else 'PALETTE_MATCH')
                if '/unused/' in tex:
                    state = 'RETAIN_UNUSED_' + state
            details.append({'pm': pm, 'texture': tex, 'new_id': pm not in native_pms,
                            'local_texture': bool(path and path.is_relative_to(art.ROOT)),
                            'state': state, 'observed': observed})
        rows.append({'group': key, 'family': family, 'expected': expected,
                     'group_texture': group_texture,
                     'group_placeholder': 'error_' in group_texture,
                     'source': source.relative_to(art.ROOT).as_posix() if source.is_relative_to(art.ROOT) else str(source),
                     'pms': details})
    counts = Counter(item['state'] for row in rows for item in row['pms'])
    unknown = [row['group'] for row in rows if not row['expected'] and any(x['state'] != 'PROTECTED' for x in row['pms'])]
    priority = {x['pm']: x for row in rows for x in row['pms']
                if (x['new_id'] or x['local_texture']) and x['state'] == 'COLOUR_REVIEW'}
    return {'status': 'READ_ONLY_COLOUR_TRIAGE', 'engine_tested': False,
            'groups_checked':len(rows), 'groups': rows, 'counts': dict(counts), 'unknown_groups': unknown,
            'unique_new_or_local_colour_review':len(priority),
            'notice': 'Heuristic review queue, not an exhaustive artistic approval. No files in common/gfx/gui are changed.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, default=Path('C:/Games/Victoria 3/game'))
    parser.add_argument('--report', action='store_true')
    args = parser.parse_args()
    art.GAME = args.game
    result = audit()
    if args.report:
        out = art.ROOT / '.asset-cache/pm_palette_2026-10-07'
        out.mkdir(parents=True, exist_ok=True)
        (out / 'audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'groups'}, indent=2))
