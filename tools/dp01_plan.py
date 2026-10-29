"""Bounded settlement cores; province envelopes are explicit gameplay approximations."""
from dp01_geography import *
import heapq
def plan():
 g=load('GEOMETRY.json');ow=ownership();regs={n.key:n for p in effective('map_data/state_regions') for n in parse(text(p))}
 im=np.asarray(Image.open(ROOT/'map_data/provinces.png').convert('RGB'),np.uint32);a=(im[:,:,0]<<16)|(im[:,:,1]<<8)|im[:,:,2]
 imp={r for n in regs.values() for r in provs(n,'impassable')};permitted={r for r,z in g.items() if z['owners'] and z['owners'][0][1]=='DUR' and z['owners'][0][0] in ['STATE_BALUCHISTAN','STATE_QUETTA'] and 5598<=z['center'][0]<=5657 and 1390<=z['center'][1]<=1480 and r not in imp}
 seeds=['x6F000D','x43F4B8','xBAE3D2','xF78D0D','xEC696F','x2B7441','x782112']
 adj=graph(a,np.array([int(r[1:],16) for r in permitted],np.uint32));result={seeds[0]}
 for target in seeds[1:]:
  q=[(0,int(r[1:],16)) for r in result];heapq.heapify(q);cost={v:0 for d,v in q};prev={};t=int(target[1:],16)
  while q:
   d,u=heapq.heappop(q)
   if d!=cost[u]:continue
   if u==t:break
   for v,b in adj[u].items():
    r=f'x{v:06X}'
    if r not in permitted or b<2:continue
    nd=d+float(np.linalg.norm(np.array(g[f'x{u:06X}']['center'])-g[r]['center']))
    if nd<cost.get(v,1e99):cost[v]=nd;prev[v]=u;heapq.heappush(q,(nd,v))
  assert t in cost,target
  while f'x{t:06X}' not in result:result.add(f'x{t:06X}');t=prev[t]
 # Fill only cells with three selected edge neighbours inside the bounded core.
 extra={r for r in permitted-result if r!='x5CBA3C' and sum(f'x{v:06X}' in result and b>=2 for v,b in adj[int(r[1:],16)].items())>=3};result|=extra
 rows=[]
 for r in sorted(result):rows.append(dict(rgb=r,state=g[r]['owners'][0][0],before='DUR',after='KAL',basis='Sarawan/Jhalawan/Kacchi and Shal/Quetta settlement core; excludes Pishin, Kharan, Las Bela and Makran; whole-cell gameplay envelope.'))
 for r in ['xA98EF8','x280F05','x96E54B','xDEFFE6']:rows.append(dict(rgb=r,state='STATE_HILL_PUNJAB',before='DUR',after='PAN',basis='Existing collective Sikh misls representation extended to adjacent plains around the native Amritsar/Ludhiana hubs; no unification under Ranjit Singh.'))
 for r in ['xA07020','x5A5F96','x394B7F']:rows.append(dict(rgb=r,state='STATE_HILL_PUNJAB',before='DUR',after='PTA',basis='Patiala/Sirhind core; three whole provinces approximate local rule, not all cis-Sutlej chiefships.'))
 for z in rows:assert ow[z['rgb']]=={(z['state'],z['before'])}
 after={r.upper():vs.copy() for r,vs in ow.items()}
 for z in rows:after[z['rgb'].upper()]={(z['state'],z['after'])}
 dump('PLAN.json',dict(reference_date='1776-01-01',scope=['STATE_BALUCHISTAN','STATE_QUETTA','STATE_HILL_PUNJAB','STATE_PUNJAB'],transfers=rows,kalat_seeds=seeds,kalat_intervening_cells=sorted(result-set(seeds)),whole_province_approximation=True,new_RGBs=False,new_State_IDs=False,restored_existing_tags=['KAL','PTA'],unchanged_multan='Both native Multan locator x918140 and the calibrated broader Multan area are already PAN; no conquest transfer.',unresolved=['Kharan/Makran/Las Bela beyond existing Gwadar MAK; exact dates and local rule need separate subdivision.','Remaining Himalayan chiefships, Jammu and Ladakh must not be certified as directly Durrani.','Bahawalpur and other fragmented cis-Sutlej chiefships need their own territorial mapping.']))
 draw(a,after,load('SITE_PROXIES.json'),load('VIEW_BOX.json'),'PROPOSED_MAP.png')
 print(json.dumps(dict(transfers=len(rows),kalat=len(result),patiala=3,misls=4,kalat_rgb=sorted(result))))
if __name__=='__main__':plan()
