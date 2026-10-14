"""Build/test the companion, or explicitly integrate its validated map in the mod.

Text override is emitted as an apply_patch, not written by this generator.
DDS files/preview/report are generated data artifacts. Never change playsets.
"""
from pathlib import Path
import ctypes
import hashlib
import json
import re
import struct
import sys

import numpy as np
from PIL import Image
from map2c_work import source_bitmap
from map2k_work import ROOT, GAME, OUT
from map2l_registry import active_registry_path

PACKAGE = OUT / 'PROTOTYPES/hre_main_map'
MOD = PACKAGE / 'mod'
TILE = 512
ORIGIN = (4152, 708)
MODE = 'mm_aor1776_hre_de_jure_prototype'


def native_override():
    native = (GAME / 'gfx/FX/coloroverlay.fxh').read_text(encoding='utf-8-sig')
    include = '\t"coloroverlay_powerbloc.fxh"'
    hook = ('\t\tvoid GameProvinceOverlayAndBlend( float2 ColorMapCoords, float3 WorldSpacePos, '
            'out float3 ColorOverlay, out float PreLightingBlend, out float PostLightingBlend )\n\t\t{')
    assert native.count(include) == native.count(hook) == 1, 'Native shader changed: review manually'
    result = native.replace(include, include + '\n\t"aor1776_hre_prototype.fxh"')
    return result.replace(hook, hook + '\n\t\t\t// Opt-in companion: vanilla modes keep the original implementation.\n'
                          '\t\t\tif ( Aor1776TryImperialOverlay( ColorMapCoords, ColorOverlay, PreLightingBlend, PostLightingBlend ) )\n'
                          '\t\t\t{\n\t\t\t\treturn;\n\t\t\t}\n')


def emit_patch(integrated=False):
    files = {
        MOD / 'gfx/FX/coloroverlay.fxh': native_override(),
        PACKAGE / 'aor1776_hre_map_prototype.mod':
            'name="1776 — Carte impériale (PROTOTYPE)"\n'
            'supported_version="1.13.*"\n'
            'tags={ "Graphics" }\n'
            f'path="{(ROOT.parent / "aor1776_hre_map_prototype").as_posix()}"\n',
    }
    if integrated:
        # Keep identical resource paths and the tested internal map-mode key.
        # This also avoids duplicate modes if the old companion stays enabled.
        files = {ROOT / 'gfx/FX/coloroverlay.fxh': native_override()}
        for relative in ['gfx/FX/aor1776_hre_prototype.fxh',
                         'gfx/map/map_modes/aor1776_hre_prototype.txt']:
            files[ROOT / relative] = (MOD / relative).read_text(encoding='utf-8-sig')
        for language, label in [('french', 'Territoires de jure du Saint-Empire'),
                                ('english', 'Holy Roman Empire de-jure territories')]:
            files[ROOT / f'localization/{language}/aor1776_hre_prototype_l_{language}.yml'] = (
                '\ufeffl_' + language + ':\n ' + MODE + ': "' + label + '"\n')
    print('*** Begin Patch')
    for path, content in files.items():
        relative = path.relative_to(ROOT).as_posix()
        if path.exists():
            old = path.read_text(encoding='utf-8')
            if old == content:
                continue
            print(f'*** Update File: {relative}\n@@')
            print('\n'.join('-' + line for line in old.splitlines()))
            print('\n'.join('+' + line for line in content.splitlines()))
        else:
            print(f'*** Add File: {relative}')
            print('\n'.join('+' + line for line in content.splitlines()))
    print('*** End Patch')


def dds(image, path):
    """Legacy A8R8G8B8 with complete mips, same dimensions/format for all slots."""
    levels = []
    w, h = image.size
    count = 0
    while True:
        pixels = np.asarray(image.resize((w, h), Image.Resampling.NEAREST), dtype=np.uint8)
        levels.append(pixels[:, :, [2, 1, 0, 3]].tobytes())
        count += 1
        if w == h == 1:
            break
        w, h = max(1, w // 2), max(1, h // 2)
    header = bytearray(128)
    header[:4] = b'DDS '
    for offset, value in [(4, 124), (8, 0x2100f), (12, image.height), (16, image.width),
                          (20, image.width * 4), (28, count), (76, 32), (80, 0x41),
                          (88, 32), (92, 0xff0000), (96, 0xff00), (100, 0xff),
                          (104, 0xff000000), (108, 0x401008)]:
        struct.pack_into('<I', header, offset, value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + b''.join(levels))


def compile_helper():
    """Compile actual helper HLSL with D3D11-compatible stand-ins for native bindings.

    This does NOT compile the Paradox include/preprocessor or run the game.
    """
    helper = (MOD / 'gfx/FX/aor1776_hre_prototype.fxh').read_text(encoding='utf-8')
    code = helper.split('[[', 1)[1].split(']]', 1)[0]
    harness = '''
Texture2DArray<float4> MapPaintingTextures : register(t0);
Texture2D<float4> ProvinceColorIndirectionTexture : register(t1);
Texture2D<float4> ProvinceColorTexture : register(t2);
SamplerState TestSampler : register(s0);
cbuffer TestConstants : register(b0) {
 bool _UseMapmodeTextures; float _OverlayOpacity;
 float2 _ProvinceMapSize; float2 AlternateProvinceColorsOffset;
};
#define PdxTex2DLod0(T, UV) T.SampleLevel(TestSampler, UV, 0)
float3 ToLinear(float3 c) { return pow(c, 2.2); }
float4 ColorSampleAtOffset(float2 uv, Texture2D<float4> a, Texture2D<float4> b, float2 off) {
 return b.SampleLevel(TestSampler, uv + off, 0);
}
''' + code + '''
float4 main(float2 uv : TEXCOORD0) : SV_Target {
 float3 color = float3(0,0,0); float before=0; float after=0;
 bool painted = Aor1776TryImperialOverlay(uv,color,before,after);
 return float4(color, painted ? after : before);
}
'''
    compiler = ctypes.WinDLL('d3dcompiler_47.dll')
    compile_fn = compiler.D3DCompile
    compile_fn.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_char_p,
                          ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p,
                          ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint,
                          ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)]
    compile_fn.restype = ctypes.c_long
    blob, errors = ctypes.c_void_p(), ctypes.c_void_p()
    source = harness.encode('utf-8')
    hr = compile_fn(source, len(source), b'HRE-prototype-harness', None, None,
                    b'main', b'ps_5_0', 0x800, 0, ctypes.byref(blob), ctypes.byref(errors))

    def read_and_release(ptr):
        if not ptr.value:
            return b''
        table = ctypes.cast(ptr, ctypes.POINTER(ctypes.POINTER(ctypes.c_void_p))).contents
        get_buffer = ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)(table[3])
        get_size = ctypes.WINFUNCTYPE(ctypes.c_size_t, ctypes.c_void_p)(table[4])
        release = ctypes.WINFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p)(table[2])
        data = ctypes.string_at(get_buffer(ptr), get_size(ptr))
        release(ptr)
        return data

    diagnostics = read_and_release(errors).decode('utf-8', errors='replace')
    bytecode = read_and_release(blob)
    return {'passed': hr >= 0 and bool(bytecode), 'hresult': hr,
            'bytecode_bytes': len(bytecode), 'diagnostics': diagnostics,
            'scope': 'Custom helper in a D3DCompile ps_5_0 harness; NOT the full game shader'}


def build_and_test():
    PACKAGE.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        assert condition, name

    ledger = json.loads(active_registry_path().read_text(encoding='utf-8'))
    rights = np.array([int(r['rgb'][1:], 16) for r in ledger], dtype=np.uint32)
    check('Distinct reviewed imperial province RGBs', len(rights) == len(set(rights)) and len(rights) >= 278)
    image = Image.open(source_bitmap()).convert('RGB')
    pixels = np.asarray(image, dtype=np.uint32)
    packed = (pixels[:, :, 0] << 16) | (pixels[:, :, 1] << 8) | pixels[:, :, 2]
    imperial = np.isin(packed, rights)
    ys, xs = np.nonzero(imperial)
    x0, y0 = ORIGIN
    check('Every imperial pixel fits the lossless 512 tile',
          xs.min() >= x0 and xs.max() < x0 + TILE and ys.min() >= y0 and ys.max() < y0 + TILE)
    check('Every registered province exists in the effective bitmap',
          set(np.unique(packed[imperial])) == set(rights))
    mask = np.zeros((TILE, TILE, 4), dtype=np.uint8)
    mask[:, :, 3] = 255
    mask[:, :, 0] = imperial[y0:y0 + TILE, x0:x0 + TILE] * 255
    sentinel = np.zeros_like(mask)
    sentinel[:, :TILE // 2] = [255, 0, 255, 255]
    sentinel[:, TILE // 2:] = [0, 255, 255, 255]
    textures = MOD / 'gfx/map/map_painting'
    dds(Image.fromarray(mask), textures / 'aor1776_hre_mask.dds')
    dds(Image.fromarray(sentinel), textures / 'aor1776_hre_sentinel.dds')
    for name, expected in [('mask', mask), ('sentinel', sentinel)]:
        decoded = np.asarray(Image.open(textures / f'aor1776_hre_{name}.dds').convert('RGBA'))
        check(f'{name} DDS round-trip is pixel-exact', np.array_equal(decoded, expected))
    # Same half-texel/floor convention as HLSL, including vertical world->PNG flip.
    u = (xs.astype(np.float64) + 0.5) / image.width
    v = 1.0 - (ys.astype(np.float64) + 0.5) / image.height
    sampled_x = np.floor(u * image.width).astype(int) - x0
    sampled_y = np.floor((1.0 - v) * image.height).astype(int) - y0
    check('Shader-coordinate emulation includes every imperial pixel',
          np.all(mask[sampled_y, sampled_x, 0] == 255))
    reconstructed = np.zeros_like(imperial)
    reconstructed[y0:y0 + TILE, x0:x0 + TILE] = mask[:, :, 0] == 255
    check('No added or omitted pixels across the full world', np.array_equal(reconstructed, imperial))
    # Conservative guard: compare all native map-painting assets at the two probes.
    collisions, unreadable = [], []
    scanned = 0
    for path in (GAME / 'gfx/map/map_painting').rglob('*.dds'):
        try:
            rgba = np.asarray(Image.open(path).convert('RGBA'), dtype=float) / 255
            a = rgba[rgba.shape[0] // 2, rgba.shape[1] // 4]
            b = rgba[rgba.shape[0] // 2, 3 * rgba.shape[1] // 4]
            scanned += 1
            if a[0] > .99 and a[1] < .01 and a[2] > .99 and a[3] > .99 and b[0] < .01 and b[1] > .99 and b[2] > .99 and b[3] > .99:
                collisions.append(str(path))
        except (OSError, ValueError) as exc:
            unreadable.append({'path': str(path), 'error': str(exc)})
    check('No native texture matches the prototype-only double sentinel', not collisions and not unreadable and scanned > 0)
    check('Non-texture vanilla modes return before any sentinel sample',
          'if ( !_UseMapmodeTextures )' in (MOD / 'gfx/FX/aor1776_hre_prototype.fxh').read_text())
    check('Full native shader is preserved outside one include/entry hook',
          (MOD / 'gfx/FX/coloroverlay.fxh').read_text(encoding='utf-8-sig') == native_override())
    mode_text = (MOD / 'gfx/map/map_modes/aor1776_hre_prototype.txt').read_text()
    check('All ten array slots explicitly use same-format 512 textures',
          len(re.findall(r'(?:primary|secondary|alternate)_color_\w+\s*=', mode_text)) == 10)
    check('New visible native mode, no replacement of existing modes',
          'is_visible = yes' in mode_text and len(re.findall(r'^mm_\w+\s*=\s*{', mode_text, re.M)) == 1)
    icon = ROOT / 'gfx/interface/icons/map_mode_icons/aor1776_hre_territories.dds'
    target_icon = MOD / 'gfx/interface/icons/map_mode_icons/aor1776_hre_territories.dds'
    target_icon.parent.mkdir(parents=True, exist_ok=True)
    target_icon.write_bytes(icon.read_bytes())
    check('User-approved map icon preserved byte-for-byte', target_icon.read_bytes() == icon.read_bytes())
    for language in ['french', 'english']:
        path = MOD / f'localization/{language}/aor1776_hre_prototype_l_{language}.yml'
        # Normalise generated localization encoding only, without changing source text.
        if not path.read_bytes().startswith(b'\xef\xbb\xbf'):
            path.write_bytes(b'\xef\xbb\xbf' + path.read_bytes())
        check(f'{language} localization includes visible map name', f' {MODE}:' in path.read_text(encoding='utf-8-sig'))
    gpu = compile_helper()
    check('Custom HLSL helper compiles with Windows D3DCompile', gpu['passed'])
    preview = np.zeros((TILE, TILE, 3), dtype=np.uint8)
    preview[:] = [86, 89, 92]
    preview[mask[:, :, 0] == 255] = [240, 204, 61]
    Image.fromarray(preview).save(PACKAGE / 'mask_preview.png')
    report = {'status': 'PASS_OFFLINE_NATIVE_GAME_TEST_PENDING', 'checks': checks,
              'province_RGBs': len(rights), 'imperial_pixels': int(imperial.sum()),
              'bitmap_dimensions': list(image.size), 'tile_origin_png': list(ORIGIN), 'tile_size': TILE,
              'native_map_painting_textures_checked': scanned, 'native_collisions': collisions,
              'hlsl_harness': gpu, 'registry_sha256': hashlib.sha256(active_registry_path().read_bytes()).hexdigest(),
              'native_coloroverlay_sha256': hashlib.sha256((GAME / 'gfx/FX/coloroverlay.fxh').read_bytes()).hexdigest(),
              'runtime_verified': False, 'active_playset_changed': False,
              'limitations': ['Actual mode registration/array upload/native shader compilation need an in-game test.',
                              'Static de-jure registry, not a dynamic engine filter for arbitrary state modifiers.',
                              'World UV vertical orientation must be confirmed in game.',
                              'Other mods replacing coloroverlay.fxh conflict; disable them for the test.']}
    (PACKAGE / 'VALIDATION.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if sys.argv[1:] == ['--emit-patch']:
        emit_patch()
    elif sys.argv[1:] == ['--build-test']:
        build_and_test()
    elif sys.argv[1:] == ['--emit-integrated-patch']:
        emit_patch(integrated=True)
    elif sys.argv[1:] == ['--integrated-build-test']:
        MOD = ROOT
        PACKAGE = OUT / 'MAIN_MAP'
        build_and_test()
    else:
        raise SystemExit('Use --emit-patch/--build-test or --emit-integrated-patch/--integrated-build-test. No launcher mutation.')
