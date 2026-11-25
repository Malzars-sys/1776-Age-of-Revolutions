"""Build the experimental, optional passive-AI data layer outside the repository."""

import argparse
import json
from pathlib import Path
import sys

from copy_ai_save import cohort
from simperf56_save_state import parse


TRIGGER = "aor_phase2_country_is_passive"


def patch_block(raw, node, lines):
    start = raw.index("{", node.start, node.end)
    if raw[node.end - 1] != "}":
        raise ValueError(f"Expected a block for {node.key}")
    return start + 1, node.end - 1, lines(raw[start + 1:node.end - 1])


def apply_blocks(raw, patches):
    for start, end, value in sorted(patches, reverse=True):
        raw = raw[:start] + value + raw[end:]
    parse(raw)
    return raw


def default_strategy(raw):
    fields = {"wanted_construction_output": 0, "aggression": -100, "change_law_chance": -1000}
    strategy, = [node for node in parse(raw) if node.key == "ai_strategy_default"]
    patches = []
    for key, passive_value in fields.items():
        node, = strategy.children(key)
        patches.append(patch_block(raw, node, lambda original: (
            f"\n\t\tif = {{ limit = {{ {TRIGGER} = yes }} add = {passive_value} }}"
            f"\n\t\telse = {{ add = {{{original}\n\t\t}} }}\n\t"
        )))
    return apply_blocks(raw, patches)


def regional_objectives(raw):
    patches = []
    for objective in parse(raw):
        possible, = objective.children("possible")
        patches.append(patch_block(raw, possible, lambda original: (
            f"\n\t\t{TRIGGER} = no" + original
        )))
        for invalid in objective.children("invalid"):
            patches.append(patch_block(raw, invalid, lambda original: (
                f"\n\t\tOR = {{ {TRIGGER} = yes AND = {{{original}\n\t\t}} }}\n\t"
            )))
    if not patches:
        raise ValueError("The game has no recognized regional objectives.")
    return apply_blocks(raw, patches)


def write(folder, relative, data, encoding="utf-8"):
    path = folder / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding=encoding, newline="\n") as stream:
        stream.write(data)


def build(mod, steam, output, default_on):
    output.mkdir()
    write(output, ".metadata/metadata.json", json.dumps({
        "name": "1776 Phase 2 — Experimental Passive AI",
        "version": "0.1.0",
        "supported_game_version": "1.15.*",
        "id": "",
        "short_description": "Experimental rule for minor-country AI.",
        "tags": [],
        "relationships": [],
    }, indent=2))

    default_path = Path("common/ai_strategies/00_default_strategy.txt")
    region_path = Path("common/ai_regional_objectives/00_ai_regional_objectives.txt")
    for path, transform in ((default_path, default_strategy), (region_path, regional_objectives)):
        source = (mod / path) if (mod / path).is_file() else (steam / path)
        write(output, path, transform(source.read_text(encoding="utf-8-sig")), "utf-8-sig")

    trigger = f"""{TRIGGER} = {{
    has_variable = aor_phase2_passive_cohort
    is_ai = yes
    NOT = {{ has_variable = aor_phase2_active_cooldown }}
    NOT = {{ AND = {{ exists = overlord overlord = {{ is_player = yes }} }} }}
    NOT = {{ any_enemy_in_diplo_play = {{ is_player = yes }} }}
    NOT = {{ any_cobelligerent_in_diplo_play = {{ is_player = yes }} }}
}}
"""
    write(output, "common/scripted_triggers/zz_aor_phase2_passive.txt", trigger, "utf-8-sig")

    tags = "\n".join(f"        c:{tag} ?= {{ set_variable = aor_phase2_passive_cohort }}"
                     for tag in sorted(cohort("E")))
    start = """on_game_started_after_lobby = { on_actions = { aor_phase2_initialize_passive } }
on_war_end = { on_actions = { aor_phase2_war_cooldown } }

aor_phase2_initialize_passive = {
    trigger = { has_game_rule = aor_phase2_passive_ai }
    effect = {
""" + tags + """
        debug_log = "AOR_PHASE2|PASSIVE_COHORT_INITIALIZED"
    }
}

aor_phase2_war_cooldown = {
    effect = {
        if = {
            limit = { scope:actor ?= { is_player = yes } }
            scope:target ?= {
                if = {
                    limit = { has_variable = aor_phase2_passive_cohort }
                    set_variable = { name = aor_phase2_active_cooldown days = 60 }
                }
            }
        }
        if = {
            limit = { scope:target ?= { is_player = yes } }
            scope:actor ?= {
                if = {
                    limit = { has_variable = aor_phase2_passive_cohort }
                    set_variable = { name = aor_phase2_active_cooldown days = 60 }
                }
            }
        }
    }
}
"""
    write(output, "common/on_actions/zz_aor_phase2_passive.txt", start, "utf-8-sig")

    default = "aor_phase2_passive_ai" if default_on else "aor_phase2_full_ai"
    rule = f"""aor_phase2_country_ai = {{
    default = {default}
    aor_phase2_full_ai = {{ }}
    aor_phase2_passive_ai = {{ }}
}}
"""
    write(output, "common/game_rules/zz_aor_phase2_passive.txt", rule, "utf-8-sig")
    for lang, labels in {
        "english": ("Minor Country AI", "Full AI", "Countries follow their usual AI plans.",
                    "Passive AI", "Selected countries lower their construction capacity targets and scale back foreign ambitions. Human players, their subjects and countries involved in their conflicts keep regular AI planning where applicable."),
        "french": ("IA des pays mineurs", "IA complète", "Les pays suivent leurs stratégies habituelles.",
                   "IA passive", "Les pays concernés réduisent leurs objectifs de capacité de construction et leurs ambitions diplomatiques. Les joueurs, leurs sujets et les pays impliqués dans leurs conflits gardent leur fonctionnement habituel."),
    }.items():
        keys = ("rule_aor_phase2_country_ai", "setting_aor_phase2_full_ai", "setting_aor_phase2_full_ai_desc",
                "setting_aor_phase2_passive_ai", "setting_aor_phase2_passive_ai_desc")
        loc = f"l_{lang}:\n" + "".join(f' {key}:0 "{value}"\n' for key, value in zip(keys, labels))
        write(output, f"localization/{lang}/aor_phase2_ai_l_{lang}.yml", loc, "utf-8-sig")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mod", type=Path)
    parser.add_argument("steam_game", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--test-with-passive-default", action="store_true")
    args = parser.parse_args()
    build(args.mod, args.steam_game, args.output, args.test_with_passive_default)


if __name__ == "__main__":
    main()
