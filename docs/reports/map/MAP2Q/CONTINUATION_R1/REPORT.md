# MAP-2Q — Reprise démographique R1

**Statut : MAP2Q_PARTIAL_HISTORICAL_POPULATION_UNRESOLVED.**

La nouvelle règle est conservée : un ajustement historique justifié peut modifier le total mondial, sans compensation ailleurs. Elle ne fournit pas à elle seule le nombre à installer.

## Avancée de cette reprise

L'installation Q antérieure a été vérifiée intacte avant toute intervention : noyau d'Eutin HLB, 31 cellules transférées, quatre nouveaux RGB, union personnelle native sous OLD et registre impérial. Une baseline de continuation indépendante conserve les empreintes ; la baseline initiale n'est pas remplacée.

Le volume original de Ludwig Kohli, *Handbuch einer historisch-statistisch-geographischen Beschreibung...*, volume 2, partie 2 (Bremen, 1826), est désormais consulté directement dans l'exemplaire **BSB bsb10020025**, et non seulement cité depuis un catalogue. Manifeste, OCR ciblé et trois pages originales contrôlées visuellement sont conservés dans `EVIDENCE/`, avec URL et empreinte SHA-256 pour chaque téléchargement.

| Périmètre dans Kohli | Habitants | Date réellement indiquée | Page imprimée / vue |
| --- | ---: | --- | --- |
| Ville d'Eutin | 2 652 | 1819, selon la note 36 | 126 / 148 |
| Amt Eutin | 6 824 | 1819, selon la note 36 | 132 / 154 |
| Datation des dénombrements | — | Recensement officiel de 1819 ; exception de 1806 pour quatre villages acquis en 1804 | 125 / 147 |

[Source originale et note de datation](https://www.digitale-sammlungen.de/en/view/bsb10020025?page=147).

**Ces deux chiffres ne sont pas des dénombrements de 1776.** La ville inclut aussi des maisons sous juridiction de la chancellerie et de l'Amt : une addition mécanique avec l'agrégat de l'Amt exige encore de contrôler les éventuels recouvrements. Le périmètre de 1819 doit lui-même être rapproché du noyau rasterisé. Aucune croissance rurale locale indépendante n'a été établie permettant une rétroprojection démographique argumentée vers 1776.

La piste `OLDENBURG_184732.pdf` a été effectivement lue puis écartée : elle donne un index alphabétique W–X, pas un recensement d'Eutin. Les résultats de recherche n'ont donc pas été traités comme des preuves numériques.

## Modification effectivement appliquée

**Aucune nouvelle modification runtime pendant R1.** Les 11 325 habitants restent explicitement une allocation technique provisoire. Leur maintien ne rétablit pas l'ancienne contrainte mondiale : faute de cible défendable pour 1776, aucun remplacement ni coefficient de croissance n'est inventé. Bâtiments, unités, populations voisines, bitmap, registre et union personnelle restent inchangés.

Les chiffres de 1819 servent désormais de références datées contrôlables, et non de cible automatiquement injectée dans le scénario de 1776. Les 22 000 habitants de synthèses sur la principauté sécularisée ne sont pas appliqués au noyau incomplet.

## Vérifications et suites

`RECHECK_VALIDATION.json` rejoue les contrôles statiques du Q initial sans écraser ses attestations. `VERIFICATION.json` contrôle l'intégrité de cette reprise et rejoue les cinq tests ciblés. Le premier contrôle mondial du replay constate uniquement l'absence d'ajustement dans cette version ; ce n'est pas une interdiction des deltas historiques futurs.

Les 44 doublons RGB et 12 références invalides antérieurs restent signalés dans le replay. Les six anciens échecs de snapshots ont leur analyse préexistante dans `../UNIT_TEST_RECONCILIATION.json`, sans requalification en PASS. Aucun test moteur réalisé ou prétendu. HEAD et index restent intacts ; aucun commit ou push.

Blocage précis restant : un dénombrement ou une estimation proche de 1776, assorti d'un périmètre permettant d'isoler Eutin/Amt Eutin et d'éviter les doubles comptes avec Schwartau et les possessions capitulaires encore chez les voisins. Un inventaire archivistique sans lecture des chiffres ne suffit pas. Schwartau/Kaltenhof et les domaines dispersés restent également non reconstruits ; le lot complet n'est pas annoncé terminé.
