// Targeted checks for the d909641 ownership transfers. No files are written.
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');

function parse(text, label) {
  const tokens = [...text.matchAll(/\s+|\uFEFF|#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}]|[?<>!]?=|[<>]|[^\s{}=#"<>!?]+/g)]
    .filter(m => !/^[\s\uFEFF#]/.test(m[0]))
    .map(m => ({ text: m[0], offset: m.index }));
  let i = 0;
  function block(nested = false) {
    const entries = [];
    while (i < tokens.length) {
      if (tokens[i].text === '}') {
        assert(nested, `${label}: unexpected closing brace at ${tokens[i].offset}`);
        i++;
        return entries;
      }
      const token = tokens[i++];
      assert(token.text !== '{', `${label}: block without a key at ${token.offset}`);
      const entry = { key: token.text.replace(/^"|"$/g, ''), start: token.offset };
      if (/^(?:[?<>!]?=|[<>])$/.test(tokens[i]?.text || '')) {
        entry.operator = tokens[i++].text;
        const value = tokens[i++];
        assert(value && value.text !== '}', `${label}: missing value for ${entry.key}`);
        if (value.text === '{') entry.children = block(true);
        else {
          entry.value = value.text.replace(/^"|"$/g, '');
          // Country definitions also use typed colour blocks, e.g. hsv { ... }.
          if (/^(?:hsv|hsv360|rgb|rgba)$/.test(value.text) && tokens[i]?.text === '{') {
            i++;
            entry.children = block(true);
          }
        }
      }
      entry.end = tokens[i - 1].offset + tokens[i - 1].text.length;
      entries.push(entry);
    }
    assert(!nested, `${label}: unclosed block`);
    return entries;
  }
  return block();
}
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const before = p => cp.execFileSync('git', ['show', `d909641:${p}`], { cwd: root, encoding: 'utf8', maxBuffer: 8 * 1024 * 1024 });
const child = (node, key) => node.children?.find(n => n.key === key);
const value = (node, key) => child(node, key)?.value;
const named = (tree, key) => { const n = tree[0]?.children?.find(n => n.key === key); assert(n, `Missing ${key}`); return n; };
function walk(nodes, visitor) { for (const n of nodes) { visitor(n); if (n.children) walk(n.children, visitor); } }
const stateFile = 'common/history/states/00_states.txt';
const states = parse(read(stateFile), stateFile);
const oldStates = parse(before(stateFile), `baseline ${stateFile}`);
const targets = ['DOBRUDJA', 'NUNAVUT', 'EAST_SWITZERLAND', 'GREATER_CAUCASUS', 'BESSARABIA', 'ISTRIA', 'LOMBARDY', 'SOUTH_TYROL'];
const owners = new Map();
for (const state of states[0].children) {
  const countryProvinces = new Map();
  for (const create of state.children.filter(n => n.key === 'create_state')) {
    const tag = value(create, 'country').replace(/^c:/, '');
    const provinces = child(create, 'owned_provinces').children.map(n => n.key.toUpperCase());
    assert(!countryProvinces.has(tag), `Duplicate owner block ${state.key}/${tag}`);
    countryProvinces.set(tag, provinces);
  }
  owners.set(state.key, countryProvinces);
}
for (const id of targets) {
  const key = `s:STATE_${id}`;
  const previous = named(oldStates, key);
  const previousProvinces = new Set(previous.children.filter(n => n.key === 'create_state')
    .flatMap(n => child(n, 'owned_provinces').children.map(p => p.key.toUpperCase())));
  const current = [...owners.get(key).values()].flat();
  assert.equal(current.length, new Set(current).size, `${id}: duplicate province`);
  assert.deepEqual(new Set(current), previousProvinces, `${id}: lost/added province`);
}
const expectedOwners = {
  DOBRUDJA: ['TUR'], NUNAVUT: ['HBC'], EAST_SWITZERLAND: ['SWI'],
  GREATER_CAUCASUS: ['GEO'], BESSARABIA: ['MOL'], ISTRIA: ['AUS', 'VEN'],
  LOMBARDY: ['AUS', 'VEN'], SOUTH_TYROL: ['AUS', 'VEN'],
};
for (const [id, expected] of Object.entries(expectedOwners)) {
  assert.deepEqual([...owners.get(`s:STATE_${id}`).keys()].sort(), expected.slice().sort(), `${id}: owner changed`);
}
assert(owners.get('s:STATE_LOMBARDY').get('VEN').includes('X867A90'));
assert(owners.get('s:STATE_LOMBARDY').get('VEN').includes('X9AC196'), 'Requested province must belong to Venice');
assert(!owners.get('s:STATE_LOMBARDY').get('AUS').includes('X9AC196'));
assert.equal(owners.get('s:STATE_LOMBARDY').get('VEN').length, 2);
assert.equal(owners.get('s:STATE_LOMBARDY').get('AUS').length, 6);

const popFiles = [
  'common/history/pops/01_south_europe.txt', 'common/history/pops/00_west_europe.txt',
  'common/history/pops/05_north_america.txt', 'common/history/pops/15_russia.txt',
  'common/history/pops/09_central_asia.txt',
];
function populationTotals(state) {
  const totals = {};
  walk(state.children, n => {
    if (n.key !== 'create_pop') return;
    const tuple = ['culture', 'religion', 'pop_type'].map(k => value(n, k) || '').join('|');
    totals[tuple] = (totals[tuple] || 0) + Number(value(n, 'size'));
  });
  return totals;
}
for (const file of popFiles) {
  const now = parse(read(file), file), old = parse(before(file), `baseline ${file}`);
  for (const state of now[0].children.filter(s => targets.includes(s.key.replace('s:STATE_', '')))) {
    assert.deepEqual(populationTotals(state), populationTotals(named(old, state.key)), `${file}/${state.key}: population composition changed`);
    const regions = state.children.filter(n => n.key.startsWith('region_state:'));
    assert.equal(new Set(regions.map(r => r.key)).size, regions.length, `${state.key}: duplicate population selector`);
    for (const region of regions) assert(owners.get(state.key).has(region.key.replace('region_state:', '')), `${file}/${state.key}: invalid population owner`);
    assert.deepEqual(regions.map(r => r.key.replace('region_state:', '')).sort(), [...owners.get(state.key).keys()].sort(), `${state.key}: owner without population`);
    console.log(`PASS population ${state.key}: ${Object.values(populationTotals(state)).reduce((a,b) => a+b, 0)} preserved`);
  }
}
const buildingFiles = [
  'common/history/buildings/01_south_europe.txt', 'common/history/buildings/02_east_europe.txt',
  'common/history/buildings/09_central_asia.txt', 'common/history/buildings/15_russia.txt',
  'common/history/buildings/98_build_start_1776_world_redistribution.txt',
];
for (const file of buildingFiles) {
  const tree = parse(read(file), file);
  walk(tree, n => {
    if (n.key.startsWith('s:STATE_')) assert(tree[0].children.includes(n), `${file}: nested state ${n.key}`);
  });
  for (const state of tree[0].children.filter(s => targets.includes(s.key.replace('s:STATE_', '')))) {
    for (const region of state.children.filter(n => n.key.startsWith('region_state:'))) {
      assert(owners.get(state.key).has(region.key.replace('region_state:', '')), `${file}/${state.key}: invalid building owner`);
      walk(region.children, n => {
        if (n.key !== 'add_ownership') return;
        for (const economicOwner of n.children) {
          const tag = value(economicOwner, 'country')?.replace(/^c:/, '');
          const ownerRegion = value(economicOwner, 'region');
          if (ownerRegion) assert(owners.get(`s:${ownerRegion}`)?.has(tag), `${file}: invalid ownership location ${tag}/${ownerRegion}`);
        }
      });
    }
  }
  console.log(`PASS structure and changed building references: ${file}`);
}
const armyFile = 'common/history/military_formations/00_military_formations_europe.txt';
const armies = parse(read(armyFile), armyFile), oldArmies = parse(before(armyFile), `baseline ${armyFile}`);
function unitsByCountry(tree) {
  const totals = {};
  for (const country of tree[0].children) {
    const counts = {};
    walk(country.children, n => {
      if (!['combat_unit', 'ship'].includes(n.key)) return;
      const key = `${n.key}|${value(n, 'type')}|${value(n, 'service_type') || 'regular'}`;
      counts[key] = (counts[key] || 0) + Number(value(n, 'count'));
    });
    totals[country.key] = counts;
  }
  return totals;
}
assert.deepEqual(unitsByCountry(armies), unitsByCountry(oldArmies), 'Unit types/counts changed');
for (const country of armies[0].children.filter(n => ['c:CRI', 'c:GBR', 'c:RUS'].includes(n.key))) {
  walk(country.children, n => {
    if (n.key !== 'combat_unit') return;
    assert(owners.get(value(n, 'state_region'))?.has(country.key.replace('c:', '')), `${country.key}: invalid recruitment ${value(n, 'state_region')}`);
  });
}
for (const name of ['cleanup2d3b_rus_land_4', 'cleanup2d3b_rus_naval_2']) {
  let formation;
  walk(armies, n => { if (n.key === 'create_military_formation' && value(n, 'name') === name) formation = n; });
  assert.equal(value(formation, 'hq_region'), 'sr:region_russia');
}
console.log('PASS military counts preserved; CRI/GBR/RUS recruitment and relocated HQs valid');

// The additional Venetian province keeps the existing provisional population rule.
const lombardyPops = named(parse(read(popFiles[0]), popFiles[0]), 's:STATE_LOMBARDY');
const venetianPops = populationTotals(child(lombardyPops, 'region_state:VEN'));
assert.equal(venetianPops['north_italian||'], 483226);
assert.equal(venetianPops['north_italian|jewish|'], 81);
console.log('PASS Lombardy: x9AC196 Venetian; 6:2 provinces and population totals preserved');

// State names are scoped to each owner, with no global state-region rename.
const namingFile = 'common/scripted_effects/1776_alpine_state_names.txt';
const namingTree = parse(read(namingFile), namingFile);
const namingEffect = namingTree.find(n => n.key === 'assign_1776_alpine_split_state_name');
assert(namingEffect);
const splitGuard = child(namingEffect, 'if');
assert.equal(value(child(splitGuard, 'limit'), 'is_split_state'), 'yes');
const names = {
  LOMBARDY: { AUS: 'aor1776_state_duchy_of_milan', VEN: 'aor1776_state_bergamo_brescia' },
  SOUTH_TYROL: { AUS: 'aor1776_state_trent', VEN: 'aor1776_state_venetian_tyrol' },
  ISTRIA: { AUS: 'aor1776_state_trieste', VEN: 'aor1776_state_venetian_istria' },
};
for (const [region, ownerNames] of Object.entries(names)) {
  const branch = splitGuard.children.find(n => value(child(n, 'limit') || {}, 'state_region') === `s:STATE_${region}`);
  assert(branch, `Missing name branch ${region}`);
  for (const [tag, key] of Object.entries(ownerNames)) {
    const ownerBranch = branch.children.find(n => value(n, 'set_state_name') === key);
    assert(ownerBranch, `Missing name ${key}`);
    const ownerTest = child(child(ownerBranch, 'limit'), 'owner');
    assert.equal(value(ownerTest, `c:${tag}`), 'this');
    assert.equal(child(ownerTest, `c:${tag}`).operator, '?=');
  }
}
const expectedNameKeys = Object.values(names).flatMap(n => Object.values(n)).sort();
const usedNameKeys = [];
walk(namingTree, n => { if (n.key === 'set_state_name') usedNameKeys.push(n.value); });
assert.deepEqual(usedNameKeys.sort(), expectedNameKeys);
for (const language of ['french', 'english']) {
  const file = `localization/${language}/1776_alpine_state_names_l_${language}.yml`;
  const text = read(file);
  assert(text.startsWith(`\uFEFFl_${language}:`), `${file}: missing UTF-8 BOM/header`);
  const keys = [...text.matchAll(/^ (aor1776_state_[a-z_]+):0 "[^"\r\n]+"$/gm)].map(m => m[1]);
  assert.deepEqual(keys.sort(), expectedNameKeys, `${file}: names missing or duplicated`);
}
const hookFile = 'common/on_actions/12_1776_alpine_state_names.txt';
const hooks = parse(read(hookFile), hookFile);
for (const parent of ['on_game_started', 'on_game_started_after_lobby', 'on_state_created', 'on_state_owner_change', 'on_become_subject', 'on_become_independent']) {
  const hook = hooks.find(n => n.key === parent);
  assert(hook, `Missing naming hook ${parent}`);
  assert(!child(hook, 'effect'), `${parent}: vanilla parent effect must not be replaced`);
  for (const reference of child(hook, 'on_actions').children) {
    assert(hooks.some(n => n.key === reference.key && child(n, 'effect')), `Undefined naming action ${reference.key}`);
  }
}
console.log('PASS six owner-specific split-state names; French/English BOM localization and additive hooks');

// Georgia receives a small, explicit historical baseline with all prerequisites.
const geoFile = 'common/history/countries/geo - georgia.txt';
const geoTree = parse(read(geoFile), geoFile);
const geo = named(geoTree, 'c:GEO');
assert.equal(geo.operator, '?=');
assert.equal(geoTree[0].children.length, 1, 'Georgia history must not change another country');
assert(geo.children.every(n => ['add_technology_researched', 'activate_law'].includes(n.key)), 'Unexpected Georgia country-history effect');
assert.equal(value(geo, 'activate_law'), 'law_type:law_monarchy');
assert.equal(geo.children.filter(n => n.key === 'activate_law').length, 1, 'Only the monarchic title is in scope');
const grants = geo.children.filter(n => n.key === 'add_technology_researched').map(n => n.value);
assert.equal(new Set(grants).size, grants.length, 'Duplicated Georgian technology grant');
const expectedGrants = [
  'improved_husbandry', 'traditional_food_processing', 'distillation',
  'organized_textile_production', 'organized_workshops', 'shaft_mining',
  'organized_military_establishments', 'regulated_small_arms', 'light_infantry_tactics',
  'international_relations', 'systematic_administrative_statistics', 'institutionalized_scientific_exchange',
];
assert.deepEqual(grants.slice().sort(), expectedGrants.slice().sort());
const technologies = new Map();
const technologyDir = path.join(root, 'common/technology/technologies');
for (const file of fs.readdirSync(technologyDir).filter(f => f.endsWith('.txt')).sort()) {
  for (const technology of parse(fs.readFileSync(path.join(technologyDir, file), 'utf8'), file)) {
    if (expectedGrants.includes(technology.key)) {
      assert(!technologies.has(technology.key), `Duplicate technology definition ${technology.key}`);
      technologies.set(technology.key, technology);
    }
  }
}
for (const id of grants) {
  const technology = technologies.get(id);
  assert(technology, `Undefined Georgian technology ${id}`);
  assert.notEqual(value(technology, 'can_research'), 'no', `Compatibility-only technology ${id}`);
  assert(['era_1', 'era_2', 'era_3'].includes(value(technology, 'era')), `${id}: unexpected late-era starting grant`);
  for (const dependency of child(technology, 'unlocking_technologies')?.children || []) {
    assert(grants.includes(dependency.key), `${id}: missing starting prerequisite ${dependency.key}`);
  }
}
console.log(`PASS Georgia: ${grants.length} explicit defined technologies, no missing prerequisite`);

const geoCharacterFile = 'common/history/characters/geo - georgia.txt';
const geoCharacters = named(parse(read(geoCharacterFile), geoCharacterFile), 'c:GEO');
assert.equal(geoCharacters.operator, '?=');
assert.equal(geoCharacters.children.length, 1, 'Only the requested Georgian ruler is created');
const ruler = child(geoCharacters, 'create_character');
assert.equal(value(ruler, 'ruler'), 'yes');
assert.equal(value(ruler, 'historical'), 'yes');
assert.equal(value(ruler, 'birth_date'), '1720.11.7');
assert.equal(value(ruler, 'culture'), 'cu:georgian');
assert.equal(value(ruler, 'religion'), 'rel:orthodox');
assert.equal(value(ruler, 'interest_group'), 'ig_armed_forces');
assert.equal(value(ruler, 'ideology'), 'ideology_modernizer_leader');
assert.deepEqual(child(ruler, 'traits').children.map(n => n.key).sort(), ['brave', 'innovative']);
assert(!child(ruler, 'is_general'), 'No unrequested military role is introduced');
const characterDir = path.join(root, 'common/history/characters');
let georgianRulers = 0;
for (const file of fs.readdirSync(characterDir).filter(f => f.endsWith('.txt'))) {
  const tree = parse(fs.readFileSync(path.join(characterDir, file), 'utf8'), file);
  for (const country of tree[0].children.filter(n => n.key === 'c:GEO')) {
    walk(country.children, n => { if (n.key === 'create_character' && value(n, 'ruler') === 'yes') georgianRulers++; });
  }
}
assert.equal(georgianRulers, 1, 'Duplicate scripted Georgian ruler');
const rulerKeys = [value(ruler, 'first_name'), value(ruler, 'last_name')].sort();
for (const language of ['french', 'english']) {
  const file = `localization/${language}/1776_georgia_ruler_l_${language}.yml`;
  const text = read(file);
  assert(text.startsWith(`\uFEFFl_${language}:`));
  assert.deepEqual([...text.matchAll(/^ (aor1776_[a-z_]+):0 "[^"\r\n]+"$/gm)].map(m => m[1]).sort(), rulerKeys);
}
console.log('PASS Georgian ruler: one historical Erekle II, birth 1720.11.7, French/English names');
assert(read('common/ideologies/01_character_ideologies.txt').includes('ideology_modernizer_leader = {'));
const maxPersonalityTraits = Number(read('common/defines/00_defines.txt').match(/MAX_TRAITS_PERSONALITY\s*=\s*(\d+)/)[1]);
assert(child(ruler, 'traits').children.length <= maxPersonalityTraits, 'Too many personality traits');
console.log('PASS Georgian profile: Armed Forces / Modernizer; Brave + Innovative within personality cap');

const countryNamesFile = 'common/dynamic_country_names/00_dynamic_country_names.txt';
const countryNames = parse(read(countryNamesFile), countryNamesFile);
const oldCountryNames = parse(before(countryNamesFile), `baseline ${countryNamesFile}`);
const geoNameBlocks = countryNames.filter(n => n.key === 'GEO');
assert.equal(geoNameBlocks.length, 1, 'Duplicate Georgian dynamic-name definition');
assert.equal(geoNameBlocks[0].children.length, 1, 'Existing name rule is adjusted, not duplicated');
const geoName = child(geoNameBlocks[0], 'dynamic_country_name');
assert.equal(value(geoName, 'name'), 'aor1776_kartli_kakheti_kingdom');
assert.equal(value(geoName, 'adjective'), 'aor1776_kartli_kakheti_kingdom_adj');
assert.equal(value(geoName, 'is_main_tag_only'), 'yes');
const geoNameActor = child(child(geoName, 'trigger'), 'scope:actor');
assert.equal(value(geoNameActor, 'has_law'), 'law_type:law_monarchy');
assert(!child(geoNameActor, 'is_country_type'), 'Historical name must work for recognized GEO');
assert.equal(value(child(geoNameActor, 'NOT'), 'has_technology_researched'), 'nationalism');
assert(!grants.includes('nationalism'), 'Historical starting name must be active');
const structural = n => ({ key: n.key, operator: n.operator, value: n.value, children: n.children?.map(structural) });
assert.deepEqual(countryNames.filter(n => n.key !== 'GEO').map(structural), oldCountryNames.filter(n => n.key !== 'GEO').map(structural), 'Another country name was changed');
const geoDefinition = parse(read('common/country_definitions/00_countries.txt'), 'country definitions').find(n => n.key === 'GEO');
assert.equal(value(geoDefinition, 'country_type'), 'recognized', 'Do not reclassify Georgia for a display name');
const countryNameKeys = [value(geoName, 'name'), value(geoName, 'adjective')].sort();
for (const language of ['french', 'english']) {
  const file = `localization/${language}/1776_georgia_country_name_l_${language}.yml`;
  const text = read(file);
  assert(text.startsWith(`\uFEFFl_${language}:`));
  assert.deepEqual([...text.matchAll(/^ (aor1776_[a-z_]+):0 "[^"\r\n]+"$/gm)].map(m => m[1]).sort(), countryNameKeys);
}
console.log('PASS Kartli-Kakheti starting name: monarchy rule, recognized status preserved, French/English localization');
console.log('All targeted map-rework history checks passed. Unrelated baseline errors are outside this check.');
