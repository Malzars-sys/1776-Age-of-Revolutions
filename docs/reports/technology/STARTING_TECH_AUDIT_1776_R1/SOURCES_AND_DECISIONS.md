# Sources et décisions — 1776-01-01

Consultation du 24 octobre 2026. Audit fonctionnel distinct du chantier territorial SERG. Aucun reçu humain ancien ne couvre les technologies ou la méthode de production modifiées ici.

## Référence technique réellement lue

- Exécutable local : Victoria 3 **1.13.11**, propriété ProductVersion/FileVersion. Données vanilla sous `C:/Games/Victoria 3/game`, consultées sans écriture.
- `descriptor.mod` remplace entièrement les technologies et les eras vanilla. Les historiques nationaux chargés résultent de l'overlay par chemin de fichier ; plusieurs fichiers peuvent compléter le même TAG. Les effets communs sont résolus récursivement, les branches conditionnelles sont séparées des attributions certaines.
- `common/scripted_effects/00_starting_inventions.txt` : sept paliers explicites 1776. Ils remplacent les listes vanilla 1836 ; leurs contenus ne sont pas copiés aveuglément. `effect_starting_politics_reactionary`, lui, provient du vanilla `00_political_setup.txt` : **il ne donne aucune technologie** et contient des lois modernes dont les gates ont changé dans le mod.
- Historique BGT existant, avec ce seul effet politique et des lois ; aucune attribution technologique directe ou par palier. Ses noms et les hooks impériaux ne remplacent pas un profil technologique. Définition nationale reconnue, carte et historique présents : ni TAG absent ni historique manquant.
- Mine standard : `common/buildings/10_tech6a1b_salt_buildings.txt`, gate `shaft_mining`. Pioches/pelles sans gate supplémentaire ; 4500 ouvriers et 500 commerçants de capacité par niveau, outils 2 → sel 20 à plein fonctionnement. La méthode additionnelle de données active exigeait `scientific_metrology`, papier 0,1 et 10 employés ; **ce n'était pas un besoin de l'extraction traditionnelle**. Elle est remplacée uniquement dans l'historique BGT par `pm_1776_no_raw_data_reporting`, méthode neutre déjà définie et par défaut. Capacité totale écrite après correction : **5000**, recrutement réellement possible à mesurer en jeu.
- Ressource sel de la région technique Tyrol : quantité découverte **18**, non découverte **0**. Ce total n'est pas la capacité propre à BGT. La répartition par portion et l'accès effectif sont moteur ; l'ancienne capture du joueur montrait une capacité locale de deux niveaux, sans valider la version actuelle.
- La mine reste publique, niveau 1, réserves 1 ; aucune subvention ajoutée. Avec 1000 habitants et la chancellerie de 100 postes, le plein emploi de 5000 postes est impossible. Les habitants ne sont pas tous des travailleurs : aucun effectif recruté, PIB, taux de remplissage ou équilibre de marché n'est inventé.

## Sources historiques et usage borné

| Source effectivement consultée | Fait utilisé | Limite / décision |
| --- | --- | --- |
| [Exploitant du Salzbergwerk Berchtesgaden, histoire](https://www.salzbergwerk.de/de/das-salzbergwerk/das-erwartet-sie/geschichte-des-salzbergwerks) | Petersberg en activité depuis 1517, transformation de saumure avant 1776 ; conduite Reichenhall de 1817 | Justifie extraction souterraine traditionnelle ; aucune pompe de 1817 ou mine industrielle à vapeur accordée. |
| [Parc national de Berchtesgaden, plan historique forestier](https://www.nationalpark-berchtesgaden.de/service/publikationen/veroeffentlichungen/doc/nationalparkplan_bestandesplan.pdf) | Bois pour le sel, agriculture et artisanat ; objectif d'approvisionnement durable formulé en 1602 | Passage textuel indexé lu, pas lecture intégrale du PDF. Étaye `organized_forestry` ; pas d'exploitation forestière moderne inventée. |
| [Archives provinciales de Bolzano, corporation des meuniers/boulangers de Bressanone](https://kulturgueter.provinz.bz.it/it/news/l-opera-pia-di-maria-schwarz-vedova-wanner-a-bressanone-1621) | Organisation artisanale du pain ancienne et durable | Étaye nourriture et ateliers. Le profil agricole/textile courant est une calibration régionale prudente, pas une liste recensée de manufactures. |
| [Imprimeur Weger, histoire de ses collections et de son entreprise](https://www.weger.bz.it/de/unternehmen/geschichte.html) | Imprimerie à Brixen depuis 1550, presse ancienne et archives conservées | Justifie accès aux techniques et réseaux imprimés ; ne crée ni papeterie ni usine. |
| [Bibliothèque municipale de Trente, notice Monauni](https://bibcom.trento.it/content/download/39814/435325/file/tipografi_ester.pdf) | Impressions depuis 1725, imprimeur épiscopal confirmé en 1758 puis 1765 ; textes religieux, scolaires et périodiques | Passage indexé lu. Soutient l'imprimé avant 1776. `medical_degrees` était déjà donné à TRT ; son parent scientifique est rétabli, sans nouvelle académie militaire. |
| [Musées de Liège, dossier MULUM](https://lesmuseesdeliege.be/wp-content/uploads/2021/11/essentiel-mulum.pdf) ; [Province de Liège, dossier La mine](https://www.provincedeliege.be/sites/default/files/media/8274/DansLeTemps_theorique_final.pdf) | Exploitation houillère antérieure à 1776 | Passages indexés lus : ajout du seul `shaft_mining` à LGE pour sa mine installée. Pas de coke ou vapeur ajouté. |
| [National Army Museum, guerre de Sept Ans, section Inde](https://www.nam.ac.uk/explore/seven-years-war) ; [étude du Carnatique, Review of Agrarian Studies](https://ras.org.in/articles/202/text/article.html) | Armées et guerres du Carnatique avant 1776, appareil de Muhammad Ali Wallajah | CAR possédait déjà `regulated_small_arms` ; seul le parent administratif militaire manque. Aucune arme avancée ni unité nouvelle. |

Recherches et preuves locales réutilisées : `TECH_START_1776_SECOND_PASS_COUNTRY_PLAN.csv`, résolutions et décisions de fermeture ; `TECH_START_1776_FINAL_IMPLEMENTATION_REPORT.md` ; `TECH_START_1776_ALLOYS_AND_DIPLOMACY_DISTRIBUTION.md` ; sources BGT/BRX/TRT/MCA dans SERG_CLOSURE ; historiques et décisions MAP2F/MAP2H. Ces documents ont des dates différentes : leurs cibles ne sont pas traitées comme des copies exactes du workspace actuel.

## Huit corrections concrètes

- **BGT 0→10** : huit capacités agricoles, artisanales, alimentaires, imprimées et diplomatiques communes, plus extraction par puits et foresterie. Aucun nœud militaire, coke, vapeur, rails, finance avancée ou académies techniques.
- **BRX 1→8** : même socle courant, sans spécialisation saline ni capacités complètes de l'Autriche.
- **TRT 4→10** : socle commun et parent `institutionalized_scientific_exchange` de la médecine déjà attribuée. Pas de nouvelle profession.
- **LGE 12→13** : seule extraction par puits, justifiée par l'activité houillère.
- **PAP 15→16**, **CAR 6→7** : seul `organized_military_establishments`, parent manquant de capacités déjà accordées, notamment génie pour PAP et armes réglementées pour CAR. Les capacités supérieures ne sont pas nouvelles.
- **ARK 18→19**, **VIE 18→19** : seul `improved_husbandry`, socle manquant sous les techniques agricoles déjà présentes. Cela ne certifie pas toutes leurs techniques avancées héritées ; les révisions historiques restent signalées par pays.
- **MCA** conserve ses dix technologies artisanales et médicales cohérentes avec le noyau de résidence installé. Carrare n'est pas transformée en mine dans un territoire encore non représenté.
- Les profils simples de petits États allemands correspondant aux cinq nœuds communs déjà recherchés pour ANH sont conservés. Leur petite taille n'impose ni suppression ni ajout automatique. Les listes de 21 nœuds copiées de profils régionaux restent à vérifier pour leurs capacités spécialisées ; la présence d'un historique ne suffit pas à les certifier.

Les effets nouveaux utilisent un socle partagé puis des extensions étroites. Ils sont appelés uniquement dans un historique additionnel, sans événement, hook de démarrage ou premier tick. Les effets de paliers existants et les fichiers nationaux antérieurs restent inchangés.

## Exceptions et questions maintenues

- Certains profils vides sont explicitement voulus par la recherche existante ou le palier 7 ; ils ne sont pas assimilés à BGT. Huit communautés décentralisées n'ont pas d'historique retrouvé : elles restent `MISSING_HISTORY`, sans profil occidental forcé. Les trois cas vides hors plan vérifié restent en revue.
- `sericulture` est un marqueur régional ancien non recherchable avec effet réel sur la soie : ce n'est pas un alias obsolète à supprimer.
- L'ancien plan contient `systematic_administrative_statistics`, absent de l'arbre actuel. Il est signalé comme référence périmée, jamais réattribué comme un ID réel. Les autres écarts avec les plans anciens restent visibles.
- Sept pays possèdent `alloysworking` sans `coke_smelting` dans le graphe actuel. La note historique des alliages et le graphe sont contradictoires. Aucun coke artificiel n'est accordé pour masquer cette dette ; arbitrage de définition requis.
- Les huit attributions de `standardized_naval_signals` ont une classification ancienne tardive mais des distributions ultérieures : signalement pour revue, aucune suppression d'un chantier naval concurrent.
- Le CSV des conflits couvre les déclarations initiales, y compris des couches potentiellement complétées par d'autres historiques. Il ne prouve pas à lui seul le blocage final dans le moteur. Les ports, baleinières, universités, armureries et PM industriels demandent une réconciliation par processus, pas l'attribution automatique de tous leurs gates.
- BGT : les lois héritées de l'effet politique vanilla ont aussi des problèmes **distincts des technologies**. Les écoles religieuses sont incompatibles avec le servage dans le mod ; les variantes douanières et de liberté impériale restreignent leurs TAG autorisés et n'incluent pas BGT. Le journal existant signale des lois non retenables. Aucun de ces textes politiques n'est modifié dans cette mission, conformément à la protection des lois ; ils restent à arbitrer et à observer. Les technologies nouvelles ne prétendent pas résoudre ces incompatibilités.

Statut de toute nouvelle installation : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun lancement du moteur par l'agent, aucune nouvelle validation humaine, aucun changement territorial ou comptable SERG.
