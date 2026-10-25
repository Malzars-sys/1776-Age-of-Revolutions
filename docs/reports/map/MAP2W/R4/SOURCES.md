# Sources et provenance

Consultation : 18 octobre 2026. Les fichiers conservés sont des preuves documentaires, pas des ressources chargées par le jeu.

| Source | Apport et limites | Copie locale |
| --- | --- | --- |
| [HLB, Passau : territoire et structure, Marc von Knorring](https://www.historisches-lexikon-bayerns.de/Lexikon/Passau,_Hochstift:_Territorium_und_Struktur) | Chronologie territoriale, distinction propriété/souveraineté, environ 900 km² immédiats à l’époque moderne. Ce chiffre n’est pas un relevé cadastral de 1776. | `EVIDENCE/PASSAU_HLB.html` ; illustration ancienne `PASSAU_HLB_BOUNDARIES.jpg` |
| [HLB, Freising : histoire politique](https://www.historisches-lexikon-bayerns.de/Lexikon/Freising,_Bistum:_Politische_Geschichte_(Sp%C3%A4tmittelalter)) | Formation des possessions temporelles, différente de l’étendue diocésaine. Ne suffit pas à dater chaque parcelle en 1776. | `FREISING_HLB.html` |
| [HLB, Werdenfels, Johannes Haslauer](https://www.historisches-lexikon-bayerns.de/Lexikon/Werdenfels,_Grafschaft) | Possession territoriale freisingoise, voisinage d’Ettal, sources cartographiques anciennes. | `WERDENFELS_HLB.html` |
| [HLB, Regensburg : territoire et structure, Diethard Schmid](https://www.historisches-lexikon-bayerns.de/Lexikon/Regensburg,_Hochstift:_Territorium_und_Struktur) | Possessions temporelles et engagements ; distinction du domaine épiscopal et de la ville. | `REGENSBURG_HLB.html` |
| [Germania Sacra, Ludwig Joseph von Welden, GSN 077-00562-001](https://personendatenbank.germania-sacra.de/persons/view/338846) | Identité et dates d’épiscopat, 1769–1788. | `WELDEN_GERMANIA_SACRA.html` |
| [Liste officielle des évêques de Regensburg](https://bistum-regensburg.de/bistum/bischoefe/liste-der-regensburger-bischoefe) | Anton Ignaz, 1769–1787, également prévôt d’Ellwangen. | `REGENSBURG_BISHOPS.html` |
| [Bistum Passau, histoire du séminaire](https://www.bistum-passau.de/bistum-pfarreien/priesterseminar-st-stephan/historie-seminar) | Confirme Firmian, 1763–1783 ; ne définit pas les limites temporelles. | Consultation web, pas de copie HTML locale |
| [Ville de Regensburg, étude patrimoniale de l’Altstadt](https://www.regensburg.de/fm/121/entwicklungskonzept-altstadt-fussgaengerzone.pdf) | Auto-administration urbaine et maintien du statut impérial jusqu’en 1803. Seul le passage textuel indexé a été consulté ; PDF non téléchargé ni rendu. | Aucune copie locale |
| [BSB, Reilly, Das Hochstift Passau, 1791, bsb00090513](https://www.digitale-sammlungen.de/de/details/bsb00090513) | Feuille avec Passau, Freising et Werdenfels ; document postérieur, donc pas une frontière 1776 prête à appliquer. Le manifest indique le domaine public. | `BSB_1791.html`, `BSB_1791_MANIFEST.json`, `BSB_1791_INFO.json`, `BSB_1791_READING.jpg` (3000 px, original annoncé 7650×5686) |
| [BnF, Seutter, Accurata delineatio episcopat. Frisingensis](https://catalogue.bnf.fr/ark:/12148/cb40642782x) | Autre carte ancienne identifiée, édition non précisément datée par la notice ; ni téléchargée ni calée dans R4. | Notice web seulement |
| [Atlas historique de Bavière, Veit, Passau, 1978](https://badw.de/en/publications.html?cHash=86826d9ad7235959d61a356f4a5ab194&tx_badwdb_publications%5Baction%5D=show&tx_badwdb_publications%5Bcontroller%5D=Publications&tx_badwdb_publications%5Bpub_id%5D=10623) | Référence spécialisée identifiée ; le volume et ses planches ne sont **pas** présentés comme consultés intégralement. | Référence bibliographique, pas de planche acquise |
| [BVV, bulletin OpenData 2024/2](https://geodaten.bayern.de/odd/m/3/pdf/newsletter_archiv/2024_02.pdf) | Annonce le WFS sans identifiant du Basis-DLM. Consultation du texte indexé seulement. | Aucune copie du PDF |

## Hydrographie physique indépendante

Service officiel observé : `https://geoservices.bayern.de/wfs/v1/ogc_atkis_basisdlm.cgi`.

Métadonnées `BAYERN_WFS_CAPABILITIES.xml`, schéma `WASSERLAUF_SCHEMA.xml`, échantillons conservés. La première couche `AX_Gewaesserachse` décrit ici surtout les petits cours d’eau : elle n’a pas été utilisée pour déclarer les grands fleuves absents. Les confluents proviennent de **`AX_Gewaesserstationierungsachse`**, noms et identifiants de géométrie conservés.

Cinq fenêtres limitées puis un contexte des huit seules rivières nommées : requêtes intégrales dans `AXES_REQUESTS_4326.json`, `STATION_REQUESTS_4326.json` et `CONTEXT_REQUEST.json`. Respectivement 21/194/366/143/102 petits axes, puis 33/55/146/67/36 axes de stationnement ; contexte : 3035 objets, inférieur au plafond de 10000. Pas de reconstruction d’index ni de téléchargement de toute la Bavière.

L’ordre GML **EPSG:4326 est latitude, longitude** ; le diagnostic le convertit explicitement en longitude, latitude. Le CRS84 non annoncé et le préfixe implicite de la première requête BBOX ont échoué ; réponses d’erreur conservées dans les premiers `*_AXES.gml`. La seconde requête, avec EPSG annoncé et namespace explicite, a fonctionné. La première liste de noms plafonnée à 20 objets (`RIVERS_NAMED.xml`) n’est pas utilisée comme inventaire complet.

Ces données modernes servent uniquement à reconnaître les formes physiques. Elles ne démontrent aucune frontière politique de 1776. Aucun statut de licence pour redistribution comme ressource de jeu n’est déduit de leur seule accessibilité publique.

## Recherche locale ColGrep

Deux tentatives, une recherche utile achevée. La première a échoué sur le verrou d’index hors workspace. La même recherche a ensuite abouti avec le droit d’accès requis, sans changer de modèle ou d’intégration :

```powershell
& 'C:\Users\simeo\.cargo\bin\colgrep.exe' --agent 'Locate existing reports, maps and implementation tools for territorial Freising, Passau, Regensburg and free imperial city Regensburg in Bavaria in 1776; identify already installed Eichstaett cores. Read-only search; return paths and line numbers.' .
```

Sortie finale, code 0 : `MAP2L/FRANCONIA_CONTINUATION/REPORT.md:18–20` (transferts EIC vérifiés), `FRANCONIA_CONTINUATION/REGISTRY_MIGRATION.json:1–897` (existence et lignes de migration vérifiées), `tools/map_1776_audit.py:24` (liste REGIONS, **non pertinent pour Freising/Passau**, écarté). Ce sont des pistes vérifiées, pas une décision historique déléguée.

La sortie capturée ne contient pas le journal détaillé du backend : elle prouve l’appel `--agent` terminé, **pas une télémétrie GPU ou un décompte des tokens du modèle local**. Une mesure précise de durée et un compteur exhaustif de recherches classiques n’ont pas été instrumentés ; les tokens Codex ne sont pas accessibles ici. Pas d’affirmation d’économie chiffrée. `rg` a servi aux noms/identifiants exacts et aux lignes déjà connues ; aucune recherche sémantique répétée pour gonfler les statistiques.
