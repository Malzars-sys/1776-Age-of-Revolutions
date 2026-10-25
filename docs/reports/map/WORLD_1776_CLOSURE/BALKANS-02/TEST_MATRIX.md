# Vingt domaines de vérification — BALKANS-02

Le succès statique n'est ni une validation moteur, ni la preuve que toutes les questions historiques sont closes.

| Domaine de la mission | Vérification exécutée | Limite restante |
| --- | --- | --- |
| 1. Syntaxe Paradox | Tous les textes fonctionnels propres au lot sont analysés ; reconstruction exacte des mutations attendues | Le parseur n'est pas le chargeur natif |
| 2. TAGs | RAG absent à l'entrée, définition propre, références explicites | Sélection dans l'interface à tester |
| 3. Propriétaires | Trois nouvelles affectations RGB : RAG, TUR, TUR ; anciennes clés inchangées | Statut historique fin traité séparément |
| 4. RGB et cellules | Couleurs libres à l'entrée, une région par RGB, terrains hérités, 122 pixels autorisés | Aucun nouveau trait de côte dessiné |
| 5. Frontières et connexité | Les deux passages touchent la Bosnie et la mer par voisinage orthogonal ; Sutorina sépare Raguse de Cattaro | Contact insulaire artificiel hérité ; tracé approximatif ; Lastovo absent |
| 6. Voisins | Aucune mutation pixel hors `x11A0E0`, aucun transfert AUS/HUN/TRS/MON | L'Istrie de contact reste réservée |
| 7. POPs | Monde 834 936 539 avant/après ; transfert de 30 000 du pool dalmate existant | Calibration de 1776, passages sans répartition fine |
| 8. Cultures et religions | Culture croate transférée sans conversion ; religion catholique implicite conservée | Minorités ragusaines non quantifiées |
| 9. Professions et emploi | Pas de profession POP changée ; capacité cumulée 6 200 emplois, postes non négatifs | Embauche réelle et financement non simulés |
| 10. Gouvernements | Gouvernement et titres dédiés, conditions RAG/république/oligarchie | Sélection et rendu natifs à tester ; rotation mensuelle non simulée |
| 11. Dirigeants | Personnage procédural explicitement non historique | Recteur exact de janvier non identifié ; critère historique partiel |
| 12. Lois | Identifiants résolus et cadre républicain après l'effet initial générique | Institutions complètes non reconstituées |
| 13. Technologies | 19 identifiants, prérequis fermés, absence de grants industriels tardifs | Profil historique abstrait, pas inventaire exhaustif des savoirs |
| 14. Bâtiments et PM | PMG résolus ; PM initiaux autorisés et technologies compatibles ; pêche répartie 3 → 2+1 | Port et chef-lieu minoritaires à vérifier dans la région partagée |
| 15. Ressources | Bloc de ressources dalmate conservé, seule liste de provinces étendue | Répartition et trait Krka hérités : économie historique incomplète |
| 16. Unités militaires | Aucune armée existante touchée ; aucune armée ou flotte fictive ajoutée à RAG | Garde et marine de l'époque non quantifiées |
| 17. Diplomatie | Type tributaire valide pour pays reconnus, pas de participation automatique aux guerres, marché propre | Transfert à 5 % abstrait ; activation et persistance à tester |
| 18. Autres lots | Cyclades 01 et modifications TECH-R2 conservées ; changements externes ALLOYS/TECH-R3 recensés | Mécaniques externes non validées par ce lot |
| 19. SERG | 873 fichiers de preuves identiques ; territoires et pixels hors masque inchangés | Aucun reçu humain SERG nouveau |
| 20. Concurrence | Empreintes avant écriture ; masques et textes reconstruits ; dix fichiers externes attribués séparément | Les agents parallèles peuvent poursuivre après ce reçu daté |

Exécution reproductible : `tools/world1776_balkans02.py --validate`. `--apply` est réservé à l'installation initiale et refuse une deuxième application.
