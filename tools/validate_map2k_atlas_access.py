"""Regress actual lens dropdown wiring; native rendering still needs a game test."""
import validate_diplomacy_ottoman_1776 as cw
from map2k_work import ROOT, GAME
from map2k_imperial_atlas_access import LENS, without_atlas_access, augment_atlas_access

def validate_atlas_access(check, node, textnode):
 raw=(ROOT/LENS).read_text(encoding='utf-8-sig')
 native=(GAME/LENS).read_text(encoding='utf-8-sig')
 check('atlas_access_preserves_all_native_lens_contents',without_atlas_access(raw)==native)
 check('atlas_access_generator_is_repeatable',without_atlas_access(without_atlas_access(raw))==native)
 tree=cw.parse(raw)
 widgets=list(cw.walk(tree))
 dropdown=next(n for n in widgets if n.key=='dropDown' and n.one('datamodel')=='"[GetMapModeIndices]"')
 scroll=next(n for n in cw.walk(dropdown.children('list')) if n.key=='scrollwidget')
 check('native_scrollwidget_item_descriptor_has_exactly_one_child',len(scroll.children())==1 and scroll.children()[0].key=='fixedgridbox')
 grid=scroll.children('fixedgridbox')
 check('native_map_grid_has_no_injected_atlas_header_or_offset',len(grid)==1 and not grid[0].children('position') and 'aor1776_hre_atlas_dropdown_entry' not in raw)
 native_dropdown=next(n for n in cw.walk(cw.parse(native)) if n.key=='dropDown' and n.one('datamodel')=='"[GetMapModeIndices]"')
 check('entire_native_map_dropdown_is_unchanged',raw[dropdown.start:dropdown.end]==native[native_dropdown.start:native_dropdown.end])
 for key in ['active_item','item','list']:
  descriptor=dropdown.children(key)[0]
  check('native_dropdown_descriptor_single_child:'+key,len(descriptor.children())==1)
 check('atlas_access_regeneration_keeps_corrected_toolbar',augment_atlas_access({LENS:raw})[LENS]==raw)
 check('entire_toolbar_restored_to_native',raw==native)
 check('native_map_selection_callbacks_preserved',dropdown.one('onselectionchanged')=='"[SetDefaultMapMode]"' and dropdown.one('selectedindex')=='"[GetSelectedMapMode]"')
 check('obsolete_bitmap_atlas_toolbar_button_removed','aor1776_hre_atlas_open' not in raw and 'aor1776_hre_atlas_toolbar_button' not in raw)
 journal=(ROOT/'gui/journal_entry_widgets/1776_imperial_widgets.gui').read_text(encoding='utf-8-sig')
 check('requested_journal_bitmap_map_retained','gfx/interface/journal_entries/aor1776_hre_registered_map.dds' in journal)
