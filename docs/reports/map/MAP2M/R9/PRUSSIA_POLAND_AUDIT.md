# Frontière Prusse–Pologne — bilan distinct de la Peene

**PARTIAL. Aucun nouveau transfert prusso-polonais dans R9.** `PRUSSIA_POLAND_CHANGES.csv` ne contient que son en-tête. Les propositions de Thorn figurent ailleurs, jamais parmi les changements appliqués.

Les sources et conclusions R2–R8 sont réutilisées : les scans Grund disponibles, Güssefeld1775, Pfau, le manuscrit N1146/1 et la conclusion politique du liseré méridional de R7. Aucune nouvelle campagne de recalage ni nouvelle optimisation des anciens points.

| Secteur | Constat actuel | Décision R9 |
| --- | --- | --- |
| Deutsch Krone / Wałcz et Piła | Les diagnostics figés tombent dans x0180A0 PRU, STATE_POMERANIA | Noyaux cohérents avec la souveraineté de1776 ; contour complet du district non certifié |
| Kamin | Diagnostic dans x945000 PRU, STATE_WEST_PRUSSIA | Conserver ; ne pas assimiler le district historique à toute la province native |
| Bromberg / Bydgoszcz | Noyau xEDB010 :85cellules PRU ; xFCC7B7 :142cellules PLC | Conserver les acquis, mais ne pas annoncer tout Bromberg corrigé |
| Inowrocław | Diagnostic figé dans xC02121 PLC alors que la ville doit être prussienne | Anomalie de représentation connue ; pas d'annexion de toute la province qui recouvre aussi des territoires polonais |
| Thorn / Toruń | x41A021 :153cellules PRU ; ferme native au sud de la rivière, diagnostic géographique au nord | Correction non appliquée, arbitrage urbain ciblé préparé |
| Dantzig / Gdańsk | x80A0A0 PLC | Propriété conservée ; pas d'annexion1793 |
| Poznań | x999CEE PLC | Propriété conservée |
| Gniezno | Diagnostic grossier dans xC02121 PLC | Conserver ; ce RGB ne peut pas être transféré en bloc pour corriger Inowrocław |

## Point important : le noyau de Bromberg n'est pas une garantie de placement de toute la ville

L'ancien hub rural nommé Bromberg est dans le noyau PRU. Le profil géographique R5 figé place cependant le diagnostic arrondi de Bydgoszcz vers **(4507.54,763.63)**, dans le résidu polonais `xFCC7B7`. Il s'agit d'un écart entre le diagnostic géographique et la représentation rurale native, pas de la découverte d'un nouveau locator de ville.

R9 signale cette discordance au lieu de répéter « Bromberg est correctement représentée » pour toute la région. Le profil seul ne permet pas d'étendre de plusieurs cellules un contour politique non qualifié. Les85cellules acceptées restent strictement préservées. Une correction urbaine pourrait être arbitrée séparément, sans rendre faux le statut manuel de la version R3 inspectée.

## Pourquoi la ligne méridionale n'est pas réappliquée

R7 a identifié un conflit précis : Schubin/Szubin se trouve hors du liseré proposé alors que la synthèse municipale indique une incorporation prussienne en1773. Une limite dessinée en1772, une voïvodie ou un ajout de couleur ne donnent donc pas automatiquement l'état souverain de janvier1776. Les notices de bornage1776/1777 et les deux rectos d'un même manuscrit ne constituent pas des preuves indépendantes de cette date d'effet.

Le manque est une délimitation politique datée, pas un meilleur score sur les mêmes points. Les quatre districts ne sont pas déclarés terminés. Aucun état de1793 n'est importé pour combler ce manque. Thorn n'est pas bloquée administrativement par cette question : elle possède son diagnostic, son arbitrage et ses dépendances propres.

## Appartenance impériale

`xEDB010`, `xFCC7B7`, `x41A021` et `x80A0A0` ne sont pas ajoutés au registre impérial. La souveraineté de la monarchie prussienne en Prusse royale/Netze ne signifie pas appartenance de ces acquisitions au SERG. Une région économique partagée ne doit pas entraîner l'enregistrement impérial de toutes ses provinces.
