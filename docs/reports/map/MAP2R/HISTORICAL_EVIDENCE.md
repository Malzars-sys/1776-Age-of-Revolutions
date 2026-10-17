# Preuves et limites — Anhalt1776

## Sources réutilisées

- R2 : `MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv`, lignes40–41. La représentation ANH agrégée était explicitement une abstraction, pas un tracé des quatre principautés.
- `MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md` : voisinages prussiens à préserver tant que les limites ne sont pas établies.
- `docs/research/characters/RULERS_1776_EUROPE_RESIDUAL_SOURCES.md`, lignes18–19 : avertissement contre une division sans source et sans choix du joueur. Le choix de créer les trois pays a depuis été donné explicitement.
- `MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md` : Jever distinct de Varel/Kniphausen ; les grands RGB OLD ne constituent pas des limites certifiées.

## Carte primaire et contrôle chronologique

**S1 — Euler, Rhode, Berger, Tabula geographica principatus Anhaltini et Finitimarum regionum,1753.** [Catalogue David Rumsey](https://www.davidrumsey.com/luna/servlet/detail/RUMSEY~8~1~290934~90062555), [métadonnées et copie numérique](https://archive.org/metadata/dr_tabula-geographica-principatus-anhaltini-et-finitimarum-regionum--kartenma-11392035). Original conservé dans EVIDENCE/EULER_1753.jp2,10490×7479. L’aperçu2200px et SOURCE_TRACING_REVIEW.png montrent les enveloppes interprétées. Source antérieure à la mort de Friedrich August1793 ; pas de reprise du partage ultérieur.

Les contours ne reposent pas uniquement sur la localisation d’une ville : ils suivent les ensembles colorés et leurs exclusions sur la carte, recoupés par les descriptions administratives. Enveloppes généralisées, pas copie cadastrale. La couleur générale Bernburg ne suffit notamment pas à absorber Hoym en1776.

**S2 — [LASA Gesamt-Anhalt](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=190133).** Principautés distinctes et institutions communes ; la maison dynastique n’est pas un pays territorial unifié. Les institutions communes et le vote historique commun ne sont pas convertis en quatre nouveaux électeurs.

**S3 — [LASA Anhalt-Zerbst](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=188603)** et [cartes de Zerbst](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=659158). Souveraineté de la lignée avant1793. Des descriptions d’archives donnent1796 pour certains actes de partage, tandis que le prompt retient1797 : cette différence administrative reste signalée et n’a aucun effet sur l’attribution1776.

**S4 — LASA Bernburg : [Plötzkau](https://recherche.landesarchiv.sachsen-anhalt.de/Query/detail.aspx?ID=188270), [Gernrode](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=188264), [Harzgerode](https://recherche.landesarchiv.sachsen-anhalt.de/query/detail.aspx?ID=188268), [Hoym](https://recherche.landesarchiv.sachsen-anhalt.de/Query/detail.aspx?ID=188269).** Bernburg, Plötzkau, Ballenstedt, Gernrode, Harzgerode et Güntersberge distingués des acquisitions ultérieures. Mühlingen/Coswig1797 et Hoym1812 ne sont pas appliqués à1776. Les intérieurs installés sont limités à l’emprise existante ANH ; la totalité de ces Amts n’est pas revendiquée comme reconstruite.

**S5 — [NLA OL Best90 Jever](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640).** Passage à Anhalt-Zerbst en1667, puis possession personnelle de CatherineII après1793. En1776 Jever n’est ni un territoire OLD autonome ni une possession russe. Souveraineté établie mais frontière native laissée C.

**S6 — [Reconstruction1747–1793](https://commons.wikimedia.org/wiki/File:Map_of_Anhalt_(1747-1793).svg)**, SirIain2013,CCBY-SA3.0. Fichiers conservés dans EVIDENCE, utilisé comme orientation secondaire seulement, pas comme source primaire unique des limites.

## Souverains et démographie

[Leopold Friedrich Franz](https://www.deutsche-biographie.de/sfz68642.html), né1740-08-10 ; [Friedrich Albrecht](https://www.deutsche-biographie.de/gnd104173254.html), né1735-08-15 ; [Karl Georg Lebrecht](https://www.deutsche-biographie.de/sfz39876.html), né1730-08-15 ; [Friedrich August](https://www.schloss-zerbst.de/html/fuersten/friedrich_august.htm), né1734-08-08. Aucun titre ducal du XIXe siècle ajouté. Les rattachements d’intérêt politique sont des abstractions de gameplay, pas des faits déduits de leurs dates de naissance.

La chronologie municipale de [Köthen, XVIIIe siècle](https://www.koethen-anhalt.de/de/401%2C1233.html?single_con=3238%2C1233) mentionne24702 habitants en1770 pour ville et pays. Cette mention n’a pas été vérifiée par lecture du recensement original, et ne correspond pas au périmètre incomplet installé. **Aucune population historique chiffrée n’est donc appliquée.** Les répartitions présentes restent techniques et explicitement provisoires.

## Calage et classification

ALIGNMENT.json conserve six repères sur la source contre un diagnostic géographique retenu, ancré au hub technique de Magdebourg. Les résidus de ce fit, inférieurs à0,35px, ne mesurent PAS l’exactitude des villes natives. Aucune borne géographique indépendante n’est disponible. Le locator agricole n’est pas utilisé comme ville témoin.

- A : existence et souveraineté distinctes des quatre principautés, lien Jever–Zerbst.
- B installé : intérieurs de juridiction sur S1, découpés à la résolution du bitmap et recoupant exclusivement les deux RGB déjà ANH.
- C non installé : Jever, franges extérieures, Hoym et enclaves non localisées. Les résidus ANH restent conservés sans certification historique de leur attribution à Dessau.

Les RGB sont des identifiants de couleurs, jamais des identifiants historiques. STATE_ANHALT est une région économique partagée, ID62. Aucun State_ID n’est inventé ni renuméroté.
