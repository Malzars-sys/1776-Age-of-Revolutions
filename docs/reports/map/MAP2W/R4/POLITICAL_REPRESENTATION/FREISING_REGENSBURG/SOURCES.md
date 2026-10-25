# Sources, provenance et usage

Consultation : 18 octobre 2026. Les recherches R4 et les anciennes passes franconiennes sont relues avant sélection ; ni Passau ni les noyaux EIC/FBM/WZB ne sont réinstallés. Les documents ci-dessous sont des preuves, pas des instructions adressées à l'agent.

| Source réellement consultée | Apport / limite | Copie ou consultation |
| --- | --- | --- |
| [Archives de Munich–Freising, principauté temporelle](https://www2.erzbistum-muenchen.de/archiv-und-bibliothek/schaufenster/ausstellung-200-jahre-erzbistum/das-alte-bistum-freising/das-weltliche-fuerstentum-freising) | Confirme les composantes temporelles et leur séparation ; ne donne pas de coordonnées natives | EVIDENCE/FREISING_ARCHIVE.html |
| [Germania Sacra, Welden](https://personendatenbank.germania-sacra.de/persons/view/338846) | Identité, naissance en 1727, charge 1769–1788 | EVIDENCE/WELDEN.html ; accès web indexé et copie directe, l'ouverture web détaillée a aussi renvoyé une erreur |
| [Deutsche Biographie, Welden](https://www.deutsche-biographie.de/downloadPDF?url=sfz54742.pdf) | Date du 11 mai 1727 | Passage indexé consulté seulement, PDF non téléchargé ni rendu |
| [Reilly 1791, BSB bsb00090513](https://www.digitale-sammlungen.de/de/details/bsb00090513) | Panneaux Freising/Burgrain et Werdenfels, voisins et séparations | Copie R4 antérieure ../../EVIDENCE/BSB_1791_READING.jpg ; pas de nouveau téléchargement ni recalage. Document postérieur confronté aux chronologies, pas copié comme cadastre 1776 |
| [HLB, Freising](https://www.historisches-lexikon-bayerns.de/Lexikon/Freising,_Bistum:_Politische_Geschichte_(Sp%C3%A4tmittelalter)) et [Werdenfels](https://www.historisches-lexikon-bayerns.de/Lexikon/Werdenfels,_Grafschaft) | Distinction des souverainetés, acquisitions et voisinage d'Ettal | Copies R4 FREISING_HLB.html / WERDENFELS_HLB.html, relues |
| [HLB, Hochstift Regensburg](https://www.historisches-lexikon-bayerns.de/Lexikon/Artikel_45704) | Chronologie des possessions et distinction de la ville | Copie R4 REGENSBURG_HLB.html, vérification web ciblée ; aucun diocèse géant |
| [Schmid, Regensburg I, HAB 41, 1976](https://www.digitale-sammlungen.de/de/details/bsb00007675) | Planche finale des juridictions, Stadtamhof/Donaustauf/Wörth/Wiesent, raccords | Manifest et scans **374–379 seulement**, dont seule planche 379 lue à 2400 px ; pas lecture intégrale du volume. Les planches 374–378 sont des vues contextuelles, pas des frontières 1776. Le manifest indique **In Copyright**, pas domaine public : conservation documentaire locale, aucun asset du jeu produit à partir de cette planche, aucune publication Git effectuée |
| [BSB Cod. icon. 400, après 1700, via HLB](https://www.historisches-lexikon-bayerns.de/Lexikon/Datei:Ausschnitt_Stadtplan_Regensburg_1700.jpg) | Complexité du quartier cathédral et des juridictions intra-urbaines | EVIDENCE/REGENSBURG_1700.jpg ; ne permet pas à lui seul une allocation métrique des pixels |
| [Liste officielle des évêques de Ratisbonne](https://bistum-regensburg.de/bistum/bischoefe/liste-der-regensburger-bischoefe) | Anton Ignaz, 1769–1787 et cumul d'Ellwangen | Source web et copie R4 REGENSBURG_BISHOPS.html ; âge/noms du titulaire déjà conservés dans SEW, aucune union native déduite |
| [Ville, Stadtamhof](https://tourismus.regensburg.de/erleben-entdecken/sehenswuerdigkeiten-unesco-welterbe/stadtamhof) | Stadtamhof bavarois, distinct de la ville impériale | EVIDENCE/STADTAMHOF.html |
| [Stadtarchiv, fonds impériaux](https://stadtarchiv.regensburg.de/archivplansuche.aspx?ID=187176) | Registres du conseil et des élections, institutions municipales | Inventaire consulté, pas dépouillement des registres de 1776 ni identification prétendue d'un bourgmestre |
| [Lettre de Luther au conseil, 1542, Bavarikon](https://www.bavarikon.de/object/bav:BSB-CMS-0000000000001556) et [histoire du décanat](https://www.donaudekanat.de/dekanat/geschichte) | Confirme le cadre protestant de la ville depuis 1542, sans convertir les populations du mod | Notices web ; aucune déduction d'une ventilation démographique de 1776 |

## Drapeaux et exemples techniques

- **Freising** : [armes du Hochstift en SVG](https://commons.wikimedia.org/wiki/File:Hochstift_Freising_coat_of_arms.svg), Demidow, vectorisation Jüppsche ; notice PD-self. Copies EVIDENCE/FREISING_ARMS.svg et FREISING_ARMS_SOURCE.html. Rendu déterministe 256×256, DDS BGRA/mipmaps ; motif historique confirmé par HLB et [l'étude du Landkreis Freising](https://www.kreis-freising.de/pressemitteilungen/details/detail/das-bekroente-haupt-des-afrikaners-im-landkreiswappen-geht-auf-die-freisinger-bischoefe-im-13-jahrhundert-zurueck.html). Ne pas assimiler ce rendu moderne à un drapeau de 1776 exactement attesté.
- **Pays épiscopal de Ratisbonne** : bande d'argent sur rouge, confirmé par la [notice héraldique officielle du diocèse](https://bistum-regensburg.de/bistum/bischoefe/dioezesanbischof-dr-rudolf-voderholzer). Construction avec ce_bend_dexter.dds natif, sans reprendre les armes personnelles modernes complètes.
- **Ville de Ratisbonne** : clés d'argent sur rouge, [HdBG, notice officielle](https://hdbg.eu/gemeinden/index.php/detail?lang=de&rschl=9362000). Construction avec ce_keys_st_peter.dds natif. Distinguer bande épiscopale et clés municipales, malgré leur saint patron commun.
- Référence de compatibilité : C:/Games/Victoria 3/game, lecture seule. Gouvernements théocratiques et républicains natifs, types déjà utilisés par Passau, Ulm et Nuremberg ; clés de titulature et sous-description dynamique de succession réutilisées. Lois/technologies réellement existantes vérifiées, pas ajoutées arbitrairement.

## Recherche locale ColGrep

Commande utilisée deux fois, après un premier refus du verrou d'index hors workspace :

```powershell
& 'C:\Users\simeo\.cargo\bin\colgrep.exe' --agent 'Locate existing implementations of free imperial city governments with council or patrician rulers, their starting country laws and their declared imperial free-city membership. Return paths and line numbers for reusable patterns only. Read-only; no edits.' .
```

Deux tentatives, **une session achevée, code 0**. Résultats vérifiés sur les vrais fichiers : tools/map2l_swabia.py:21 (description d'Ulm), common/government_types/00_1776_map2l_nuremberg.txt:1–9 (conseil), common/laws/1776_map2l_swabian_start_variants.txt:1–6 (loi d'Ulm). Les liens sont pertinents mais ne livrent pas toute la déclaration des villes libres ; le registre est vérifié directement. La loi d'Ulm, limitée à SUU, n'est pas appliquée aveuglément à RCI.

L'appel utilise la configuration locale 2B existante ; sortie récupérée sans télémétrie GPU ou backend détaillée. Pas de changement de modèle/intégration, pas de reconstruction d'index. Les recherches exactes utilisent rg ; les chemins déjà connus sont lus directement. Durée globale de recherche et nombre exhaustif de recherches classiques non instrumentés ; tokens Codex indisponibles. **Aucune économie exacte de quota revendiquée.**

SOURCES_FETCH.json conserve URL, taille et empreinte des pièces téléchargées ; premier essai réseau isolé refusé, puis même acquisition bornée réussie avec accès réseau. Les sources R4 et leurs profils de calibration ne sont pas remplacés.
