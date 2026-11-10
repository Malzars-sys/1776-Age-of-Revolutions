# Mission 42 — Modificateurs temporaires des événements d'agitateurs

9 novembre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Installation canonique consultée en lecture seule : Victoria 3 **1.15.0**. Aucune simulation ni validation humaine nouvelle.

## Correction installée

Deux appels `add_modifier` utilisaient `scandalous`, identifiant d'un trait de personnage, absent du catalogue des modificateurs statiques. Leurs équivalents vanilla actuels utilisent `modifier_scandalous`. Ce fournisseur existe déjà et applique une pénalité temporaire de popularité de **50 points** ; il est hérité sans nouvelle définition ou modification de ses coefficients.

| Événement / option | Destinataire conservé | Avant | Après |
| --- | --- | --- | --- |
| `agitator_legal_events.5` / `.5.a` | `scope:opposing_ig_leader` | `scandalous` | `modifier_scandalous` |
| `agitator_legal_events.12` / `.12.b` | `scope:da_boss` | `scandalous` | `modifier_scandalous` |

Seul `events/agitators_events/agitator_law_events_2.txt` est modifié, aux deux valeurs concernées. Le fichier installé est exactement la copie d'entrée augmentée de ces deux substitutions : **71 653 → 71 671 octets**, soit 18 octets ajoutés. Durées `normal_modifier_time`, portées, conditions, autres options/effets, traits, localisations, BOM éventuel et fins de ligne sont conservés.

Le vanilla ajoute aussi un trait permanent dans une branche de l'événement 5. Cette modification distincte n'est pas importée : le lot restaure uniquement les deux effets temporaires déjà écrits dans le mod. Il ne transforme pas tous les usages légitimes du trait `scandalous` en modificateurs.

## Preuves et contrôles

- Candidat : **17/17 contrôles**, **4/4 contrôles négatifs**. Installation réelle : mêmes résultats.
- Témoins en mémoire : ancien identifiant de trait, mauvais destinataire, durée différente, fournisseur dupliqué. Aucun témoin n'est installé dans les fichiers actifs.
- Comparaison des deux blocs `add_modifier` avec leurs homologues natifs ; fournisseur unique, popularité -50, icône résolue et textes hérités uniques FR/EN : « Scandale de notoriété publique » / « Publicly Known Scandal ».
- Inventaire littéral dans les événements, effets scriptés, boutons et on_actions : **6 511 références**. Les références sans fournisseur passent de **trois à une**, sans erreur de parsing. Ce contrôle ne simule pas les scopes, la sélection des événements ou les autres familles de commandes.
- La référence restante, `institutions_of_socialism_modifier` dans `events/communism.txt:675`, est conservée dans les résultats. Elle relève d'une qualification séparée ; aucune restauration arbitraire de récompense ou modification du travail IA/journaux n'est effectuée.
- `SOURCE_PROTECTION.json` contrôle les **2 961 fichiers de fonctionnement préexistants** : seul le fichier autorisé diffère, exactement selon le candidat. Aucun ajout de fichier de fonctionnement, ni changement du vanilla, de l'index ou de HEAD. Les fournisseurs de l'inventaire final sont également revérifiés.

Les rapports antérieurs, les changements économiques récents, les journaux 39, cultures 40, le travail IA de Hawk et les historiques/carte/lois restent conservés. Aucune écriture Git, publication ou modification du vanilla.

## Consultation et reproduction

Commencer par `CHANGES_NORMALIZED.patch`, `INSTALLATION_RECEIPT.json`, `CANDIDATE_VALIDATION.json`, `LIVE_VALIDATION.json` et `SOURCE_PROTECTION.json`. Les versions d'entrée/candidat et cinq sources natives sont figées dans les sous-dossiers correspondants. Le premier `CHANGES.patch`, dont les fins de ligne rendent l'affichage moins lisible, est conservé ; le patch normalisé sert à la revue et n'est pas appliqué automatiquement.

```text
python -B tools/compatibility/issue42_agitator_modifiers_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE42_AGITATOR_MODIFIERS_2026_11_09/RECHECK_NEW.json
```

L'outil refuse un nom de sortie déjà utilisé. Il lit les données et conserve ses témoins en mémoire ; il ne comporte aucun installateur et n'écrit aucun fichier du jeu.

La fiche GitHub **42** contient la réservation et cette livraison. Le statut demandé est **In review**. La session navigateur disponible est déconnectée : sa colonne Project et la relation parent ne peuvent pas être modifiées ou certifiées dans cette passe. Le lien de chantier est 25, sans changement de son acceptation ou de sa colonne.

Le protocole moteur est séparé dans `RUNTIME_PROTOCOL.md`. Une résolution statique ne certifie pas encore l'application ou la disparition de la pénalité en partie.
