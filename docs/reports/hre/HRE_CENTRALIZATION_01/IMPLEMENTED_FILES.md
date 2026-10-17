# Fichiers de la livraison

## Runtime

- `common/diplomatic_actions/1776_imperial_centralization.txt`
- `common/diplomatic_actions/1776_imperial_subjects.txt`
- `common/diplomatic_actions/37_subjects_decrease_autonomy.txt`
- `common/diplomatic_plays/1776_imperial_plays.txt`
- `common/game_concepts/1776_imperial_subjects.txt`
- `common/on_actions/1776_imperial_constitution.txt`
- `common/scripted_buttons/1776_imperial_centralization.txt`
- `common/scripted_effects/1776_imperial_centralization.txt`
- `common/scripted_effects/1776_imperial_constitution.txt`
- `common/scripted_effects/1776_imperial_reforms.txt`
- `common/scripted_triggers/1776_imperial_centralization.txt`
- `common/scripted_triggers/1776_imperial_constitution.txt`
- `common/subject_types/1776_imperial_centralization.txt`
- `common/subject_types/1776_imperial_reforms.txt`
- `common/war_goal_types/00_annex_country.txt`
- `common/war_goal_types/1776_imperial_war_goals.txt`
- `common/war_goal_types/27_unification.txt`
- `gui/1776_imperial_subject_texticons.gui`
- `localization/english/1776_imperial_reforms_l_english.yml`
- `localization/english/1776_imperial_subjects_l_english.yml`
- `localization/french/1776_imperial_reforms_l_french.yml`
- `localization/french/1776_imperial_subjects_l_french.yml`

## Images

- `gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_estate.dds` et maître `workshop_assets/source/HRE_CENTRALIZATION_01/imperial_estate.png`
- `gfx/interface/icons/diplomatic_action_icons/aor1776_imperial_elector.dds` et maître `workshop_assets/source/HRE_CENTRALIZATION_01/imperial_elector.png`

Les PNG maîtres sont adaptés par détourage intégré ; les DDS128px avec mipmaps sont vérifiés par décodage identique. Les deux feuilles originales fournies par le joueur ne sont pas modifiées.

## Outils

- `tools/hre_centralization_01.py` : couche de compilation, capture, validation et compagnon isolé.
- `tools/test_hre_centralization_01.py` : contrats statiques et modèles, sans moteur.
- `tools/map2k_imperial_system.py` : appel de la nouvelle couche en fin de compilation ; elle empêche la réapparition du doublon lors d’une régénération.

## Compagnon non activé

- `docs/prototypes/HRE_CENTRALIZATION_01/HRE_CENTRALIZATION_01_TEST.mod`
- `mod/descriptor.mod`
- `mod/common/scripted_effects/zz_hre_centralization_01_test.txt`
- `mod/common/scripted_effects/1776_imperial_constitution.txt` : copie effective du fichier principal, seule enveloppe de succession remplacée. Cela utilise le remplacement de fichier du chargeur, pas deux définitions concurrentes du même effet dans des fichiers différents.

Le compagnon n’est ni installé dans un playset ni activé par cette livraison. Il doit être régénéré si le fichier impérial principal évolue.
