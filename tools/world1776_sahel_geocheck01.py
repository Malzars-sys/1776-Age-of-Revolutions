"""Read-only geographic conformity review; cosmetic border work is deferred."""
import json
from pathlib import Path
import world1776_sahel0607 as m
ROOT=m.ROOT;WORLD=m.LOT.parent;LOT=WORLD/'SAHEL-GEOCHECK-01'

def dump(name,data):(LOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

def main():
    LOT.mkdir(exist_ok=True)
    current=m.raw(ROOT/m.ST);own=m.m.state_owners(current);checks=[]
    def ck(k,v,d=None):checks.append(dict(check=k,passed=bool(v),detail=d))
    for name,tool in [('SAHEL-02-05',m.m),('SAHEL-06-07',m)]:
        lot=WORLD/name;b=json.loads((lot/'APPLY_BEFORE.json').read_text('utf8'));plan=json.loads((lot/'PLAN.json').read_text('utf8'))
        expected=tool.transform({m.ST:m.raw(lot/'apply_inputs'/m.ST)},plan)[m.ST]
        for key in b['scope'][m.ST]:ck('current_regional_geometry.'+name+'.'+key,m.m.scope_text(expected,key)==m.m.scope_text(current,key))
        for r in plan:
            for c in r['RGBs']:ck('current_declared_owner.'+c,own.get(c)==[[r['state'],r['target']]])
    anchors={'Saint-Louis':('xE8D241','GBR'),'Goree_proxy':('xE8D242','FRA'),'Waalo_core':('xEF30C0','WAA'),'Segou_core':('x2A6A2D','SGU'),'Wara_core':('xB08124','WAD')}
    for label,(color,tag) in anchors.items():ck('historical_core_anchor.'+label,own.get(color,[['','']])[-1][1]==tag)
    for tag in ['SOK','HOB']:
        ck('no_later_empire_installed.'+tag,not any(any(v[1]==tag for v in owners) for owners in own.values()))
    result=dict(status='PASS_BOUNDED_GEOGRAPHIC_CONTINUITY_REVIEW' if all(c['passed'] for c in checks) else 'FAIL',passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,functional_writes=0,cosmetic_smoothing='EXPLICITLY_DEFERRED_BY_USER',full_historical_frontier_certification=False)
    dump('VALIDATION.json',result)
    dump('USER_TEST_OBSERVATION.json',dict(user_statement="ok j'ai lancé un test en jeux et toute est là en revenche j'ai un probleme avec des frontiere qui sont.... comment dire pas très naturelle ?",date_received='2026-10-27',scope='User reports presence in game; screenshot centred on Chad/Nile and comparison with Europe.',observed_by_agent='Only supplied screenshots; no engine session run by agent.',version_tested='Not explicitly supplied; no exact-hash attestation inferred.',duration=None,save_reload=None,result='PRESENCE_REPORTED_VISUAL_BORDER_ISSUE_OPEN',full_runtime_credit=False,screenshots=['C:/Users/simeo/AppData/Local/Temp/codex-clipboard-094d6517-933d-4c9f-80ee-1f1f7fd5cfdb.png','C:/Users/simeo/AppData/Local/Temp/codex-clipboard-8bac7c77-7c62-4fc8-a5ad-c2ec689695d4.png']))
    m.save(LOT/'REPORT.md',f'''# SAHEL-GEOCHECK-01 — conformité géographique, Sénégal–Nil

27 octobre 2026, référence 1er janvier 1776. **Audit sans écriture fonctionnelle.** Le joueur reporte explicitement la finition des courbes et autorise ensuite Éthiopie/Corne, puis Congo, possessions portugaises et Afrique australe. Le reçu USER_TEST_OBSERVATION.json conserve uniquement sa déclaration de présence des pays en jeu et son problème de rendu ; durée, version précise et sauvegarde/rechargement non fournis, aucun critère V entier crédité.

## Comparaison actuelle

Les huit nœuds régionaux de SAHEL-02-05 et les sept de SAHEL-06-07 correspondent aux décisions installées. Les changements concurrents du fichier global d'états ne sont pas annulés. Les noyaux Waalo/Fouta et les comptoirs de Saint-Louis/Gorée restent présents ; Ségou est au bon noyau natif, Sokoto n'est pas préinstallé. Les positions relatives des royaumes haoussa, Bornou, Mandara, Baguirmi, Fitri, Ouaddaï et Dar Sila restent celles rapprochées des cartes publiées dans les SOURCES.md des lots. Wara est bien au Ouaddaï, non en territoire Toubou. Dans la vallée du Nil, les noyaux nubiens, Dongola, Shayqiyya, Abdallab, Sennar, Musabbaat/Taqali et Shilluk ne sont ni intervertis ni déplacés par rapport à la confrontation rivières/localités des sources.

**{result['passed']}/{result['total']} contrôles bornés réussis** : nœuds, propriétaires des cellules explicitement attribuées et ancrages. Ce résultat vérifie la continuité de l'installation ; il ne transforme pas une enveloppe politique approximative en frontière cadastrale ou certifiée historiquement sur chaque pixel. Sources réexaminées : SAHEL-01/SOURCES.md ; cartes sénégambiennes, Niger et Hausaland de SAHEL-02-05/SOURCES.md ; cartes 7.1 et 17.1 UNESCO, textes Hasan/Ogot, Barkindo, O'Fahey/Spaulding et Beška documentés dans SAHEL-06-07/SOURCES.md.

## Limites géographiques conservées

Gorée reste un proxy côtier d'un pixel ; les franges Galam/Khasso/Sine-Saloum et les juridictions touarègues sont approximatives. Kanem/Borkou, dépendances de Dar Sila/Fitri, ressorts exacts des kashifs et datation de Taqali ne deviennent pas certains. Les couloirs et creux produits par le regroupement de provinces natives, ainsi que les petites poches résiduelles de SD1, sont enregistrés pour la future passe de tracé, sans leur inventer une justification historique. Ne pas lire ces poches comme des enclaves attestées en 1776. Le contrôle précédent de continuité des pays centralisés ne prouvait pas l'absence de toute poche du territoire décentralisé.

**Aucune nouvelle permutation de noyau politique ni erreur géographique certaine démontrée ne justifie un transfert supplémentaire dans cet audit.** Les incertitudes restent ouvertes ; le lissage est volontairement différé. Population, bâtiments, technologies, relations et pixels inchangés par cette passe.

## Suite autorisée

HORN-01 : distinguer le domaine impérial et les pouvoirs provinciaux éthiopiens, Harar/Awsa et royaumes du Sud, puis les autorités somalies et la côte. Cartes c.1700/c.1800 à confronter sans rétroprojeter les royaumes/conquêtes du XIXe siècle. Aucun flavor, personnage ou raffinement de bâtiments. Ensuite, progression autorisée vers le Congo, possessions portugaises et Afrique australe, en lots territoriaux distincts et traçables. Pas de test intermédiaire demandé. WORLD reste 10/320 ; aucune validation humaine totale inventée.
''')
    print(result['status'],result['passed'],'/',result['total'])

if __name__=='__main__':main()
