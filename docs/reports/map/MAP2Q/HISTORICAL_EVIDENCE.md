# Preuves et périmètres — MAP-2Q

Consultation ciblée du 16 octobre 2026 ; réutilisation du dossier `R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0035.md`.

## Sources

1. [NLA Oldenburg, Best. 30](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails.action?fondsId=2633&request_locale=en) : distingue le territoire du prince-évêque (Eutin et ses offices), le chapitre cathédral, le chapitre collégial et les biens privés. La notice décrit 32 villages et sept avant-domaines pour l'Amt Eutin, six villages et deux avant-domaines autour de Schwartau. Sa graphie « Kaltendorf » est conservée comme celle de la notice ; le nom usuel de l'office est Kaltenhof. Elle prévient aussi que l'incorporation des possessions des chapitres accroît fortement le domaine princier en 1803. **Pas de chiffre exploitable de population 1776 dans cette notice.**
2. [Landesarchiv Schleswig-Holstein, classification 21](https://arcinsys.schleswig-holstein.de/arcinsys/showClassificationPointDetails?classificationPointId=21) : trois institutions distinctes avant 1803, articulation des fonds de Schleswig et Oldenburg. La notice de fonds n'est pas un polygone de souveraineté.
3. [Reilly, Wagrien et Hochstift Lübeck/Eutin, n° 300](https://www.vintage-maps.com/en/antique-maps/europe/germany/von-reilly-germany-schleswig-holstein-wagrien-1795::464) : gravure historique vers 1790–1795 ; reproduction conservée avec empreinte dans `EVIDENCE/` et `REILLY_PROVENANCE.json`. Un exemplaire institutionnel est catalogué par la Schleswig-Holsteinische Landesbibliothek, inventaire **2017-1-13**, objet **dc00018389**, vers 1790. Le noyau coloré d'Eutin sert à la généralisation B ; la date n'est pas transformée en attestation exacte de chaque frontière de 1776. Reproduction : Götzfried Antique Maps, lien d'attribution ci-dessus.
4. [Detlev Kraack, Eutin, Akademie der Wissenschaften, 2019](https://adw-goe.de/la/digitale-bibliothek/residenzstaedte-im-alten-reich-1300-1800/id/RESIST-HB1-BD1-ART039) : siège du pouvoir temporel et religieux protestant, situation entre les lacs, histoire urbaine. **Environ 2 300 habitants en 1801 concerne la ville, pas le pays de 1776.**
5. [Gesellschaft für Schleswig-Holsteinische Geschichte](https://geschichte-s-h.de/sh-von-a-bis-z/f/fuerstbistum-fuerstentum-luebeck/) : chronologie de la principauté et changements ultérieurs ; ne pas remonter les acquisitions de 1867 en 1776.
6. [Frederic Zangel / Universität Kiel / Archäologisches Landesamt, Kaltenhof](https://www.kuladig.de/Objektansicht/KLD-290005) : emplacement du domaine épiscopal, séparation d'avec la ville de Lübeck. Un point de bâtiment ne délimite pas l'ensemble de l'Amt.

## Démographie : sources écartées pour le chiffre demandé

**Complément courant R2 :** une [estimation documentée](CONTINUATION_R2/HISTORICAL_POPULATION_SOURCES.md) de 7 600 habitants est désormais acceptée et installée. Le dossier distingue les mentions urbaines de 1755/1791, l'estimation rurale de Hennings vers 1769 et les transcriptions AGGSH de 1819. Ce changement ne transforme aucune des valeurs ci-dessous en recensement de 1776 ; les raisons de leur exclusion comme cible directe restent valables.

La [Statistikstelle de la ville de Lübeck](https://bekanntmachungen.luebeck.de/dokumente/d/1936/inline) distingue explicitement les estimations de la **ville intérieure** (17 644 en 1769 ; 18 693 en 1788) des séries sur un autre périmètre. Ces nombres **ne concernent pas HLB**. Ils ne permettent pas non plus d'attribuer automatiquement un chiffre à l'ensemble des possessions de LUB.

Le chiffre de 22 000 associé à la sécularisation de 1803 dans des synthèses n'est pas un recensement de 1776, ni un chiffre du seul noyau effectivement installé. Aucune interpolation ou division arbitraire par deux n'est appliquée. Le fonds Best. 30 comporte des dossiers de population, mais une simple mention de leur existence ne vaut pas lecture d'un dénombrement.

## Incertitudes contradictoires

### Source statistique effectivement lue à la reprise R1

Kohli, *Handbuch...*, volume 2 partie 2, 1826, exemplaire [BSB bsb10020025](https://www.digitale-sammlungen.de/en/view/bsb10020025?page=147), note 36 p. 125 : les nombres d'habitants sont ceux du recensement officiel de **1819** (quatre villages acquis en 1804 font exception, chiffres de 1806). Ville d'Eutin : 2 652, p. 126 ; Amt Eutin : 6 824, p. 132. Trois pages vérifiées visuellement et OCR ciblé dans `CONTINUATION_R1/EVIDENCE/`. Ce sont des références postérieures, pas des cibles établies pour 1776 ; la simple somme ne règle ni la datation ni les recouvrements juridictionnels. Voir `CONTINUATION_R1/POPULATION_EVIDENCE.json`.

### Limites maintenues

- La carte de Reilly simplifie et déforme les positions urbaines. La cohérence des symboles et la régression ne certifient pas les coordonnées natives.
- L'ensemble du Hochstift, le domaine directement gouverné par le prince-évêque et la principauté sécularisée ne sont pas des périmètres interchangeables.
- Des ouvrages sur Stockelsdorf distinguent des situations foncières et juridictionnelles locales antérieures à 1803 ; cela interdit de raisonner seulement à partir d'un nom moderne ou d'une acquisition tardive. Ces parcelles restent C, non appliquées.
