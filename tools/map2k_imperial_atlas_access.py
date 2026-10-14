"""Retire standalone bitmap atlas; preserve native selectors and journal map."""
from map2k_work import ROOT, GAME
from map2a_patch import edits
from map2k_imperial_repairs import gui_end, map_menu_range

LENS = 'gui/lens_toolbar.gui'
GRID_OFFSET = '\n # Imperial atlas header occupies the first 40 pixels.\n position = { 0 40 }\n'
BUTTONS = []
LEGACY_BUTTONS = ['aor1776_hre_atlas_dropdown_entry', 'aor1776_hre_atlas_toolbar_button']

def without_atlas_access(raw):
 for name in LEGACY_BUTTONS:
  marker = 'name = "'+name+'"'
  if marker in raw:
   start = raw.rfind('button = {', 0, raw.index(marker))
   end = gui_end(raw, start)
   # Our insertion includes a leading and trailing newline only.
   raw = raw[:start-1] + raw[end+1:]
 return raw.replace(GRID_OFFSET, '')

def augment_atlas_access(files):
 source = ROOT / LENS
 raw = files.get(LENS, (source if source.exists() else GAME / LENS).read_text(encoding='utf-8-sig'))
 files[LENS] = without_atlas_access(raw)
 # Earlier compiler passes still support retiring old atlas revisions. Strip
 # their known insertions at the final UI pass, not unrelated HUD/menu content.
 rel='gui/right_click_menu.gui'
 raw=files.get(rel,(ROOT/rel if (ROOT/rel).exists() else GAME/rel).read_text(encoding='utf-8-sig'))
 a,b=map_menu_range(raw)
 if 'aor1776_hre_atlas_open' in raw[a:b]:
  native=(GAME/rel).read_text(encoding='utf-8-sig');x,y=map_menu_range(native)
  raw=edits(raw,[(a,b,native[x:y])])
 files[rel]=raw
 rel='gui/ingame_hud.gui'
 raw=files.get(rel,(ROOT/rel if (ROOT/rel).exists() else GAME/rel).read_text(encoding='utf-8-sig'))
 marker='name = "aor1776_hre_imperial_atlas"'
 if marker in raw:
  start=raw.rfind('widget = {',0,raw.index(marker));end=gui_end(raw,start)
  raw=raw[:start-1]+raw[end+1:]
 files[rel]=raw
 return files
