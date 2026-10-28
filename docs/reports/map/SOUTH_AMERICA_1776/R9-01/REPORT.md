# R9-01 — premier lot installé après CENTRAL-02

**27 octobre 2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Cette première correction ne clôt pas l'Amérique du Sud. Les recommandations R9 existantes ont été réutilisées ; les noyaux et preuves CENTRAL-01/CENTRAL-02 restent préservés.

## Résultat

- **17 provinces de l'enveloppe STATE_ICA**, auparavant IQU, rejoignent **SC3, Pérou colonial**. Iquicha ne forme plus au départ une colonie distincte de l'Espagne, anachronisme signalé par les recherches. La définition du TAG demeure disponible ; son ancien pacte colonial initial est retiré.
- **La Paz et deux provinces de raccord**, soit **3 sur les 89** de STATE_LA_PAZ, rejoignent SC3. On ne donne pas toute l'Amazonie ou toutes les hautes terres de cette région à l'Espagne sur la seule base d'un titre impérial. Les vingt provinces transférées rejoignent le noyau de Lima par terre, sans nouvelle côte, nouveau poste isolé ou corridor décentralisé.
- **39 600 Quechua** d'IQU et **158 970 South Andean** de La Paz passent à SC3, au sein de leur région de départ. **Aucun ajout, retrait ou conversion de population.** Les autres **458 067 habitants** de La Paz restent dans leur portion héritée, sans prétendre que cette attribution AP7/Kayapó soit historiquement correcte. La révision des autres autorités reste un lot ouvert.
- **Casernes d'Ica : 3 + 1 = 4 niveaux conservés**, fusionnés dans une seule commande pour éviter le risque d'écrasement après réunion des propriétaires. Même PM `pm_no_organization`, même valeur de réserves ; propriété économique réaffectée de l'ancien IQU à SC3. Tous les autres bâtiments et toutes les formations sont préservés.

**Quatre fichiers runtime modifiés**, manifestés avec empreintes :

1. `common/history/states/00_states.txt` ;
2. `common/history/pops/07_south_america.txt` ;
3. `common/history/buildings/07_south_america.txt` ;
4. `common/history/diplomacy/00_subject_relationships.txt`.

Aucun bitmap, State_ID, ressource, hub, définition de pays ou profil technologique modifié. La région technique dite ICA contient aussi Cusco : la correspondance des noms modernes n'a pas été déduite du nom du State_ID. Les hypothèses géographiques rejetées et le premier patch de casernes restent archivés, à côté de la livraison finale `PATCH.json`.

## Contrôles

**16/16 contrôles techniques installés réussis** : empreintes, syntaxe, vingt attributions exactes, autres propriétaires inchangés, absence de nouveau doublon ou RGB vide, conservation des identités/effectifs par région, absence de scopes économiques IQU orphelins, casernes fusionnées à quatre niveaux et PM/réserves conservés, autres bâtiments inchangés, données de carte/profils/armées préservées, noyaux CENTRAL-02 conservés, liaison terrestre prouvée, autres pactes préservés et absence de changement concurrent non listé.

L'audit technologique reste **FAIL_STATIC** pour les profils préexistants : **SC3 : 18 signalements avant et après ; AP7 : 2 avant et après. Aucun signalement nouveau ou résolu.** Ces dettes ne sont ni masquées ni présentées comme des pannes observées en jeu. Les tests communs de la mission, exécutés à la livraison CENTRAL-02, ont donné 8 réussites ; ils ne sont pas comptés comme une seconde exécution R9.

Vérifications effectuées sur les historiques et scripts, **aucun lancement de Victoria 3 attesté**. Nouvelle partie à tester : propriétaires des anciens secteurs IQU, La Paz, continuité terrestre, total de population des deux régions et quatre niveaux de casernes d'Ica ; simuler un mois et sauvegarder/recharger. Vérifier en particulier les effets des portions de région partagées sur l'emploi et les marchés.

## Recherche et suite R9

Les sources, dates, limites et correspondances sont dans `SOURCES.md`. Les champs non résolus du dossier canonique R9 n'ont pas été réécrits en conclusions certaines. Le noyau urbain de La Paz est corrigé ; la carte AP7 restante n'est pas validée. Les cultures et effectifs sont les agrégats hérités du mod, pas des recensements précis de 1776.

La suite prioritaire est le **Río de la Plata** : Colônia do Sacramento encore portugaise, occupations espagnoles au Rio Grande de São Pedro et dépendances institutionnelles avant août 1776. Puis viennent les Guyanes et la Guajira, Araucanie/Valdivia et la frontière pampéenne/patagonienne, sans attendre les réserves secondaires de CENTRAL-02. Les Malouines demandent de distinguer présence espagnole, évacuation britannique et revendications ; aucun transfert de toutes les îles atlantiques sous une même couleur n'est prescrit.

ColGrep local : **un appel agent terminé en 181,65 secondes**, utile pour retrouver les recommandations et incertitudes canoniques R9. Les chemins et lignes ont été vérifiés puis les sources historiques décisives relues. Pas de compteur de tokens Codex ni de comparaison témoin ; **aucune économie exacte de quota démontrée**. L'appel a produit des extraits trop longs, qui n'ont pas été traités comme des décisions d'implémentation.

Aucun commit, push, merge, rebase ou modification du vanilla. Aucun suivi WORLD ou SERG modifié. Les baselines antérieures et les travaux concurrents préexistants restent conservés.
