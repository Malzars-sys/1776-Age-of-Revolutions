# Mission 43 — Récompense des institutions socialistes

9 novembre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Jeu canonique consulté : Victoria 3 **1.15.0**. Aucune simulation ni acceptation humaine nouvelle.

## Résultat et choix de compatibilité

L'option `communism.6.a` de l'événement conservé par le mod appelle `institutions_of_socialism_modifier`, dont la définition avait disparu du catalogue effectif. Le lot restaure ce fournisseur et ses noms français et anglais dans trois fichiers neufs. Aucun événement ou journal n'est réécrit ou réactivé.

Le bonus récupéré est **`country_bureaucracy_mult = 0.2`**, soit un bonus de **20 % de bureaucratie**. Ce n'est pas une réduction du coût des institutions. L'icône est le document positif déjà livré avec le jeu. La durée de l'appel existant reste `long_modifier_time`, dont le fournisseur effectif actuel vaut **3 650 jours**, soit dix ans selon le commentaire canonique.

Le bloc complet de l'événement `communism.6` actuellement dans le mod correspond structurellement à celui de la source ancienne consultée. Cette concordance, le nom du fournisseur et la disponibilité actuelle du paramètre étayent une restauration à l'identique. Il n'est pas remplacé par la récompense moderne `modifier_social_revolution`, dont le parcours et le nettoyage sont différents.

## Provenance consultée

Source récupérée dans le miroir versionné [Victoria-3-files, commit fc8143b](https://github.com/tjysdsg/Victoria-3-files/tree/fc8143b83f54f8abed97fc556b556e4085b6e691/game), décrit par ce dépôt comme le passage de 1.8.7 à 1.9.0 :

- [Définition ancienne, `content_1_modifiers.txt`, ligne 671](https://github.com/tjysdsg/Victoria-3-files/blob/fc8143b83f54f8abed97fc556b556e4085b6e691/game/common/static_modifiers/content_1_modifiers.txt), blob `d8f8e8d180b2846acd699824e9bde674b33d3a6e`.
- Événement `communism.6` dans le fichier `game/events/communism.txt` du même commit.
- Noms des fichiers `content_1_l_french.yml` et `content_1_l_english.yml` du même commit : **« Institutions socialistes »** / **« Institutions of Socialism »**.

Ce miroir n'est pas un dépôt officiel Paradox et ne prouve pas la valeur exacte de chaque version 1.13/1.14. `LEGACY_PROVENANCE.json` conserve les URL, commit, blobs disponibles et extraits réellement consultés. Les valeurs réinstallées proviennent de ces extraits ; aucune récompense nouvelle n'est inventée.

L'installation canonique actuelle enregistre toujours `country_bureaucracy_mult`, conserve l'icône et fournit la durée. L'appel du mod est un événement de pays ; il n'exige pas de portée de personnage pour ce bonus. Les textes actuels de l'événement consultés utilisent uniquement ROOT pour leur référence de pays et restent inchangés.

## Surface livrée

| Fichier neuf | Contenu |
| --- | --- |
| `common/static_modifiers/1776_legacy_communist_reward.txt` | Uniquement le modificateur ancien, son icône et son coefficient d'origine |
| `localization/french/1776_legacy_communist_reward_l_french.yml` | Un nom consommé, UTF-8 avec BOM |
| `localization/english/1776_legacy_communist_reward_l_english.yml` | Un nom consommé, UTF-8 avec BOM |

Pas de description sans consommateur, d'alias, de nouvelle technologie/loi, de changement de durée ou de routage. L'ancien événement, les journaux de 39 et le parcours distinct `aor1776_v115_ai_progression.1` restent intacts. La coexistence de ces parcours n'est pas certifiée par cette restauration de fournisseur.

## Vérifications réellement exécutées

- Candidat : **16/16 contrôles** et **5/5 contrôles négatifs**. Installation réelle : mêmes résultats.
- Témoins uniquement en mémoire : fournisseur absent, fournisseur dupliqué, bonus erroné, nom français absent et durée d'événement altérée.
- Identité du payload historique ; fournisseur unique ; paramètre actuel enregistré ; icône résolue ; noms historiques uniques FR/EN ; un seul nom consommé par fichier ; événement et durée préservés.
- Inventaire littéral : **6 511 références** dans les événements, effets scriptés, boutons et on_actions ; une cible manquante avant, **zéro après**, sans erreur de parsing. Ce résultat est limité à ces familles et commandes ; il ne prouve ni accessibilité des événements ni comportement moteur global.
- Garde finale : les **2 962 fichiers de fonctionnement préexistants** sont byte-identiques. Les seuls ajouts sont les trois fichiers annoncés. Les 681 fournisseurs du contrôle final, les noms, les entrées natives suivies, l'index et HEAD sont courants/préservés. Aucun Git write, changement du vanilla ou publication.

Les résultats et empreintes figurent dans `CANDIDATE_VALIDATION.json`, `LIVE_VALIDATION.json`, `SOURCE_PROTECTION.json` et les reçus d'installation. Le candidat ne doit pas remplacer un fichier existant si le workspace évolue.

```text
python -B tools/compatibility/issue43_legacy_reward_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE43_LEGACY_COMMUNIST_REWARD_2026_11_09/RECHECK_NEW.json
```

Utiliser un nom de sortie neuf. L'outil lit les données et conserve ses témoins en mémoire ; il n'installe aucun fichier et n'écrase aucune preuve.

Fiche de suivi : **43**, liée au chantier 25. La livraison est prête pour revue, mais la colonne Project n'est pas présentée comme modifiée ou vérifiée depuis la session navigateur déconnectée constatée précédemment. Les essais restent décrits dans `RUNTIME_PROTOCOL.md` ; aucune mission parente n'est clôturée par les contrôles statiques.
