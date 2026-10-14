# MAP2L — Bergstraße–Starkenburg et possessions du Main–Spessart

Date de référence : 1er janvier 1776. Implémentation de ce lot, pas certification de toutes les possessions de Mayence.

## Sources et continuité territoriale

La [carte de De Wit conservée à e-rara](https://www.e-rara.ch/bes_1/content/titleinfo/29609156), déjà utilisée dans le lot Neckar, est réemployée pour la Bergstraße. Son image conservée est `../RHINE_CENTRAL/DE_WIT_MAINZ_3500.jpg`. Le calage local Neckar n'est pas extrapolé à Orb. [Heppenheim](https://heppenheim.de/heppenheim-erleben/stadtgeschichte) est confirmé mayençais jusqu'en 1803 ; l'ancien engagement palatin prend fin en 1623. Ne pas confondre cette possession avec la province hessoise ultérieure appelée Starkenburg.

Pour le Main–Spessart, la [carte détaillée de l'Oberstift](https://www.historisches-lexikon-bayerns.de/Lexikon/Datei:Artikel_45154_bilder_value_4_oberstift2.jpg) représente 1789 et provient de l'atlas de Spindler/Diepolder, 1969, p. 30. Elle est conservée uniquement comme comparaison documentaire, sous copyright Bayerischer Schulbuchverlag ; ce n'est pas un asset du jeu. Elle distingue les juridictions voisines et ne doit pas être confondue avec l'ancienne carte générale dynastique de 1789 écartée pour le découpage fin.

La notice de l'[Historisches Lexikon Bayerns sur l'Oberstift](https://www.historisches-lexikon-bayerns.de/Lexikon/Artikel_45154) distingue les possessions séculières de Mayence de son ressort diocésain. Le présent tracé couvre le raccord Steinheim/Seligenstadt/Dieburg, Aschaffenburg–Spessart et les secteurs d'Orb/Lohr et de Klingenberg–Miltenberg–Amorbach. Il ne projette pas la réforme administrative de 1782 sur les institutions de départ. La portion méridionale au-delà de ce raccord n'est pas implémentée ici.

La date de la comparaison n'est pas traitée comme preuve suffisante de la situation de 1776. Les continuités principales sont confrontées aux chronologies locales : [Lohr](https://www.lohr.de/tourismus/stadtgeschichte-chronik), mayençais depuis 1559 ; [Orb](https://stadt-bad-orb.de/Leben-Wohnen/Stadtportrait/Geschichte-von-Orb/), dont les engagements de 1665–1721 ne valent plus à la date de départ ; [Miltenberg](https://www.miltenberg.de/miltenberg/stadtgeschichte/geschichte-in-stichworten/), mayençais jusqu'à la sécularisation.

Correction de la liste proposée précédemment : [Rieneck appartient aux Nostitz depuis 1673](https://www.rieneck.de/geschichte-der-stadt-rieneck). La ville/seigneurie n'est donc pas absorbée dans Mayence en invoquant l'ancienne succession du comté de Rieneck. Les exclusions tracées couvrent aussi les contacts d'Isenburg, de Würzburg et d'Erbach et les territoires non mayençais de Freudenberg et Kleinheubach. Les propriétaires de gameplay inchangés dans ces franges restent à auditer séparément : leur maintien ne certifie pas leur souveraineté historique.

## Calage vérifiable

Deux modèles locaux explicites sont conservés dans `TRACING.json` et `ALIGNMENT.json` :

- Bergstraße : affine du lot Neckar, limitée au secteur au sud de Darmstadt.
- Oberstift : quatre symboles urbains observés sur la carte (Frankfurt, Aschaffenburg, Lohr, Miltenberg) ajustent la carte vers les coordonnées géographiques ; Frankfurt, Würzburg et Heidelberg relient ces coordonnées aux locators du jeu. Ce modèle à trois ancrages est exact par construction, pas une mesure indépendante de précision historique.

Wertheim est réservé au contrôle indépendant, sans participer à l'ajustement. L'écart reproduit est de **0,7401 pixel** du jeu. Coordonnées, liens, matrices, résidus et empreintes des images sont enregistrés dans l'alignement. Les symboles urbains, et non le centre des libellés, définissent les points. Les limites sont tracées sur les juridictions figurées : aucune partition territoriale par distance à une ville n'est employée.

Les fichiers `DE_WIT_OVERLAY.png` et `HL_OVERLAY.png` permettent de revoir le tracé. `BEFORE_AFTER.png` montre les propriétaires de gameplay, sans prétendre certifier les franges inchangées.

## Abstraction et travaux restants

Les micro-enclaves sous la résolution du jeu ne sont pas agrandies. Le contact d'un pixel avec le Ladenburg palatin et les trois pixels au bord des tracés de Würzburg restent dans leurs anciens titulaires, compte tenu de l'incertitude du raccord. Les contours ne constituent pas un relevé cadastral.

Restent distincts de cette passe : Buchen, Tauberbischofsheim et Krautheim au sud, Erfurt/Eichsfeld au nord, le grand noyau mayençais encore grossier et le complément du Rheingau. Le Palatinat occidental et les propriétaires résiduels non certifiés exigent également leurs propres lots. Aucun territoire extérieur au périmètre impérial n'est modifié ici.
