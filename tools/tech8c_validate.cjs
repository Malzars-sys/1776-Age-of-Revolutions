#!/usr/bin/env node
// Read-only targeted validation. This is NOT an engine/runtime test.
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const root = path.resolve(__dirname, "..");
const game = process.argv[2] || "C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game";
const expectedProducers = [
  {
    "building": "building_phosphate_mine",
    "path": "common/buildings/15_tech6c6b_phosphate_mine.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_alloys_plant",
    "path": "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_bauxite_mine",
    "path": "common/buildings/14_tech6c5c_bauxite_mine.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_copper_mine",
    "path": "common/buildings/13_tech6c5b_copper_mine.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_oil_refinery",
    "path": "common/buildings/12_tech6c4_oil_refinery.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_cement_works",
    "path": "common/buildings/11_tech6c1b_cement_works.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_port",
    "path": "common/buildings/11_private_infrastructure.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_private_infrastructure"
  },
  {
    "building": "building_trade_center",
    "path": "common/buildings/11_private_infrastructure.txt",
    "pmg": "pmg_1776_trade_data_reporting",
    "group": "bg_trade"
  },
  {
    "building": "building_limestone_quarry",
    "path": "common/buildings/10_tech6c1_limestone_quarry.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_salt_mine",
    "path": "common/buildings/10_tech6a1b_salt_buildings.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_salt_mining"
  },
  {
    "building": "building_salt_pan",
    "path": "common/buildings/10_tech6a1b_salt_buildings.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_government_administration",
    "path": "common/buildings/07_government.txt",
    "pmg": "pmg_1776_administrative_data_reporting",
    "group": "bg_bureaucracy"
  },
  {
    "building": "building_university",
    "path": "common/buildings/07_government.txt",
    "pmg": "pmg_1776_institutional_data_reporting",
    "group": "bg_technology"
  },
  {
    "building": "building_coal_mine",
    "path": "common/buildings/03_mines.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_iron_mine",
    "path": "common/buildings/03_mines.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_lead_mine",
    "path": "common/buildings/03_mines.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_sulfur_mine",
    "path": "common/buildings/03_mines.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_gold_mine",
    "path": "common/buildings/03_mines.txt",
    "pmg": "pmg_1776_raw_data_reporting",
    "group": "bg_mining"
  },
  {
    "building": "building_food_industry",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_light_data_reporting",
    "group": "bg_light_industry"
  },
  {
    "building": "building_textile_mill",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_light_data_reporting",
    "group": "bg_light_industry"
  },
  {
    "building": "building_furniture_manufactory",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_light_data_reporting",
    "group": "bg_light_industry"
  },
  {
    "building": "building_glassworks",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_light_data_reporting",
    "group": "bg_light_industry"
  },
  {
    "building": "building_tooling_workshop",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_light_data_reporting",
    "group": "bg_light_industry"
  },
  {
    "building": "building_paper_mill",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_light_data_reporting",
    "group": "bg_light_industry"
  },
  {
    "building": "building_chemical_plant",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_explosives_factory",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_synthetics_plant",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_steel_mill",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_motor_industry",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_shipyard",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_ship_construction"
  },
  {
    "building": "building_automotive_industry",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_electrics_industry",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_heavy_industry"
  },
  {
    "building": "building_arms_industry",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_military_industry"
  },
  {
    "building": "building_artillery_foundry",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_military_industry"
  },
  {
    "building": "building_munition_plant",
    "path": "common/buildings/01_industry.txt",
    "pmg": "pmg_1776_heavy_data_reporting",
    "group": "bg_military_industry"
  }
];
const before = [
  {
    "path": "common/buildings/99_cleanup2e4_merchant_republic_monuments.txt",
    "fingerprint": "303966b4"
  },
  {
    "path": "common/buildings/15_tech6c6b_phosphate_mine.txt",
    "fingerprint": "657722b9"
  },
  {
    "path": "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt",
    "fingerprint": "7352c665"
  },
  {
    "path": "common/buildings/14_tech6c5c_bauxite_mine.txt",
    "fingerprint": "3b08c30f"
  },
  {
    "path": "common/buildings/13_tech6c5b_copper_mine.txt",
    "fingerprint": "d0895679"
  },
  {
    "path": "common/buildings/13_construction.txt",
    "fingerprint": "fb664eb1"
  },
  {
    "path": "common/buildings/12_tech6c4_oil_refinery.txt",
    "fingerprint": "f5c3f03b"
  },
  {
    "path": "common/buildings/11_tech6c1b_cement_works.txt",
    "fingerprint": "d9d00874"
  },
  {
    "path": "common/buildings/11_private_infrastructure.txt",
    "fingerprint": "0436f19d"
  },
  {
    "path": "common/buildings/10_tech6c1_limestone_quarry.txt",
    "fingerprint": "01e8ee68"
  },
  {
    "path": "common/buildings/10_tech6a3_spice_plantation.txt",
    "fingerprint": "776d953b"
  },
  {
    "path": "common/buildings/10_tech6a1b_salt_buildings.txt",
    "fingerprint": "052ece30"
  },
  {
    "path": "common/buildings/10_canals.txt",
    "fingerprint": "11e054ca"
  },
  {
    "path": "common/buildings/09_misc_resource.txt",
    "fingerprint": "7799bdaf"
  },
  {
    "path": "common/buildings/07_government.txt",
    "fingerprint": "306b8d17"
  },
  {
    "path": "common/buildings/06_urban_center.txt",
    "fingerprint": "caad8ab3"
  },
  {
    "path": "common/buildings/05_military.txt",
    "fingerprint": "b2871380"
  },
  {
    "path": "common/buildings/04_plantations.txt",
    "fingerprint": "469f0356"
  },
  {
    "path": "common/buildings/03_mines.txt",
    "fingerprint": "7ed7b58f"
  },
  {
    "path": "common/buildings/02_agro.txt",
    "fingerprint": "b0c09172"
  },
  {
    "path": "common/buildings/01_industry.txt",
    "fingerprint": "34bf923a"
  }
];
const errors = [];
let checks = 0;
function check(condition, label) {
  checks++;
  if (!condition) errors.push(label);
}
function read(relative, base = root) { return fs.readFileSync(path.join(base, relative), "utf8"); }
function norm(s) { return s.replace(/\r\n/g, "\n").replace(/^\uFEFF/, "").trimEnd(); }
function fingerprint(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return (h >>> 0).toString(16).padStart(8, "0");
}
// String/comment masking retains offsets and newlines.
function mask(s) {
  return s.replace(/"(?:\\.|[^"\\])*"|#[^\r\n]*/g, m => m.replace(/[^\r\n]/g, " "));
}
function blocks(s, label = "") {
  const clean = mask(s);
  const re = /([A-Za-z_][\w:.-]*)\s*=\s*\{/g;
  const out = [];
  let m;
  while ((m = re.exec(clean))) {
    let depth = 1, end = m.index + m[0].length;
    for (; end < clean.length && depth; end++) {
      if (clean[end] === "{") depth++;
      if (clean[end] === "}") depth--;
    }
    if (depth) throw new Error("Unclosed " + label + ": " + m[1]);
    out.push({ id: m[1], start: m.index, end, text: s.slice(m.index, end) });
    re.lastIndex = end;
  }
  return out;
}
function body(s, id) {
  const clean = mask(s);
  const m = new RegExp("\\b" + id + "\\s*=\\s*\\{").exec(clean);
  if (!m) return null;
  const start = m.index + m[0].length;
  let d = 1, end = start;
  for (; end < clean.length && d; end++) {
    if (clean[end] === "{") d++;
    if (clean[end] === "}") d--;
  }
  if (d) throw new Error("Unclosed nested " + id);
  return s.slice(start, end - 1);
}
function tokens(s) { return (mask(s || "").match(/[A-Za-z_][\w:.-]*/g) || []); }
function number(s, id) {
  const match = new RegExp("\\b" + id + "\\s*=\\s*(-?\\d+(?:\\.\\d+)?)").exec(mask(s));
  return match ? Number(match[1]) : null;
}
function catalog(dir, bases) {
  const files = new Map();
  for (const base of bases) {
    const target = path.join(base, dir);
    if (!fs.existsSync(target)) continue;
    for (const file of fs.readdirSync(target).filter(f => f.endsWith(".txt")).sort())
      files.set(file, path.join(target, file));
  }
  const out = new Map();
  for (const filename of files.values()) {
    for (const b of blocks(fs.readFileSync(filename, "utf8"), filename)) out.set(b.id, b.text);
  }
  return out;
}
const newPaths = [
  "common/goods/18_tech8c_research_data.txt",
  "common/script_values/12_tech8c_research_laboratory.txt",
  "common/buildings/16_tech8c_research_laboratory.txt",
  "common/production_method_groups/16_tech8c_research_laboratory.txt",
  "common/production_methods/23_tech8c_research_data.txt",
  "common/production_methods/24_tech8c_research_laboratory.txt",
  "common/modifier_type_definitions/13_tech8c_research_data_modifier_types.txt",
  "common/modifier_type_definitions/14_tech8c_laboratory_output_markers.txt",
  "common/static_modifiers/11_tech8c_laboratory_operation.txt",
  "common/scripted_triggers/11_tech8c_laboratory_operation.txt",
  "common/script_values/13_tech8c_laboratory_operation.txt",
  "common/scripted_effects/13_tech8c_laboratory_operation.txt",
  "common/on_actions/11_tech8c_laboratory_operation.txt",
  "gui/tech8c_research_data_texticons.gui",
  "events/1776_research_laboratory_test_events.txt"
];
for (const f of newPaths) {
  check(!/[ \t]+\r?$/m.test(read(f)), "Trailing whitespace: " + f);
  const s = mask(read(f));
  let depth = 0;
  let invalid = false;
  for (const c of s) { if (c === "{") depth++; if (c === "}") depth--; if (depth < 0) invalid = true; }
  check(!invalid, "Extra closing brace: " + f);
  check(depth === 0, "Unbalanced braces: " + f);
}
const buildings = catalog("common/buildings", [game, root]);
const pmgs = catalog("common/production_method_groups", [game, root]);
const pms = catalog("common/production_methods", [game, root]);
const goods = catalog("common/goods", [game, root]);
// descriptor replaces the technology directory: only the mod catalog is authoritative.
const techs = catalog("common/technology/technologies", [root]);
const modifiers = catalog("common/modifier_type_definitions", [game, root]);
const newPms = [
  ...blocks(read("common/production_methods/23_tech8c_research_data.txt")),
  ...blocks(read("common/production_methods/24_tech8c_research_laboratory.txt"))
];
const newPmgs = blocks(read("common/production_method_groups/16_tech8c_research_laboratory.txt"));
const lab = buildings.get("building_research_laboratory");
check(Boolean(lab), "Missing laboratory");
check(number(read("common/script_values/12_tech8c_research_laboratory.txt"), "construction_cost_1776_research_laboratory") === 1000, "Construction must equal 1000");
check(/required_construction\s*=\s*construction_cost_1776_research_laboratory/.test(lab), "Lab construction value disconnected");
check(/expandable\s*=\s*yes/.test(lab), "Lab not extensible");
check(!/\b(?:max_level|max_levels|stateregion_max_level|potential|possible|can_build_government)\s*=/.test(mask(lab)), "Unrequested state/national construction gate");
check(/building_group\s*=\s*bg_technology/.test(lab), "Lab must use public technology group");
check(/can_build_private\s*=\s*\{\s*always\s*=\s*no/.test(lab), "Lab unexpectedly privately funded");
check(tokens(body(lab, "unlocking_technologies")).join() === "experimental_research_laboratories", "Lab access technology changed");
check(tokens(body(lab, "production_method_groups")).length === 2, "Equipment and specialization not separate");
for (const g of tokens(body(lab, "production_method_groups"))) check(pmgs.has(g), "Lab PMG missing: " + g);
for (const b of expectedProducers) {
  const s = buildings.get(b.building);
  const groups = tokens(body(s, "production_method_groups"));
  check(groups.filter(g => g === b.pmg).length === 1, "Missing/duplicate producer PMG: " + b.building);
}
const actualProducers = [...buildings].filter(([,s]) => /pmg_1776_(?:raw|light|heavy|trade|administrative|institutional)_data_reporting/.test(s)).map(([id]) => id).sort();
check(JSON.stringify(actualProducers) === JSON.stringify(expectedProducers.map(b => b.building).sort()), "Producer list mismatch");
for (const f of before) {
  const current = read(f.path).replace(/^[\t ]*pmg_1776_(?:raw|light|heavy|trade|administrative|institutional)_data_reporting[\t ]*\r?\n/gm, "");
  check(fingerprint(norm(current)) === f.fingerprint, "Preexisting building content changed beyond appended PMG: " + f.path);
}
for (const g of newPmgs) {
  const methods = tokens(body(g.text, "production_methods"));
  check(methods.length >= 2, "PMG lacks choices: " + g.id);
  for (const pm of methods) check(pms.has(pm), "PMG references missing PM: " + pm);
  check(methods.filter(pm => /is_default\s*=\s*yes/.test(pms.get(pm))).length === 1, "PMG needs exactly one default: " + g.id);
}
for (const pm of newPms) {
  check(!/\bcountry_weekly_innovation_add\s*=/.test(mask(pm.text)), "Forbidden innovation production: " + pm.id);
  for (const t of tokens(body(pm.text, "unlocking_technologies"))) check(techs.has(t), "Missing tech: " + t);
  for (const m of pm.text.matchAll(/goods_(?:input|output)_([a-z_]+)_(?:add|mult)\s*=/g))
    check(goods.has(m[1]), "Missing input/output good: " + m[1]);
  for (const m of pm.text.matchAll(/(building_1776_[a-z_]+)\s*=/g))
    check(modifiers.has(m[1]), "Unknown output marker: " + m[1]);
}
check(number(pms.get("pm_1776_raw_data_reporting"), "goods_output_raw_industrial_data_add") === 1, "Normal raw-data output changed");
check(number(pms.get("pm_1776_light_data_reporting"), "goods_output_raw_industrial_data_add") === 2, "Light industry must yield 2 raw data");
check(number(pms.get("pm_1776_heavy_data_reporting"), "goods_output_raw_industrial_data_add") === 4, "Heavy industry must yield 4 raw data");
const dataUnlocks = [
  ["raw","scientific_metrology"], ["light","scientific_metrology"], ["heavy","scientific_metrology"],
  ["trade","specialized_professional_societies"], ["administrative","specialized_professional_societies"], ["institutional","specialized_professional_societies"]
];
for (const [kind,technology] of dataUnlocks) {
  const pm = pms.get("pm_1776_" + kind + "_data_reporting");
  check(techs.has(technology), "Data unlock technology missing: " + technology);
  check(tokens(body(pm,"unlocking_technologies")).join() === technology, "Wrong data production unlock: " + kind);
  check(!/is_default\s*=\s*yes/.test(pm), "Locked data production must not be the default: " + kind);
}
check(number(pms.get("pm_1776_administrative_data_reporting"), "goods_output_organized_research_data_add") === 1, "Administrative data output");
check(number(pms.get("pm_1776_trade_data_reporting"), "goods_output_organized_research_data_add") === 1, "Trade data output");
check(number(pms.get("pm_1776_institutional_data_reporting"), "goods_output_organized_research_data_add") === 2, "University data output");
check(number(goods.get("raw_industrial_data"), "cost") === number(goods.get("steel"), "cost"), "Raw data price must match steel");
check(number(goods.get("organized_research_data"), "cost") === number(goods.get("spices"), "cost"), "Organized data price must match spices");
const compilationRecipes = [
  ["pm_1776_trade_data_reporting", 1, 0.25, 10],
  ["pm_1776_administrative_data_reporting", 1, 0.25, 10],
  ["pm_1776_institutional_data_reporting", 2, 0.5, 20]
];
for (const [id,quantity,paper,clerks] of compilationRecipes) {
  const pm = pms.get(id);
  const recipe = body(body(pm, "building_modifiers"), "workforce_scaled");
  check(number(recipe, "goods_input_raw_industrial_data_add") === quantity, "Compilation must consume raw data at 1:1: " + id);
  check(number(recipe, "goods_output_organized_research_data_add") === quantity, "Compilation output and raw input differ: " + id);
  check(number(recipe, "goods_input_paper_add") === paper, "Compilation paper recipe changed: " + id);
  check(number(pm, "building_employment_clerks_add") === clerks, "Compilation staffing changed: " + id);
  check(!/goods_input_organized_research_data_/.test(pm), "Compilation must not consume its own output: " + id);
}
for (const id of ["pm_1776_no_raw_data_reporting", "pm_1776_no_organized_data_reporting"]) {
  check(!/goods_(?:input|output)_/.test(pms.get(id)), "Disabled reporting must neither consume nor produce goods: " + id);
  check(/is_default\s*=\s*yes/.test(pms.get(id)) && body(pms.get(id),"unlocking_technologies") === null, "Off PM must remain an always-accessible default: " + id);
}
const tiers = ["manual", "electrical", "advanced"];
const caps = [5, 10, 20];
const employees = [2500, 5000, 10000];
const chemicalInputs = [5, 10, 20];
const costs = [];
for (const [i,tier] of tiers.entries()) {
  const id = "pm_1776_" + tier + "_research_laboratory";
  const s = pms.get(id);
  check(number(body(body(s, "building_modifiers"), "workforce_scaled"), "building_1776_laboratory_capacity_add") === caps[i], "Wrong/unstaffed potential output: " + id);
  check(body(s, "country_modifiers") === null, "Native output would bypass shortage monitor: " + id);
  check(number(s, "goods_input_raw_industrial_data_add") > 0, "Lab must consume raw data");
  check(i === 2 ? number(s, "goods_input_organized_research_data_add") === 40 : number(s, "goods_input_organized_research_data_add") === null, "Organized data belong only to final equipment tier");
  check(number(s, "goods_input_tools_add") > 0, "Lab must consume tools");
  check(number(body(body(s, "building_modifiers"), "workforce_scaled"), "goods_input_industrial_chemicals_add") === chemicalInputs[i], "Wrong acid/reagent input or scaling: " + id);
  check(modifiers.has("goods_input_industrial_chemicals_add"), "Missing acid/reagent input modifier");
  const jobs = [...s.matchAll(/building_employment_[a-z_]+_add\s*=\s*(\d+)/g)].reduce((sum,m) => sum + Number(m[1]), 0);
  check(jobs === employees[i], "Wrong staffing: " + id);
  const inputs = [...s.matchAll(/goods_input_([a-z_]+)_add\s*=\s*([\d.]+)/g)];
  const cost = inputs.reduce((sum,m) => sum + Number(m[2]) * number(goods.get(m[1]), "cost"), 0);
  costs.push({tier, innovationCap:caps[i], employees:jobs, industrialChemicalInput:chemicalInputs[i], inputBasePriceCost:cost, specializedInputBasePriceCost:cost + 20 * number(goods.get("organized_research_data"),"cost")});
}
check(costs[0].inputBasePriceCost < costs[1].inputBasePriceCost && costs[1].inputBasePriceCost < costs[2].inputBasePriceCost, "Equipment tiers not increasingly costly");
for (const g of ["precision_machinery","radios","telephones","pharmaceuticals","electricity"])
  check(number(pms.get("pm_1776_advanced_research_laboratory"), "goods_input_" + g + "_add") > 0, "Advanced lab lacks " + g);
for (const cat of ["production","military","society"]) {
  const pm = pms.get("pm_1776_" + cat + "_research");
  check(number(pm, "building_1776_" + cat + "_research_add") === 0.01, "Wrong specialist potential: " + cat);
  check(number(pm, "goods_input_organized_research_data_add") === 20, "Specialist must consume organized data");
  check([...pm.matchAll(/building_1776_[a-z_]+_research_add\s*=/g)].length === 1, "Specialist affects multiple categories: " + cat);
}
const researchCategories = ["production","military","society"];
const generalPm = pms.get("pm_1776_general_research");
const generalPotential = body(body(generalPm, "building_modifiers"), "workforce_scaled");
check(body(generalPm, "country_modifiers") === null, "General research must use the operational monitor");
check(!/goods_input_/.test(generalPm), "General research must not add input consumption");
check([...generalPotential.matchAll(/building_1776_[a-z_]+_research_add\s*=/g)].length === 3, "General research must affect exactly three categories");
for (const cat of researchCategories) {
  check(number(generalPotential, "building_1776_" + cat + "_research_add") === 0.0025, "General potential must be 0.25%: " + cat);
  check(number(modifiers.get("building_1776_" + cat + "_research_add"), "decimals") === 2, "General potential display must retain 0.25% precision: " + cat);
}
for (const g of ["raw_industrial_data","organized_research_data"]) {
  check(goods.has(g), "Missing data good");
  for (const io of ["input","output"]) for (const mode of ["add","mult"])
    check(modifiers.has("goods_" + io + "_" + g + "_" + mode), "Missing data modifier registration");
}
// Scripted effects make shortages reduce ONLY laboratory research benefits.
const operationalModifiers = blocks(read("common/static_modifiers/11_tech8c_laboratory_operation.txt"));
const operationalValues = read("common/script_values/13_tech8c_laboratory_operation.txt");
const operationalTriggers = read("common/scripted_triggers/11_tech8c_laboratory_operation.txt");
const operationalActions = read("common/on_actions/11_tech8c_laboratory_operation.txt");
const operationalEffects = read("common/scripted_effects/13_tech8c_laboratory_operation.txt");
const operationalMarkers = blocks(read("common/modifier_type_definitions/14_tech8c_laboratory_output_markers.txt"));
const generalWeightedLevels = body(operationalValues, "laboratory_1776_country_general_weighted_levels");
const generalWeight = number(generalWeightedLevels, "multiply");
check(generalWeight === 0.25, "General output must equal a quarter of specialized output");
check(/every_scope_building\s*=/.test(generalWeightedLevels) && /is_building_type\s*=\s*building_research_laboratory/.test(generalWeightedLevels), "General contribution must include only owned laboratories");
check(/has_active_production_method\s*=\s*pm_1776_general_research/.test(generalWeightedLevels) && [...generalWeightedLevels.matchAll(/has_active_production_method\s*=/g)].length === 1, "General contribution must exclude specialized laboratories");
check(/add\s*=\s*laboratory_1776_effective_levels/.test(generalWeightedLevels), "General contribution must use staffed, supply-adjusted levels");
check(/value\s*=\s*level\s+multiply\s*=\s*occupancy\s+multiply\s*=\s*laboratory_1776_data_efficiency/.test(body(operationalValues, "laboratory_1776_effective_levels")), "Both orientations must retain employment and shortage discounts");
check(!/general_weighted_levels/.test(body(operationalValues, "laboratory_1776_country_capacity")), "General speed weighting must not alter the innovation cap");
for (const cat of researchCategories) {
  const aggregate = body(operationalValues, "laboratory_1776_country_" + cat + "_levels");
  check(/^\s*value\s*=\s*laboratory_1776_country_general_weighted_levels/.test(aggregate), "Category must start with weighted general contribution: " + cat);
  check(/is_building_type\s*=\s*building_research_laboratory/.test(aggregate) && aggregate.includes("has_active_production_method = pm_1776_" + cat + "_research"), "Category must add its own specialized laboratories: " + cat);
  check([...aggregate.matchAll(/has_active_production_method\s*=/g)].length === 1 && /add\s*=\s*laboratory_1776_effective_levels/.test(aggregate) && !/multiply\s*=/.test(aggregate), "Category must not discount specialists or count other specialties: " + cat);
  const staticBonus = number(operationalModifiers.find(b => b.id === "laboratory_operational_" + cat + "_research").text, "country_" + cat + "_tech_research_speed_mult");
  check(staticBonus * generalWeight === number(generalPotential, "building_1776_" + cat + "_research_add"), "Actual and displayed general output disagree: " + cat);
  check(operationalEffects.includes("multiplier = laboratory_1776_country_" + cat + "_levels"), "Country bonus disconnected from weighted aggregate: " + cat);
  check(operationalEffects.indexOf("remove_modifier = laboratory_operational_" + cat + "_research") < operationalEffects.indexOf("name = laboratory_operational_" + cat + "_research"), "Switching orientations must replace, not stack, the previous contribution: " + cat);
}
for (const block of operationalModifiers) {
  check(!/country_weekly_innovation_add\s*=/.test(block.text), "Operational system must not generate points");
  for (const m of block.text.matchAll(/((?:country|building)_[a-z_]+)\s*=/g))
    check(modifiers.has(m[1]), "Unknown operational modifier: " + m[1]);
}
check(/on_action\s*=\s*laboratory_1776_monitor_tick\s+days\s*=\s*2/.test(operationalEffects), "Monitor must tick every 2 days");
check(/NOT\s*=\s*\{\s*has_variable\s*=\s*laboratory_1776_monitor_pending/.test(operationalEffects), "Monitor has no duplicate-chain guard");
check(/remove_variable\s*=\s*laboratory_1776_monitor_pending/.test(operationalActions), "Monitor pending flag never cleared");
check(/multiply\s*=\s*occupancy/.test(operationalValues), "Research effects ignore staffing");
check(/building_has_goods_shortage\s*=\s*yes/.test(operationalValues), "Other missing inputs leave full research benefits");
check(/on_state_owner_change\s*=/.test(operationalActions), "Acquired laboratories cannot start their monitor");
check(/every_scope_country/.test(operationalValues), "Shared market demand ignores other countries");
check(/market_goods_exports/.test(operationalValues), "Nominal demand ignores exports");
const compilationDemand = body(operationalValues, "laboratory_1776_nominal_compilation_raw_demand");
const marketRawDemand = body(operationalValues, "laboratory_1776_market_raw_demand");
for (const [id,quantity] of compilationRecipes) {
  check(new RegExp("has_active_production_method\\s*=\\s*" + id + "\\s*\\}\\s*add\\s*=\\s*" + quantity + "\\b").test(compilationDemand), "Nominal compilation demand not aligned with recipe: " + id);
  check(marketRawDemand.includes("has_active_production_method = " + id), "Market raw demand omits compiler: " + id);
}
check(/multiply\s*=\s*level/.test(compilationDemand) && /multiply\s*=\s*occupancy/.test(compilationDemand), "Compilation demand must scale with staffed levels");
check(/add\s*=\s*laboratory_1776_nominal_compilation_raw_demand/.test(marketRawDemand), "Compilation demand disconnected from shortage thresholds");
check(/every_scope_country/.test(marketRawDemand), "Compiler demand must include all countries in the market");
check(!/building_throughput_add\s*=/.test(operationalModifiers.map(b => b.text).join("\n")), "Output discount must not lower its own input needs");
check(/laboratory_1776_uses_organized_data\s*=\s*yes/.test(operationalTriggers), "Early general laboratories penalized for unused organized data");
for (const [id,value] of [["warning",-0.5],["severe",-0.8],["critical",-0.95]]) {
  check(number(operationalModifiers.find(b => b.id === "laboratory_data_shortage_" + id).text, "building_1776_laboratory_data_efficiency_add") === value, "Wrong visible shortage penalty");
}
check(number(operationalModifiers.find(b => b.id === "laboratory_operational_innovation_capacity").text, "country_weekly_innovation_max_add") === 1, "Country capacity aggregate disconnected");
check(number(operationalModifiers.find(b => b.id === "laboratory_equipment_shortage").text, "building_1776_laboratory_data_efficiency_add") === -0.5, "Wrong equipment shortage penalty");
for (const cat of ["production","military","society"])
  check(number(operationalModifiers.find(b => b.id === "laboratory_operational_" + cat + "_research").text, "country_" + cat + "_tech_research_speed_mult") === 0.01, "Country specialty aggregate disconnected");
for (const f of ["common/on_actions","common/scripted_effects","common/scripted_triggers","common/script_values"]) {
  const dir = path.join(root,f);
  for (const name of fs.readdirSync(dir).filter(n => /tech8c/.test(n))) {
    check(!/country_weekly_innovation_add\s*=/.test(mask(read(f + "/" + name))), "Unexpected point generation: " + name);
  }
}
// Reference coverage for new on-actions, effects, values, PMs and static modifiers.
const values = catalog("common/script_values",[game,root]);
const effects = catalog("common/scripted_effects",[game,root]);
const triggers = catalog("common/scripted_triggers",[game,root]);
const actions = catalog("common/on_actions",[game,root]);
const staticMods = catalog("common/static_modifiers",[game,root]);
for (const s of [operationalValues,operationalTriggers,operationalEffects,operationalActions]) {
  for (const m of mask(s).matchAll(/has_active_production_method\s*=\s*(pm_\w+)/g)) check(pms.has(m[1]),"Missing operational PM " + m[1]);
  for (const m of mask(s).matchAll(/\b((?:laboratory_1776_|refresh_1776_|ensure_1776_)\w+)\s*=\s*yes/g)) check(effects.has(m[1]) || triggers.has(m[1]),"Missing operational callable " + m[1]);
  for (const m of mask(s).matchAll(/\b(?:value|add|multiply|multiplier)\s*=\s*(laboratory_1776_\w+)/g)) check(values.has(m[1]),"Missing operational script value " + m[1]);
  for (const m of mask(s).matchAll(/\bon_action\s*=\s*(laboratory_1776_\w+)/g)) check(actions.has(m[1]),"Missing delayed action " + m[1]);
}
let arithmeticTests = 0;
// Table checks only: these do not substitute for game execution.
function efficiency(raw, organized, usesOrganized, otherShortage = false) {
  const ratio = usesOrganized ? Math.min(raw,organized) : raw;
  return ratio < 0.1 ? 0.05 : ratio < 0.5 ? 0.2 : ratio < 0.75 || otherShortage ? 0.5 : 1;
}
for (const [ratio,wanted] of [[0,0.05],[0.099,0.05],[0.1,0.2],[0.499,0.2],[0.5,0.5],[0.749,0.5],[0.75,1],[1,1]]) {
  check(efficiency(ratio,1,false) === wanted, "Raw shortage boundary " + ratio); arithmeticTests++;
  check(efficiency(1,ratio,true) === wanted, "Organized shortage boundary " + ratio); arithmeticTests++;
  check(efficiency(1,ratio,false) === 1, "Unused organized data must not penalize early general tier"); arithmeticTests++;
}
check(20 * efficiency(0,0,true) === 1, "Critical outage must remove 95% of advanced cap"); arithmeticTests++;
check(5 * 10 * 0.5 * efficiency(1,1,false) === 25, "Half-employment cap scaling"); arithmeticTests++;
check(20 * 10 * 0 * efficiency(0,0,true) === 0, "Empty labs must give zero output"); arithmeticTests++;
check(efficiency(1,1,false,true) === 0.5, "Missing equipment must reduce research benefits"); arithmeticTests++;
check(efficiency(0,1,true,true) === 0.05, "Data outage remains stronger than other shortage"); arithmeticTests++;
// Read quantities from actual PMs: 10 manual labs + 100 administrations +
// 50 trade levels + 25 university levels share the same market.
const compilerCases = compilationRecipes.map(([id],i) => [pms.get(id), [50,100,25][i]]);
const compilerRawDemand = compilerCases.reduce((sum,[pm,levels]) => sum + levels * number(pm,"goods_input_raw_industrial_data_add"), 0);
const compilerOutput = compilerCases.reduce((sum,[pm,levels]) => sum + levels * number(pm,"goods_output_organized_research_data_add"), 0);
const fullMarketRawDemand = 10 * number(pms.get("pm_1776_manual_research_laboratory"),"goods_input_raw_industrial_data_add") + compilerRawDemand;
check(compilerRawDemand === 200 && compilerOutput === 200, "Compilation mass-balance scenario"); arithmeticTests++;
check(fullMarketRawDemand === 400, "Raw demand must count compilers as well as laboratories"); arithmeticTests++;
check(efficiency(200/fullMarketRawDemand,1,false) === 0.5, "Compiler competition must affect laboratory shortages"); arithmeticTests++;
check(efficiency(200/(fullMarketRawDemand+100),1,false) === 0.2, "Exports still compete with compiler and laboratory demand"); arithmeticTests++;
check(compilerRawDemand * 0.5 === 100 && compilerOutput * 0.5 === 100, "Half-employment compilation input/output scaling"); arithmeticTests++;
// Formula regressions read PM quantities and the general weighting from the files.
// They check the expected arithmetic, not Paradox script execution.
function categorySpeed(category, labs) {
  const base = number(operationalModifiers.find(b => b.id === "laboratory_operational_" + category + "_research").text, "country_" + category + "_tech_research_speed_mult");
  return base * labs.reduce((sum,lab) => {
    const factor = lab.orientation === "general" ? generalWeight : lab.orientation === category ? 1 : 0;
    return sum + factor * lab.levels * lab.occupancy * efficiency(lab.raw,lab.organized,lab.usesOrganized,lab.otherShortage);
  },0);
}
function speedCheck(labs,expected,label) {
  for (const [i,category] of researchCategories.entries()) {
    check(Math.abs(categorySpeed(category,labs)-expected[i]) < 1e-12, label + ": " + category);
    arithmeticTests++;
  }
}
const fullGeneral = {orientation:"general",levels:1,occupancy:1,raw:1,organized:0,usesOrganized:false};
speedCheck([fullGeneral],[0.0025,0.0025,0.0025],"Full general level, unused organized data absent");
speedCheck([{...fullGeneral,occupancy:0.5}],[0.00125,0.00125,0.00125],"Half-staffed general level");
speedCheck([{...fullGeneral,occupancy:0}],[0,0,0],"Empty general level");
speedCheck([{...fullGeneral,raw:0.4}],[0.0005,0.0005,0.0005],"Severe raw shortage on general research");
speedCheck([{...fullGeneral,usesOrganized:true}],[0.000125,0.000125,0.000125],"Advanced general laboratory, organized data outage");
speedCheck([{...fullGeneral,otherShortage:true}],[0.00125,0.00125,0.00125],"Equipment shortage on general research");
for (const [i,tier] of tiers.entries()) for (const orientation of ["general",...researchCategories]) {
  const equipment = pms.get("pm_1776_" + tier + "_research_laboratory");
  const orientationPm = pms.get("pm_1776_" + orientation + "_research");
  const rawInput = (number(equipment,"goods_input_raw_industrial_data_add") || 0) + (number(orientationPm,"goods_input_raw_industrial_data_add") || 0);
  const organizedInput = (number(equipment,"goods_input_organized_research_data_add") || 0) + (number(orientationPm,"goods_input_organized_research_data_add") || 0);
  check(rawInput === [20,40,80][i] && organizedInput === (i === 2 ? 40 : 0) + (orientation === "general" ? 0 : 20), "Orientation must preserve equipment data recipes: " + tier + "/" + orientation); arithmeticTests++;
  const expected = researchCategories.map(cat => orientation === "general" ? 0.0025 : orientation === cat ? 0.01 : 0);
  speedCheck([{...fullGeneral,orientation,organized:1,usesOrganized:organizedInput>0}],expected,"Full output " + tier + "/" + orientation);
}
const mixedLabs = [
  {...fullGeneral,levels:4},
  {...fullGeneral,orientation:"production",levels:2,organized:1,usesOrganized:true},
  {...fullGeneral,orientation:"military",levels:3,occupancy:0.5,organized:1,usesOrganized:true},
  {...fullGeneral,orientation:"society",raw:0,organized:1,usesOrganized:true}
];
speedCheck(mixedLabs,[0.03,0.025,0.0105],"Mixed general and specialized laboratories");
speedCheck([{...fullGeneral,orientation:"society",organized:1,usesOrganized:true}],[0,0,0.01],"General to society replaces all three general contributions");
speedCheck([fullGeneral],[0.0025,0.0025,0.0025],"Society to general removes specialty output");
const assets = new Set();
const pmIconManifest = JSON.parse(read("docs/reports/assets/tech8c_laboratory_pm_icons.json"));
const expectedLaboratoryPms = blocks(read("common/production_methods/24_tech8c_research_laboratory.txt")).map(b => b.id).sort();
check(pmIconManifest.size === 208 && pmIconManifest.mipLevels === 8, "Laboratory PM icons must match native 208px / 8 mips");
check(JSON.stringify(pmIconManifest.entries.map(e => e.pm).sort()) === JSON.stringify(expectedLaboratoryPms), "Laboratory icon manifest must cover exactly the 7 PMs");
check(new Set(pmIconManifest.entries.map(e => e.output)).size === 7, "Laboratory PM icons must be distinct");
for (const entry of pmIconManifest.entries) {
  check(pms.get(entry.pm)?.includes('texture = "' + entry.output + '"'), "Wrong laboratory PM icon: " + entry.pm);
  const sourcePath = path.join(root,entry.source);
  check(fs.existsSync(sourcePath), "Missing preserved source icon: " + entry.pm);
  if (fs.existsSync(sourcePath))
    check(crypto.createHash("sha256").update(fs.readFileSync(sourcePath)).digest("hex") === entry.sourceSha256, "Laboratory PM source differs from attachment: " + entry.pm);
  const iconPath = path.join(root,entry.output);
  check(fs.existsSync(iconPath), "Missing laboratory PM DDS: " + entry.pm);
  if (!fs.existsSync(iconPath)) continue;
  const data = fs.readFileSync(iconPath);
  check(data.length === 230828, "Incomplete laboratory PM mip payload: " + entry.pm);
  if (data.length < 128) continue;
  check(data.toString("ascii",0,4) === "DDS " && data.readUInt32LE(4) === 124, "Invalid laboratory PM DDS header: " + entry.pm);
  check(data.readUInt32LE(12) === 208 && data.readUInt32LE(16) === 208, "Wrong laboratory PM image dimensions: " + entry.pm);
  check(data.readUInt32LE(28) === 8, "Laboratory PM requires full 8-level mip chain: " + entry.pm);
  check(data.readUInt32LE(80) === 0x41 && data.readUInt32LE(88) === 32, "Laboratory PM DDS must be RGBA8: " + entry.pm);
  check([92,96,100,104].map(o => data.readUInt32LE(o)).join() === [0xff,0xff00,0xff0000,0xff000000].join(), "Invalid laboratory PM DDS channel masks: " + entry.pm);
  if (pmIconManifest.transparentBackground) {
    const cutoutPath = entry.cutout ? path.join(root,entry.cutout) : null;
    check(Boolean(cutoutPath && fs.existsSync(cutoutPath)), "Missing transparent PM cutout: " + entry.pm);
    if (cutoutPath && fs.existsSync(cutoutPath))
      check(crypto.createHash("sha256").update(fs.readFileSync(cutoutPath)).digest("hex") === entry.cutoutSha256, "Transparent PM cutout differs from approved image: " + entry.pm);
    let transparent = 0, opaque = 0, partial = 0, borderTransparent = true;
    for (let y = 0; y < 208; y++) for (let x = 0; x < 208; x++) {
      const alpha = data[128 + (y * 208 + x) * 4 + 3];
      if (alpha === 0) transparent++;
      else if (alpha >= 250) opaque++;
      else partial++;
      // Ignore at most 2/255 alpha from resampling a vanishing fringe pixel.
      if ((x === 0 || x === 207 || y === 0 || y === 207) && alpha > 2) borderTransparent = false;
    }
    check(transparent > 208 * 208 * 0.2, "PM icon retains an opaque rectangular background: " + entry.pm);
    check(opaque > 208 * 208 * 0.05, "PM icon subject lost near-full opacity: " + entry.pm);
    check(partial > 0, "PM icon edges must be anti-aliased: " + entry.pm);
    check(borderTransparent, "PM icon border must be fully transparent: " + entry.pm);
  }
}
const laboratoryIcon = "gfx/interface/icons/building_icons/1776_research_laboratory.dds";
const reportingIcons = [
  ["pm_1776_raw_data_reporting", "tech_and_res_manual_data_reporting.dds"],
  ["pm_1776_light_data_reporting", "tech_and_res_manual_data_reporting.dds"],
  ["pm_1776_heavy_data_reporting", "tech_and_res_manual_data_reporting.dds"],
  ["pm_1776_trade_data_reporting", "tech_and_res_manual_data_optimization.dds"],
  ["pm_1776_administrative_data_reporting", "tech_and_res_manual_data_optimization.dds"],
  ["pm_1776_institutional_data_reporting", "tech_and_res_manual_data_optimization.dds"],
  ["pm_1776_no_raw_data_reporting", "tech_and_res_no_data_reporting.dds"],
  ["pm_1776_no_organized_data_reporting", "tech_and_res_no_data_reporting.dds"]
];
for (const [pm,filename] of reportingIcons)
  check(pms.get(pm).includes('texture = "gfx/interface/icons/production_method_icons/' + filename + '"'), "Wrong Tech & Res data icon: " + pm);
check(lab.includes('icon = "' + laboratoryIcon + '"'), "Laboratory must use the supplied illustration");
for (const mod of operationalModifiers.filter(b => b.id.startsWith("laboratory_operational_")))
  check(mod.text.includes('icon = "' + laboratoryIcon + '"'), "Laboratory modifier uses a different icon: " + mod.id);
for (const [filename,wantedHash] of [
  ["tech_and_res_manual_data_reporting.dds", "96ffac9de9c7df6a2197dcd3bd375e8fb0b9d281d348c52a2142332220982aa1"],
  ["tech_and_res_manual_data_optimization.dds", "ac09b1fe88628bcfda549e18b46a8b5fcf734da54fd60914856ac00dad8bd322"],
  ["tech_and_res_no_data_reporting.dds", "d0f76713b84b9544873e9141f9bc771b4c5b4f01fb27dea73ca89bf85258acbc"]
]) {
  const filenamePath = path.join(root,"gfx/interface/icons/production_method_icons",filename);
  check(fs.existsSync(filenamePath), "Missing copied PM icon: " + filename);
  if (fs.existsSync(filenamePath))
    check(crypto.createHash("sha256").update(fs.readFileSync(filenamePath)).digest("hex") === wantedHash, "PM icon differs from Tech & Res source: " + filename);
}
const laboratoryDdsPath = path.join(root,laboratoryIcon);
check(fs.existsSync(laboratoryDdsPath), "Laboratory DDS missing");
if (fs.existsSync(laboratoryDdsPath)) {
  const data = fs.readFileSync(laboratoryDdsPath);
  check(data.length === 349652, "Laboratory DDS mip chain has an unexpected length");
  if (data.length >= 128) {
    check(data.toString("ascii",0,4) === "DDS " && data.readUInt32LE(4) === 124, "Invalid laboratory DDS header");
    check(data.readUInt32LE(12) === 256 && data.readUInt32LE(16) === 256, "Laboratory icon should match native 256px dimensions");
    check(data.readUInt32LE(28) === 9, "Laboratory icon requires 9 mip levels");
  }
}
for (const f of newPaths) for (const m of read(f).matchAll(/(?:texture|icon|background)\s*=\s*"([^"]+\.dds)"/g)) assets.add(m[1]);
for (const asset of assets) check(fs.existsSync(path.join(root, asset)) || fs.existsSync(path.join(game, asset)), "Missing asset: " + asset);
const events = blocks(read("events/1776_research_laboratory_test_events.txt"));
check(events.length === 3, "Expected 3 manual test menus");
for (const event of events) {
  check(event.text.includes('icon = "' + laboratoryIcon + '"'), "Test menu uses an old laboratory icon: " + event.id);
  check(/orphan\s*=\s*yes/.test(event.text), "Test event may fire automatically");
  check(!/\bimmediate\s*=/.test(mask(event.text)), "Test event mutates on opening");
  check(/option\s*=\s*\{\s*name\s*=\s*research_laboratory_tests.close\s+default_option\s*=\s*yes\s*\}/.test(event.text), "Default option must change nothing");
}
const testText = read("events/1776_research_laboratory_test_events.txt");
const enableReportingOption = blocks(body(testText,"research_laboratory_tests.1")).find(b => /name\s*=\s*research_laboratory_tests\.1\.on\b/.test(b.text))?.text || "";
const enableReportingTrigger = body(enableReportingOption,"trigger") || "";
for (const technology of ["scientific_metrology","specialized_professional_societies"])
  check(enableReportingTrigger.includes("has_technology_researched = " + technology), "Test activation must respect the data technology unlock: " + technology);
for (const m of testText.matchAll(/production_method\s*=\s*(pm_\w+)/g))
  check(pms.has(m[1]), "Test references missing PM: " + m[1]);
const neededLoc = new Set([
 "raw_industrial_data","organized_research_data","building_research_laboratory",
 ...newPms.map(b => b.id), ...newPmgs.map(b => b.id),
 ...operationalModifiers.map(b => b.id), ...operationalMarkers.map(b => "modifier_" + b.id),
 ...[...testText.matchAll(/(?:title|desc|name|custom_tooltip)\s*=\s*([\w.]+)/g)].map(m => m[1])
]);
for (const lang of ["french","english"]) {
  const f = "localization/" + lang + "/tech8c_research_laboratory_l_" + lang + ".yml";
  const buffer = fs.readFileSync(path.join(root,f));
  check(buffer[0] === 0xef && buffer[1] === 0xbb && buffer[2] === 0xbf, "Localization missing UTF-8 BOM: " + lang);
  const text = buffer.toString("utf8");
  check(!/indépendante|independent|sans consommer de données brutes|No raw data are consumed|without consuming raw data/.test(text), "Outdated independent-data description: " + lang);
  check(!/[ \t]+\r?$/m.test(text), "Trailing whitespace: " + f);
  check(text.startsWith("\uFEFFl_" + lang + ":"), "Wrong language header");
  const keys = [...text.matchAll(/^ ([\w.]+):0 "(?:\\.|[^"\\])*"\r?$/gm)].map(m => m[1]);
  check(new Set(keys).size === keys.length, "Duplicate localization key: " + lang);
  for (const key of neededLoc) check(keys.includes(key), "Missing localization " + lang + ": " + key);
  for (const line of text.split(/\r?\n/).slice(1).filter(l => l.trim()))
    check(/^ [\w.]+:0 "(?:\\.|[^"\\])*"$/.test(line), "Malformed localization: " + line);
  const overridePath = "localization/" + lang + "/replace/1776_analytical_philosophy_pm_l_" + lang + ".yml";
  const overrideBuffer = fs.readFileSync(path.join(root,overridePath));
  check(overrideBuffer[0] === 0xef && overrideBuffer[1] === 0xbb && overrideBuffer[2] === 0xbf, "Analytical philosophy override missing UTF-8 BOM: " + lang);
  const overrideText = overrideBuffer.toString("utf8");
  check(overrideText.startsWith("\uFEFFl_" + lang + ":"), "Wrong analytical philosophy override language: " + lang);
  const renamedPm = lang === "french" ? "Séminaires de philosophie analytique" : "Analytical Philosophy Seminars";
  check(overrideText.includes(' pm_analytical_philosophy_department:0 "' + renamedPm + '"'), "Missing analytical philosophy PM rename: " + lang);
  for (const line of overrideText.split(/\r?\n/).slice(1).filter(l => l.trim()))
    check(/^ [\w.]+:0 "(?:\\.|[^"\\])*"$/.test(line), "Malformed analytical philosophy override: " + line);
}
check(pms.has("pm_analytical_philosophy_department") && tokens(body(pms.get("pm_analytical_philosophy_department"),"unlocking_technologies")).join() === "analytical_philosophy", "Renaming analytical philosophy must preserve its PM key and unlock");
console.log(JSON.stringify({
 status:errors.length?"FAIL":"PASS",
 checks, arithmeticTests, rawProducerTypes:expectedProducers.filter(b => /raw|light|heavy/.test(b.pmg)).length,
 organizedProducerTypes:expectedProducers.filter(b => /trade|administrative|institutional/.test(b.pmg)).length,
 preservedBuildingFiles:before.length,
 tiers:costs,
 note:"Static checks and base-price arithmetic only. Engine shortages, AI, saves and balance remain to test.",
 errors
}, null, 2));
if (errors.length) process.exitCode = 1;
