"""Build the experimental solo wake relay for the direct parties to a play or war."""

import argparse
import json
from pathlib import Path

from build_native_overlay import ATTEMPTED, PLAYER_SCOPE, ROOT_WIDGET, RULE
from build_passive_overlay import write
from copy_ai_save import COHORTS, cohort


def build(interface, output, profile):
    output.mkdir()
    write(output, ".metadata/metadata.json", json.dumps({
        "name": "1776 Phase 2 — Native AI Wake Experiment",
        "id": "", "version": "0.1.0", "supported_game_version": "1.15.*",
        "short_description": "Experimental wake relay for solo player conflicts.",
        "tags": [], "relationships": [],
    }))

    markers = "\n".join(
        f"        c:{tag} ?= {{ set_variable = {{ name = aor_phase2_native_tag value = flag:{tag} }} }}"
        for tag in sorted(cohort(profile))
    )
    hooks = f"""on_game_started_after_lobby = {{ on_actions = {{ aor_phase2_register_wake_tags }} }}
on_diplo_play_start = {{ on_actions = {{ aor_phase2_wake_direct_parties }} }}
on_diplo_play_war_start = {{ on_actions = {{ aor_phase2_wake_direct_parties }} }}

aor_phase2_register_wake_tags = {{
    trigger = {{ has_game_rule = {RULE} }}
    effect = {{
{markers}
    }}
}}

aor_phase2_wake_direct_parties = {{
    trigger = {{ has_game_rule = {RULE} has_global_variable = {ATTEMPTED} }}
    effect = {{
        if = {{
            limit = {{ initiator = {{ is_player = yes }} }}
            target = {{ aor_phase2_request_native_wake = yes }}
        }}
        else_if = {{
            limit = {{ target = {{ is_player = yes }} }}
            initiator = {{ aor_phase2_request_native_wake = yes }}
        }}
    }}
}}
"""
    write(output, "common/on_actions/zz_aor_phase2_native_wake.txt", hooks, "utf-8-sig")

    request = """aor_phase2_request_native_wake = {
    if = {
        limit = {
            has_variable = aor_phase2_native_tag
            is_player = no
            NOT = { has_variable = aor_phase2_native_wake_queued }
        }
        set_variable = { name = aor_phase2_native_wake_queued days = 60 }
        add_to_global_variable_list = { name = aor_phase2_native_wake_queue target = this days = 60 }
        set_global_variable = aor_phase2_native_wake_available
        debug_log = "AOR_PHASE2|DIRECT_WAKE|REQUESTED|[THIS.GetCountry.GetNameNoFormatting]"
    }
}
"""
    write(output, "common/scripted_effects/zz_aor_phase2_native_wake.txt", request, "utf-8-sig")

    controller = """aor_phase2_native_wake_next = {
    scope = country
    is_valid = {
        is_player = yes
        has_global_variable = aor_phase2_native_wake_available
        NOT = { has_global_variable = aor_phase2_native_wake_target }
    }
    effect = {
        remove_global_variable = aor_phase2_native_wake_available
        ordered_in_global_list = {
            variable = aor_phase2_native_wake_queue
            limit = { has_variable = aor_phase2_native_tag is_player = no }
            order_by = { value = 0 }
            max = 1
            check_range_bounds = no
            set_global_variable = { name = aor_phase2_native_wake_target value = this }
            remove_list_global_variable = { name = aor_phase2_native_wake_queue target = this }
        }
    }
}

aor_phase2_native_wake_has_pending = {
    scope = country
    is_valid = { is_player = yes has_global_variable = aor_phase2_native_wake_target }
}

aor_phase2_native_wake_can_send = {
    scope = country
    is_valid = { global_var:aor_phase2_native_wake_target ?= { is_player = no } }
}

aor_phase2_native_wake_finish = {
    scope = country
    is_valid = { is_player = yes has_global_variable = aor_phase2_native_wake_target }
    effect = {
        remove_global_variable = aor_phase2_native_wake_target
        if = {
            limit = {
                any_in_global_list = {
                    variable = aor_phase2_native_wake_queue
                    has_variable = aor_phase2_native_tag
                    is_player = no
                }
            }
            set_global_variable = aor_phase2_native_wake_available
        }
    }
}
"""
    write(output, "common/scripted_guis/zz_aor_phase2_native_wake.txt", controller, "utf-8-sig")

    context = "And3(IsInGame, GetPlayer.IsValid, And(Not(GameIsMultiplayer), Not(IsIronmanEnabled)))"
    gui = f"""
        state = {{
            name = aor_phase2_native_wake_prepare
            trigger_when = "[And({context}, GetScriptedGui('aor_phase2_native_wake_next').IsValid({PLAYER_SCOPE}))]"
            on_start = "[GetScriptedGui('aor_phase2_native_wake_next').Execute({PLAYER_SCOPE})]"
            duration = 0.25
        }}
        state = {{
            name = aor_phase2_native_wake_send
            trigger_when = "[And({context}, And(Not(GetVariableSystem.Exists('aor_phase2_wake_busy')), GetScriptedGui('aor_phase2_native_wake_has_pending').IsValid({PLAYER_SCOPE})))]"
            on_start = "[GetVariableSystem.Set('aor_phase2_wake_busy', 'true')]"
            on_start = "[ExecuteConsoleCommand(Select_CString(GetScriptedGui('aor_phase2_native_wake_can_send').IsValid({PLAYER_SCOPE}), Concatenate('enable_ai ', GetGlobalVariable('aor_phase2_native_wake_target').GetCountry.GetTagName), 'help enable_ai'))]"
            duration = 1.5
            on_finish = "[GetScriptedGui('aor_phase2_native_wake_finish').Execute({PLAYER_SCOPE})]"
        }}
        state = {{
            name = aor_phase2_native_wake_clear_busy
            trigger_when = "[And({context}, And(GetVariableSystem.Exists('aor_phase2_wake_busy'), Not(GetScriptedGui('aor_phase2_native_wake_has_pending').IsValid({PLAYER_SCOPE}))))]"
            on_start = "[GetVariableSystem.Clear('aor_phase2_wake_busy')]"
            duration = 0.25
        }}
"""
    raw = interface.read_text(encoding="utf-8-sig")
    if raw.count(ROOT_WIDGET) != 1:
        raise ValueError("Expected one time control widget in the reference interface.")
    write(output, "gui/timemanip.gui", raw.replace(ROOT_WIDGET, ROOT_WIDGET + gui), "utf-8-sig")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interface", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cohort", default="E", choices=COHORTS)
    args = parser.parse_args()
    build(args.interface, args.output, args.cohort)


if __name__ == "__main__":
    main()
