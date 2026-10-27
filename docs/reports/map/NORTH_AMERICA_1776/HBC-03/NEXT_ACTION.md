# HBC-04 — affectations territoriales et implantation protégée

Mise à jour : [HBC-04](../HBC-04/REPORT.md) prépare la nouvelle continuité militaire demandée HBC → ONT → USA, avec 233 provinces HBC et un passage ONT réservé. La proposition active est désormais `../HBC-04/LAND_LINK_CANDIDATE.json` ; suivre [sa prochaine action](../HBC-04/NEXT_ACTION.md). Le socle de conservation HBC-03 reste inchangé.

Proposition active : `EASTMAIN_CANDIDATE.json` / `EASTMAIN_ARC.png`, avec 228 provinces candidates et cinq postes reliés. Socle économique/démographique : `CONSERVATION_BASELINE.json`, à conserver sans écrasement.

Vérification complémentaire demandée par le joueur : [Kuujjuarapik/Great Whale River](KUUJJUARAPIK_CHECK.md). Aucun poste actif en 1776 établi par les sources consultées ; condition de prolongement non remplie. Conserver Eastmain comme limite de la proposition, sans intégrer un poste du XIXe siècle au départ de 1776.

1. Réutiliser les dossiers R8, les positions HBC-02 et les compléments Eastmain HBC-03. Préciser les sites/itinéraires encore approximatifs et compléter les postes de l'ouest omis du scénario de cinq points.
2. Régler les détenteurs locaux des territoires retirés à HBC, leur abstraction politique et leur démographie propre, sans prélever ni dupliquer les 108 626 habitants protégés de la compagnie.
3. Préparer le patch territorial en conservant la continuité des postes et le remplissage demandé côté littoral. Garder la réserve québécoise autour d'Eastmain ; ne pas introduire un poste de Rupert au 1er janvier sur la seule foi d'une réouverture durant l'année.
4. Appliquer le plan de conservation de tous les POPs HBC et de ses bâtiments ; actualiser les références de localisation plutôt que supprimer les contenus des portions retirées. Le transfert Nunavut→Manitoba reste une proposition de gameplay à adapter seulement en gardant tous les totaux protégés.
5. Exécuter `python tools/hbc03_quebec_arc.py --check-conservation` contre le socle figé, puis les contrôles de propriété/RGB. Vérifier ressources, niveaux, PM, propriétaires économiques et infrastructures dans une nouvelle partie ; comparer le total de population et tous les bâtiments, puis un mois et sauvegarde/rechargement.

Les suivis WORLD/SERG ne sont ni avancés ni validés par ce dossier. Aucune validation moteur ou attribution autochtone non étudiée ne doit être inventée pour clore le lot.
