"""Persistent HRE closure tracking. Never writes game data or invokes installers.

check / observe are read-only; init creates guarded documentation once; render
updates derived reports only, never task statuses or human attestations.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
import copy,datetime,hashlib,json,sys
from serg_global_closure_audit import hashes,git,digest

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/map/SERG_CLOSURE'
AUDIT=ROOT/'docs/reports/map/SERG_GLOBAL_CLOSURE_AUDIT'
G=AUDIT.relative_to(ROOT).as_posix()
PREFIX='docs/reports/map/'
STAMP='2026-10-18'
STATUSES=['NOT_STARTED','IN_PROGRESS','RESEARCH_COMPLETE','IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION','PASS_RUNTIME_USER_VALIDATED','BLOCKED','DEFERRED_APPROVED','NOT_APPLICABLE_VERIFIED']
TERMINAL={'PASS_RUNTIME_USER_VALIDATED','DEFERRED_APPROVED','NOT_APPLICABLE_VERIFIED'}
PHASES=[
 (1,'Salzbourg et principautés ecclésiastiques alpines','P0/P1',['CL1 : juridictions alpines et périphéries R4'],['F01','F02','F03','F04','F05','H05']),
 (2,'Possessions impériales des Habsbourg','P0 couverture',['CL1 : territoires habsbourgeois et Teschen'],['H01','H02','H04','H05','H06','I01','I02']),
 (3,'Allemagne septentrionale et juridictions manquantes','P1 / couverture',['CL3; socles MAP2N/Q/R/T/U'],['A01','A02','A03','A04','A05','A06','A07','A08','G01','G02','G03','H03']),
 (4,'Italie impériale','P0 couverture',['CL2; le rang change, pas le contenu historique'],['J01','J02','J03','J04']),
 (5,'Corrections occidentales et centrales restantes','P1',['CL4 + CL5; Montbéliard/Oettingen de CL6'],['B01','B02','B03','B04','B05','B06','B07','B08','B09','C01','C02','C03','C04','C05','I03','E05']),
 (6,'Petites juridictions significatives et arbitrages','P1 restant',['CL6 hors Montbéliard/Oettingen; Goslar de CL3'],['D01','D02','D03','E01','E02','E03','E04','E05','A08']),
 (7,'Cohérence impériale et validation finale','P1 / clôture',['CL7; pas développement obligatoire de mécaniques futures'],['K01','K02']),
]

# task id, phase, title, weight, original coverage sector, receipt, installed lots.
# Repeated incremental Peene/Poel/Eutin passes are coalesced: no double credit.
LEGACY=[
 ('BASE-PASSAU',1,'Passau : noyau PAS inspecté',3,'F01',G+'/RUNTIME_USER_ATTESTATION.json',['MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU']),
 ('BASE-FREISING',1,'Freising : noyau FSI inspecté',2,'F02',G+'/RUNTIME_USER_ATTESTATION.json',['MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/R4B']),
 ('BASE-REGENSBURG',1,'Ratisbonne : ville RCI et noyaux RBI inspectés',3,'F03',G+'/RUNTIME_USER_ATTESTATION.json',['MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/R4C']),
 ('BASE-BELGIUM',2,'Belgique, Liège et Stavelot : noyaux inspectés',5,'I01',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION.json',['MAP2L/BELGIUM']),
 ('BASE-EUTIN',3,'Eutin–Schwartau : HLB et union OLD–HLB inspectés',3,'A02',PREFIX+'MAP2Q/R3/RUNTIME_USER_VALIDATION.json',['MAP2Q','MAP2Q/CONTINUATION_R2','MAP2Q/R3']),
 ('BASE-SWEDISH-MECKLENBURG',3,'Wismar–Poel–Neukloster inspectés',3,'A04',PREFIX+'MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json',['MAP2N','MAP2N/COMPLETION']),
 ('BASE-PEENE',3,'Poméranie suédoise, Peene et Wolgast inspectés',3,'A06',PREFIX+'MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json',['MAP2L/PRUSSIAN_BORDERS','MAP2M/R2','MAP2M/R3','MAP2M/R8','MAP2M/R9']),
 ('BASE-ANHALT',3,'Quatre noyaux d’Anhalt inspectés',3,'G01',PREFIX+'MAP2S/MAP2R_RUNTIME_USER_VALIDATION.json',['MAP2R']),
 ('BASE-SAXONY',3,'Saxe et duchés thuringiens MAP2T inspectés',4,'G02',PREFIX+'MAP2T/RUNTIME_USER_ATTESTATION_MAP2U.json',['MAP2T']),
 ('BASE-REUSS',3,'Compléments Reuss et Sondershausen MAP2U inspectés',2,'G03',PREFIX+'MAP2W/PREVIOUS_LOTS_RUNTIME_USER_ATTESTATION.json',['MAP2U']),
 ('BASE-RHINE-WESTPHALIA',5,'Münster/Paderborn/Juliers–Berg : noyaux inspectés',3,'B01',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION.json',['MAP2L/RHINE_WESTPHALIA']),
 ('BASE-OSNABRUCK',5,'Osnabrück/Niederstift/Lingen–Tecklenburg inspectés',3,'B02',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION_RHINE_SWABIA.json',['MAP2L/RHINE_WESTPHALIA_COMPLETION']),
 ('BASE-EMDEN',5,'Emden : approximation côtière PRU inspectée',2,'B08',PREFIX+'MAP2P/MAP2O_RUNTIME_USER_VALIDATION.json',['MAP2O']),
 ('BASE-RHINE-CENTRAL',5,'Neckar et noyaux du Rhin central inspectés',2,'C01',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION.json',['MAP2L/RHINE_CENTRAL']),
 ('BASE-NASSAU-FULDA',5,'Noyaux R2-B Hesse–Nassau–Fulda explicitement inspectés',4,'C04',G+'/RUNTIME_USER_ATTESTATION.json',['MAP2W/R2B']),
 ('BASE-FRANCONIA',6,'Franconie principale et continuation inspectées',6,'D01',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION.json',['MAP2L/FRANCONIA','MAP2L/FRANCONIA_CONTINUATION']),
 ('BASE-SWABIA',6,'Première Souabe : noyaux inspectés',3,'E01',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION_RHINE_SWABIA.json',['MAP2L/SWABIA']),
 ('BASE-SWABIA-FINISH',6,'Salem/Waldburg/Constance : finition inspectée',3,'E03',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION_SWABIA_FINISH.json',['MAP2L/SWABIA_FINISH']),
 ('BASE-SWABIA-CITIES',6,'Villes libres/Weingarten : dernières corrections inspectées',3,'E04',PREFIX+'MAP2L/RUNTIME_USER_VALIDATION_SWABIA_COMPLETION.json',['MAP2L/SWABIA_COMPLETION']),
]

# id | phase | weight | priority | sectors | issue IDs | kind | status | title | acceptance-specific
JOBS="""SC1-SALZBURG|1|6|P0|F05|R01|territorial|NOT_STARTED|Noyau fonctionnel du prince-archevêché de Salzbourg|Noyau B défendable, pays/capitale/gouvernement/titulaire/démographie cohérents; aucune annexion de toute Autriche ou Bavière; test indépendant.
SC1-TRENTO|1|3|P1|H05|R04|territorial|NOT_STARTED|Principauté épiscopale de Trente|Distinguer droits tyroliens et domaine épiscopal au 1 janvier; ne pas anticiper le changement de titulaire en cours de 1776.
SC1-BRIXEN|1|3|P1|H05|R04|territorial|NOT_STARTED|Principauté épiscopale de Brixen|Établir juridiction temporelle et dépendances, pas le diocèse ni tout SOUTH_TYROL.
SC1-BERCHTESGADEN|1|2|P1|F04|R05|territorial|NOT_STARTED|Prévôté princière de Berchtesgaden|Noyau temporel et population comparables; pas tout un RGB alpin attribué depuis une ville.
SC1-FREISING-OUTLIERS|1|3|P1|F02|R06|territorial|BLOCKED|Werdenfels, Burgrain et Ismaning hors noyau FSI|Nouvelles preuves permettant une approximation politique sans corridor traversant Munich; FSI 14 cellules protégé.
SC1-REGENSBURG-OUTLIERS|1|2|P1|F03|R06|territorial|BLOCKED|Hohenburg et périphéries épiscopales de Ratisbonne|Distinguer domaines médiats homonymes, protéger RBI/RCI; immunités intra-urbaines P2 séparées.
SC1-PASSAU-OUTLIERS|1|2|P1|F01|R06|territorial|NOT_STARTED|Possessions périphériques de Passau|Préserver PAS 40 cellules; établir limites de 1765 et possessions non cédées avant 1782, sans copier 1791.
SC1-REGENSBURG-DEMOGRAPHY|1|2|P1|F03|R07|territorial|NOT_STARTED|Population historique de la représentation de Ratisbonne|RCI 713 est technique; estimation au périmètre comparable, religion étayée; pas compensation mondiale ni population de convenance.
SC1-ORTENBURG|1|1|P1|F04|R05|territorial|NOT_STARTED|Arbitrage d’Ortenbourg|Confirmer souveraineté, noyau représentable et distinction des possessions médiates avant toute création.
SC2-BOHEMIA|2|6|P0|H01|R02|territorial|NOT_STARTED|Audit territorial de la Bohême|Audit daté suffisant des grands contours et juridictions; le TAG AUS et la bibliographie macro ne suffisent pas.
SC2-MORAVIA|2|3|P0|H02|R02|territorial|NOT_STARTED|Moravie hors réparations MAP2A|Conserver x71E080/xF0E080; contrôler les autres contours, pas refonte des réparations acquises.
SC2-AUSTRIAN-SILESIA|2|3|P0|H02|R02|territorial|NOT_STARTED|Silésie autrichienne et frontière impériale|Partition avant 1776; ne pas assimiler région économique à souveraineté; scopes MAP2A protégés.
SC2-AUSTRIA|2|5|P0|H04|R02|territorial|NOT_STARTED|Haute et Basse Autriche|Examen territorial indépendant des possessions intercalées et des limites extérieures à l’Empire.
SC2-INNER-AUSTRIA|2|4|P0|H04|R02|territorial|NOT_STARTED|Styrie, Carinthie et Carniole|Trois pays historiques distingués, interface Hongrie/Croatie documentée; pas Slovénie moderne rétroprojetée.
SC2-TYROL|2|3|P0|H05|R02|territorial|NOT_STARTED|Comté du Tyrol, hors nouvelles principautés de phase 1|Réconcilier domaines habsbourgeois/épiscopaux; ne pas refaire les noyaux validés.
SC2-ANTERIOR-AUSTRIA|2|3|P0|H06|R02|territorial|NOT_STARTED|Autriche antérieure et interface adriatique|Fribourg/Nellenburg/Landvogtei conservés; autres possessions impériales distinguées des territoires cédés et vénitiens.
SC2-TESCHEN|2|2|P1|H02|R24|territorial|NOT_STARTED|Teschen et registre x9061E0|179 cellules AUS en WEST_GALICIA hors registre; établir la portion impériale sans intégrer toute la Galicie.
SC2-MAP2A-VALIDATION|2|2|P1|H02;J01|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle des corrections MAP2A|Quatre RGB existants et dépendances inchangées; test scoped absent de l’audit; aucune nouvelle correction.
SC2-LUXEMBOURG-VALIDATION|2|1|P1|I02|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle Luxembourg sous BEO|Ancien LUX xD001A0, habitants/bâtiments/unités transférés; pas nouveau tracé luxembourgeois.
SC3-HOLSTEIN|3|4|P1|A01|R08|territorial|NOT_STARTED|Holstein royal, Schleswig et liens danois|Règlement de 1773, Eutin distinct, Holstein impérial/Schleswig extérieur; aucun regroupement automatique.
SC3-MECKLENBURG|3|3|P1|A05|R09|territorial|NOT_STARTED|Mecklembourg hors possessions suédoises|Contrôler Schwerin/Strelitz et limites; protéger Wismar/Poel/Neukloster.
SC3-BRUNSWICK-HARZ|3|5|P1|A08|R09|territorial|NOT_STARTED|Hanovre, Brunswick et Harz|Branches et juridictions indépendantes dont Quedlinburg à qualifier; préparer Goslar sans doubler la correction SC6-GOSLAR.
SC3-HILDESHEIM|3|3|P1|A08|R09|territorial|NOT_STARTED|Hochstift Hildesheim|Institution distincte avant 1802/1803, pas absorption HAN/BRA/PRU par défaut; noyau et administration cohérents.
SC3-BRANDENBURG|3|4|P1|A07|R11|territorial|NOT_STARTED|Brandebourg, Magdebourg et Halberstadt|Possessions impériales de PRU seulement; conserver Anhalt/T/U et économie existante.
SC3-SILESIA-LUSATIA|3|3|P1|H03|R11|territorial|NOT_STARTED|Silésie prussienne, Glatz et Lusaces|Partition 1742/1763, pas acquisitions 1815; diagnostics MAP1B ne sont pas limites certifiées.
SC3-SWEDISH-DEPENDENCIES|3|2|P1|A03|R10|territorial|NOT_STARTED|Arbitrage des dépendances LUB/MEC/MST|Choix de gameplay hérité distingué du droit historique; aucune suppression automatique des liens sans décision.
SC3-NORTHERN-JURISDICTIONS|3|2|P1|A03;A08|R09|territorial|NOT_STARTED|Villes hanséatiques et juridictions septentrionales restantes|Pays présents conservés, frontières et petites temporalités examinées; Goslar et Hildesheim réservés à leurs tâches.
SC4-EXISTING-ITALIAN-STATES|4|6|P0|J04|R03|territorial|NOT_STARTED|Statut impérial de MOD/PAR/TUS/LUC|Ces TAG existent; audit juridique et territorial réel, exclusions pontificales; aucune création depuis un inventaire incomplet.
SC4-SAVOY-NICE|4|3|P0|J03|R03|territorial|NOT_STARTED|Savoie et Nice|Droits et frontières de 1776 établis; pas île de Sardaigne impériale par simple appartenance SAR au bloc.
SC4-LIGURIAN-FIEFS|4|3|P0|J03|R03|territorial|NOT_STARTED|Gênes et fiefs ligures|GEN actif; statuts propres des fiefs et enclaves, pas impérialité automatique de toute la république.
SC4-PIOMBINO|4|3|P0|J04|R03|territorial|NOT_STARTED|Principauté de Piombino et île d’Elbe partagée|Réutiliser R1-0023; distinguer Portoferraio, Porto Longone et juridictions princières.
SC4-MASSA-CARRARA|4|3|P0|J04|R03|territorial|NOT_STARTED|Massa-Carrare|Réutiliser R1-0024/0025; arbitrer mariage dynastique vs institutions territoriales, sans fusion automatique MOD.
SC4-MILAN-OUTLIERS|4|2|P1|J01|R03|territorial|NOT_STARTED|Possessions habsbourgeoises italiennes hors liaison acquise|Conserver Crémonais 64 cellules et Trois Ligues SWI; contrôler autres limites datées, pas recul du correctif.
SC4-MILAN-VALIDATION|4|2|P1|J01|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle Milanais–Crémonais|Liaison AUS installée; pas reçu spécifique suffisant retrouvé; test indépendant.
SC4-PIEDMONT-VALIDATION|4|1|P1|J02|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle de l’inclusion piémontaise|Neuf RGB SAR inscrits, pas Sardaigne; ne pas rejouer le découpage pour obtenir un reçu.
SC5-PRUSSIAN-WEST|5|4|P1|B05|R14|territorial|NOT_STARTED|Gueldre, Clèves, Mark et Ravensberg|Partage de 1713 et limites importantes; Minden acquis conservé, pas acquisitions XIXe.
SC5-JEVER|5|2|P1|B09|R12|territorial|BLOCKED|Jever sous Anhalt-Zerbst|Titre AZR établi mais contour OLD candidat non résolu; noyau B justifié ou report autorisé, jamais tout OLD.
SC5-EAST-FRISIA-SOUTH|5|2|P1|B09|R13|territorial|BLOCKED|Leer et Rheiderland|319 cellules Emden PRU conservées; nouvelles preuves d’intersection, pas 1240 erreurs supposées.
SC5-WESTPHALIAN-ESTATES|5|4|P1|B06;B07|R15|territorial|NOT_STARTED|Dortmund et temporalités/comtés westphaliens|Gage de Bentheim, Corvey abbaye, Essen/Werden, Steinfurt/Rietberg; pas pays automatique pour chaque enclave.
SC5-HESSE-RHINE|5|4|P1|C05|R16|territorial|NOT_STARTED|Worms/Spire, Hombourg et Hanau|Villes, évêchés et apanages distingués; aucune principauté souveraine déduite d’un nom dynastique.
SC5-NASSAU-FULDA-OUTLIERS|5|2|P1|C04;C05|R16|territorial|NOT_STARTED|Franges de Nassau et Fulda|Noyaux R1/R2A/R2B protégés, pas Nassau unifié 1806 ni acquisitions tardives.
SC5-MONTBELIARD|5|2|P1|E05|R20|territorial|BLOCKED|Comté de Montbéliard|Quatre seigneuries françaises après 1748 distinguées; aucune rétroprojection du traité 1786.
SC5-OETTINGEN|5|2|P1|E05|R20|territorial|NOT_STARTED|Branches d’Oettingen|Titulaires et grandes possessions établis sans annexion des noyaux souabes voisins.
SC5-BELGIAN-FRINGES|5|2|P1|I03|R23|territorial|NOT_STARTED|Limbourg, Maastricht et franges belges|Condominiums et statuts distincts; BEO/LGE/STM déjà validés protégés.
SC5-ERFURT|5|3|P1|C03|R17|territorial|BLOCKED|Arbitrage Erfurt–Eichsfeld|Pas nouvelle optimisation sur mêmes points ni translation 7,20 px; preuves nouvelles ou report P1 explicitement approuvé.
SC5-MINDEN-VALIDATION|5|1|P1|B03|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle Minden|76 cellules PRU installées; ne pas étendre le reçu voisin; aucune reconstruction supplémentaire.
SC5-COLOGNE-VALIDATION|5|1|P1|B04|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle duché de Westphalie/Vest|84 cellules KCL et EDAB00–07 protégés; test du seul sous-lot.
SC5-MAINZ-VALIDATION|5|2|P1|C02|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle des trois couches Mayence|Rheingau/Spessart/Bergstraße/Tauber inspectés, Erfurt exclue.
SC6-HOHENLOHE|6|4|P1|D02|R18|territorial|BLOCKED|Branches significatives de Hohenlohe|Candidats R3 retirés, aucune réinstallation sur référentiel refusé; B politique étayé ou arbitrage autorisé.
SC6-CASTELL-WERTHEIM|6|3|P1|D02|R18|territorial|BLOCKED|Castell et Wertheim|Branches de 1776 et droits partagés; aucun titre ou acquisition de 1803/1813 rétroprojeté.
SC6-FRANCONIAN-CITIES|6|3|P1|D02|R19|territorial|BLOCKED|Rothenburg, Schweinfurt, Windsheim, Weißenburg|Noyaux politiques représentables ou report explicitement accepté; pas quatre cellules automatiquement autorisées.
SC6-GOSLAR|6|1|P1|A08|R09|territorial|NOT_STARTED|Ville impériale de Goslar|Ne pas lui attribuer le Rammelsberg brunswickois depuis 1552; coordination avec SC3-BRUNSWICK-HARZ.
SC6-SWABIAN-ARBITRATIONS|6|2|P1|D03;E05|R20;R27;R29|territorial|NOT_STARTED|Dernières juridictions significatives franconiennes/souabes|Noyaux déjà validés protégés; micro-enclaves P2 reportées sans devenir des frontières historiquement corrigées.
SC6-SWABIA-CONTINUATION-VALIDATION|6|1|P1|E02|R21|pending_runtime|IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION|Portée manuelle Fürstenberg/Ellwangen|Le reçu FINISH ne couvre pas automatiquement toute la continuation; contrôle borné sans reconstruire SFU/SEW.
SC7-MEMBERS-ELECTORS|7|3|P1|K01|R22|technical|NOT_STARTED|Membres, neuf électeurs, gouvernements et souverains|Listes et dignités cohérentes, droits territoriaux séparés du TAG; absence de correction nécessaire démontrée ou corrections validées.
SC7-REGISTRY|7|3|P1|K01;H02|R24|technical|NOT_STARTED|Registre territorial et périmètre impérial final|Chaîne approuvée, Teschen et exclusions vérifiés; pas SERG = possessions de toutes les dynasties.
SC7-INSTITUTIONS|7|4|P1|K01|R22|territorial|NOT_STARTED|Sujets, transitions, sécession et successions réellement utilisés|Taux 15/10, sortie impériale et scénarios actifs testés; prototype isolé non activé n’est pas automatiquement à développer.
SC7-DEMOGRAPHY-ECONOMY|7|3|P1|K01|R07;R34|technical|NOT_STARTED|Populations, bâtiments, PM, propriété et unités|Invariants ou changements historiques explicites tracés; pas obligation de conserver une population mondiale artificielle.
SC7-NONREGRESSION|7|3|P1|K01|R32;R33|technical|NOT_STARTED|Non-régression cartographique et dette technique|44 doublons/12 références hérités et vieux snapshots classés; aucun test bloquant inexpliqué.
SC7-P2-REGISTER|7|1|P1|K01;K02|R25;R26;R27;R28;R29;R30;R31;R32;R33;R34|documentation|NOT_STARTED|Registre final des B et P2 reportés|Décisions explicites et portée conservées; P2 ne bloque pas le cadastre, mais un crash réel n’est pas masqué.
SC7-P1-DECISIONS|7|2|P1|K01|R01;R02;R03|documentation|NOT_STARTED|Revue des P0/P1 et des secteurs obligatoires|Chaque P1 traité ou report non bloquant approuvé; aucun P0 ou grand secteur sans audit esquivé.
SC7-FINAL-APPROVAL|7|6|P1|K01|R21;R22|final_closure|NOT_STARTED|Validation finale en jeu et approbation de clôture|Nouvelle partie 1776, mois et contrôles adaptés, puis accord explicite du responsable pour SERG_TERRITORIAL_1_0_COMPLETE."""

def load_json(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def snapshot(name):
    if not re_safe(name):raise ValueError('Simple snapshot name required')
    path=OUT/'snapshots'/(name+'.json')
    if path.exists():raise ValueError('Never overwrite a snapshot')
    idx=ROOT/git('rev-parse','--git-path','index')
    obj=dict(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=git('rev-parse','HEAD'),branch=git('branch','--show-current'),index_sha256=digest(idx),runtime_hashes=hashes(),audit_hashes={p.relative_to(ROOT).as_posix():digest(p) for p in AUDIT.rglob('*') if p.is_file()},agents_text=(ROOT/'AGENTS.md').read_text(encoding='utf-8-sig'),status=git('status','--porcelain=v1','--untracked-files=all').splitlines())
    write_json(path,obj);print('Snapshot',path.relative_to(ROOT));return path
def re_safe(value):return value and all(c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in value)

def init():
    if (OUT/'ROADMAP_STATE.json').exists():raise ValueError('Roadmap exists: update it; never reinitialize')
    if not (OUT/'snapshots/INITIAL_WORKSPACE.json').exists():snapshot('INITIAL_WORKSPACE')
    regions={r['ID']:r for r in load_json(AUDIT/'REGIONAL_DATA.json')}
    issues={r['ID']:r for r in load_json(AUDIT/'ISSUE_DATA.json')}
    sources=[AUDIT/n for n in ['REPORT.md','CLOSURE_ROADMAP.md','CLOSURE_CRITERIA.md','REMAINING_WORK.csv','REGIONAL_COVERAGE.csv','IMPERIAL_STATES_INVENTORY.csv','TABLE_DATA.json','VALIDATION.json','REGISTRY_CHECKS.json','EFFECTIVE_GEOMETRY_CHECKS.json','SUPPLEMENTAL_CHECKS.json','RUNTIME_USER_ATTESTATION.json']]
    manifest={p.relative_to(ROOT).as_posix():digest(p) for p in sources}
    tasks=[]
    for id,phase,title,weight,sec,receipt,lots in LEGACY:
        region=regions[sec]
        tasks.append(dict(id=id,phase=phase,title=title,weight=weight,weight_basis='Socle de noyaux inspectés; pas complétude de la région entière',priority='P1',kind='legacy_core',status='PASS_RUNTIME_USER_VALIDATED',sectors=[sec],issues=[],historical_sources=[region['Preuve']],before=region['Problemes_ouverts'],expected='Conserver les seuls noyaux antérieurement inspectés, sans réouverture hors régression prouvée',depends_on=[],acceptance_profile='legacy_core',acceptance=['Portée limitée à celle du reçu; périphéries affectées à d’autres tâches'],implementation_report=[PREFIX+lot+'/REPORT.md' for lot in lots],installed_lots=lots,static_tests=dict(status='VERIFIED_AT_IMPORT',evidence=[G+'/VALIDATION.json',G+'/REGISTRY_CHECKS.json']),runtime_validation=dict(required=True,status='PASS_RUNTIME_USER_VALIDATED',attestation=receipt,scope=title,new_details_invented=False),decision=None,residual_uncertainty=region['Problemes_ouverts'],mandatory_1_0=True))
    pending_lots={
      'SC2-MAP2A-VALIDATION':['MAP2A'],'SC2-LUXEMBOURG-VALIDATION':['LUX_BEO_INTEGRATION_2026-10-10'],
      'SC4-MILAN-VALIDATION':['MAP2L/MILAN_CREMONESE'],'SC4-PIEDMONT-VALIDATION':['MAP2L/PIEDMONT'],
      'SC5-MINDEN-VALIDATION':['MAP2L/MINDEN_RAVENSBERG'],'SC5-COLOGNE-VALIDATION':['MAP2L/DUCHY_WESTPHALIA'],
      'SC5-MAINZ-VALIDATION':['MAP2L/MAINZ_PALATINATE','MAP2L/MAINZ_ESTATES','MAP2L/MAINZ_COMPLETION'],
      'SC6-SWABIA-CONTINUATION-VALIDATION':['MAP2L/SWABIA_CONTINUATION']}
    for line in JOBS.splitlines():
        id,phase,weight,prio,sectors,issueids,kind,status,title,accept=line.split('|')
        secs=sectors.split(';');iis=issueids.split(';')
        evidence=list(dict.fromkeys([issues[i]['Preuve'] for i in iis]+[regions[s]['Preuve'] for s in secs]))
        reports=[]
        for lot in pending_lots.get(id,[]):
            choices=[ROOT/PREFIX/lot/n for n in ('REPORT.md','MAP2A_EXECUTIVE_SUMMARY.md')]
            p=next((p for p in choices if p.exists()),None)
            if p:reports.append(p.relative_to(ROOT).as_posix())
        tasks.append(dict(id=id,phase=int(phase),title=title,weight=int(weight),weight_basis='Barème 1–6; enjeu/étendue du travail et dépendances, pas surface ni RGB',priority=prio,kind=kind,status=status,sectors=secs,issues=iis,historical_sources=evidence,before='; '.join(dict.fromkeys(regions[s]['Problemes_ouverts'] for s in secs)),expected=accept,depends_on=[],acceptance_profile='runtime_only' if kind=='pending_runtime' else 'no_functional_change' if kind in ('technical','documentation') else 'final_closure' if kind=='final_closure' else 'territorial',acceptance=[accept],implementation_report=reports,installed_lots=pending_lots.get(id,[]),static_tests=dict(status='VERIFIED_AT_IMPORT' if kind=='pending_runtime' else 'NOT_RUN',evidence=[G+'/VALIDATION.json'] if kind=='pending_runtime' else []),runtime_validation=dict(required=kind in ('territorial','pending_runtime','final_closure'),status='PENDING' if kind=='pending_runtime' else 'NOT_RUN',attestation=None,scope=None,new_details_invented=False),decision=None,residual_uncertainty='Ancien blocage conservé; aucune nouvelle recherche ou installation dans cette mission' if status=='BLOCKED' else 'Voir sources; pas de validation ni décision nouvelle présumée',mandatory_1_0=True))
    byid={t['id']:t for t in tasks}
    for id in ('SC1-TRENTO','SC1-BRIXEN','SC1-BERCHTESGADEN'):
        byid[id]['depends_on']=['SC1-SALZBURG']
    byid['SC2-TYROL']['depends_on']=['SC1-TRENTO','SC1-BRIXEN']
    byid['SC6-GOSLAR']['depends_on']=['SC3-BRUNSWICK-HARZ']
    final=byid['SC7-FINAL-APPROVAL']
    final['depends_on']=[t['id'] for t in tasks if t['id']!=final['id'] and t['mandatory_1_0']]
    for t in tasks:
        if t['kind']=='legacy_core':
            t['implementation_report']=[p if (ROOT/p).exists() else regions[t['sectors'][0]]['Preuve'].rsplit(':',1)[0] for p in t['implementation_report']]
    p2=[]
    for id,issue in issues.items():
        if issue['Priorite']!='P2':continue
        # Only two prior human decisions are already explicit, not a blanket waiver.
        approved=id in {'R25','R26'}
        p2.append(dict(id='P2-'+id,audit_issue=id,title=issue['Probleme'],status='DEFERRED_APPROVED' if approved else 'RESEARCH_COMPLETE',blocking_1_0=False,decision='Abstraction antérieure explicitement acceptée; pas correction historique exhaustive' if approved else 'Report non bloquant proposé; décision explicite à consigner',authority='Décision utilisateur antérieure documentée dans source' if approved else None,evidence=[issue['Preuve']],caveat='Reclasser P0/P1 si impact fonctionnel grave prouvé; ne pas masquer un crash'))
    state=dict(schema_version=1,scope_version='1.0.0',historical_date='1776-01-01',initialized_on=STAMP,canonical_roadmap='docs/reports/map/SERG_CLOSURE/ROADMAP.md',mission_status='SERG_CLOSURE_ROADMAP_INITIALIZED',territorial_status='INCOMPLETE',initialization=dict(territorial_changes=0,new_runtime_tests=0,previous_indicator=None),workspace_reference='docs/reports/map/SERG_CLOSURE/snapshots/INITIAL_WORKSPACE.json',source_manifest=manifest,allowed_statuses=STATUSES,terminal_statuses=sorted(TERMINAL),progress_model=dict(formula='100 * sum(weight of qualified terminal tasks) / sum(weight of all scoped tasks)',nonterminal_credit=0,weights_units='relative management points, not land area or historical coverage',rounding='2 decimals, ROUND_HALF_UP; no rounded 100 before closure gates',scope_manifest='docs/reports/map/SERG_CLOSURE/scopes/1.0.0.json'),acceptance_profiles={
      'legacy_core':['Correction présente vérifiée par audit actuel','Reçu humain déjà existant, limité aux noyaux inspectés','Aucune frontière périphérique ou durée de simulation ajoutée au reçu'],
      'territorial':['Souveraineté datée et correspondance politique défendable','Avant/après RGB, propriétaires, capitales et références documentés','Populations historiques au périmètre comparable; économie, propriété et unités cohérentes','Corrections justifiées installées, tests statiques et non-régression; sinon décision explicite sans changement','Nouvelle partie et mois pour tout nouveau correctif; validation indépendante'],
      'runtime_only':['Ne pas refaire l’installation','Contrôle statique de conservation au moment du test','Reçu humain spécifique au sous-lot réellement inspecté'],
      'no_functional_change':['Vérification documentaire/technique bornée, preuve explicite','Aucune correction nécessaire démontrée, ou changements suivis dans tâche territoriale distincte','NA ne signifie pas étape ignorée; validation technique adaptée, pas moteur inventé'],
      'final_closure':['Toutes les autres tâches obligatoires dans état terminal justifié','Aucun P0/P1 bloquant ni grand secteur non audité','Protocole final réel nouvelle partie 1776 et simulation, selon périmètre','Approbation explicite du responsable de projet, liée au test final et à cette version de périmètre']},
      phases=[dict(id=n,title=title,priority=prio,reconciles=old,sectors=secs) for n,title,prio,old,secs in PHASES],tasks=tasks,deferred_p2=p2,closure_approval=dict(approved=False,source=None,scope_version=None,approved_by=None),events=[])
    first=dict(id='SERG-RM-0001',date=STAMP,kind='INITIALIZATION',scope_version='1.0.0',source='C:/Users/simeo/.codex/attachments/57bd6f72-ff46-4aac-9ccc-df2a102fd7a7/Texte collé.txt',changes=[],initial_statuses={t['id']:t['status'] for t in tasks},note='Import des anciens noyaux acceptés; aucune nouvelle correction ou validation moteur; indicateur auparavant absent')
    state['events']=[first]
    scope=dict(version='1.0.0',previous_version=None,reason='Périmètre opérationnel initial demandé; consolidation audit CL1–CL7 en sept phases, pas couverture historique exhaustive',tasks=[{k:t[k] for k in ('id','phase','title','weight','priority','kind','mandatory_1_0')} for t in tasks],total_weight=sum(t['weight'] for t in tasks),initial_event_sha256=hashlib.sha256(json.dumps(first,sort_keys=True,ensure_ascii=False).encode()).hexdigest())
    write_json(OUT/'scopes/1.0.0.json',scope)
    write_json(OUT/'ROADMAP_STATE.json',state)
    write_json(OUT/'INITIAL_STATE.json',state)
    print('Initialized',len(tasks),'tasks; weight',scope['total_weight'])

def add_region_details():
    """One-time documentation enrichment; preserve the captured initial state."""
    path=OUT/'ROADMAP_STATE.json';state=load_json(path)
    if any(e['id']=='SERG-RM-0002' for e in state['events']):raise ValueError('Metadata already recorded')
    regions={r['ID']:r for r in load_json(AUDIT/'REGIONAL_DATA.json')}
    issues={r['ID']:r for r in load_json(AUDIT/'ISSUE_DATA.json')}
    for t in state['tasks']:
        t['historical_region']=[regions[s]['Secteur'] for s in t['sectors']]
        t['historical_perimeter']=[regions[s]['Perimetre_historique'] for s in t['sectors']]
        t['jurisdiction']=t['title']
        t['identified_problem']=[issues[i]['Probleme'] for i in t['issues']] or [t['before']]
    state['events'].append(dict(id='SERG-RM-0002',date=STAMP,kind='INITIALIZATION_DETAILS',scope_version=state['scope_version'],
      source=G+'/REGIONAL_DATA.json',changes=[],note='Régions, juridictions et problèmes nommés explicitement depuis l’audit; aucun changement de poids, statut, territoire ou reçu. Base inchangée : 60/235 = 25,53 %.'))
    write_json(path,state)

def file_ref(ref):
    """Repository evidence path with optional one-based line; no URL execution."""
    raw=str(ref or '')
    path,sep,last=raw.rpartition(':')
    if sep and last.isdigit():raw=path
    candidate=(ROOT/raw).resolve()
    if not candidate.is_relative_to(ROOT):raise ValueError('Evidence must stay in repository: '+raw)
    return candidate

def refs_exist(refs):
    try:return bool(refs) and all(file_ref(r).is_file() for r in refs)
    except (ValueError,TypeError):return False

def explicit_decision(t,field):
    d=t.get('decision') or {}
    return (d.get(field) is True and d.get('approved_by')=='user'
            and bool(d.get('reason')) and refs_exist(d.get('evidence')))

def terminal_evidence(t,state):
    """Mechanical evidence checks; historical truth still requires human review."""
    status=t['status']
    if status not in TERMINAL:return False
    if status=='DEFERRED_APPROVED':
        return (t['priority']!='P0' and t['kind']!='final_closure'
                and explicit_decision(t,'nonblocking_1_0') and bool(t['residual_uncertainty']))
    if status=='NOT_APPLICABLE_VERIFIED':
        return (t['kind'] not in ('pending_runtime','final_closure','legacy_core')
                and explicit_decision(t,'no_correction_required')
                and refs_exist(t['static_tests'].get('evidence')))
    rv=t['runtime_validation'];st=t['static_tests']
    if not refs_exist(t['implementation_report']) or not refs_exist(st.get('evidence')):return False
    if st['status'] not in ('VERIFIED_AT_IMPORT','PASS'):return False
    if rv.get('status')!='PASS_RUNTIME_USER_VALIDATED' or not refs_exist([rv.get('attestation')]):return False
    try:receipt=load_json(file_ref(rv['attestation']))
    except (ValueError,OSError):return False
    if receipt.get('status')!='PASS_RUNTIME_USER_VALIDATED' or receipt.get('automated_engine_test') is True:return False
    if receipt.get('scope_type')=='INSTALLED_SUB_LOTS_ONLY' or receipt.get('regional_closure_approved') is False:return False
    if t['kind']=='legacy_core':
        # Immutable import; no old receipt may be repurposed to bless a new scope.
        initial=load_json(OUT/'INITIAL_STATE.json')
        old=next((a for a in initial['tasks'] if a['id']==t['id']),None)
        manual=(receipt.get('automated_engine_test') is False or 'Manual validation declared by the player, not an automated engine test' in receipt.get('method',''))
        return bool(manual and old and all(t[k]==old[k] for k in ('title','installed_lots','runtime_validation','implementation_report','static_tests')))
    # New receipts explicitly enumerate covered stable tasks and actual protocol.
    if not (receipt.get('automated_engine_test') is False and t['id'] in receipt.get('task_ids',[]) and receipt.get('new_game_date')=='1776-01-01'
            and receipt.get('simulation_months',0)>=1 and receipt.get('source')):return False
    if st['status']!='PASS':return False
    try:static_reports=[load_json(file_ref(p)) for p in st['evidence']]
    except (ValueError,OSError):return False
    if not all(t['id'] in r.get('task_ids',[]) and r.get('total',0)>0
               and r.get('passed')==r.get('total') and not r.get('failed') for r in static_reports):return False
    if t['kind']=='final_closure':
        approval=state['closure_approval']
        return (approval.get('approved') is True and approval.get('approved_by')=='user'
                and approval.get('scope_version')==state['scope_version']
                and refs_exist([approval.get('source')]))
    return True

def partial_runtime_evidence(t):
    """A scoped receipt can validate installed corrections while the region stays blocked."""
    if t['status']!='BLOCKED' or t.get('installed_delivery_status')!='PASS_RUNTIME_USER_VALIDATED':return False
    rv=t.get('runtime_validation',{});lots=t.get('installed_sub_lots',[])
    if not lots or not all(l.get('status')=='PASS_RUNTIME_USER_VALIDATED' for l in lots):return False
    if rv.get('status')!='PASS_RUNTIME_USER_VALIDATED' or not refs_exist([rv.get('attestation')]):return False
    try:r=load_json(file_ref(rv['attestation']))
    except (ValueError,OSError):return False
    return bool(r.get('status')=='PASS_RUNTIME_USER_VALIDATED' and r.get('scope_type')=='INSTALLED_SUB_LOTS_ONLY'
        and r.get('regional_closure_approved') is False and r.get('points_awarded')==0
        and r.get('automated_engine_test') is False and t['id'] in r.get('task_ids',[])
        and sorted(r.get('sub_lot_ids',[]))==sorted(l['id'] for l in lots)
        and r.get('new_game_date')=='1776-01-01' and r.get('simulation_months',0)>=1
        and refs_exist([r.get('source')]) and bool(t.get('blocking_reason')))

def mixed_partial_runtime_evidence(t):
    """A historical tested version does not approve a subsequent technical revision."""
    if t['status']!='BLOCKED' or t.get('installed_delivery_status')!='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION':return False
    lots=t.get('installed_sub_lots',[])
    accepted=[l for l in lots if l.get('status')=='PASS_RUNTIME_USER_VALIDATED']
    pending=[l for l in lots if l.get('status')=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION']
    if not accepted or not pending or len(accepted)+len(pending)!=len(lots):return False
    historical=dict(t,installed_delivery_status='PASS_RUNTIME_USER_VALIDATED',installed_sub_lots=accepted,runtime_validation=t.get('historical_runtime_validation',{}))
    if not partial_runtime_evidence(historical):return False
    r=load_json(file_ref(historical['runtime_validation']['attestation']))
    version=r.get('validated_delivery_version');rv=t.get('runtime_validation',{})
    manifest=r.get('tested_delivery_manifest')
    return bool(version and version==t.get('historical_validated_delivery_version')
        and r.get('excludes_later_revisions') is True
        and sorted(r.get('excluded_revision_ids',[]))==sorted(l['id'] for l in pending)==sorted(rv.get('pending_revision_ids',[]))
        and refs_exist([manifest]) and digest(file_ref(manifest))==r.get('tested_delivery_manifest_sha256')
        and rv.get('attestation') is None
        and all(l.get('supersedes_sub_lot') in [a['id'] for a in accepted]
                and l.get('supersedes_delivery_version')==version and l.get('attestation') is None
                and refs_exist([l.get('protocol')]) for l in pending))


def qualifications(state):
    byid={t['id']:t for t in state['tasks']};done={}
    def visit(id,trail=()):
        if id in trail:raise ValueError('Dependency cycle: '+' -> '.join(trail+(id,)))
        if id not in byid:raise ValueError('Missing dependency '+id)
        if id not in done:
            t=byid[id]
            deps=[visit(d,trail+(id,)) for d in t['depends_on']]
            done[id]=terminal_evidence(t,state) and all(deps)
        return done[id]
    for id in byid:visit(id)
    return done

def progress(state):
    done=qualifications(state)
    total=sum(t['weight'] for t in state['tasks'])
    earned=sum(t['weight'] for t in state['tasks'] if done[t['id']])
    if total<=0:raise ValueError('Positive denominator required')
    percent=(Decimal(earned)*100/Decimal(total)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    closure=all(done.values()) and state['closure_approval'].get('approved') is True
    # Rounding guard only; the explicit final milestone normally prevents this case.
    if not closure and percent>=100:percent=Decimal('99.99')
    eligible=[t for t in state['tasks'] if not done[t['id']]
              and t['status'] in ('NOT_STARTED','IN_PROGRESS','RESEARCH_COMPLETE')
              and all(done[d] for d in t['depends_on'])]
    eligible.sort(key=lambda t:(int(t['priority'][1:]),t['phase'],t['status']!='IN_PROGRESS'))
    next_id=eligible[0]['id'] if eligible else None
    # A scoped installation may explicitly hand control back to the player.
    # Keep its runtime protocol as the next action without granting any credit
    # or automatically dispatching the next eligible geographical task.
    hold=state.get('runtime_validation_hold')
    if hold:
        held=next(t for t in state['tasks'] if t['id']==hold['task_id'])
        if held['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' or held.get('installed_delivery_status')=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION':next_id=held['id']
    return dict(scope_version=state['scope_version'],total_tasks=len(done),qualified_tasks=sum(done.values()),
                total_weight=total,earned_weight=earned,exact_fraction=str(Fraction(earned*100,total)),
                percent=str(percent),complete=closure,next_task=next_id,
                awaiting_runtime=[t['id'] for t in state['tasks'] if t['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'],
                blocked=[t['id'] for t in state['tasks'] if t['status']=='BLOCKED'],
                phases=[dict(id=p['id'],title=p['title'],tasks=sum(t['phase']==p['id'] for t in state['tasks']),
                             total_weight=sum(t['weight'] for t in state['tasks'] if t['phase']==p['id']),
                             earned_weight=sum(t['weight'] for t in state['tasks'] if t['phase']==p['id'] and done[t['id']])) for p in state['phases']])

def structural_errors(state):
    errors=[]
    def test(ok,message):
        if not ok:errors.append(message)
    ids=[t['id'] for t in state['tasks']]
    test(len(ids)==len(set(ids)),'Duplicate stable task IDs')
    test([p['id'] for p in state['phases']]==list(range(1,8)),'Seven ordered phases required')
    test(state['allowed_statuses']==STATUSES,'Status enumeration drift')
    manifest=file_ref(state['progress_model']['scope_manifest'])
    scope=load_json(manifest)
    test(scope['version']==state['scope_version'],'Scope manifest/version mismatch')
    keys=('id','phase','title','weight','priority','kind','mandatory_1_0')
    test(scope['tasks']==[{k:t[k] for k in keys} for t in state['tasks']], 'Scope changed without a new manifest/version')
    test(scope['total_weight']==sum(t['weight'] for t in state['tasks']),'Wrong denominator')
    initial=load_json(OUT/'INITIAL_STATE.json')
    test(set(ids)>=set(t['id'] for t in initial['tasks']),'Initial tasks must not disappear')
    test(state['events'][:len(initial['events'])]==initial['events'],'Initial history altered')
    first_digest=hashlib.sha256(json.dumps(initial['events'][0],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    original_scope=load_json(OUT/'scopes/1.0.0.json')
    test(original_scope['initial_event_sha256']==first_digest,'Initial scope event hash mismatch')
    test(original_scope['tasks']==[{k:t[k] for k in keys} for t in initial['tasks']], 'Initial scope manifest changed')
    replay=dict(initial['events'][0]['initial_statuses'])
    event_ids=[]
    for e in state['events']:
        event_ids.append(e['id'])
        for change in e.get('changes',[]):
            id=change['task_id']
            test(replay.get(id)==change['before'],'History before/status mismatch '+id)
            replay[id]=change['after']
    test(len(event_ids)==len(set(event_ids)),'Duplicate history events')
    test(replay=={t['id']:t['status'] for t in state['tasks']},'Status change without additive history')
    if state['scope_version']!='1.0.0':
        test(bool(scope.get('previous_version')) and bool(scope.get('reason')),'Scope revision needs predecessor/reason')
        test(any(e['kind']=='SCOPE_CHANGE' and e['scope_version']==state['scope_version']
                 and all(k in e for k in ('before_weight','after_weight','before_percent','after_percent','reason')) for e in state['events']),
             'Scope revision lacks explicit denominator/progress impact event')
    for t in state['tasks']:
        test(t['status'] in STATUSES,'Unknown status '+t['id'])
        test(type(t['weight']) is int and t['weight']>0,'Invalid weight '+t['id'])
        test(t['phase'] in range(1,8),'Invalid phase '+t['id'])
        test(t['priority'] in ('P0','P1','P2'),'Invalid priority '+t['id'])
        test(t['acceptance_profile'] in state['acceptance_profiles'],'Unknown acceptance profile '+t['id'])
        test(refs_exist(t['historical_sources']),'Missing historical evidence '+t['id'])
        if t['implementation_report']:test(refs_exist(t['implementation_report']),'Missing implementation report '+t['id'])
        for dep in t['depends_on']:test(dep in ids,'Unknown dependency '+dep)
        if t['status'] in TERMINAL:test(terminal_evidence(t,state),'Unjustified terminal status '+t['id'])
        if t.get('installed_delivery_status')=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' and t['status']=='BLOCKED':
            test(bool(t.get('blocking_reason')),'Missing regional block for partial installation '+t['id'])
            protocol=t.get('runtime_validation',{}).get('protocol')
            test(bool(protocol) and refs_exist([protocol]),'Missing partial runtime protocol '+t['id'])
            test(t.get('runtime_validation',{}).get('attestation') is None,'Unprocessed receipt on pending partial installation '+t['id'])
            test((all(lot.get('status')=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' for lot in t.get('installed_sub_lots',[])) and bool(t.get('installed_sub_lots'))) or mixed_partial_runtime_evidence(t),'Missing partial installation statuses '+t['id'])
        if t.get('installed_delivery_status')=='PASS_RUNTIME_USER_VALIDATED' and t['status']=='BLOCKED':
            test(partial_runtime_evidence(t),'Unjustified partial runtime receipt '+t['id'])
    issues=load_json(AUDIT/'ISSUE_DATA.json')
    mapped={i for t in state['tasks'] for i in t['issues']}|{d['audit_issue'] for d in state['deferred_p2']}
    test(mapped>={i['ID'] for i in issues},'Audit issue lost')
    test(len(state['deferred_p2'])==10,'P2 inventory lost')
    try:
        p=progress(state)
        test(not (state['territorial_status']=='SERG_TERRITORIAL_1_0_COMPLETE' and not p['complete']),'Premature territorial completion')
        test(all(qualifications(state)[t['id']] for t in state['tasks'] if t['status'] in TERMINAL),'Terminal task with unresolved dependency')
    except ValueError as e:errors.append(str(e))
    return errors

def observe(state):
    """Read-only comparison. A concurrent difference is reported, never reverted."""
    baseline=load_json(file_ref(state['workspace_reference']))
    current=hashes();old=baseline['runtime_hashes']
    idx=ROOT/git('rev-parse','--git-path','index')
    changed=[p for p in sorted(set(current)|set(old)) if current.get(p)!=old.get(p)]
    source_changes=[p for p,h in baseline['audit_hashes'].items() if not file_ref(p).is_file() or digest(file_ref(p))!=h]
    return dict(runtime_files=len(current),runtime_changed=changed,source_audit_changed=source_changes,
                head_unchanged=git('rev-parse','HEAD')==baseline['head'],branch_unchanged=git('branch','--show-current')==baseline['branch'],
                index_unchanged=digest(idx)==baseline['index_sha256'],
                agents_original_preserved=(ROOT/'AGENTS.md').read_text(encoding='utf-8-sig').startswith(baseline['agents_text']))

def link(ref,label=None):
    p=file_ref(ref);label=label or p.name
    return '['+label+'](<'+p.as_posix()+'>)'

def md(name,lines):
    (OUT/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')

def render():
    state=load_json(OUT/'ROADMAP_STATE.json')
    errors=structural_errors(state)
    if errors:raise ValueError('\n'.join(errors))
    p=progress(state);done=qualifications(state)
    initial_progress=progress(load_json(OUT/'INITIAL_STATE.json'))
    tasks=state['tasks'];byid={t['id']:t for t in tasks}
    regions={r['ID']:r for r in load_json(AUDIT/'REGIONAL_DATA.json')}
    issues=load_json(AUDIT/'ISSUE_DATA.json')
    header='**SERG TERRITORIAL 1.0 — PROGRESSION : '+p['percent'].replace('.',',')+' %**'
    common=[header,'','Périmètre `'+state['scope_version']+'` — référence historique : 1er janvier 1776. Indicateur de jalons acceptés, pas pourcentage de frontières exactes.','']
    lines=['# Feuille de route canonique — clôture territoriale du SERG','',*common,
      '## Protocole obligatoire de chaque passe SERG','',
      '1. Lire ce fichier, puis '+link(OUT/'ROADMAP_STATE.json')+', '+link(OUT/'NEXT_ACTION.md')+' et '+link(OUT/'BLOCKERS.md')+', puis les seuls rapports du sous-lot choisi.',
      '2. Vérifier branche/HEAD/index en lecture, état réel des fichiers, dernier sous-lot installé, reçu utilisateur et travaux concurrents. Si le suivi contredit le mod, documenter l’écart avant de corriger. Aucune restauration depuis une ancienne baseline.',
      '3. Choisir selon priorité P0/P1, dépendances, cohérence géographique, contrôle indépendant et risque de conflit. Ne pas refaire un noyau accepté hors régression démontrée; un blocage local ne gèle pas les autres régions.',
      '4. Dans une mission territoriale autorisée : réutiliser les sources, vérifier les attributions, installer seulement les corrections défendables, puis contrôles cumulatifs et protocole manuel borné. Pas de rapport de préparation indéfiniment répété.',
      '5. Mettre à jour l’état et les preuves, ajouter un événement à l’historique sans effacer les précédents, recalculer le pourcentage et régénérer les vues. Un test statique ne vaut jamais reçu humain.',
      '6. Le rapport final commence par la ligne de progression ci-dessus; préciser phase/sous-lot/statut, installé/validé, blocages, avant/après, prochaine action et test attendu. `READY_FOR_SCOPED_RUNTIME_VALIDATION` est le libellé de livraison; le statut structuré correspondant reste `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.','',
      'La mission d’initialisation (`SERG_CLOSURE_ROADMAP_INITIALIZED`) n’a installé aucun territoire. Lecture et génération ne lancent aucun chantier géographique. État courant de Salzbourg : `'+byid['SC1-SALZBURG']['status']+'`.','',
      '## Socle initial et calcul courant','',
      f"État courant : {p['qualified_tasks']} jalons justifiés; **{p['earned_weight']} / {p['total_weight']} points**, {p['total_tasks']} tâches définies dans une liste finie. {len(p['awaiting_runtime'])} tâches installées attendent un reçu spécifique.",
      '', f"À l’initialisation : {initial_progress['qualified_tasks']} noyaux/jalons antérieurs acceptés, {initial_progress['earned_weight']}/{initial_progress['total_weight']} points = {initial_progress['percent'].replace('.',',')} %. Indicateur auparavant absent; aucune nouvelle correction ni validation humaine pendant cette seule mission. L’historique conserve ensuite les évolutions.",
      '', '`progression = 100 × Σ poids des tâches terminales justifiées / Σ poids de toutes les tâches du périmètre`','',
      'Les statuts de recherche, blocage ou installation non testée apportent **zéro** point. Pondération fixe : 1 = contrôle borné/petite juridiction; 2 = correction locale ou arbitrage; 3 = principauté/ensemble local significatif; 4 = groupe de juridictions ou cohérence institutionnelle; 5 = grand ensemble régional; 6 = grand déficit de couverture ou approbation finale. Le champ `weight_basis` précise les socles consolidés. C’est un barème de gestion explicite, non une mesure du travail scientifique ou des habitants.',
      '', 'Les 19 socles sont crédités uniquement pour les noyaux installés et inspectés, avec rapprochement des rapports, reçus et contrôles de l’audit. Peene, Eutin et Poel ne sont pas crédités une fois par passe incrémentale; RBI et RCI constituent un seul socle Ratisbonne. Les franges et les corrections ultérieures restent des tâches distinctes. Le nombre de RGB du registre ne constitue pas le dénominateur.',
      '', 'Arrondi à deux décimales, demi vers le haut; un arrondi numérique ne peut afficher 100 avant les critères finaux. Le jalon final de six points est inaccessible sans reçu final, toutes les dépendances acceptées et approbation explicite de l’utilisateur sur ce périmètre. `SERG_TERRITORIAL_1_0_COMPLETE` est interdit avant cet accord.',
      '', '## Sept phases et rapprochement de l’ancien plan','',
      '| Phase | Tâches | Points acceptés / total | Origine audit |','| --- | ---: | ---: | --- |']
    for phase in state['phases']:
        metric=next(a for a in p['phases'] if a['id']==phase['id'])
        lines.append(f"| {phase['id']} — {phase['title']} | {metric['tasks']} | {metric['earned_weight']} / {metric['total_weight']} | {'; '.join(phase['reconciles'])} |")
    lines += ['', 'L’ordre demandé prévaut : l’ancien CL1 est scindé entre phases 1 et 2; CL2 devient phase 4; CL3 devient phase 3 (Goslar en 6); CL4/CL5 deviennent phase 5; Montbéliard/Oettingen de CL6 passent en 5, le reste en 6; CL7 devient 7. Le contenu de couverture n’est pas supprimé par ce réordonnancement.',
      '', '## Tâches et critères vérifiables','',
      'Chaque fiche complète est conservée dans '+link(OUT/'ROADMAP_STATE.json')+' : ID stable, région/secteurs historiques, juridiction, problème, priorité, sources avec lignes vérifiables, avant/résultat attendu, dépendances, profil et critères d’acceptation, rapports, contrôles, reçu et incertitudes. Les profils communs ci-dessous s’ajoutent au critère propre à chaque fiche.']
    for profile,criteria in state['acceptance_profiles'].items():
        lines += ['', '**'+profile+'** : '+'; '.join(criteria)+'.']
    for phase in state['phases']:
        lines += ['', '### Phase '+str(phase['id'])+' — '+phase['title'],'']
        for t in tasks:
            if t['phase']!=phase['id']:continue
            region='; '.join(regions[s]['Secteur'] for s in t['sectors'])
            lines += ['#### '+t['id']+' — '+t['title'],'',
                      f"{t['priority']} · poids {t['weight']} · `{t['status']}` · profil `{t['acceptance_profile']}`.",
                      '', 'Région/périmètre : '+region+'. Dépendances : '+(', '.join(t['depends_on']) if t['depends_on'] else 'aucune')+'.',
                      '', 'Acceptation : '+t['expected'],
                      '', 'Source de départ : '+link(t['historical_sources'][0],t['historical_sources'][0])+'. Rapports, autres sources et incertitudes : fiche JSON du même ID.','']
    lines += ['## Mises à jour additives et stabilité du périmètre','',
      'Ne jamais réinitialiser le suivi. Pour chaque passe : modifier les seules fiches concernées, conserver les reçus anciens, ajouter un événement daté et sourcé dans `events` (ID unique; `changes` avec `task_id`, `before`, `after`; résultats/progression avant-après). Les preuves de décision et les reçus nouveaux sont des fichiers distincts dans le rapport du sous-lot; aucun faux test moteur. Puis exécuter le validateur, régénérer les vues, vérifier le diff et ajouter le bilan à l’événement. Les vues sont dérivées de l’historique intégral, pas un journal libre effacé à chaque passe.',
      '', 'Nouvelle erreur P0/P1 : conserver l’ancienne tâche, ajouter ou étendre explicitement le périmètre avec justification. Versionner `scope_version`, créer un nouveau manifeste immuable `scopes/<version>.json` avec `previous_version`, ajouter un événement `SCOPE_CHANGE` contenant `before_weight`, `after_weight`, `before_percent`, `after_percent`, `reason`. L’ancien dénominateur et la baisse éventuelle restent visibles. Aucun retrait de tâche pour améliorer le score. Un cas P2 révélant un crash doit être reclassé.',
      '', 'Schéma de preuve des futurs états terminaux : un PASS a un rapport d’implémentation, un rapport statique JSON (`task_ids`, `passed = total > 0`, `failed` vide), et un reçu humain (`status`, `task_ids`, `source`, `new_game_date`, `simulation_months`, `automated_engine_test: false`). Les reçus hérités sont acceptés tels quels, sans leur inventer un mois de simulation. Un NA exige une décision sourcée (`no_correction_required: true`, `approved_by: user`, `reason`, `evidence`) et des contrôles adaptés. Un report P1 exige `nonblocking_1_0: true` et la même autorité; jamais un P0 ou une validation finale reporté. Ce garde-fou mécanique vérifie des pièces, pas leur vérité historique : lecture et responsabilité de l’agent restent indispensables.',
      '', '### Outils de lecture et vues','',
      '`python -B -X utf8 tools/serg_closure_roadmap.py check` : état, preuves, dépendances, périmètre, historique et vues; lecture seule.',
      '', '`python -B -X utf8 tools/serg_closure_roadmap.py observe` : changements depuis l’instantané initial; lecture seule. Une future correction autorisée changera normalement les empreintes; documenter ces différences, ne pas les restaurer.',
      '', '`python -B -X utf8 tools/serg_closure_roadmap.py render` : régénère uniquement ces rapports et `PROGRESS_SNAPSHOT.json`, sans changer état, reçus, historique ou fichiers du jeu. `init` refuse toute réinitialisation. Utiliser le Python disponible sans installer de dépendance.',
      '', '## Référence unique, protection et démarrage','',
      link(AUDIT/'CLOSURE_ROADMAP.md','Ancien CL1–CL7')+' reste une source historique figée de l’audit, pas une seconde feuille opérationnelle. Les CSV originaux, l’inventaire des 158 entrées et les critères sont reliés par les sources et empreintes de `source_manifest`; ils ne sont pas recopiés comme une nouvelle vérité territoriale.',
      '', 'Conserver noyaux validés de Franconie, Rhénanie, Souabe, territoires suédois, Anhalt, Thuringe/Reuss, Fulda/Nassau, Passau/Freising/Ratisbonne. Protéger le chantier américain, accords franco-américains, obligations, Minutemen, événements/unités, Saint-Gobain/Anzin et modifications françaises. Pas de Git en écriture ni de vanilla modifié dans cette mission.',
      '', 'Le renvoi court de `AGENTS.md` est limité aux futures passes SERG. La [documentation officielle des instructions de dépôt](https://learn.chatgpt.com/docs/agent-configuration/agents-md) décrit leur chargement au démarrage d’une session, selon leur portée et les éventuels overrides; ce n’est pas un hook d’exécution. Aucun nouveau lancement de session n’a été testé ici. Ligne de démarrage de secours à inclure dans tout nouveau prompt SERG :',
      '', '> Lis `docs/reports/map/SERG_CLOSURE/ROADMAP.md`, puis `ROADMAP_STATE.json`, `NEXT_ACTION.md` et `BLOCKERS.md`; vérifie le workspace et les anciennes passes avant de choisir le sous-lot autorisé; actualise le suivi et les preuves à la fin, sans refaire les noyaux validés.',
      '', 'Liens : '+ ' · '.join(link(OUT/n) for n in ('PROGRESS_HISTORY.md','CLOSURE_CHECKLIST.md','DEFERRED_P2.md','BLOCKERS.md','NEXT_ACTION.md','INITIAL_STATE.json'))+'.']
    campaign=state.get('closure_campaign',{})
    if campaign.get('status')=='ACTIVE':
        lines[6:6]=['## Priorité actuelle — campagne de levée des blocages','',
            'Création systématique de nouveaux territoires suspendue selon '+link(campaign['source'])+'. Auditer et clore les installations existantes avant toute nouvelle expansion. Aucun changement du périmètre, des 81 tâches ou des 235 points.',
            '', 'Audit des huit installations : '+link(campaign['installed_audit'])+'. Matrice des blocages : '+link(campaign['blocked_matrix'])+'. Tâche de clôture traitée : `'+campaign['selected_blocked_task']+'` ; décision proposée, aucune approbation présumée.','']
    resolution=campaign.get('luxembourg_resolution')
    map2a_reception=campaign.get('map2a_reception')
    grouped_reception=campaign.get('grouped_reception')
    if resolution:
        lines[6:6]=['## '+('Réception antérieure' if grouped_reception else 'Résolution actuelle')+' — Luxembourg administratif','',
            'Un niveau ordinaire BEO/Wallonie installé, trois niveaux flamands conservés ; contrat BUILD réconcilié. Rapport : '+link(resolution['report'])+'. Statut : `'+byid['SC2-LUXEMBOURG-VALIDATION']['status']+'`. '+('Reçu humain limité à cette tâche : '+link(resolution['attestation'])+'.' if resolution.get('attestation') else 'Aucun reçu humain ajouté.'),'',
            'Prochaine action limitée aux validations groupées : '+link(campaign['grouped_protocol'])+'. La matrice antérieure reste une archive ; aucun nouveau territoire autorisé.','']
    if map2a_reception:
        lines[6:6]=['## Réception '+('antérieure' if grouped_reception else 'actuelle')+' — MAP2A','',
            '`SC2-MAP2A-VALIDATION` : `'+byid['SC2-MAP2A-VALIDATION']['status']+'`. Reçu limité aux quatre corrections et à leurs dépendances inspectées : '+link(map2a_reception['attestation'])+'. Rapport : '+link(map2a_reception['report'])+'.','',
            'Luxembourg reste reçu. SC2-TESCHEN, TE-R-CORE, la mine de sel et les autres tâches ne sont pas validés par MAP2A. Seules les validations installées restantes sont proposées selon '+link(campaign['grouped_protocol'])+'. Aucun nouveau territoire commencé.','']
    if grouped_reception:
        lines[6:6]=['## Réception groupée — '+str(len(grouped_reception['task_ids']))+' tâches','',
            'Protocoles intégralement confirmés par le joueur, reçus distincts : '+', '.join('`'+id+'`' for id in grouped_reception['task_ids'])+'. Rapport : '+link(grouped_reception['report'])+'.','',
            'Les '+str(len(p['blocked']))+' tâches BLOCKED restent inchangées. TE-R-CORE et BG-E-SALT-NATIVE-R1 attendent leurs confirmations propres selon '+link(grouped_reception['protocol'])+'. Préparation des trois voies de clôture, sans nouveau chantier : '+link(grouped_reception['readiness'])+'.','']
    md('ROADMAP.md',lines)
    lines=['# Historique additif des décisions et validations','',*common,
      'Les anciens reçus ne sont pas remplacés. Leur import ne constitue ni un nouveau test du moteur ni une certification historique. Aucun indicateur antérieur comparable : avant = non défini; après initialisation = '+initial_progress['percent'].replace('.',',')+' % sur le périmètre initial. Avancement territorial produit par la mission d’initialisation : zéro.','']
    for e in state['events']:
        lines += ['## '+e['id']+' — '+e['date']+' — '+e['kind'],'',
                  'Périmètre : `'+e['scope_version']+'`. Source : '+e.get('source','non renseignée')+'.','',e.get('note',''),'']
        if 'before_percent' in e:lines += ['Progression : '+str(e['before_percent'])+' → '+str(e.get('after_percent','à vérifier'))+' %.','']
        if e.get('changes'):
            lines += ['',*['- '+c['task_id']+' : `'+str(c['before'])+'` → `'+c['after']+'`.' for c in e['changes']]]
        if e['kind']=='SCOPE_CHANGE':lines += ['', 'Impact du périmètre : '+str({k:e[k] for k in ('before_weight','after_weight','before_percent','after_percent','reason')})]
    lines += ['', '## Socle importé, sans duplication des passes incrémentales','']
    for t in tasks:
        if t['kind']=='legacy_core':lines.append('- '+t['id']+' : '+str(t['weight'])+' points; '+link(t['runtime_validation']['attestation'])+'; seuls noyaux du reçu.')
    lines += ['', 'Référence initiale immuable : '+link(OUT/'INITIAL_STATE.json')+'. Périmètre et poids : '+link(OUT/'scopes/1.0.0.json')+'. Les statuts suivants restent ouverts jusqu’à preuve nouvelle; un ancien test ne couvre pas une nouvelle extension.']
    md('PROGRESS_HISTORY.md',lines)
    nxt=byid.get(p['next_task'])
    lines=['# Prochaine intervention recommandée','',*common]
    if nxt:
        lines += ['## '+nxt['id']+' — '+nxt['title'],'',f"Phase {nxt['phase']} · {nxt['priority']} · `{nxt['status']}` · poids {nxt['weight']}.",
          '', 'La recommandation seule ne vaut pas autorisation d’installation. Respecter la mission active et vérifier les travaux concurrents. Pendant l’initialisation, aucun sous-lot territorial ne doit être lancé.',
          '', 'Objectif : '+nxt['expected'], '', 'Dépendances préalables : '+(', '.join(nxt['depends_on']) or 'aucune tâche bloquante; conserver les couches déjà installées')+'.',
          '', 'Sources de départ : '+', '.join(link(ref,ref) for ref in nxt['historical_sources'])+'. Profils et critères : fiche '+nxt['id']+' dans ROADMAP_STATE.json.',
          '', 'Attendu de la passe territoriale : noyau B représentable si défendable, liste avant/après des portions RGB/State_ID/propriétaires, population historique comparable, pays/capitale/gouvernement/titulaire cohérents, registre et dépendances, contrôles cumulatifs. Si aucune correction n’est nécessaire, le démontrer; si tâche documentaire/technique, appliquer son profil adapté.',
          '', 'Si preuves insuffisantes : décision précise, maintien du blocage, autre tâche prioritaire indépendante; pas recalage forcé ni rapport général supplémentaire. Aucun report de P0 pour atteindre un pourcentage.',
          '', 'Pour une nouvelle correction fonctionnelle : nouvelle partie 1776, contrôles du seul sous-lot puis un mois; résultat humain enregistré seulement après confirmation. La livraison statique demeure `READY_FOR_SCOPED_RUNTIME_VALIDATION`, état structuré `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.']
        if nxt['id']=='SC1-SALZBURG':
            lines += ['', 'Particularités de Salzbourg : réutiliser '+link(AUDIT/'HISTORICAL_GAPS.md')+' et '+link(ROOT/'docs/reports/map/MAP2W/R4/POLITICAL_REPRESENTATION','R4 — représentation politique')+'. Le Land contemporain n’est pas une frontière de 1776; distinguer domaine temporel, évêché et province technique. Vérifier/réserver le TAG et les RGB réellement disponibles, sans ID inventé dans cette feuille. Ne pas reprendre PAS/FSI/RBI/RCI ni attribuer toute l’Autriche/Bavière à Salzbourg.']
        hold=state.get('runtime_validation_hold')
        if hold and nxt['id']==hold['task_id'] and (nxt['status']=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION' or nxt.get('installed_delivery_status')=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION'):
            lines=['# Prochaine action — validation du sous-lot installé','',*common,
                '## '+nxt['id']+' — test joueur en attente','',
                '`READY_FOR_SCOPED_RUNTIME_VALIDATION` — état structuré `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Aucun point supplémentaire acquis avant reçu explicite.','',
                'Le sous-lot est installé. Protocole : '+link(hold['protocol'])+'.','',
                hold.get('test_summary','Nouvelle partie au 1er janvier 1776 : inspecter le pays SLZ, son noyau, Colloredo, le gouvernement, les 16 000 habitants, l’administration, les droits impériaux et les noyaux voisins; simuler un mois puis sauvegarder/recharger. Signaler les résultats et anomalies.'),'',
                'Aucun nouveau `PASS_RUNTIME_USER_VALIDATED` sans confirmation explicite du joueur couvrant ce sous-lot. Pas de reçu humain créé par l’agent.','',
                'Après réception : enregistrer le résultat réel, contrôler la conservation et recalculer. En cas d’échec, corriger le sous-lot concerné et retester.','',
                'Prochain candidat territorial préparé : `'+hold['next_implementation_candidate']+'` ('+byid[hold['next_implementation_candidate']]['priority']+', dépendances actuelles satisfaites). Il reste `NOT_STARTED`; aucune recherche ni installation de ce lot n’a commencé. Le choix sera revérifié lors d’une prochaine mission autorisée.','',
                hold.get('scope_note','Trente, Brixen et Berchtesgaden conservent leur dépendance à l’acceptation de Salzbourg. Les possessions salzbourgeoises périphériques et l’incertitude de représentation B restent documentées dans le rapport.')]
    review=state.get('decision_review_hold')
    if nxt and review and nxt['id']==review['task_id'] and nxt['status']=='RESEARCH_COMPLETE':
        lines=['# Prochaine action — revue de la décision après audit','',*common,
            '## '+nxt['id']+' — audit sans nouvelle installation','',
            '`RESEARCH_COMPLETE`. Aucun point acquis pour cette tâche; aucune validation moteur nouvelle créée.','',
            review['summary'],'',
            'Décision concrète proposée : '+link(review['decision'])+'. Rapport : '+link(review['report'])+'.','',
            'Contrôle joueur préparé : '+link(review['protocol'])+'. Les observations doivent rester limitées aux vérifications réellement faites.','',
            'Pour un état terminal sans correction, le suivi exige une décision explicitement approuvée par le responsable. Aucune approbation n’est déduite de l’autorisation générale de travailler ou du reçu d’une autre tâche.','',
            'Après décision et contrôle des preuves, candidate suivante : `'+review['next_implementation_candidate']+'`. Elle reste `NOT_STARTED`, sans recherche ni installation commencée dans cette mission. La sélection sera recalculée.','',
            review['scope_note']]
    partial=[t for t in tasks if t['status']=='BLOCKED' and t.get('installed_delivery_status')=='IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION']
    if partial:
        lines += ['', '## Corrections installées dans une tâche régionale bloquée','',
            'Le test de ces corrections est la prochaine action joueur. Il ne clôture pas les lacunes régionales et ne rapporte aucun point à lui seul. La candidate indépendante ci-dessus reste non commencée; une nouvelle mission sera nécessaire.','']
        for t in partial:
            lines += ['- '+t['id']+' : tâche `BLOCKED`; '+('révision technique restante' if mixed_partial_runtime_evidence(t) else 'installations')+' `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Protocole : '+link(t['runtime_validation']['protocol'])+'. '+t.get('blocking_reason','')]
    mixed=[t for t in partial if mixed_partial_runtime_evidence(t)]
    if mixed:
        lines += ['', '## Noyaux validés dans une version antérieure','',*['- '+t['id']+' : '+t['historical_validated_delivery_version']+' validée selon '+link(t['historical_runtime_validation']['attestation'])+'. Ce reçu ne couvre pas la révision technique postérieure.' for t in mixed]]
    accepted_partial=[t for t in tasks if t['status']=='BLOCKED' and t.get('installed_delivery_status')=='PASS_RUNTIME_USER_VALIDATED']
    if accepted_partial:
        lines += ['', '## Corrections partielles validées, couverture régionale encore bloquée','',
            *['- '+t['id']+' : seuls '+', '.join(l['id'] for l in t['installed_sub_lots'])+' sont `PASS_RUNTIME_USER_VALIDATED`. '+link(t['runtime_validation']['attestation'])+'. Tâche régionale `BLOCKED`, aucun point supplémentaire. '+t['blocking_reason'] for t in accepted_partial]]
    lines += ['', '## Installations antérieures en attente de reçu spécifique','',
              'Ces lacunes peuvent être testées séparément sans reconstruire les territoires ni étendre les attestations voisines.','',
              *['- '+id+' — '+byid[id]['title']+'.' for id in p['awaiting_runtime'] if id!=state.get('runtime_validation_hold',{}).get('task_id')]]
    if campaign.get('status')=='ACTIVE':
        lines=['# Prochaine action — campagne de levée des blocages','',*common,
            'La création systématique de nouveaux territoires est suspendue. `SC3-HOLSTEIN` ne doit pas être lancé automatiquement. Source : '+link(campaign['source'])+'.','',
            '## Huit installations : contrôles manquants uniquement','',
            'Protocole groupé : '+link(campaign['grouped_protocol'])+'. Audit : '+link(campaign['installed_audit'])+'. Onze points possibles, aucun crédit sans preuves terminales suffisantes. Le changement de portée administrative au Luxembourg doit être réconcilié explicitement.','',
            '## '+campaign['selected_blocked_task']+' — décision de clôture à examiner','',
            'Dossier : '+link(campaign['selected_review'])+'. Observation utilisateur limitée : '+link(campaign['user_observation'])+'. Aucun mois, sauvegarde/rechargement ou validation globale MAP2A n’est ajouté à cette observation.','',
            'La proposition de conservation B ne vaut pas approbation et ne contourne pas le test du registre déjà installé. Aucun nouveau sous-lot fonctionnel dans cette passe.','',
            'Classement des autres blocages : '+link(campaign['blocked_matrix'])+'. Candidate de clôture suivante : `'+campaign['next_closure_candidate']+'`, seulement recommandée, non commencée. Les anciens tests partiels et obligations restent dans BLOCKERS.md et les fiches canoniques.']
    if resolution:
        lines=['# Prochaine action — validations SERG groupées','',*common,
            '## Luxembourg R1 — priorité de validation','',
            'Le conflit administratif est réparé. Un niveau BEO/Wallonie est installé, les trois niveaux flamands sont conservés ; aucun changement de frontière ou de population. Rapport : '+link(resolution['report'])+'.','',
            'Protocole limité : '+link(resolution['protocol'])+'. Statut : `'+byid['SC2-LUXEMBOURG-VALIDATION']['status']+'` ; aucun point avant reçu explicite et validation des critères.','',
            '## Une même session pour les installations encore en attente','',
            'Liste et contrôles : '+link(campaign['grouped_protocol'])+'. Huit tâches représentent onze points conditionnels. Les éléments manquants des sous-lots Teschen et de la mine de sel sont séparés, sans clôture régionale automatique.','',
            *['- '+id+' — '+byid[id]['title']+'.' for id in p['awaiting_runtime']],
            '', 'La vérification en jeu déjà rapportée pour Teschen reste à sa portée réelle. Aucun nouveau test, accord de conservation ou reçu n’est inventé. Aucun nouveau territoire, aucune tâche de clôture supplémentaire et aucun lancement de SC3-HOLSTEIN.']
    if resolution and resolution.get('attestation'):
        pending=p['awaiting_runtime'];pending_weight=sum(byid[id]['weight'] for id in pending)
        lines=['# Prochaine action — validations SERG restantes','',*common,
            '## Luxembourg reçu et clôturé','',
            '`SC2-LUXEMBOURG-VALIDATION` : `'+byid['SC2-LUXEMBOURG-VALIDATION']['status']+'`. Reçu : '+link(resolution['attestation'])+'. Bilan de réception : '+link(resolution['acceptance_report'])+'. Aucun contrôle Luxembourg à refaire.','',
            '## Prochaine validation joueur recommandée','',
            ('`'+pending[0]+'` ; les autres lots peuvent être contrôlés dans la même session.' if pending else 'Aucune des validations groupées initiales ne reste ouverte.'),'',
            'Liste et contrôles : '+link(campaign['grouped_protocol'])+'. '+str(len(pending))+' tâches installées, '+str(pending_weight)+' points conditionnels. Aucun statut des autres tâches n’est modifié par les reçus nommés ci-dessus.','',
            *['- '+id+' — '+byid[id]['title']+'.' for id in pending],
            '', 'Les sous-lots Teschen et de la mine de sel restent distincts selon le protocole groupé. Aucun reçu ou accord supplémentaire n’est présumé. Aucun nouveau territoire, aucune installation et aucun lancement de SC3-HOLSTEIN.']
    if map2a_reception:
        at=lines.index('## Prochaine validation joueur recommandée')
        lines[at:at]=['## MAP2A reçu et clôturé','',
            '`SC2-MAP2A-VALIDATION` : `'+byid['SC2-MAP2A-VALIDATION']['status']+'`. Reçu : '+link(map2a_reception['attestation'])+'. Conservation : '+link(map2a_reception['checks'])+'. Aucun contrôle MAP2A à refaire ; TE-R-CORE demeure distinct.','']
    if grouped_reception:
        lines=['# Prochaine action — préparation des clôtures SERG','',*common,
            '## Réception groupée enregistrée','',
            *['- `'+id+'` : `'+byid[id]['status']+'` ; '+link(grouped_reception['receipts'][id])+'.' for id in grouped_reception['task_ids']],
            '', 'Luxembourg et MAP2A restent reçus. Rapport : '+link(grouped_reception['report'])+'. Aucun reçu historique remplacé.',
            '', ('Aucun des huit protocoles complets initiaux ne reste en attente.' if not p['awaiting_runtime'] else 'Protocoles complets encore ouverts : '+', '.join(p['awaiting_runtime'])+'.'),
            '', '## Deux sous-lots restent à confirmer séparément','',
            'Teschen `TE-R-CORE` et Berchtesgaden `BG-E-SALT-NATIVE-R1` : '+link(grouped_reception['protocol'])+'. Les six reçus ne les valident pas. Leurs tâches régionales restent BLOCKED.',
            '', '## Trois voies de clôture recommandées, sans démarrage','',
            '1. `SC2-TESCHEN` : protocole propre du registre, puis décision explicite sur la portée B territoriale et démographique.',
            '2. `SC5-EAST-FRISIA-SOUTH` : arbitrage B ou report P1 non bloquant explicitement approuvé, sans conformité positive inventée.',
            '3. `SC1-ORTENBURG` : noyau reçu ; villages souverains et population rurale comparable encore à établir. Clôture non acquise.',
            '', 'Justifications, obligations essentielles et réserves de précision : '+link(grouped_reception['readiness'])+'. Matrice actuelle : '+link(grouped_reception['blocked_matrix'])+'.',
            '', 'Aucune de ces tâches n’est clôturée par cette préparation. Les P0/P1 substantiels restent ouverts ; aucune reclassification artificielle en P2. Aucun nouveau territoire, aucun sous-lot fonctionnel et aucun lancement de SC3-HOLSTEIN.']
    md('NEXT_ACTION.md',lines)
    lines=['# Critères bloquants de clôture territoriale 1.0','',*common,
      'La présence d’un document ou l’achèvement d’une recherche ne coche pas un critère territorial. Chaque état terminal doit être justifié; les étapes documentaires/techniques peuvent être validées sans faux test du moteur.','']
    gates=[('Tous les jalons obligatoires terminaux justifiés',all(done.values())),
      ('Aucun P0 non résolu, y compris couverture des Habsbourg et de l’Italie',all(done[t['id']] for t in tasks if t['priority']=='P0')),
      ('Tous les P1 traités ou reports non bloquants explicitement autorisés',all(done[t['id']] for t in tasks if t['priority']=='P1')),
      ('Protocoles complets des huit installations initiales reçus (hors révisions partielles)',all(done[id] for id in [t['id'] for t in tasks if t['kind']=='pending_runtime'])),
      ('Membres/neuf électeurs/statuts et gouvernements contrôlés',done['SC7-MEMBERS-ELECTORS']),
      ('Registre impérial final validé',done['SC7-REGISTRY']),
      ('Relations, successions et transitions actives vérifiées',done['SC7-INSTITUTIONS']),
      ('Démographie historique/économie/PM/propriété/unités cohérentes',done['SC7-DEMOGRAPHY-ECONOMY']),
      ('Aucun test de non-régression bloquant inexpliqué',done['SC7-NONREGRESSION']),
      ('P2/abstractions documentés et décisions explicites consignées',done['SC7-P2-REGISTER']),
      ('Revue de tous les grands secteurs et arbitrages P0/P1',done['SC7-P1-DECISIONS']),
      ('Campagne humaine finale et approbation explicite de l’utilisateur',done['SC7-FINAL-APPROVAL'])]
    lines += [('- [x] ' if ok else '- [ ] ')+title for title,ok in gates]
    lines += ['', 'Les 19 socles validés ne ferment pas les régions environnantes. Les nouvelles corrections exigeront leurs propres tests. Les 44 doublons et 12 références invalides préexistants restent une dette identifiée, pas des régressions nouvelles; une erreur fonctionnelle prouvée ne peut être masquée sous P2.',
      '', 'Pas d’obligation de cadastre intégral ou de développement de toutes les futures mécaniques impériales. Les scénarios effectivement utilisés doivent fonctionner. Dernier jalon : accord humain explicitement lié à la version du périmètre et au test final; aucun nom de sauvegarde/hash/date de test ne sera inventé.']
    md('CLOSURE_CHECKLIST.md',lines)
    lines=['# Registre des P2 et abstractions non bloquantes','',*common,
      'Pas de poids supplémentaire par micro-enclave. La tenue et l’arbitrage final de ce registre relèvent du jalon SC7-P2-REGISTER (un point). Aucun P0/P1 n’est déplacé ici. Deux décisions antérieures explicitement acceptées; les huit autres reports sont proposés, pas approuvés par défaut. Leur géométrie ne bloque pas 1.0 mais leur disposition finale doit être consignée.','']
    for d in state['deferred_p2']:
        lines += ['## '+d['id']+' — '+d['title'],'', '`'+d['status']+'` — '+d['decision']+'.', '', 'Autorité : '+str(d['authority'] or 'à recueillir; ne pas inventer')+'.', '', 'Preuve : '+link(d['evidence'][0],d['evidence'][0])+'.', '',d['caveat']+'.','']
    md('DEFERRED_P2.md',lines)
    lines=['# Blocages et couverture restant à traiter','',*common,
      'Trois problèmes P0 et vingt et un P1 de l’audit restent reliés ci-dessous. Un défaut de couverture ne démontre pas que toutes les possessions actuelles sont fausses. Les tâches de socle ne suppriment pas ces problèmes périphériques. Une résolution partielle conserve les tâches restantes visibles.','']
    for issue in issues:
        if issue['Priorite']=='P2':continue
        linked=[t for t in tasks if issue['ID'] in t['issues']]
        lines += ['## '+issue['ID']+' — '+issue['Priorite']+' — '+issue['Probleme'],'',
                  'Action bornée héritée : '+issue['Action_bornee']+'.','',
                  'Tâches : '+('; '.join(t['id']+' `'+t['status']+'`' for t in linked) or 'À relier explicitement avant progression')+'.',
                  '', 'Preuve : '+link(issue['Preuve'],issue['Preuve'])+'.','']
        for task in linked:
            if task.get('current_delivery_note'):
                lines += ['État actuel '+task['id']+' : '+task['current_delivery_note']+' '+', '.join(link(ref) for ref in task['implementation_report'])+'.','']
    lines += ['## Blocages explicites à ne pas recycler indéfiniment','',*['- '+id+' : '+byid[id].get('blocking_reason',byid[id]['expected']) for id in p['blocked']],
      '', 'Les dépendances alpines sont calculées depuis les reçus acquis : Salzbourg validé ne clôture pas Trente/Brixen, dont dépend le Tyrol. Goslar est coordonné au dossier Brunswick–Harz. Si un dossier reste bloqué, avancer un autre P0/P1 indépendant sans lui attribuer de crédit fictif.',
      '', '## Tests non encore attestés','',*['- '+id+': '+byid[id]['title'] for id in p['awaiting_runtime']],
      '', 'Pas de relance d’Erfurt sur les mêmes points, pas de translation 7,20 px; Hohenlohe reste catégorie C, candidats retirés. Les locators ne constituent pas des vérités géographiques.']
    if partial:
        lines += ['', '## Tests de corrections partielles sous blocage régional','',
            *['- '+t['id']+' : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` '+('pour la révision technique restante; noyau antérieur validé séparément selon '+link(t['historical_runtime_validation']['attestation']) if mixed_partial_runtime_evidence(t) else 'pour les seuls sous-lots installés; aucun reçu humain')+'. '+link(t['runtime_validation']['protocol'])+'. Le blocage régional et les points restent inchangés après ce seul test.' for t in partial]]
    if accepted_partial:
        lines += ['', '## Validations partielles sans clôture territoriale','',
            *['- '+t['id']+' : '+str(len(t['installed_sub_lots']))+' sous-lots installés validés selon '+link(t['runtime_validation']['attestation'])+'. Le blocage régional demeure; aucun point attribué.' for t in accepted_partial]]
    if campaign.get('status')=='ACTIVE':
        lines += ['', '## Campagne de levée des blocages en cours','',
            'Matrice des lacunes essentielles, réserves B/P2 et actions de clôture : '+link(campaign['blocked_matrix'])+'. Les obligations historiques ne sont pas effacées pour augmenter le pourcentage.','',
            'Huit installations initiales : '+link(campaign['installed_audit'])+'. '+('Luxembourg : reçu humain enregistré, tâche clôturée selon '+link(resolution['attestation'])+'. ' if resolution and resolution.get('attestation') else 'Luxembourg : conflit administratif réparé, test joueur requis selon '+link(resolution['report'])+'. ' if resolution else 'Luxembourg : évolution administrative ultérieure à réconcilier, pas restauration automatique. ')+'Protocole groupé : '+link(campaign['grouped_protocol'])+'.','',
            'Teschen : vérification en jeu rapportée selon '+link(campaign['user_observation'])+', sans nouveau reçu de protocole complet. Décision proposée : '+link(campaign['selected_review'])+'. Les critères humains manquants et la réserve démographique restent explicites.']
    if map2a_reception:
        lines += ['', '## Réception MAP2A sans extension à Teschen','',
            '`SC2-MAP2A-VALIDATION` clôturée selon '+link(map2a_reception['attestation'])+'. Les quatre corrections et leurs dépendances inspectées sont reçues ; la précision cadastrale générale, SC2-TESCHEN et TE-R-CORE restent hors reçu. Luxembourg reste clôturé.','',
            (str(len(p['awaiting_runtime']))+' autres validations installées restent ouvertes' if p['awaiting_runtime'] else 'Aucune autre validation complète des huit installations initiales ne reste ouverte')+' selon '+link(campaign['grouped_protocol'])+'. Les blocages régionaux, le test du registre Teschen et celui de la mine de sel sont conservés ; aucun nouveau territoire commencé.']
    if grouped_reception:
        lines += ['', '## Six réceptions distinctes ; blocages régionaux conservés','',
            'Reçus et contrôles : '+link(grouped_reception['report'])+'. Les '+str(len(p['blocked']))+' tâches BLOCKED restent inchangées. État des installations déjà testées et obligations historiques restantes : '+link(grouped_reception['blocked_matrix'])+'.','',
            'Trois voies préparées uniquement : '+link(grouped_reception['readiness'])+'. Les vérifications propres à Teschen et à la mine ordinaire restent ouvertes selon '+link(grouped_reception['protocol'])+'. Aucun point supplémentaire de clôture régionale ni report P1 approuvé.']
    md('BLOCKERS.md',lines)
    write_json(OUT/'PROGRESS_SNAPSHOT.json',p)
    print(json.dumps(p,ensure_ascii=False,indent=2))

def check():
    state=load_json(OUT/'ROADMAP_STATE.json');errors=structural_errors(state)
    for ref,h in state['source_manifest'].items():
        if not file_ref(ref).is_file() or digest(file_ref(ref))!=h:errors.append('Source changed: '+ref)
    p=progress(state)
    if not (OUT/'PROGRESS_SNAPSHOT.json').exists() or load_json(OUT/'PROGRESS_SNAPSHOT.json')!=p:errors.append('Stale progress view: render required')
    for name in ('ROADMAP.md','PROGRESS_HISTORY.md','NEXT_ACTION.md','CLOSURE_CHECKLIST.md','DEFERRED_P2.md','BLOCKERS.md'):
        if not (OUT/name).is_file():errors.append('Missing '+name)
    return dict(status='PASS' if not errors else 'FAIL',errors=errors,progress=p,automated_engine_test=False)

def record_initial_validation():
    """Explicit documentation output; never a game/runtime attestation."""
    target=OUT/'VALIDATION.json'
    if target.exists():raise ValueError('Initialization evidence exists; do not overwrite it')
    state=load_json(OUT/'ROADMAP_STATE.json');result=check();protection=observe(state)
    tests=load_json(OUT/'TESTS.json')
    checks=[('roadmap_consistency',result['status']=='PASS'),
            ('tracker_tests',tests['passed']==tests['total'] and not tests['failed']),
            ('no_functional_edits',not protection['runtime_changed']),
            ('source_audit_preserved',not protection['source_audit_changed']),
            ('head_preserved',protection['head_unchanged']),('index_preserved',protection['index_unchanged']),
            ('branch_preserved',protection['branch_unchanged']),('original_agents_preserved',protection['agents_original_preserved']),
            ('salzburg_not_started',next(t['status'] for t in state['tasks'] if t['id']=='SC1-SALZBURG')=='NOT_STARTED'),
            ('no_new_runtime_receipts',state['initialization']['new_runtime_tests']==0),
            ('explicit_final_approval_still_missing',state['closure_approval']['approved'] is False)]
    files=[p for p in OUT.rglob('*') if p.is_file() and p!=target]
    obj=dict(status='SERG_CLOSURE_ROADMAP_INITIALIZED' if all(ok for _,ok in checks) else 'FAIL',
      recorded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      passed=sum(ok for _,ok in checks),total=len(checks),failed=[name for name,ok in checks if not ok],
      checks=[dict(id=name,passed=ok) for name,ok in checks],tracker_tests=dict(passed=tests['passed'],total=tests['total']),
      progress=result['progress'],protection=protection,territorial_changes=0,new_runtime_tests=0,automated_engine_test=False,
      colgrep_calls=0,colgrep_reason='Known audit locations and exact references; no semantic localization needed',
      agents_loading_test='Scoped root instruction and documented startup fallback; no fresh agent session executed',
      artifacts_sha256={p.relative_to(ROOT).as_posix():digest(p) for p in files},
      tools_sha256={p.relative_to(ROOT).as_posix():digest(p) for p in (Path(__file__),ROOT/'tools/test_serg_closure_roadmap.py')},
      agents_sha256=digest(ROOT/'AGENTS.md'))
    write_json(target,obj);print(json.dumps({k:obj[k] for k in ('status','passed','total','tracker_tests','territorial_changes','new_runtime_tests')},indent=2))
    if obj['failed']:raise SystemExit(1)

if __name__=='__main__':
    command=sys.argv[1] if len(sys.argv)>1 else 'check'
    if command=='init':init()
    elif command=='add-region-details':add_region_details()
    elif command=='render':render()
    elif command=='observe':print(json.dumps(observe(load_json(OUT/'ROADMAP_STATE.json')),ensure_ascii=False,indent=2))
    elif command=='record-initial-validation':record_initial_validation()
    elif command=='check':
        result=check();print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(result['errors']))
    else:raise SystemExit('Supported: init, render, check, observe. No installer or automatic status transition.')
