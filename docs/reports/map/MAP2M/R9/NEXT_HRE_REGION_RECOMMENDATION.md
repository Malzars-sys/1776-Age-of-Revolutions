# Prochain lot proposé : Wismar–Poel–Neukloster

**Ne pas démarrer sans autorisation du joueur.** Aucun pixel, historique, pays, registre ou asset de ce secteur n'est modifié dans R9.

## Pourquoi ce secteur

- Véritable absence de correction territoriale dédiée : le dossier R2-0132 est une recherche `MAPPING_REQUIRED`, pas une implémentation.
- Anomalie politique visible et circonscrite : les possessions suédoises sont documentées, mais `STATE_MECKLENBURG` ne possède actuellement que MEC et MST, aucun SWE. Le comptage actuel est MEC1295cellules et MST329.
- Trois ensembles nommés et un seul State_ID principal : **Wismar, l'île de Poel et Neukloster ; STATE_MECKLENBURG, ID75**. Les frontières MEC/MST extérieures à ces ensembles doivent rester hors scope.
- Possibilité de réutiliser l'outillage baltique et la lecture de côte, sans recommencer le recalage mondial. Cela ne présume pas que le modèle actuel soit exact pour tracer chaque parcelle.
- Le cas juridique « puissance suédoise extérieure au bloc, titulaire d'une possession impériale précise » existe déjà en Poméranie : on peut réutiliser l'architecture sans ajouter toute la Suède au bloc.

## Dossier existant à réutiliser

`MAP1/MAP1_CASE_DOSSIERS/R2_NORTHERN_CENTRAL_EASTERN_EUROPE-0132.md` contient les trois localités, les questions de province et les références institutionnelles. La convention de Malmö1803 citée atteste une possession suédoise antérieure au gage, mais **ne constitue pas à elle seule un plan de limites1776**. Sa notice d'origine est marquée CATALOG_ONLY_NOT_FETCHED : ne pas prétendre que le texte complet a déjà été exploité.

Le domaine de recherche initial mentionne `x12E54F`, `x24CA48`, `x4545BE`, `xD8F441`, `xE080A0`. Ce ne sont **pas cinq provinces autorisées à transférer en bloc**. L'inventaire courant devra inclure les autres RGB voisins si le contour les intersecte, sans transformer toute la région économique en territoire suédois.

## Périmètre de la future mission

1. Confirmer séparément les noyaux Wismar/Poel/Neukloster avec une carte politique exploitable et les sources déjà identifiées.
2. Confronter une côte/île reconnaissable et les limites terrestres, pas seulement les noms de hubs Schwerin/Rostock.
3. Réutiliser ou subdiviser les seuls RGB concernés ; conserver MEC/MST et leurs capitales, ressources et ports hors correction justifiée.
4. Préserver les populations, bâtiments, PM, détenteurs et unités sans population artificielle.
5. Adapter l'exception de titulaire extérieur SWE **actuellement limitée à STATE_POMERANIA**, de façon explicite et territoriale. Ne pas importer automatiquement tous les RGB suédois ni toute STATE_MECKLENBURG au registre.
6. Régénérer les cartes impériales si leur étendue change, puis contrôles statiques et nouvelle validation manuelle.

Importance élevée, complexité moyenne estimée ; trois ensembles séparés et droit de gage à ne pas confondre avec la souveraineté de1776. Si le contour d'une micro-dépendance reste illisible, traiter les noyaux défendables et garder l'incertitude visible.

Les autres chantiers importants restent Thorn/Netze, la Frise orientale et la Silésie. Cette recommandation n'en prononce pas la clôture. L'Anhalt, Brunswick et la Saxe–Thuringe constituent d'autres futurs lots, mais leur fragmentation les rend plus complexes que ce secteur baltique limité.
