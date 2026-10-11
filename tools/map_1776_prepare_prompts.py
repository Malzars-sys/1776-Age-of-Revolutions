"""Generate nine bounded research briefs from the audited allocation CSV."""
import csv
from collections import defaultdict
from pathlib import Path
from map_1776_audit import REGIONS

OUT=Path(__file__).resolve().parents[1]/'docs/reports/map'
CUSTOM=[
('Europe occidentale',
 'Îles Britanniques et Irlande, France, Pays-Bas historiques, péninsule Ibérique, Italie et îles attribuées dans le périmètre ci-dessous; aucune colonie extra-européenne par sa seule métropole.',
 'Luxembourg/Wallonie xD001A0 : identifier souveraineté et administration au 1er janvier; ne pas assimiler une province du jeu à un duché sans mapping. Lombardie : x867A90 est doublonnée AUS/VEN dans le candidat non intégré, x9AC196 y change de propriétaire. Auditer Venise et Gênes, leurs enclaves, les possessions et dépendances italiennes; préserver leurs historiques particuliers.',
 'Unions dynastiques, principautés, enclaves, juridictions et possessions discontinues. Distinguer souveraineté du souverain, administration provinciale et occupation. Cartes composites des Pays-Bas et frontières italiennes peuvent amalgamer plusieurs dates.',
 'Priorité : Luxembourg/Wallonie, Lombardie, frontière alpine avec R2, enclaves italiennes et autorités locales. Les retouches fiscales, industrielles et militaires existantes ne constituent pas une preuve territoriale.'),
('Europe septentrionale, centrale et orientale',
 'Scandinavie et Islande, territoires germaniques et suisses, Europe centrale/orientale, Balkans et Russie européenne; exclure les territoires extra-européens de ces souverains.',
 'Travaux déjà intégrés : Dobroudja, Suisse orientale, Bessarabie, Istrie et Tyrol du Sud. Le nouveau candidat contient des commandes Git parasites en Bessarabie; elles ne sont pas des données historiques. Hautes/Basses Silésies : plusieurs provinces sont attribuées dans le mauvais State_ID et certains propriétaires se superposent; examiner le registre des anomalies.',
 'Saint-Empire et juridictions imbriquées, unions personnelles, couronnes et sujets habsbourgeois, autonomie provinciale ottomane, rapports russes avec Crimée et Pologne-Lituanie. Ne pas projeter les réorganisations napoléoniennes ou les frontières de 1836.',
 'Priorité : Silésie, subdivisions impériales et enclaves, Istrie/Tyrol, Bessarabie/Dobroudja, Europe ottomane. Coordonne le Caucase et les marches des steppes avec R3, la limite de mission de Sibérie avec R5.'),
('Moyen-Orient, Afrique du Nord, Caucase et Asie centrale',
 'Anatolie, Levant, Égypte et Afrique septentrionale, Sahara selon la liste, péninsule Arabique, Perse, Caucase et Asie centrale; Afghanistan confié principalement à cette région, interface baloutche avec R4.',
 'Greater Caucasus a été réattribué CAUC→GEO dans les travaux antérieurs. L’Égypte a maintenant des couples EGY distincts du catalogue ancien. Les provinces métropolitaines britanniques ou russes ne relèvent pas de cette mission. Toutes les références de sujets doivent être comparées à l’autorité réellement attestée.',
 'Autorités provinciales ottomanes, beyliks, pouvoirs mamelouks, tribus et confédérations, fiscalité saharienne, khanats et rapports tributaires. Ne pas considérer une suzeraineté nominale, une caravane, un fort ou une revendication impériale comme administration uniforme. Contradictions probables entre atlas impériaux et études locales.',
 'Priorité : articulation Égypte/Porte, régences maghrébines, Caucase, khanats et steppes, autonomie d’Arabie, frontières afghanes. Coordonner Nil/Sahel avec R7 et Caucase/Balkans avec R2 sans reprendre leurs territoires.'),
('Asie du Sud',
 'Sous-continent indien, Pakistan/Baloutchistan selon la liste, Ceylan et interfaces himalayennes; les régions birmanes sont confiées à R6, Tibet principal à R5, Afghanistan principal à R3.',
 'De nombreux États sont partagés entre TAGs : ne pas fusionner BIC, souverainetés locales et autres compagnies. Les modifications antérieures de populations acceptées et propriété financière britannique ne prouvent pas un contrôle territorial historique.',
 'Compagnies à autorité fiscale ou militaire, souveraineté moghole nominale et administration effective, confédération marathe, principautés, pouvoirs sikhs et comptoirs côtiers. Délimiter comptoir, district fiscal, zone militaire et État autonome. Cartes rétrospectives du Raj sont insuffisantes.',
 'Priorité : possessions et revenus effectifs de BIC au 1er janvier, entités locales, enclaves européennes, frontières du Bengale, Punjab, Mysore, Sri Lanka et Himalaya. Séparer les transformations postérieures dans l’année 1776.'),
('Asie orientale',
 'Chine, Mongolie et Tibet selon la liste, Corée, Japon, Ryukyu et Sibérie/Extrême-Orient attribués ici; l’Indochine et le Siam sont confiés à R6, l’Alaska à R8.',
 'Gansu contient une attribution historique de xBD5671, classé comme lac dans default.map et hors de sa State Region. Les revendications russes et l’autorité des TAGs autochtones de Sibérie doivent être distinguées du mapping existant.',
 'Administration Qing et frontières à juridictions différentes, rapports tributaires coréens et ryukyuans, gouvernement shogunal/domaines, souverainetés aïnues, contrôle russe à implantation inégale. Ne pas confondre tribut, hommage, échanges et annexion. Comparer cartographie officielle et travaux locaux.',
 'Priorité : marches Qing/Tibet/Mongolie, côte mandchoue, Hokkaido/Sakhaline et populations locales, Sibérie. Coordonner Himalaya avec R4, Yunnan/Tonkin avec R6, steppes avec R3 et frontière de mission transouralienne avec R2.'),
('Asie du Sud-Est et Océanie',
 'Indochine et Siam, Birmanie, péninsule malaise, archipels indonésiens et philippins, Nouvelle-Guinée, Australasie et Pacifique, y compris Hawaii; chaque territoire exact est listé ci-dessous.',
 'Une province de STATE_WEST_MICRONESIA, xEF50C0, n’a pas de propriétaire écrit au départ. L’affectation à un chercheur n’est pas une proposition de propriétaire. L’ancienne région source classait à tort les États indochinois dans R5 et Hawaii dans R8.',
 'Mandala politique, tribut et autonomie locale, compagnies commerciales et ports, pouvoirs insulaires, souverainetés autochtones d’Australie et du Pacifique. Aucun remplissage colonial automatique des intérieurs ou des îles. Des frontières linéaires modernes peuvent être historiquement indéfendables.',
 'Priorité : autorité effective de DEI, districts côtiers et comptoirs, rapports politiques indochinois, Timor/Moluques/Philippines, absence ou faiblesse du contrôle européen en Océanie. Coordonner Birmanie avec R4, Tonkin avec R5.'),
('Afrique subsaharienne',
 'Afrique au sud des périmètres sahariens convenus, espaces sahéliens listés ici, Corne orientale attribuée, Madagascar, Cap-Vert et îles de l’océan Indien attribuées ici; aucun rattachement par métropole.',
 'La mission inclut des zones autrefois stockées dans 03_north_africa.txt : ce fichier n’est pas une frontière historique. Country_Type=decentralized décrit le moteur, pas l’absence de souveraineté. Vérifier la portée territoriale des compagnies et ports européens plutôt que recopier la couleur actuelle.',
 'Royaumes, cités, chefferies et confédérations, réseaux tributaires et mobiles, souverainetés pastorales, comptoirs, colonies permanentes limitées, juridictions portuaires. Attention aux projections coloniales du XIXe siècle et aux sources excluant les pouvoirs locaux.',
 'Priorité : contrôle côtier réel, États et autorités locales, Sahel/Nil, Corne, Cap, Madagascar et îles. Signaler les zones sans frontière linéaire défendable; coordonner Sahara/Nil avec R3 sans attribuer tous les espaces à une métropole.'),
('Amérique du Nord et Caraïbes',
 'Amérique du Nord, Groenland, Alaska, Mexique, Amérique centrale et Caraïbes; Hawaii relève de R6. Ne pas répartir les colonies britanniques, françaises, espagnoles ou danoises entre missions européennes.',
 'Nunavut a été regroupé sous HBC dans des travaux déjà intégrés. Des attributions contradictoires existent en Alaska, Nouveau-Mexique et ailleurs : voir le registre. x26A0BA au Yukon et x8D15CB en Ontario sont aussi répétés pour le même propriétaire, ce qui n’est pas le même type de conflit. Chiapas comporte un sélecteur de bâtiment UCA sans territoire initial correspondant.',
 'Colonies, rébellion et administrations britanniques, compagnies de commerce, forts et revendications à faible contrôle, souverainetés autochtones, alliances/confédérations, frontières espagnoles. Ne pas projeter l’indépendance de juillet 1776 sur le 1er janvier ni les futurs traités sur les souverainetés présentes.',
 'Priorité : colonies américaines au jour exact, Louisiane, frontières canadiennes/HBC, Alaska, Nord-Ouest et nations autochtones, Mexique et Caraïbes. Coordonner l’isthme avec R9; ne pas valider l’extension HBC par son seul TAG.'),
('Amérique du Sud',
 'Amérique du Sud et îles attribuées à ses State_IDs, Guyanes, bassins amazoniens, Andes, Brésil, cône Sud et Patagonie; l’Amérique centrale appartient à R8.',
 'STATE_PASTAZA référence un bâtiment region_state:SC2 sans territoire correspondant au départ. Les TAGs BRZ, SC2/SC3/SC4 et les autres noms du scénario ne sont pas une preuve d’indépendance historique : rechercher l’autorité et représenter séparément les dépendances.',
 'Administration ibérique, capitaineries et juridictions, missions, implantation fluviale, souverainetés autochtones, zones de revendication et traités contestés. Comparer frontières de droit, présence permanente et souveraineté locale; une carte coloniale peut représenter une prétention plutôt qu’un contrôle.',
 'Priorité : frontière luso-espagnole au 1er janvier, Guyanes, Amazonie, Andes et intérieur, Patagonie et contrôles locaux. Ne pas utiliser une division administrative créée plus tard en 1776 comme état initial; coordonner l’isthme avec R8.'),
]

def main():
    rows=list(csv.DictReader((OUT/'MAP_1776_9_REGIONS.csv').open(encoding='utf-8-sig')))
    issues=list(csv.DictReader((OUT/'MAP_1776_KNOWN_ISSUES.csv').open(encoding='utf-8-sig')))
    sections=['# MAP-0 — Neuf missions indépendantes prêtes à transmettre\n\nAucune mission n’a été lancée. Chaque bloc est autonome et doit être envoyé avec les quatre fichiers de référence cités. Les listes sont calculées depuis l’inventaire actuel, non depuis des frontières historiques supposées.\n']
    for reg,(title,scope,known,forms,priority) in zip(REGIONS,CUSTOM):
        rr=[r for r in rows if r['Region_ID']==reg]; grouped=defaultdict(list)
        for r in rr: grouped[r['State_ID']].append(r['Owner_TAG'])
        tags=sorted({r['Owner_TAG'] for r in rr})
        interfaces=sorted({r['Secondary_Region_ID'] for r in rr if r['Secondary_Region_ID']})
        im=[i for i in issues if any(s in grouped for s in i['State_ID'].split('|'))]
        issue_ids=' | '.join(i['Issue_ID'] for i in im) or 'Aucune anomalie statique enregistrée dans ce périmètre; cela ne prouve pas l’exactitude historique.'
        text=f'''Mission autonome : {reg} — {title}

Tu es responsable de la recherche territoriale au 1er janvier 1776 (1776-01-01) pour le mod Victoria 3 « 1776 Age of Revolutions ». Tu recherches, tu ne modifies ni fichiers historiques ni carte, et tu ne pousses aucun changement. Les valeurs initiales du mod et les noms de TAGs ne sont pas des conclusions historiques.

PIÈCES À RECEVOIR : MAP_1776_BASELINE.csv, MAP_1776_9_REGIONS.csv, MAP_1776_RESEARCH_SCHEMA.md, MAP_1776_KNOWN_ISSUES.csv. Utilise uniquement les lignes Region_ID={reg} comme périmètre principal. Les IDs RGB sont ceux du bitmap du jeu, pas des numéros arbitraires. Les lignes d’un même State_ID avec plusieurs Owner_TAG restent distinctes.

PÉRIMÈTRE : {scope}
L’inventaire comprend {len(rr)} couples pays/État et {len(grouped)} State_IDs distincts. TAGs existants à auditer dans ce seul périmètre : {', '.join(tags)}.
Interlocuteurs secondaires prévus : {', '.join(interfaces) or 'aucun prédéfini; signaler toute interface découverte'}. Une métropole qui possède ailleurs ne t’attribue pas ces territoires. Les mers et lacs sont une référence technique, pas des territoires politiques à attribuer à un pays.

PROBLÈMES DÉJÀ OBSERVÉS : {known}
Références du registre à lire : {issue_ids}
Un conflit de syntaxe ou de fichier n’est pas une preuve historique. Le candidat georg3mx n’est pas fusionné dans main; la baseline représente main actuel.

FORMES DE SOUVERAINETÉ ET DIFFICULTÉS : {forms}
PRIORITÉS : {priority}

Pour chaque territoire, distinguer administration directe, occupation militaire peu administrée, dépendance/vassalité, protectorat/tribut/influence, compagnie à autorité territoriale, autonomie/souveraineté autochtone, revendication seule, contrôle disputé ou fluctuant, et zone sans frontière précise défendable. Examiner présence administrative, fiscalité, juridiction, garnisons, fortifications, implantations permanentes, traités et structures politiques locales. Un comptoir n’équivaut pas à souveraineté sur toute une State Region. Dater séparément les changements survenus après le 1er janvier, même dans l’année 1776.

SOURCES : atlas historiques argumentés, travaux universitaires spécialisés, traités/documents administratifs contemporains, cartes d’époque avec date et biais, travaux sur les souverainetés locales et autochtones. Pour chaque correction importante, cite au moins une preuve précise. Fournis auteur, titre, date, URL ou référence bibliographique, pages/cartes pertinentes; une URL seule ou une carte moderne non justifiée ne suffit pas. Signale les contradictions et compare la nature des preuves; ne tranche pas silencieusement.

LIVRABLES : {reg}_RECOMMENDATIONS.csv conforme à toutes les colonnes et valeurs contrôlées du schéma joint; {reg}_SOURCES.csv; {reg}_UNCERTAINTIES.md; {reg}_COVERAGE.csv avec une ligne pour chaque couple listé, y compris REVIEWED_NO_CHANGE. Cartes annotées facultatives mais utiles. Chaque changement doit distinguer conclusion historique, correspondance géographique proposée, approximation de gameplay et incertitude non résolue.

Si tu ne peux pas faire correspondre une frontière aux provinces du jeu, laisse Province_ID/Province_IDs vides, utilise Mapping_Status=MAPPING_REQUIRED et décris précisément la zone (toponymes, coordonnées, limites, carte/page). N’invente aucun ID ni nouveau TAG. Préfère A_EXISTING_PROVINCES, puis B_STATE_REGIONS; ne demande C_GEOMETRY qu’avec preuve que les provinces existantes sont insuffisantes. Indique Requires_New_Tag et Requires_State_Split sans créer l’entité.

INCERTITUDES ET TRANSMISSION : attribue Change_ID stable, Source_IDs vérifiables et Confidence justifiée. Toute contradiction reste UNRESOLVED; renseigne Cross_Region_Conflict et Secondary_Region_ID, décris les sources opposées et transmets à la synthèse centrale. L’interlocuteur secondaire relit l’interface mais ne duplique pas ta recommandation. Une nouvelle zone extérieure au périmètre est signalée OUTSIDE_BASELINE pour attribution centrale, pas annexée à ta mission. VEN et GEN sont recherchés normalement mais leurs historiques particuliers de population/bâtiments sont protégés. Ne redistribue pas ces données. Aucun résultat n’est automatiquement intégré.

LISTE EXHAUSTIVE DES ÉTATS ET PROPRIÉTAIRES ACTUELS À AUDITER :
'''
        text+='\n'.join(f'{s} : {" | ".join(sorted(ts))}' for s,ts in sorted(grouped.items()))
        sections.append(f'\n## {reg}\n\n```text\n{text}\n```\n')
    (OUT/'MAP_1776_REGIONAL_PROMPTS.md').write_text('\n'.join(sections),encoding='utf-8')
    assert len(sections)==10
    print('PASS: nine autonomous briefs generated from actual territory allocation; no researchers launched.')

if __name__=='__main__': main()
