# Mission 39 — migration technique complète, 11 novembre 2026

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION — carte GitHub passée en In review.**
La migration des journaux du catalogue effectif est terminée. La mission reste
ouverte pour les essais moteur et l'acceptation du mainteneur ; cette livraison
ne crée aucune attestation humaine. Référence canonique : installation locale
Victoria 3 1.15.0, consultée en lecture seule.

## Catalogue livré

| Ensemble | Entrées | Résultat |
| --- | ---: | --- |
| Anciennes entrées converties par R4 | 400 | Toutes retrouvées et vérifiées |
| Autres entrées avec outcomes compatibles | 91 | Contrats et références revérifiés |
| Hubs/dummy sans conclusion authored | 3 | Exceptions individuelles conservées |
| Total | **494** | **1 045 outcomes**, aucun champ de conclusion legacy restant |

`CATALOGUE_MIGRE.csv` contient une ligne par entrée, son fournisseur, sa ligne,
son contexte, sa classification, les issues et le besoin d'une cible. Les 447
blocs d'ajout génériques sont uniquement des aides d'inspection, pas une preuve
d'activation naturelle. Les 47 autres cas ne reçoivent pas une commande vide
de cible ou de contexte. `DECLENCHEURS_JOURNAUX.json` conserve les 525
instructions effectives d'ajout et leurs consommateurs sources.

Les trois exceptions sont `je_colonial_administration` (hub de boutons),
`je_new_imperialism` (hub sans objectif final unique) et
`je_spain_glorious_revolution_dummy` (dummy conservé). Le contrat 1.15 autorise
zéro outcome ; aucune victoire ou défaite artificielle ne leur est ajoutée.

Les anciennes familles Canada/Australie, avant-garde communiste et Commune
remplacent toujours quatre identifiants natifs distincts. Toutes leurs entrées
effectives sont migrées. Elles ne constituent pas une promesse d'adoption de
toutes les nouvelles mécaniques natives : cette décision de contenu demeure
distincte sous 24. Les chaînes espagnoles désactivées et les partitions
polonaises retirées restent telles quelles.

## Derniers défauts corrigés

Le nouveau lecteur suit les descriptions conditionnelles et leurs alias,
au-delà des seuls titres/en-têtes déjà contrôlés. Il a trouvé :

1. L'aperçu conservé de `je_red_summer` demandait
   `red_summer_on_complete_tt`, supprimé du catalogue natif actuel. La clé
   rétablie en **français et anglais** présente les deux voies conditionnelles
   et réutilise les noms/effets d'événements natifs existants. Aucun prédicat,
   événement exécuté ou ordre de conclusion n'est changé.
2. Trois mauvaises références anglaises héritées du vanilla : `$ideology$`,
   `$Signs of the Times$` et `$Exhibition Points$`. Elles deviennent
   respectivement `$concept_ideology$`, `$sol_events.1.t$` et le libellé simple
   « exhibition points ». Le reste des chaînes natives est conservé exactement.
   Les textes français correspondants étaient déjà corrects.

Installation : deux **nouveaux fichiers de localisation** dans
`localization/french/replace/` et `localization/english/replace/`, nommés
`1776_v115_journal_preview_links_l_<langue>.yml`. UTF-8 avec BOM ; une clé FR,
quatre clés EN. Trois surcharges natives EN sont explicites ; aucune collision
avec une autre clé du mod. `INSTALLATION.json` conserve sources, transformations
exactes, empreintes et contenu attendu. Aucun fichier de journal existant
n'est modifié par cette dernière passe.

La seconde rédaction immersive des textes de progression demeure liée à une
validation humaine de leur fonctionnement. Cette réparation de références
conserve les proses existantes et ne se fait pas passer pour cette acceptation.

## Contrôles exécutés sur cette livraison

| Contrôle | Résultat statique |
| --- | --- |
| Contrats, métadonnées, FR/EN et comptabilité des entrées | 494 entrées, zéro constat |
| Consommateurs littéraux, dont sélecteurs `je:` | 2 920 références, zéro cible littérale manquante |
| Dépendances transitives, événements directs/aléatoires et on_actions | Zéro cible connue manquante ; zéro erreur de parsing |
| Textes de présentation et alias transitifs | 2 895 clés FR / 3 010 clés EN parcourues ; zéro lien manquant |
| Mapping R4 avec corrections ultérieures neutralisées **en mémoire** | 11 117/11 117 ; 14/14 régressions volontaires détectées |
| Objets restaurés et auxiliaires | 65/65 |
| Raccordement antérieur de la Commune conservé | 13/13 ; trois contre-exemples détectés |
| Contrôles du nouveau lecteur de présentation | 5/5 |
| Vérification finale, fichiers, conservation et syntaxe des sept blocs de test | **20/20** |

La fermeture transitive part des 494 journaux et atteint 1 258 événements,
707 effets scriptés, 326 triggers, 377 boutons, 62 barres, 23 valeurs scriptées
à corps structuré et un on_action. Il s'agit de résolution de symboles connus,
pas d'un vérificateur complet des types de scopes du moteur ou de la vérité
des conditions. Les références paramétrées restent distinguées dans le scan
des consommateurs. Les doublons de localisation restent visibles ; aucun ordre
de chargement général n'est inventé. Les trois surcharges précises livrées ici
sont traitées explicitement et leurs fournisseurs conservés dans la preuve.

L'échec brut de l'ancien test de mapping reste conservé dans `MAPPING_RAW.json` :
les correctifs 50/51/53 ont légitimement changé trois fichiers depuis R4.
Leurs empreintes actuelles sont identiques aux reçus déjà réconciliés. Le
rejeu en mémoire emploie les octets décodés sans normalisation des fins de
ligne et passe dans `MAPPING_SCOPED_R2.json`. La première tentative
`MAPPING_SCOPED.json`, qui normalisait CRLF en LF et faussait les offsets,
reste archivée ; aucun fichier du mod n'a été restauré pour obtenir le succès.

Les preuves précédentes R4 et `V1_15_ISSUE39_COMPLETENESS_REVIEW_2026_11_11`
restent intactes. Leurs nombres datés ne sont pas réécrits rétroactivement.

## Conservation, limites moteur et suite

Les **2 988 fichiers existants** capturés avant cette passe sont identiques,
y compris carte, populations, lois, technologies, recettes, assets et index
Git. Les sources natives consultées sont inchangées. Les seuls ajouts de
runtime sont les deux fichiers de localisation ; aucun Git write, changement
du vanilla, synchronisation Steam ou publication.

Empreinte du manifeste local complet de 2 990 fichiers :
`8bf4911cd63a71657ef166db7992402b7aa10966dc93e53b0d7311f6fd0b5e07`.
La liste est dans `FINAL_VALIDATION.json` ; elle identifie la livraison locale,
sans l'assimiler au candidat d'intégration antérieur figé sous 25.

Les anciens logs existants ont été capturés avec leurs empreintes. Ils ne
permettent pas d'identifier cette livraison active : plusieurs positions
renvoient aux scripts natifs plutôt qu'aux corps du mod. Ils ne sont donc ni
une validation moteur de 39, ni une comparaison avant/après probante. Aucun
essai moteur ou DLC supplémentaire n'est revendiqué.

**Prochaine action : essais moteur groupés de cette livraison**, avec les
blocs de `TESTS_MOTEUR.md`. Les familles expiration, invalidation, concurrence,
all-involved, plans avancés et DLC restent détaillées dans
`../V1_15_ISSUE39_JOURNAL_CATALOGUE_2026_11_09/MIGRATION_R4/RUNTIME_PROTOCOL.md`
et `../V1_15_ISSUE39_COMPLETENESS_REVIEW_2026_11_11/RUNTIME_PROTOCOL.md`.
Après confirmation humaine, traiter les éventuelles anomalies puis la seconde
passe immersive applicable et la validation combinée 24/25. Aucune nouvelle
migration par lots n'est laissée en attente pour le catalogue effectif.

## Mise à jour du suivi externe

Le statut **In review** de la carte 39 a été effectivement appliqué et observé
dans le navigateur. La tentative distincte de publication du bilan détaillé
et de mise à jour d'une case de revue statique a été refusée par le contrôle
automatique : l'autorisation antérieure de changement de colonne ne couvre
pas clairement cette communication publique précise. Le corps de l'issue
n'a pas été modifié. `ISSUE_PROPOSED.md` contient le texte prêt à publier et
`ISSUE_UPDATE_REJECTION.json` conserve le résultat réel. Une autorisation
explicite a été demandée ; elle ne conditionne pas les correctifs locaux déjà
installés et vérifiés.


### Publication après autorisation explicite

Le mainteneur a répondu « Oui, publie le bilan préparé ». Le texte préparé de
`ISSUE_PROPOSED.md`, avec la case de revue statique cochée, a ensuite été publié
dans l’issue GitHub 39. Une relecture de l’issue confirme le corps exact ; sa
mise à jour est datée par GitHub du 11 novembre 2026 à 18:29:01 UTC.
`ISSUE_UPDATE_RECEIPT.json` conserve le reçu. Le refus antérieur reste archivé
comme historique. L’issue demeure ouverte pour la validation moteur ; aucune
nouvelle attestation de test ni clôture n’est ajoutée.
