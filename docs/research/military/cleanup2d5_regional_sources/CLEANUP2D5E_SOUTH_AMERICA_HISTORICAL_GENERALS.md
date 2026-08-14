# CLEANUP-2D-5E — HISTORICAL GENERALS 1776 — SOUTH AMERICA

**Projet :** *1776 – Age of Revolutions* (Victoria 3)  
**Dépôt :** `Malzars-sys/1776-Age-of-Revolutions`  
**Branche auditée :** `cleanup-post-release`  
**Date de référence immuable :** `1776-01-01`  
**Nature de la phase :** recherche historique uniquement — **aucune implémentation, aucun commit, aucun push**.

## 1. Conclusion exécutive

Le périmètre actuel contient **cinq formations terrestres sud-américaines**. L'audit conduit à trois remplacements historiques défendables et deux maintiens procéduraux.

| ID | Tag | Formation actuelle | Décision | Candidat | Classement |
|---|---|---|---|---|---|
| GEN1776-093 | BRZ | `Exrcito_Imperial_Brasileiro` | **IMPLEMENT_HISTORICAL** | João Henrique Böhm | `HIGHER_COMMAND_ABSTRACTION` |
| GEN1776-094 | SC4 | `Ejrcito_Argentino` | **KEEP_PROCEDURAL** | aucun commandant unique | `NO_DEFENSIBLE_MAPPING` |
| GEN1776-095 | SC2 | `Ejrcito_del_Ecuador` | **IMPLEMENT_HISTORICAL** | José Diguja | `COLONIAL_MILITARY_COMMAND` |
| GEN1776-096 | SC2 | `Ejrcito_de_la_Nueva_Granada` | **IMPLEMENT_HISTORICAL** | Manuel de Guirior | `HIGHER_COMMAND_ABSTRACTION` |
| GEN1776-097 | SC2 | `Ejrcito_de_Venezuela` | **KEEP_PROCEDURAL** | aucun commandant unique | `NO_DEFENSIBLE_MAPPING` |

Le critère déterminant n'est pas le futur État-nation, mais **la chaîne de commandement réellement existante au 1er janvier 1776**. Les noms de formations `Imperial Brasileiro`, `Argentino`, `Ecuador`, `Nueva Granada` et `Venezuela` sont donc traités comme abstractions de gameplay, et non comme preuve d'une armée nationale déjà constituée.

---

## 2. Périmètre exact du dépôt

Fichier de référence :

`common/history/military_formations/02_military_formations_south_america.txt`

Formations terrestres présentes :

1. **BRZ — `Exrcito_Imperial_Brasileiro`**, HQ `region_brazil`  
   États/unités codés : Rio de Janeiro et Paraíba.
2. **SC4 — `Ejrcito_Argentino`**, HQ `region_la_plata`  
   États/unités codés : Buenos Aires et Tucumán.
3. **SC2 — `Ejrcito_del_Ecuador`**, HQ `region_andes`  
   État codé : Ecuador.
4. **SC2 — `Ejrcito_de_la_Nueva_Granada`**, HQ `region_gran_colombia`  
   États codés : Cundinamarca, Cauca, Antioquia.
5. **SC2 — `Ejrcito_de_Venezuela`**, HQ `region_gran_colombia`  
   États codés : Zulia, Miranda, Bolívar.

Les recherches ciblées dans les fichiers de formations n'ont pas fait apparaître de formation terrestre initiale distincte pour `PEU` ou `CHL` dans ce périmètre actuel.

### Réemploi interne

Le dépôt contient :

- `common/character_templates/historical_commanders_americas.txt`, mais les profils sud-américains identifiés sont essentiellement du XIXe siècle (Caxias, Tamandaré, Grau, etc.) et ne sont pas admissibles en 1776 ;
- des rulers coloniaux issus de CLEANUP-2C-1 pour certains tags (`BRZ`, `SC2`, `SC4`), mais **un ruler n'est pas automatiquement un commandant** et aucun DNA/template de commandant correspondant à Böhm, Diguja, Guirior, Vértiz ou Agüero n'a été identifié.

---

## 3. Méthode de classement

- `FORMATION_COMMAND` : commandant documenté de la formation elle-même ou d'un corps correspondant presque exactement.
- `THEATRE_COMMAND` : commandant d'un théâtre opérationnel correspondant à la formation.
- `COLONIAL_MILITARY_COMMAND` : autorité coloniale possédant un commandement terrestre militaire explicite et documenté.
- `HIGHER_COMMAND_ABSTRACTION` : autorité supérieure réelle sur les forces terrestres, utilisable pour représenter une formation de gameplay plus large que l'organisation historique.
- `NO_DEFENSIBLE_MAPPING` : aucune personne unique ne couvre honnêtement la géographie et la chaîne de commandement de la formation au `1776-01-01`.

Un gouverneur, président d'audience ou vice-roi n'est retenu **que si une fonction militaire indépendante est documentée**.

---

## 4. GEN1776-093 — BRZ — `Exrcito_Imperial_Brasileiro`

### Décision

**IMPLEMENT_HISTORICAL — João Henrique Böhm**  
Classification : **`HIGHER_COMMAND_ABSTRACTION`**  
Confiance : **haute**.

### Identité

- **Nom historique :** Johann Heinrich Böhm ; en service portugais : **João Henrique Böhm**.
- **Naissance :** année **1708** certaine ; la *Deutsche Biographie* donne un **baptême le 20 juin 1708 à Brême**. Il ne faut donc pas transformer automatiquement le 20 juin en jour de naissance.
- **birth_date_precision :** `YEAR`.
- **Lieu :** Brême.
- **Polité :** Ville libre impériale de Brême, Saint-Empire.
- **State V3 proposé :** `STATE_ELBE`.
- **Décès :** **22 décembre 1783**, Rio de Janeiro, selon Oberacker et les traditions documentaires citées dans son étude.
- **Religion au 1776-01-01 :** réformée/protestante. Conversion au catholicisme seulement en 1782.
- **Culture V3 proposée :** `north_german`.

### Grade et commandement au 1776-01-01

La biographie allemande documente qu'en 1767 Böhm fut promu **Generalleutnant / tenente-general** et envoyé au Brésil comme **inspecteur général de toutes les troupes**, subordonné uniquement au vice-roi. La lettre royale du 22 juin 1767, citée dans l'historiographie militaire, lui confiait le gouvernement et commandement des troupes d'infanterie, cavalerie et artillerie « en qualquer parte do Brasil ».

En **décembre 1774**, il prit en plus le commandement en chef de l'**armée portugaise du Sud**. Les pièces du Conselho Ultramarino de novembre-décembre 1775 l'appellent explicitement :

- « general em chefe do exército do Sul » ;
- « tenente-general João Henrique Bohm » ;
- et une pièce précise qu'il répond au gouverneur espagnol Vértiz **bien qu'il ne soit pas lui-même gouverneur**.

C'est une preuve particulièrement forte au regard du critère de cette phase : Böhm est un **commandant militaire autonome**, pas un gouverneur transformé artificiellement en général.

### Théâtre

- haut commandement des troupes du Brésil portugais depuis 1767 ;
- théâtre opérationnel principal en 1776 : Rio Grande de São Pedro et frontière méridionale ;
- préparation de la reconquête des positions espagnoles, avec opérations en 1775-1776.

### Profil politique/social

Officier professionnel germano-brêmois, passé par les armées prussiennes/schaumbourgeoises puis portugaises, réformateur militaire associé au système du comte de Lippe.  
Mapping IG : **Armed Forces** fortement défendable.  
Idéologie : loyalisme monarchique/ordre militaire possible comme abstraction, mais éviter de lui attribuer une idéologie politique moderne non sourcée.

### Portrait et DNA

- **Portrait contemporain vérifié : non trouvé dans la recherche présente.**
- **DNA/template 1776 existant : aucun identifié.**

### Pourquoi ce mapping est acceptable malgré le nom anachronique de la formation

`Exrcito_Imperial_Brasileiro` ne doit pas être lu comme une armée impériale brésilienne indépendante en 1776. Böhm est retenu comme **haut commandant réel des forces terrestres de l'Amérique portugaise**, ce qui correspond mieux à l'abstraction actuelle que tout futur général brésilien du XIXe siècle.

### Sources majeures

1. Fundação Biblioteca Nacional / Projeto Resgate, Conselho Ultramarino, AHU-Rio Grande do Sul, documents de novembre-décembre 1775 :  
   https://www.gov.br/bn/pt-br/central-de-conteudos/projeto-resgate/catalogos-tematicos/caminhos/brasil-limites
2. Deutsche Biographie, « Böhm, Johann Heinrich » :  
   https://www.deutsche-biographie.de/sfz4986.html
3. Carlos H. Oberacker Junior, « João Henrique Böhm, o fundador do exército brasileiro », *Revista de História* (USP), vol. 18, n° 38 (1959), p. 339-358 :  
   https://revistas.usp.br/revhistoria/article/view/107500

---

## 5. GEN1776-094 — SC4 — `Ejrcito_Argentino`

### Décision

**KEEP_PROCEDURAL**  
Classification : **`NO_DEFENSIBLE_MAPPING`**  
Confiance : **haute**.

### Pourquoi aucun commandant unique n'est acceptable

La formation actuelle combine **Buenos Aires** et **Tucumán**. Au 1er janvier 1776, ces espaces ne constituent pas encore une « armée argentine » unifiée.

#### Candidat très fort pour Buenos Aires : Juan José de Vértiz y Salcedo

- **Naissance :** 4 juillet 1719, Mérida, Yucatán, selon J. Ignacio Rubio Mañé, directeur de l'Archivo General de la Nación du Mexique.
- **Polité de naissance :** province/capitainerie du Yucatán, vice-royauté de Nouvelle-Espagne, monarchie espagnole.
- **State V3 proposé :** `STATE_YUCATAN`.
- **Grade :** mariscal de campo.
- **Fonction militaire documentée :** un bando du 20 septembre 1770 le qualifie d'**« Inspector General de todas las Tropas Veteranas y de Milicias de esta Provincia del Rio de la Plata »**, en plus de gouverneur et capitaine général.
- **Culture :** espagnole / créole de Nouvelle-Espagne.
- **Religion :** catholique.
- **Profil :** officier de carrière et administrateur bourbonien, chevalier de Calatrava.
- **Décès :** 1798 ; une étude de Buenos Aires fondée sur la *Gazeta de Madrid* donne le 30 juillet 1798. PARES possède toutefois une notice d'autorité discordante (naissance 2 février 1719, décès 1799). Pour l'implémentation, préférer la biographie de Rubio Mañé pour la naissance et conserver la divergence PARES dans le dossier de sources.

Vértiz est donc un **excellent candidat pour Buenos Aires/Río de la Plata**.

#### Mais Tucumán a sa propre chaîne de commandement

Après la mort de Jerónimo Matorras, **Francisco Gabino Arias** exerce comme gouverneur intérimaire du Tucumán à partir du **16 novembre 1775**, avec un parcours de colonel de milices et d'officier de frontière. Cela suffit à invalider l'idée qu'au `1776-01-01` Vértiz commanderait naturellement toute la géographie codée par la formation actuelle.

### Conclusion

Utiliser Vértiz pour `Ejrcito_Argentino` fusionnerait artificiellement deux juridictions que le jeu a regroupées pour ses besoins. **Le maintien procédural est historiquement plus honnête.**

### Sources majeures

1. J. Ignacio Rubio Mañé, *Boletín del Archivo General de la Nación* (Mexique), « Noticias para la biografía... Juan José de Vértiz y Salcedo (1719-1798) » :  
   https://bagn.archivos.gob.mx/index.php/legajos/article/view/1597
2. Transcription du bando du 20 septembre 1770, *Documentos para la historia del Virreinato del Río de la Plata* :  
   https://es.wikisource.org/wiki/Bando_del_Gobernador_Don_Juan_Jos%C3%A9_V%C3%A9rtiz_reglamentando_con_penalidades%3A_el_uso_de_armas%2C_tr%C3%A1nsito_a_caballo_por_la_ciudad%2C_alumbrado%2C_juego%2C_bailes%2C_panader%C3%ADas%2C_tr%C3%A1fico_por_las_calles%2C_etc.%2C_etc.
3. Archivo Histórico de la Provincia de Tucumán, collections coloniales :  
   https://archivoh-beta.tucuman.gov.ar/Pi/index/65
4. PARES, notice d'autorité Vértiz — utile surtout pour documenter la divergence biographique :  
   https://pares.mcu.es/ParesBusquedas20/catalogo/autoridad/118881

---

## 6. GEN1776-095 — SC2 — `Ejrcito_del_Ecuador`

### Décision

**IMPLEMENT_HISTORICAL — José Diguja**  
Classification : **`COLONIAL_MILITARY_COMMAND`**  
Confiance : **haute pour le commandement ; faible à moyenne pour certaines données biographiques**.

### Identité

- **Nom :** José Diguja.
- **Naissance :** date exacte non établie dans les sources fiables consultées.
- **birth_date_precision :** `UNKNOWN`.
- **Indication seulement :** González Suárez écrit qu'en 1778 Diguja avait soixante ans, donc environ 1718. **Ne pas convertir cette estimation en faux jour/mois.**
- **Lieu :** Benavente, Castille la Vieille.
- **Polité :** Couronne de Castille / monarchie espagnole.
- **State V3 proposé :** `STATE_LEON`.
- **Décès :** bibliographie discordante ; une tradition fondée sur Fernández Duro donne **1786** à Ciudad Rodrigo. À revalider avant de graver une date gameplay exacte.
- **Culture :** espagnole/castillane.
- **Religion :** catholique.

### Grade et fonction

González Suárez le décrit comme :

- **Brigadier de los Reales Ejércitos** ;
- **Teniente Coronel de la Real Armada** ;
- ingénieur ;
- militaire ayant rempli plusieurs commissions en Amérique.

Il arrive à Quito le **8 juillet 1767** et prend le pouvoir ce jour-là. Un document de 1767 le qualifie également de **Coronel de los Reales Ejércitos y Presidente**.

Le point décisif pour cette phase est qu'il ne s'agit pas seulement d'un président civil. Les sources le décrivent comme **militaire de carrière et commandant général** de Quito. De plus, le dossier AHN/PARES `ESTADO,3410,Exp.9`, daté de 1772 à 1777, conserve sa correspondance au roi au sujet de l'établissement portugais sur le **Marañón**, preuve d'une responsabilité effective de défense de frontière pendant la date de référence.

### Théâtre

Audience/Présidence de Quito et frontière amazonienne orientale.

### Profil

Officier de carrière, ingénieur, administrateur colonial réputé discipliné.  
IG : **Armed Forces** défendable.  
Éviter toute idéologie « équatorienne » ou indépendantiste anachronique.

### Portrait et DNA

- portrait contemporain vérifié : **non trouvé** ;
- DNA/template dans le dépôt : **aucun identifié**.

### Sources majeures

1. Federico González Suárez, *Historia general de la República del Ecuador*, t. V, Biblioteca Virtual Miguel de Cervantes :  
   https://www.cervantesvirtual.com/obra-visor/historia-general-de-la-republica-del-ecuador-tomo-quinto--0/html/0016c7de-82b2-11df-acc7-002185ce6064_22.html  
   https://www.cervantesvirtual.com/obra-visor/historia-general-de-la-republica-del-ecuador-tomo-quinto--0/html/0016c7de-82b2-11df-acc7-002185ce6064_23.html
2. Archivo Histórico Nacional / PARES : dossier `ESTADO,3410,Exp.9`, « Carta del presidente de Quito, José Diguja, al Rey sobre el establecimiento de los portugueses en el río Marañón », 1772-09-02 / 1777-06-08.
3. Biblioteca Virtual Miguel de Cervantes, transcription de 1767 : *Testimonio del seqüestro del Colegio Máximo de Quito*, qui le qualifie de « Coronel de los Reales Ejércitos y Presidente » :  
   https://www.cervantesvirtual.com/obra-visor/testimonio-del-sequestro-sic-del-colegio-maximo-de-quito-actuado-el-20-de-agosto-de-1767/html/

---

## 7. GEN1776-096 — SC2 — `Ejrcito_de_la_Nueva_Granada`

### Décision

**IMPLEMENT_HISTORICAL — Manuel de Guirior**  
Classification : **`HIGHER_COMMAND_ABSTRACTION`**  
Confiance : **haute pour le commandement**.

### Identité

- **Nom complet :** José Manuel de Guirior Portal de Huarte Herdozain y González de Sepúlveda.
- **Nom d'usage :** Manuel de Guirior.
- **Naissance :** Banco de la República : **23 mai 1708**, Aoiz (Navarre).
- **Attention :** d'autres biographies donnent **21 mars 1708**. Le record ruler `SC2` du dépôt contient `1708.3.23`, qui ne correspond à aucune des deux principales dates retrouvées. Cette date du dépôt doit être considérée **à vérifier**, pas comme source.
- **birth_date_precision :** `DAY_WITH_SOURCE_CONFLICT`.
- **Polité :** Royaume de Navarre, monarchie espagnole.
- **State V3 :** `STATE_NAVARRA`.
- **Décès :** 1788, Madrid (année sûre dans la source institutionnelle consultée).
- **Culture :** espagnole, origine navarraise.
- **Religion :** catholique ; chevalier de l'Ordre de Saint-Jean.

### Grade et fonction militaire

Banco de la República le donne comme **teniente general de la Real Armada**.

La question « vice-roi = général ? » est résolue par la description institutionnelle du **fonds Virreyes de l'Archivo General de la Nación de Colombia**. Les documents sont adressés au :

**« Virrey, Gobernador y Capitán General del Nuevo Reino de Granada »**.

L'AGN explique explicitement que, **comme Capitán General**, le vice-roi avait :

- la défense intérieure et extérieure du vice-royaume ;
- le commandement des **forces de mer et de terre** ;
- le mouvement et le soutien des troupes ;
- l'achat d'armes ;
- la construction des fortifications.

Il s'agit donc bien d'un **haut commandement militaire documenté**, pas d'une simple extrapolation depuis le titre civil de vice-roi.

### Présence au 1er janvier 1776

Guirior occupe le vice-royaume de 1773 à 1776. Son successeur Manuel Antonio Flórez arrive à Cartagena le **11 janvier 1776** et **assume le 10 février 1776**. Guirior est donc encore le titulaire légitime au `1776-01-01`.

### Théâtre

La géographie codée de la formation — Cundinamarca, Cauca, Antioquia — correspond bien mieux à ce haut commandement du Nouveau Royaume que dans les deux cas rejetés (Argentine/Venezuela).

### Profil

Noble navarrais, officier de marine de haut rang, administrateur bourbonien, loyaliste de la Couronne.  
IG : **Armed Forces** défendable.  
Idéologie : ne pas imposer un libéralisme ou nationalisme postérieur.

### Portrait et DNA

Un portrait formel de Guirior est reproduit dans les collections/portails historiques péruviens ; il constitue une **piste iconographique exploitable**, mais la datation et la provenance précise doivent être vérifiées avant création d'un asset.

Aucun DNA/template de commandant Guirior n'a été identifié dans le dépôt.

### Sources majeures

1. Archivo General de la Nación de Colombia, fonds **Virreyes**, description institutionnelle du rôle militaire de Capitán General :  
   https://tesorosdocumentales.archivogeneral.gov.co/collection/822424
2. Banco de la República, « Manuel Guirior » :  
   https://enciclopedia.banrepcultural.org/index.php/Manuel_Guirior
3. Banco de la República, « Virreyes de la Nueva Granada » :  
   https://www.banrepcultural.org/biblioteca-virtual/credencial-historia/numero-20/virreyes-de-la-nueva-granada

---

## 8. GEN1776-097 — SC2 — `Ejrcito_de_Venezuela`

### Décision

**KEEP_PROCEDURAL**  
Classification : **`NO_DEFENSIBLE_MAPPING`**  
Confiance : **très haute**.

### Problème structurel

La formation actuelle contient :

- `STATE_MIRANDA` — noyau de la province de Venezuela/Caracas ;
- `STATE_ZULIA` — Maracaibo ;
- `STATE_BOLIVAR` — Guayana.

Or ces provinces ne sont pas encore réunies sous un même commandement militaire au `1776-01-01`.

La Fundación Empresas Polar décrit la chronologie juridique :

- du **12 février 1742 au 8 septembre 1777**, le chef de Venezuela/Caracas est gouverneur et capitaine général de **sa province**, tandis que les autres provinces ont leurs propres gouverneurs/commandants ;
- le **8 septembre 1777**, une Real Cédula agrège les autres provinces à Caracas **en matière gubernative et militaire** ;
- seulement à partir de ce moment le capitaine général de Venezuela obtient juridiction militaire sur elles.

### Candidat partiel : José Carlos de Agüero

La Fundación Empresas Polar indique que **José Carlos de Agüero**, brigadier et chevalier de Santiago, prend ses fonctions de **gouverneur et capitaine général de la province de Venezuela** le **25 février 1772** et les conserve jusqu'au **17 juin 1777**.

Il est donc parfaitement valable pour **Caracas/Venezuela**, mais **pas** pour Maracaibo et Guayana au 1er janvier 1776.

L'existence d'un gouverneur propre à Maracaibo dans les années 1775 et la réorganisation militaire de 1777 confirment la séparation.

### Conclusion

Agüero ne doit pas être étendu artificiellement à toute la formation actuelle. Le maintien d'un général procédural est préférable à l'invention d'une Capitanía General de Venezuela unifiée un an et huit mois trop tôt.

### Sources majeures

1. Fundación Empresas Polar, « Capitanía general » :  
   https://bibliofep.fundacionempresaspolar.org/dhv/entradas/c/capitania-general/
2. Fundación Empresas Polar, « Caracas, provincia de » :  
   https://bibliofep.fundacionempresaspolar.org/dhv/entradas/c/caracas-provincia-de/
3. Fundación Empresas Polar, chronologie 1772, entrée de José Carlos de Agüero :  
   https://bibliofep.fundacionempresaspolar.org/_custom/static/cronologia_hv/zoom/s18/1772-1.html
4. Fundación Empresas Polar, « Venezuela, provincia de » :  
   https://bibliofep.fundacionempresaspolar.org/dhv/entradas/v/venezuela-provincia-de/

---

## 9. Contrôle des dates et conflits à conserver

### João Henrique Böhm

- **Ne pas encoder `1708.06.20` comme naissance certaine.**
- Source allemande : **baptisé** le 20 juin 1708.
- Année de naissance : 1708.
- Religion : réformée/protestante en 1776 ; catholique seulement après juillet 1782.

### Juan José de Vértiz y Salcedo

- AGN Mexique / Rubio Mañé : **4 juillet 1719**.
- PARES : notice d'autorité discordante **2 février 1719** et décès 1799.
- La notice PARES doit être signalée comme conflit et non utilisée pour écraser automatiquement l'étude biographique de l'AGN.

### José Diguja

- Aucun jour/mois de naissance démontré.
- « 60 ans en 1778 » = indice approximatif, **pas** une date à convertir.
- Année de décès également à revalider si une date gameplay exacte devient nécessaire.

### Manuel de Guirior

- Banco de la República : **23 mai 1708**.
- Autres biographies : **21 mars 1708**.
- Dépôt actuel : `1708.3.23`.
- Il existe donc un conflit réel ; ne pas considérer la date du dépôt comme une preuve.

---

## 10. Portraits et réemploi graphique

| Candidat | Portrait vérifié dans cette passe | DNA/template commandant existant |
|---|---|---|
| João Henrique Böhm | Non | Non |
| Juan José de Vértiz | Piste iconographique trouvée, provenance à sécuriser | Non |
| José Diguja | Non | Non |
| Manuel de Guirior | Oui, portrait formel reproduit par des institutions historiques ; datation/provenance à sécuriser | Non |
| José Carlos de Agüero | Non | Non |

Le fichier `common/character_templates/historical_commanders_americas.txt` contient bien plusieurs profils historiques sud-américains, mais ils sont postérieurs à la date de départ et ne doivent pas être recyclés pour 1776.

---

## 11. Décisions finales à transmettre à la future phase d'implémentation

**GEN1776-093 — BRZ**  
`IMPLEMENT_HISTORICAL` → João Henrique Böhm  
`HIGHER_COMMAND_ABSTRACTION`

**GEN1776-094 — SC4**  
`KEEP_PROCEDURAL`  
`NO_DEFENSIBLE_MAPPING`  
Raison : Buenos Aires (Vértiz) + Tucumán (Arias) = deux commandements distincts.

**GEN1776-095 — SC2 / Ecuador**  
`IMPLEMENT_HISTORICAL` → José Diguja  
`COLONIAL_MILITARY_COMMAND`

**GEN1776-096 — SC2 / Nueva Granada**  
`IMPLEMENT_HISTORICAL` → Manuel de Guirior  
`HIGHER_COMMAND_ABSTRACTION`

**GEN1776-097 — SC2 / Venezuela**  
`KEEP_PROCEDURAL`  
`NO_DEFENSIBLE_MAPPING`  
Raison : Caracas, Maracaibo et Guayana ne sont unifiées militairement qu'à partir du 8 septembre 1777.

---

## 12. Limites de la recherche

1. Cette passe n'a pas inventé de dates manquantes : les baptêmes, âges approximatifs et dates contradictoires sont signalés comme tels.
2. Les `State V3` de naissance sont des **correspondances géographiques proposées**, à vérifier contre les IDs exacts de la version de Victoria 3 utilisée lors de l'implémentation.
3. Le portrait de Guirior doit faire l'objet d'une vérification de provenance/licence avant intégration graphique.
4. Les cas Vértiz et Agüero sont volontairement **non implémentables sur les formations actuelles** malgré la qualité de leur profil militaire, car la géographie des formations excède leur juridiction au 1er janvier 1776.
5. Aucun fichier gameplay du dépôt n'a été modifié pendant cette phase.
