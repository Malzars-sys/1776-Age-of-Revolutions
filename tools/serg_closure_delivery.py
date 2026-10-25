"""Audit-only consolidation and map. Never imports an installer or compiler."""
from pathlib import Path
import collections,csv,json,re,textwrap
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from serg_global_closure_audit import ROOT,OUT,save
from serg_closure_tables import BASE,W,V,I,P,D,N,C,ref

RECEIPTS={
'MAP2L/BELGIUM':'MAP2L/RUNTIME_USER_VALIDATION.json',
'MAP2L/FRANCONIA':'MAP2L/RUNTIME_USER_VALIDATION.json',
'MAP2L/FRANCONIA_CONTINUATION':'MAP2L/RUNTIME_USER_VALIDATION.json',
'MAP2L/RHINE_CENTRAL':'MAP2L/RUNTIME_USER_VALIDATION.json',
'MAP2L/RHINE_WESTPHALIA':'MAP2L/RUNTIME_USER_VALIDATION.json',
'MAP2L/RHINE_WESTPHALIA_COMPLETION':'MAP2L/RUNTIME_USER_VALIDATION_RHINE_SWABIA.json',
'MAP2L/SWABIA':'MAP2L/RUNTIME_USER_VALIDATION_RHINE_SWABIA.json',
'MAP2L/SWABIA_FINISH':'MAP2L/RUNTIME_USER_VALIDATION_SWABIA_FINISH.json',
'MAP2L/SWABIA_COMPLETION':'MAP2L/RUNTIME_USER_VALIDATION_SWABIA_COMPLETION.json',
'MAP2L/PRUSSIAN_BORDERS':'MAP2L/RUNTIME_USER_VALIDATION_PRUSSIAN_CORE.json',
'MAP2M/R2':'MAP2M/R3/R2_USER_RUNTIME_VALIDATION.json',
'MAP2M/R3':'MAP2M/R4/R3_USER_RUNTIME_VALIDATION.json',
'MAP2M/R8':'MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json',
'MAP2M/R9':'MAP2M/R8_R9_USER_RUNTIME_VALIDATION_2026_10_15.json',
'MAP2N':'MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json',
'MAP2N/COMPLETION':'MAP2N/RUNTIME_USER_VALIDATION_2026_10_15.json',
'MAP2O':'MAP2P/MAP2O_RUNTIME_USER_VALIDATION.json',
'MAP2Q':'MAP2Q/CONTINUATION_R2/RUNTIME_USER_VALIDATION.json',
'MAP2Q/CONTINUATION_R2':'MAP2Q/CONTINUATION_R2/RUNTIME_USER_VALIDATION.json',
'MAP2Q/R3':'MAP2Q/R3/RUNTIME_USER_VALIDATION.json',
'MAP2R':'MAP2S/MAP2R_RUNTIME_USER_VALIDATION.json',
'MAP2T':'MAP2T/RUNTIME_USER_ATTESTATION_MAP2U.json',
'MAP2U':'MAP2W/PREVIOUS_LOTS_RUNTIME_USER_ATTESTATION.json',
'MAP2W':'MAP2W/RUNTIME_USER_ATTESTATION_R2B.json',
'MAP2W/R2':'MAP2W/RUNTIME_USER_ATTESTATION_R2B.json',
'MAP2W/R2B':'SERG_GLOBAL_CLOSURE_AUDIT/RUNTIME_USER_ATTESTATION.json',
'MAP2W/R4/POLITICAL_REPRESENTATION/PASSAU':'SERG_GLOBAL_CLOSURE_AUDIT/RUNTIME_USER_ATTESTATION.json',
W+'/R4B':'SERG_GLOBAL_CLOSURE_AUDIT/RUNTIME_USER_ATTESTATION.json',
W+'/R4C':'SERG_GLOBAL_CLOSURE_AUDIT/RUNTIME_USER_ATTESTATION.json'}

# Priority | sectors | problem | decision | roadmap | evidence (relative to map reports).
ISSUES="""P0|F05|Salzbourg sans souveraineté territoriale distincte|Noyau et démographie historiques à établir; pas contour administratif moderne|CL1|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P0|H01;H04;H05;H06|Couverture insuffisante des grands territoires habsbourgeois|Blocage de couverture, pas preuve que toute attribution AUS est erronée|CL1|SERG_GLOBAL_CLOSURE_AUDIT/REGIONAL_COVERAGE.csv
P0|J03;J04|Italie impériale et Savoie insuffisamment auditées|Investitures et exclusions datées à contrôler; pays MOD/PAR/TUS/SAR déjà présents|CL2|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P1|H05|Trente et Brixen sans distinction politique|Séparer juridictions épiscopales des droits tyroliens; pas tout SOUTH_TYROL à transférer|CL1|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P1|F04|Berchtesgaden et Ortenbourg|Berchtesgaden attesté; compléter preuve datée d’Ortenbourg et noyaux représentables|CL1|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P1|F02;F03|Werdenfels, Burgrain, Ismaning, Hohenburg|Arbitrer possessions significatives sans corridor traversant une souveraineté voisine|CL1|MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md
P1|F03|Ratisbonne : 713 habitants techniques, confession héritée|Estimer population historique sur périmètre comparable, sans compensation mondiale exigée ni chiffre inventé|CL1|MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md
P1|A01|Holstein royal après 1773, Schleswig extérieur|Vérifier HOL/SCH et lien danois sans fusion d’Eutin|CL3|MAP1/inputs/regional_originals/R2_NORTHERN_CENTRAL_EASTERN_EUROPE_RECOMMENDATIONS.csv
P1|A05;A08|Mecklembourg, Hildesheim et branches Brunswick-Lunebourg/Harz|Pays existants à contrôler; Hildesheim et Goslar distincts attestés; Quedlinburg à délimiter|CL3|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P1|A03|Liens suédois natifs LUB/MEC/MST hérités|Gameplay explicitement préservé dans MAP2K, pas vérité historique; décision de clôture à formaliser|CL3|MAP2K/MAP2K_EXECUTIVE_SUMMARY.md
P1|A07;H03|Magdebourg/Halberstadt, Lusaces et partition silésienne|Préserver MAP2A et Anhalt/T/U; vérifier uniquement les limites non démontrées|CL3|MAP2M/R9/PRUSSIAN_HRE_BORDERS_AUDIT.md
P1|B09|Jever dans les enveloppes OLD candidates|Titre AZR établi; délimiter noyau viable ou report motivé explicite, jamais OLD entier vers AZR|CL4|MAP2S/JEVER_HISTORICAL_EVIDENCE.md
P1|B09|Leer et Rheiderland : sud de Frise orientale|319 cellules PRU conservées; déterminer si et où la juridiction déborde, pas 1240 erreurs supposées|CL4|MAP2P/REPORT.md
P1|B05|Gueldre prussienne et Clèves/Mark/Ravensberg|Délimiter partage de 1713 et principales franges, pas acquisitions XIXe|CL4|MAP2L/RHINE_WESTPHALIA_COMPLETION/UNRESOLVED.csv
P1|B07|Dortmund et principales temporalités westphaliennes|Dortmund attestée; Corvey/Essen/Steinfurt/Rietberg et Bentheim gagé à délimiter et arbitrer ensemble|CL4|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P1|C05|Worms/Spire, Hombourg et Hesses|Séparer villes, évêchés, apanages et possessions souveraines avant création éventuelle|CL5|MAP2W/R2B/UNRESOLVED_R2B.csv
P1|C03|Erfurt–Eichsfeld mayençais toujours gelé|Nouvelles preuves homologues seulement; sinon report P1 motivé accepté, aucune translation répétée|CL5|MAP2L/ERFURT_EICHSFELD/REPORT.md
P1|D02|Hohenlohe, Castell et Wertheim|Aucun R3 installé; décision B justifiée ou report explicite sans refaire le même calage|CL6|MAP2W/R3/CALIBRATION/REPORT.md
P1|D02|Rothenburg, Schweinfurt, Windsheim, Weißenburg|Absences distinctes attestées; arbitrer noyaux politiques, pas une cellule automatique par ville|CL6|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P1|E05|Montbéliard, Oettingen et grands raccords souabes|Comté distinct des seigneuries françaises; branches à établir avant ajout|CL6|MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv
P1|B03;B04;C02;E02;I02;J01;J02|Portée manuelle manquante pour couches installées|Contrôle groupé des seules couches non couvertes; pas extrapolation des reçus voisins|CL7|SERG_GLOBAL_CLOSURE_AUDIT/COMPLETED_LOTS.csv
P1|K01|Transitions et succession des sujets impériaux natifs|Tester conversions/taux/élection séparément; prototype de succession non activé ne vaut pas PASS|CL7|docs/reports/hre/HRE_CENTRALIZATION_01/REPORT.md
P1|I03|Limbourg, Maastricht et franges belges|Décision sur condominium et droits impériaux, sans refaire les noyaux LGE/STM validés|CL5|MAP2L/BELGIUM/IMPLEMENTATION.md
P1|H02|Écart de couverture impériale de x9061E0 (Teschen technique)|179 cellules AUS dans WEST_GALICIA restent hors registre malgré MAP2A; délimiter la portion impériale sans inscrire toute la Galicie|CL1|SERG_GLOBAL_CLOSURE_AUDIT/SUPPLEMENTAL_CHECKS.json
P2|A06|Peendamm non séparé|Abstraction acceptée; ne pas présenter l’omission comme frontière reconstruite|CL7|MAP2M/R9/REPORT.md
P2|E04|Augsbourg et Kempten : une cellule par ville|Autorisation explicite à conserver, distincte des évêché/abbaye|CL7|MAP2L/SWABIA_COMPLETION/REPORT.md
P2|E05|Esslingen, Isny, Lindau, Kaufbeuren|Non-prolifération conservée; ne pas étendre l’autorisation une cellule à toutes les villes|CL6|MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv
P2|F03|Immunités et abbayes intra-urbaines de Ratisbonne|St-Emmeram/Obermünster/Niedermünster abstraits, pas fusion historique avec conseil ou diocèse|CL7|MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/UNRESOLVED.md
P2|E03;E05|Waldburg, Salem et offices minuscules|Condominiums, droits superposés et propriétés foncières ne deviennent pas automatiquement TAGs|CL6|MAP2L/SWABIA_COMPLETION/UNRESOLVED.csv
P2|G04;A02|Petites enclaves Anhalt/Thuringe et chapitre de Lübeck|Conserver noyaux validés et inventaire explicite des possessions différées|CL7|MAP2Q/R3/REPORT.md
P2|K02|Liechtenstein et chevalerie immédiate sous-résolus|Abstraction explicite possible, sans nier leur existence historique|CL1|SERG_GLOBAL_CLOSURE_AUDIT/HISTORICAL_GAPS.md
P2|K01|44 doublons RGB et 12 références invalides hérités|Dette QA préexistante; reclasser si impact bloquant prouvé, pas nouveau correctif territorial|CL7|SERG_GLOBAL_CLOSURE_AUDIT/DIAGNOSTIC_SUMMARY.json
P2|K01|Deux assertions anciennes de dernière couche Passau|Conserver les échecs documentés; maintenance des snapshots, pas régression territoriale démontrée|CL7|MAP2W/R4/POLITICAL_REPRESENTATION/FREISING_REGENSBURG/TESTS.json
P2|D03;C04;E05|Drapeaux procéduraux et démographie provisoire|Héraldique séparée des frontières; prioriser les effectifs matériellement trompeurs|CL7|MAP2W/R2B/UNRESOLVED_R2B.csv"""

def make():
    regions=json.loads((OUT/'REGIONAL_DATA.json').read_text());entities=json.loads((OUT/'ENTITY_DATA.json').read_text());layers=json.loads((OUT/'LAYERS.json').read_text())
    issues=[]
    for line in ISSUES.splitlines():
        prio,sec,title,action,lot,evidence=line.split('|')
        ev=evidence if evidence.startswith('docs/') else BASE+evidence
        issues.append(dict(ID=f'R{len(issues)+1:02}',Priorite=prio,Secteurs=sec,Probleme=title,Preuve=ref(ev),Action_bornee=action,Lot_recommande=lot,Installation_autorisee='NON'))
    save('ISSUE_DATA.json',issues)
    completed=[]
    def add(lot,date,kind,scope,nrgb=None,chain=None,report=None):
        directory=ROOT/BASE/lot
        if report is None:
            candidates=[directory/'REPORT.md',directory/'IMPLEMENTATION.md',directory/(lot.split('/')[-1]+'_EXECUTIVE_SUMMARY.md')]
            report=next((p for p in candidates if p.exists()),None)
            if report is None and directory.exists():report=next(directory.glob('*.md'),None)
        receipt=RECEIPTS.get(lot)
        completed.append(dict(Ordre=len(completed)+1,Lot=lot,Date_documentee=date,Type=kind,Installe_actuellement='OUI — portée limitée',Statut=V if receipt else I,Portee=scope,Nouveaux_RGB_declares=nrgb,Ordre_chaine_registre=chain,Rapport=ref(report.relative_to(ROOT).as_posix()) if report else 'Voir rapport parent MAP2N et migration',Preuve_installation='REGISTRY_CHECKS.json; EFFECTIVE_GEOMETRY_CHECKS.json; SUPPLEMENTAL_CHECKS.json',Attestation=ref(BASE+receipt) if receipt else 'Aucune attestation spécifique suffisante retrouvée',Limite='Portée inspectée seulement; ni nombre de campagnes moteur indépendantes ni certification de toutes frontières'))
    add('LUX_BEO_INTEGRATION_2026-10-10','2026-10-10','souveraineté et dépendances','xD001A0 BEO; ancien LUX sans territoire; frontière inchangée',0)
    add('MAP2A','2026-10-10','réparations souveraineté/scopes','Trois Ligues et Silésie autrichienne; quatre RGB existants',0)
    add('MAP2K','2026-10-13','électorats et cadre impérial','Cinq provinces anciennes, quatre TAG actifs supplémentaires, neuf titres',0)
    add('MAP2L/BELGIUM','2026-10-13','redécoupage politique','Liège, Stavelot et noyaux belges',37)
    add('MAP2L/PIEDMONT','2026-10-13','extension du registre et bloc','Neuf RGB SAR piémontais, pas île de Sardaigne',0)
    for layer in layers:
        lot=layer['path'].removeprefix(BASE)
        if lot=='MAP2N':
            for sub in ('R2','R3','R8','R9'):
                add('MAP2M/'+sub,'2026-10-15','retouches de couleurs existantes / contexte extérieur','Peene progressive; R2 inclut Bromberg 85 cellules hors SERG, Netze non achevée',1 if sub=='R2' else 0)
        date='2026-10-13' if layer['order']<7 else '2026-10-14' if layer['order']<=16 else '2026-10-15' if layer['order']<=18 else '2026-10-16' if layer['order']<=21 else '2026-10-17' if layer['order']<=27 else '2026-10-18'
        add(lot,date,'couche territoriale approuvée',';'.join(layer.get('regions') or [])+'; nouveaux membres '+','.join(layer['new_members']),layer['new_rgb_count'],layer['order'])
        if lot=='MAP2Q':add('MAP2Q/CONTINUATION_R2','2026-10-16','démographie historique approuvée','Eutin 7600; HLB 9206 après R3; monde -3725 sans compensation',0,report=ROOT/BASE/'MAP2Q/REPORT.md')
    for suffix in ('','/FEEDBACK_R1','/SECESSION_LENS_R2'):
        p=ROOT/'docs/reports/hre'/('HRE_CENTRALIZATION_01'+suffix)/'REPORT.md'
        add('HRE_CENTRALIZATION_01'+suffix,'2026-10-17','institutionnel — non territorial','Sujets / taux-transitions / lentille; prototype de succession isolé non activé',0,report=p)
    completed.sort(key=lambda r:(r['Date_documentee'],r['Ordre']))
    for order,r in enumerate(completed,1):r['Ordre']=order
    save('LOT_DATA.json',completed)
    uncovered=[dict(ID=r['ID'],Macro_region=r['Macro_region'],Secteur=r['Secteur'],Recherche_effectuee='Index docs/tools; MAP1/R1/R2; migrations; anciens bilans R9/Q3/W; corpus économie/technologies/personnages hors MAP',Trouve=r['Preuve'],Pourquoi_insuffisant=r['Problemes_ouverts'],Conclusion='Aucun audit territorial détaillé suffisant retrouvé; ne signifie pas aucune recherche de contexte',Prochain_lot='CL1' if r['ID'].startswith('H') else 'CL2' if r['ID'].startswith('J') else 'CL3' if r['ID'].startswith('A') else 'CL7') for r in regions if r['Statut']==N]
    abstract=[dict(ID=r['ID'],Secteur=r['Secteur'],Classe='B — REPRÉSENTATION SCHÉMATIQUE ACCEPTÉE' if r['Representation_schematique_acceptee']=='OUI' else 'C — DIFFÉRÉ / NON INSTALLÉ',Statut=r['Statut'],Justification=r['Perimetre_historique'],Limite=r['Problemes_ouverts'],Preuve=r['Preuve'],Decision='Conserver installé' if r['Statut'] in {V,I} else 'Aucun transfert nouveau autorisé') for r in regions if r['Representation_schematique_acceptee']=='OUI' or r['Statut']==D]
    for r in issues:
        if r['Priorite']=='P2':abstract.append(dict(ID=r['ID'],Secteur=r['Probleme'],Classe='P2 — report proposé, pas approbation inventée',Statut=D,Justification=r['Probleme'],Limite=r['Action_bornee'],Preuve=r['Preuve'],Decision='Décision 1.0 explicite nécessaire, pas installation'))
    tables=dict(REGIONAL_COVERAGE=regions,IMPERIAL_STATES_INVENTORY=entities,COMPLETED_LOTS=completed,REMAINING_WORK=issues,UNCOVERED_REGIONS=uncovered,ABSTRACTIONS_AND_DEFERRED=abstract)
    save('TABLE_DATA.json',tables)
    summary=dict(status='SERG_GLOBAL_CLOSURE_AUDIT_COMPLETE',macro_regions_considered=11,subsectors=len(regions),subsector_status_counts=dict(collections.Counter(r['Statut'] for r in regions)),inventory_entries=len(entities),inventory_scope='principal entities, possessions and groups; NOT exhaustive historical denominator',entries_with_active_tag_and_rgb=sum(bool(r['TAG_actuel'] and r['RGB_identifies']) for r in entities),confirmed_distinct_representation_absences=sum(r['Representation']=='ABSENCE POLITIQUE DISTINCTE CONFIRMÉE' for r in entities),explicit_abstracted_inventory_entries=sum('ABSTRACTION' in r['Representation'] for r in entities),installed_documented_rows=len(completed),intervention_types=dict(collections.Counter(r['Type'] for r in completed)),installed_rows_with_manual_receipt=sum(r['Statut']==V for r in completed),registry_migration_layers=len(layers),issues_by_priority=dict(collections.Counter(r['Priorite'] for r in issues)),closure_1_0=False,engine_executed=False,overall_percentage=None)
    save('COVERAGE_METRICS.json',summary)
    index=json.loads((OUT/'DOCUMENT_INDEX.json').read_text())
    lines=['# Index des preuves et des anciens travaux','','Les références chemin:ligne sont résolues sur le dépôt actuel. DOCUMENT_INDEX.json conserve les empreintes des 1020 documents candidats repérés. Ce balayage machine ne signifie pas lecture intégrale de 1020 pièces ni certification de leurs conclusions.','','## Conclusions régionales','']
    for r in regions:lines.append(f"- {r['ID']} — {r['Secteur']} : {r['Preuve']}. {r['Statut']}. {r['Problemes_ouverts']}")
    lines+=['','## Chronologie des installations et reçus','']
    for r in completed:lines.append(f"- {r['Ordre']} — {r['Lot']} ({r['Date_documentee']}) : {r['Rapport']}; reçu : {r['Attestation']}. {r['Portee']}")
    lines+=['','## Corpus non cartographiques vérifiés comme pistes, pas comme frontières',
      '- docs/research/WORLD_BORDERS_1776_COMPARISON_ROADMAP_CLEAN (1).md : contexte macro, pas mapping local.',
      '- docs/reports/buildings/BUILD_START_1776_CENTRAL_EUROPE_GERMAN_ITALY_RESEARCH.md : économie, pas attribution des frontières.',
      '- docs/reports/technology/recherche régional/TECH_START_1776_CENTRAL_EUROPE_GERMAN_ITALY_RESEARCH.md : technologies, noms historiques parfois antérieurs aux splits.',
      '- docs/research/characters/RULERS_1776_EUROPE_RESIDUAL_SOURCES.md : identités, ne prouve pas contours.',
      '- docs/research/military/CLEANUP2D2_IMPERIAL_AND_COMPANY_FORCE_ALLOCATION.csv : forces, pas souveraineté par province.',
      '- docs/reports/hre/HRE_CENTRALIZATION_01 et suites : institutions réellement installées, prototype isolé de succession distinct et non activé.',
      '', '## Index machine des pistes documentaires (pas toutes lues intégralement)','']
    lines += [f"- {r['path']}:1 — {r['lines']} lignes; SHA-256 {r['sha256']}." for r in index if not r['path'].startswith('tools/')]
    (OUT/'SOURCE_AND_REPORT_INDEX.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':make()
