# Audit de l’installation réellement consultée

Sources locales en lecture seule : `C:/Games/Victoria 3/game/`. La compatibilité annoncée par le mod est1.13.* ; les définitions ci-dessous proviennent des fichiers installés, pas d’une hypothèse sur un wiki. Les empreintes originales sont dans BASELINE.json. Aucun numéro de build binaire supplémentaire n’est certifié.

- `common/subject_types/00_subject_types.txt`, bloc `subject_type_crown_land` : autonomie1 ; diplomatie propre interdite ; participation militaire ; dirigeant distinct ; absorption lors de formation de pays activée ; alternatives d’autonomie vanilla. Le nouveau type clone la syntaxe reconnue puis désactive absorption et alternatives. Aucune définition vanilla n’est écrasée.
- `common/diplomatic_actions/50_subject_crown_land.txt` : pacte avec junior, paiement basé sur le second pays, direction second vers premier, `cost=10`, `income_transfer=0.15`. La localisation française installée annonce40%, alors que cette donnée et l’écran fourni indiquent15% : ne pas copier aveuglément le chiffre du texte.
- `common/diplomatic_plays/00_diplomatic_plays.txt`, `dp_annex_subject` : liste explicite de pactes colonie/fantoche/vassal/crown_land. Nos pactes ne sont pas ajoutés à cette liste.
- `common/war_goal_types/00_annex_country.txt` : validation scriptable en plus du traitement moteur. Ajout d’une garde locale, sans réécrire le reste du but de guerre.
- `27_unification.txt` : cible État et effets prédéfinis côté moteur. Gardes sur possible/valid pour les États appartenant à nos sujets impériaux.
- `37_subjects_decrease_autonomy.txt` : interaction utilisant `can_decrease_autonomy` et `decrease_autonomy`. Garde ciblée ajoutée à potential/possible. Le reste est identique.
- `43_subjects_handle_states.txt`, `take_state` : liste explicite colonie/fantoche/vassal ; nos types n’y sont pas ajoutés. Aucun changement à cette interaction.
- `22_subject_personal_union.txt` et exception OLD–HLB : conservés. Les effets de transfert isolés ne parcourent que les nouveaux sujets impériaux directs.
- Localisations `diplomacy_l_french.yml` et `concepts_l_french.yml` : contrat nom avec icône, variante `_no_icon`, nom de concept et `_desc`, liens `[concept_...]` / `[Concept(...)]`. Les trois concepts impériaux sont réellement définis.

Les fonctions consultées ne justifient pas l’invention d’un champ `can_be_annexed` ou d’une propriété de masquage des types. Aucun de ces champs n’est ajouté. Les limites moteur sont déclarées séparément.
