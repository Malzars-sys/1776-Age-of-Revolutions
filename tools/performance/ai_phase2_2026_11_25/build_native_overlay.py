"""Build the solo native-AI startup experiment using documented GUI command queues."""

import argparse
import json
from pathlib import Path

from build_passive_overlay import write
from copy_ai_save import COHORTS, cohort


RULE = "aor_phase2_native_performance"
PLAYER_SCOPE = "GuiScope.SetRoot(GetPlayer.MakeScope).End"
ROOT_WIDGET = '\t\tname = "timemanip"'
READY = "aor_phase2_native_batch_completed"
ARMED = "aor_phase2_native_startup_armed"
ATTEMPTED = "aor_phase2_native_batch_attempted"


def concat(parts):
    if len(parts) == 1:
        return parts[0]
    middle = len(parts) // 2
    return f"Concatenate({concat(parts[:middle])}, {concat(parts[middle:])})"


def command_for(tag):
    gate = f"GetScriptedGui('aor_phase2_native_{tag}').IsValid({PLAYER_SCOPE})"
    return f"Select_CString({gate}, 'disable_ai {tag};', '')"


def build(interface, output, profile, test_default):
    selected = sorted(cohort(profile))
    assert "FRA" not in selected
    output.mkdir()
    write(output, ".metadata/metadata.json", json.dumps({
        "name": "1776 Phase 2 — Native AI Startup Experiment",
        "id": "", "version": "0.1.0", "supported_game_version": "1.15.*",
        "short_description": "Experimental solo rule for country AI controllers.",
        "tags": [], "relationships": [],
    }))

    guard = f"""aor_phase2_native_dispatch = {{
    scope = country
    is_valid = {{
        is_player = yes
        has_game_rule = {RULE}
        has_global_variable = {ARMED}
        NOT = {{ has_global_variable = {ATTEMPTED} }}
        game_date = 1776.1.1
    }}
}}

aor_phase2_native_save_dispatch_attempt = {{
    scope = country
    is_valid = {{ is_player = yes has_global_variable = {ARMED} }}
    effect = {{ set_global_variable = {ATTEMPTED} }}
}}
"""
    for tag in selected:
        guard += f"""
aor_phase2_native_{tag} = {{
    scope = country
    is_valid = {{
        c:{tag} ?= {{
            is_ai = yes
            NOT = {{ is_direct_subject_of = root }}
            NOT = {{ any_enemy_in_diplo_play = {{ is_player = yes }} }}
            NOT = {{ any_cobelligerent_in_diplo_play = {{ is_player = yes }} }}
        }}
    }}
}}
"""
    write(output, "common/scripted_guis/zz_aor_phase2_native.txt", guard, "utf-8-sig")
    on_start = f"""on_game_started_after_lobby = {{ on_actions = {{ aor_phase2_native_arm_startup }} }}

aor_phase2_native_arm_startup = {{
    trigger = {{ has_game_rule = {RULE} game_date = 1776.1.1 }}
    effect = {{ set_global_variable = {ARMED} }}
}}
"""
    write(output, "common/on_actions/zz_aor_phase2_native.txt", on_start, "utf-8-sig")

    start_gate = (f"GetScriptedGui('aor_phase2_native_dispatch').IsValid({PLAYER_SCOPE})")
    flags = "And(Not(GameIsMultiplayer), Not(IsIronmanEnabled))"
    state = f"""
        state = {{
            name = aor_phase2_native_dispatch
            trigger_when = "[And4(IsInGame, TimeKeeper.IsPaused, GetPlayer.IsValid, And({flags}, And(Not(GetVariableSystem.Exists('aor_phase2_native_dispatched')), {start_gate})))]"
            on_start = "[GetVariableSystem.Set('aor_phase2_native_dispatched', 'true')]"
            duration = 1
            on_finish = "[PdxGuiTriggerAllAnimations('aor_phase2_native_batch_0')]"
        }}
"""
    batches = [selected[start:start + 24] for start in range(0, len(selected), 24)]
    for index, tags in enumerate(batches):
        commands = concat([command_for(tag) for tag in tags] + ["'help disable_ai'"])
        if index + 1 < len(batches):
            next_actions = [f"PdxGuiTriggerAllAnimations('aor_phase2_native_batch_{index + 1}')"]
        else:
            persist = f"GetScriptedGui('aor_phase2_native_save_dispatch_attempt').Execute({PLAYER_SCOPE})"
            next_actions = [persist, f"GetVariableSystem.Set('{READY}', 'true')"]
        finish = "\n".join(f'            on_finish = "[{action}]"' for action in next_actions)
        state += f"""
        state = {{
            name = aor_phase2_native_batch_{index}
            on_start = "[ExecuteConsoleCommands({commands})]"
            duration = 4
{finish}
        }}
"""
    raw = interface.read_text(encoding="utf-8-sig")
    if raw.count(ROOT_WIDGET) != 1:
        raise ValueError("Expected one time control widget in the reference interface.")
    write(output, "gui/timemanip.gui", raw.replace(ROOT_WIDGET, ROOT_WIDGET + state), "utf-8-sig")

    default = RULE if test_default else "aor_phase2_native_full"
    rule = f"""aor_phase2_native_country_ai = {{
    default = {default}
    aor_phase2_native_full = {{ }}
    {RULE} = {{ }}
}}
"""
    write(output, "common/game_rules/zz_aor_phase2_native.txt", rule, "utf-8-sig")
    for lang, labels in {
        "english": ("Minor Country AI", "Full AI", "Performance", "Turns off AI for selected countries in solo campaigns."),
        "french": ("IA des pays mineurs", "IA complète", "Performance", "Désactive l’IA des pays sélectionnés dans les campagnes en solo."),
    }.items():
        keys = ("rule_aor_phase2_native_country_ai", "setting_aor_phase2_native_full",
                "setting_aor_phase2_native_performance", "setting_aor_phase2_native_performance_desc")
        loc = f"l_{lang}:\n" + "".join(f' {key}:0 "{text}"\n' for key, text in zip(keys, labels))
        write(output, f"localization/{lang}/aor_phase2_native_l_{lang}.yml", loc, "utf-8-sig")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("interface", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cohort", default="E", choices=COHORTS)
    parser.add_argument("--test-with-performance-default", action="store_true")
    args = parser.parse_args()
    build(args.interface, args.output, args.cohort, args.test_with_performance_default)


if __name__ == "__main__":
    main()
