# HOTFIX-4C - Iwakura Mission

## 1. Resume

Decision : import gameplay bloque.

Le hotfix contient bien deux fichiers dedies pour la mission Iwakura :

- `common/journal_entries/07_iwakura_mission.txt`
- `events/japan_events/ep2_iwakura_events.txt`

Cependant, la mission n'est pas autonome. Son point d'entree normal est le scripted button vanilla `je_iwakura_mission_button`, attache a `common/journal_entries/00_meiji_restoration.txt`. Or le fork remplace `common/journal_entries` et possede deja son propre `00_meiji_restoration.txt`, sans ce bouton. Importer Iwakura proprement demanderait donc une fusion manuelle du setup Meiji local, ce qui sort du cadre de cette phase et risque de toucher aux corrections Japon existantes.

Conclusion : aucun fichier gameplay n'a ete modifie. Seul ce rapport a ete cree.

## 2. Decision : import effectue ou non

Import non effectue.

Raison principale : dependance critique d'activation manquante dans le fork courant. Les fichiers dedies `07_iwakura_mission.txt` et `ep2_iwakura_events.txt` pourraient etre ajoutes, mais la mission ne serait pas accessible proprement en jeu sans modifier `common/journal_entries/00_meiji_restoration.txt`.

Le prompt autorise un import conditionnel seulement si toutes les dependances sont disponibles ou importables proprement. Ici, le hook d'activation impose une fusion dans un fichier global Japon existant, non liste dans le diff attendu et potentiellement conflictuel avec le setup 1776.

## 3. Fichiers hotfix etudies

| Fichier | Role | Statut |
|---|---|---|
| `common/journal_entries/07_iwakura_mission.txt` | Definit `je_iwakura_mission` | lu, non importe |
| `events/japan_events/ep2_iwakura_events.txt` | Definit `iwakura_mission.1` a `.9` | lu, non importe |
| `common/journal_entries/00_meiji_restoration.txt` | Hotfix attache `je_iwakura_mission_button` a Meiji | lu par recherche, non importe |
| `events/meiji_restoration.txt` | Hotfix reference `iwakura_mission_finished` | lu par recherche, non importe |

## 4. Chemins remplaces ou non par le mod

| Chemin | Remplace par le mod ? | Consequence |
|---|---:|---|
| `common/journal_entries` | oui | Les JE vanilla Iwakura/Meiji sont masquees si non presentes dans le fork |
| `events` | oui | Les evenements vanilla Iwakura sont masques si non presents dans le fork |
| `common/scripted_buttons` | non | Les boutons vanilla restent disponibles |
| `common/scripted_effects` | non | Les scripted effects vanilla restent disponibles |
| `common/static_modifiers` | non | Les modifiers vanilla restent disponibles |
| `common/messages` | non | Les messages vanilla Iwakura restent disponibles |
| `localization` | non | La localisation vanilla reste disponible, mais un fichier dedie FR/EN serait preferable si import |

Les `replace_paths` viennent de `.metadata/metadata.json`. `descriptor.mod` ne declare pas de `replace_path`.

## 5. Dependances trouvees

| Dependence | Presente dans fork ? | Presente dans hotfix ? | Presente dans vanilla ? | Action recommandee |
|---|---:|---:|---:|---|
| `je_iwakura_mission` | non | oui | oui | importer seulement apres hook Meiji decide |
| `iwakura_mission.*` | non | oui | oui | importer seulement apres hook Meiji decide |
| `je_iwakura_mission_recall_mission` | non localement | non dedie hotfix | oui, `common/scripted_buttons/07_iwakura_buttons.txt` | disponible via vanilla |
| `je_iwakura_mission_button` | non localement | reference dans hotfix `00_meiji_restoration.txt` | oui, `common/scripted_buttons/meiji_reform_buttons.txt` | bouton disponible, mais non attache au JE local |
| `iwakura_mission_save_learning` | non localement | non dedie hotfix | oui, `00_victoria_ep2_scripted_effects.txt` | disponible via vanilla |
| `iwakura_mission_cleanup` | non localement | appele par event hotfix | oui, `00_victoria_ep2_scripted_effects.txt` | disponible via vanilla |
| `iwakura_calculate_world_politics_progressiveness` | non localement | appele par event hotfix | oui | disponible via vanilla |
| `iwakura_character_change_ideology_with_world_politics` | non localement | appele par event hotfix | oui | disponible via vanilla |
| Modifiers `modifier_iwakura_mission_*` | non localement | appeles par event hotfix | oui, `00_ep2_04_modifiers.txt` | disponible via vanilla |
| Localisation Iwakura EN/FR | non dediee | absente du hotfix localise | oui, `ep2_04_l_english.yml` / `ep2_04_l_french.yml` | a extraire seulement si import |

## 6. Compatibilite avec setup Japon local

| Point de compatibilite | Statut | Risque | Action |
|---|---|---|---|
| Ne force pas Tenpo au depart 1776 | Les fichiers Iwakura dedies ne touchent pas Tenpo directement | faible si import dedie seul | OK |
| Ne force pas l'ouverture du Japon | Le bouton vanilla exige de ne plus avoir `law_isolationism` ni `law_closed_borders` | faible | OK |
| Ne modifie pas Sakoku | Aucun fichier Sakoku requis | faible | OK |
| Ne modifie pas pays/states/pops/buildings | Les fichiers Iwakura dedies ne touchent pas ces historiques | faible | OK |
| Depend d'un changement dans `jap - japan.txt` | Aucune dependance directe trouvee | faible | OK |
| Depend d'un hook on_action global | Aucun hook on_action direct trouve | faible | OK |
| Depend d'un hook dans `00_meiji_restoration.txt` | Oui : bouton `je_iwakura_mission_button` attache au JE Meiji vanilla/hotfix | eleve | bloquer import gameplay |

## 7. Fichiers modifies

Aucun fichier gameplay modifie.

Fichier cree :

- `docs/reports/hotfix/HOTFIX_4C_IWAKURA_MISSION.md`

## 8. Localisations EN/FR ajoutees

Aucune localisation ajoutee, car le gameplay Iwakura n'a pas ete importe.

Si une phase future importe le bloc, il faudra creer :

- `localization/english/hotfix_iwakura_l_english.yml`
- `localization/french/hotfix_iwakura_l_french.yml`

Ces fichiers devront couvrir au minimum :

- `iwakura_mission.1` a `iwakura_mission.9`
- `je_iwakura_mission`
- `je_iwakura_mission_reason`
- `je_iwakura_mission_complete_header`
- `je_iwakura_mission_on_complete_header`
- `je_iwakura_mission_recall_mission`
- `je_iwakura_mission_recall_mission_desc`
- `iwakura_mission_status_loc_*`
- `iwakura_mission_*_tt`
- `notification_iwakura_mission_*`
- `modifier_iwakura_mission_*`

## 9. Ce qui n'a pas ete importe

- Pas de `common/journal_entries/07_iwakura_mission.txt`.
- Pas de `events/japan_events/ep2_iwakura_events.txt`.
- Pas de scripted button dedie.
- Pas de scripted effect dedie.
- Pas de localisation Iwakura dediee.
- Pas de modification de `common/journal_entries/00_meiji_restoration.txt`.
- Pas de modification de `events/meiji_restoration.txt`.
- Pas de Zaibatsu.
- Pas de Hokkaido/Ezo.
- Pas de Ryukyu.
- Pas de Tenpo.
- Pas de Sakoku.
- Pas de changements pays/states/pops/buildings.

## 10. Risques restants

- La mission Iwakura reste absente du fork courant tant qu'une fusion Meiji dediee n'est pas faite.
- Une importation naive des fichiers hotfix `00_meiji_restoration.txt` ou `events/meiji_restoration.txt` risquerait d'ecraser les adaptations 1776 et les corrections japonaises locales.
- Une phase future devra comparer finement le `00_meiji_restoration.txt` du fork, du hotfix et de la vanilla The Great Wave avant d'ajouter le bouton `je_iwakura_mission_button`.
- La localisation FR/EN devra etre creee dans la meme phase que l'import gameplay pour eviter les cles brutes.

## 11. Tests a faire en jeu apres une future importation

1. Lancer en `JAP` avec The Great Wave actif.
2. Verifier que la mission Iwakura n'apparait pas en 1776 tant que le Japon est sous isolationnisme/frontieres fermees.
3. Declencher ou simuler la progression Meiji et verifier que le bouton `Envoyer la mission vers l'Occident` apparait au bon moment.
4. Lancer la mission et verifier l'apparition de `je_iwakura_mission`.
5. Tester le rappel de mission via `je_iwakura_mission_recall_mission`.
6. Laisser les evenements `iwakura_mission.4` a `.9` progresser et verifier `error.log`.
7. Verifier l'absence de cles brutes en francais pour `iwakura_mission.*`, `je_iwakura_mission`, notifications et modifiers.

## 12. Liste exacte des fichiers crees/modifies

- `docs/reports/hotfix/HOTFIX_4C_IWAKURA_MISSION.md`

## 13. Confirmations

- Pas de Zaibatsu importe.
- Pas de Hokkaido/Ezo modifie.
- Pas de Ryukyu modifie.
- Pas de Tenpo modifie.
- Pas de Sakoku modifie.
- Aucun pays/state/pop/building modifie.
- Aucun `SKH`, `ULT` ou `EZO` modifie.
- Aucun NAVY modifie.
- Aucun ADMIN modifie.
- Aucun IR1 / HOTFIX-3 modifie.
- Aucun BIC modifie.
- Stash MARATH non touche.
- Aucun commit effectue.
