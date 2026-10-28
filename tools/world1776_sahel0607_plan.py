"""Explicit reviewed native-province envelopes; no automatic geographic partition."""
import json
import world1776_sahel0607_inspect as q
ROOT,LOT,ST=q.ROOT,q.LOT,q.ST
PREFIX='1776_world_sahel0607'
BASE=list(q.previous.planmod.BASE)
RURAL=list(q.previous.planmod.RURAL)
MIL=q.previous.planmod.MIL

# Central polities use negotiated local trade customs, not maritime insurance.
# These are local knowledge profiles, never a tier or metropolitan copy.
COUNTRIES={
 'MDR':dict(fr='Mandara',en='Mandara',adj_fr='mandara',adj_en='Mandaran',color=[190,147,81],culture=['kanuri'],religion='sunni',capital='STATE_BORNU',tech=BASE+[MIL],basis='Dulo/Doulo sultanate, royal retainers, farming/cattle, iron/textiles and exchange with Bornu; Barkindo UNESCO V ch17. Kanuri is a native regional proxy, not a Mandara ethnic census.'),
 'BIL':dict(fr='Fitri',en='Fitri',adj_fr='bilala',adj_en='Bilala',color=[120,167,133],culture=['baguirmi'],religion='sunni',capital='STATE_CHAD',tech=BASE,basis='Bilala/Yao authority around Lake Fitri; cereal cultivation, livestock, fishing and market exchange. Baguirmi is a broad native linguistic-area proxy; exact 1776 external tribute is unresolved.'),
 'DLS':dict(fr='Dar Sila',en='Dar Sila',adj_fr='du Dar Sila',adj_en='Dar Sila',color=[145,116,169],culture=['fur'],religion='sunni',capital='STATE_CHAD',tech=RURAL+['international_relations',MIL],basis='Daju frontier sultanate, cattle/farming, metalworking, armed retainers and negotiation with Wadai/Darfur; Kapteijns 1983 and Triaud 1990. Fur is a native regional proxy; no Daju culture exists.'),
 'SNR':dict(fr='Sennar',en='Sennar',adj_fr='sennarien',adj_en='Sennari',color=[65,143,132],culture=['sudanese'],religion='sunni',capital='STATE_BLUE_NILE',tech=BASE+[MIL],basis='Funj/Hamaj court on Blue Nile, irrigated/rain-fed farming, livestock, weaving, craft production, caravan diplomacy and established military service; Hasan/Ogot ch7.'),
 'ABD':dict(fr='Abdallab',en='Abdallab',adj_fr='abdallabi',adj_en='Abdallabi',color=[178,144,83],culture=['sudanese','bedouin'],religion='sunni',capital='STATE_DONGOLA',tech=BASE+[MIL],basis='Northern Funj feudatories, Nile/Atbara and Butana chiefly communities, farming/livestock, weaving, crafts, trade and armed retainers; Hasan/Ogot and O Fahey/Spaulding. Aggregate political envelope, not direct administration of every village.'),
 'SHQ':dict(fr='Shayqiyya',en='Shayqiyya',adj_fr='shayqi',adj_en='Shayqi',color=[126,148,183],culture=['sudanese'],religion='sunni',capital='STATE_DONGOLA',tech=BASE+[MIL],basis='Independent Nile-bend chiefly kingdoms with cavalry/retainers, river agriculture, cattle, weaving and trading contacts. The country aggregates several makks; not a single invented dynasty.'),
 'DNG':dict(fr='Dongola',en='Dongola',adj_fr='dongolais',adj_en='Dongolawi',color=[178,124,107],culture=['sudanese'],religion='sunni',capital='STATE_DONGOLA',tech=BASE+[MIL],basis='Zubayr makks before the Shayqiyya conquest of the 1780s; river farming, cattle, weaving, crafts and Nile commerce. Sudanese is the available Nubian-area proxy; nuba is deliberately not substituted for Nubian.'),
 'NUB':dict(fr='Nubie ottomane',en='Ottoman Nubia',adj_fr='nubien',adj_en='Nubian',color=[166,155,112],culture=['sudanese','bedouin'],religion='sunni',capital='STATE_DONGOLA',tech=BASE+[MIL],basis='Hereditary Nubian kashifs and fortified garrison corridor south of Aswan, nominal Ottoman-Egyptian dependency; Hasan/Ogot and Beska. Distinct from Dongola and from the Egyptian conquest of 1820/21.'),
 'MSB':dict(fr='Musabbaat',en='Musabbaat',adj_fr='musabbaat',adj_en='Musabbaat',color=[183,130,73],culture=['fur','sudanese'],religion='sunni',capital='STATE_KORDOFAN',tech=RURAL+['international_relations',MIL],basis='Hashim/Musabbaat central Kordofan royal and military network, farming/cattle, craft and caravan contacts, restored around 1772; O Fahey/Spaulding 1972. Not Darfur annexation of 1785/86.'),
 'TQL':dict(fr='Taqali',en='Taqali',adj_fr='taqali',adj_en='Taqali',color=[138,169,87],culture=['nuba'],religion='sunni',capital='STATE_KORDOFAN',tech=RURAL+['international_relations',MIL],basis='Northeastern Nuba highland kings and protective brokerage, cereal/cattle economy, iron crafts and armed service. Ewald 1990/published archaeological reconnaissance; exact consolidation date and alleged Funj tributary relation remain debated.'),
 'SLQ':dict(fr='Shilluk',en='Shilluk',adj_fr='shilluk',adj_en='Shilluk',color=[124,169,153],culture=['nilotic'],religion='animist',capital='STATE_BLUE_NILE',tech=BASE+[MIL],basis='Reth kingship, sedentary cattle/cereal villages and Nile ferry/trade authority up to Alays attested by Bruce in 1772; Hasan/Ogot ch7. Nilotic is the native broad culture identifier, not a Dinka replacement.'),
 'SRA':dict(fr='Sara',en='Sara',adj_fr='sara',adj_en='Sara',color=[179,236,217],culture=['sara'],religion='animist',capital='STATE_WADDAI',kind='decentralized',tech=RURAL,basis='Native dormant Sara tag activated for plural southern Chari communities; raiding/tribute spheres are not permanent Wadai government. Rural capabilities only, no united Sara kingdom asserted.'),
}

def make_plan(text):
    cells=json.loads((LOT/'GEOMETRY_CELLS.json').read_text('utf8'))
    index={key:{r[key]:r for r in cells if key in r} for key in ['CHAD_index','NILE_index']}
    result=[];used=set()
    def pick(key,source,target,indices,basis):
        rows=[index[key][i] for i in indices]
        assert all(r['owner']==source for r in rows),(source,target,[(r[key],r['owner']) for r in rows])
        for sid in dict.fromkeys(r['state'] for r in rows):
            chosen=[r['RGB'] for r in rows if r['state']==sid]
            assert not used&set(chosen),(source,target,'duplicate transfer')
            used.update(chosen)
            result.append(dict(state=sid,source=source,target=target,RGBs=chosen,historical_basis=basis,
                precision='POLITICAL_APPROXIMATION_NATIVE_PROVINCES_NOT_CADASTRAL'))
    C='CHAD_index';N='NILE_index'
    pick(C,'TBI','WAD',[213],'Wara historical Wadai royal core immediately north of Abeche; locality is a diagnostic anchor, frontier an explicit native-province approximation.')
    pick(C,'BOR','MDR',[357,368,370],'Northern Mandara/Dulo approaches adjoining Bornu; local sultanate and Bornu tributary relationship, before revolt circa 1781.')
    pick(C,'BGI','MDR',[278],'Doulo/Mandara eastern native province; no wholesale annexation of the Mandara mountains.')
    pick(C,'WAD','BIL',[197,177,266,160],'Lake Fitri/Yao Bilala local royal core, not direct Wadai administration; external suzerainty fluctuates and is not fixed without a dated 1776 source.')
    pick(C,'WAD','DLS',[137,161,243,205,192,265,211,230,131],'Daju Dar Sila core south of Wadai between Wadai and Darfur; bounded native envelope including its internal cell, no nineteenth-century Dar Masalit projected backwards.')
    pick(C,'WAD','DLS',[301,299],'Southern continuation of the same Dar Sila envelope, contiguous with its Goz Beida core.')
    pick(C,'WAD','BGI',[107,341,325,326,330,319,340,339,313,350,332,327],'Bokoro and eastern Chari/Massenya Baguirmi royal hinterland, separate from later Wadai domination; approximate direct/tributary boundary on native edges, no detached southern outposts.')
    # Southern communities outside the reviewed Wadai/Baguirmi/Dar Sila cores.
    remaining=[r[C] for r in cells if r['state']=='STATE_WADDAI' and r['owner']=='WAD' and r['RGB'] not in used]
    pick(C,'WAD','SRA',remaining,'Southern Chari/Sara plural communities, beyond the royal cores; raiding range does not establish territorial annexation.')
    pick(C,'BGI','SRA',[273,280,288,296,297,314,321,336,338,343,345,346,348],'Southern portion of inherited Bagirmi outline beyond the retained Massenya/Chari core; decentralised communities, not a single new kingdom.')
    pick(N,'SD1','EGY',[74,42,50,47,69,64,68,48,95],'Aswan and Kharga Egyptian authority; native corridor between oasis and Nile retained for gameplay, not a surveyed desert border. Michel/IFAO Ottoman oasis research.')
    pick(N,'SD1','NUB',[52,77,76,205,223,146,142,124,155,118],'Nile/Abu Simbel-Wadi Halfa-Say kashif and garrison corridor; local Ottoman-Egyptian dependency, no eastward desert strip or blanket conquest of Sudan.')
    pick(N,'SD1','DNG',[204,104,115,113,107,99,201,148],'Kerma/Old Dongola Zubayr royal riverine core before Shayqiyya annexation of the 1780s.')
    pick(N,'SD1','SHQ',[139,224,105,110,226,189,164,119],'Shayqiyya great Nile bend chiefly kingdoms; several makks aggregated, no later conquest of Dongola anticipated.')
    pick(N,'SD1','ABD',[161,179,144,131,214,165,114,196,171,158,102,120,213,143],'Northern Funj Abdallab Nile/Atbara chiefly and tributary envelope, distinct from Dongola and Shayqiyya.')
    pick(N,'SD1','ABD',[311,354,363,326,360,334,342,341,335],'Kerri/Halfaya and northern Gezira/Butana core of the Abdallab feudatories, linked to the northern Nile portion.')
    pick(N,'SD1','SNR',[314,347,356,358,374,365,369,378,381,336,340,367,352,327,329,332,355,313,324,328,319,350,312,382],'Funj/Hamaj Sennar Blue Nile core from Arbaji/central Gezira towards Fazughli; not the whole modern Sudan or Ethiopian highlands.')
    pick(N,'SD1','SLQ',[343,370,345,315,349,379,339,368,380,361,364,377],'Shilluk riverine envelope from Alays south along White Nile; broad native cells may straddle bank, not exclusive ethnic ownership of both banks.')
    pick(N,'SD1','SLQ',[239],'West-bank White Nile link within the same Shilluk riverine envelope; retains continuity without assigning the Melut east-bank province.')
    pick(N,'SD1','MSB',[310,255,304,267,276,254,232,301,242,244,256,230,240,275,264,268,251,235],'Central Kordofan Musabbaat/Hashim local authority and routes, between Darfur claims, pastoral autonomy and Funj influence; not all Kordofan.')
    pick(N,'SD1','TQL',[265,243],'Two native provinces around northeastern Taqali/Rashad massif, not all Nuba mountains; independent core without imposing disputed Funj vassalage.')
    return result

if __name__=='__main__':
    data=make_plan(q.previous.raw(ROOT/ST));q.dump('PLAN.json',data);q.dump('COUNTRY_PROFILES.json',COUNTRIES)
    print(len(data),'groups;',sum(len(r['RGBs']) for r in data),'native province transfers;',len(COUNTRIES),'country profiles.')
