"""Read-only CLI for the reusable empirical R5 profile, never exact coordinates."""
import sys,json
import work as w
import review as r
model=w.load('TRANSFORMATIONS.json')['selected_native']
if len(sys.argv) not in [4,5] or sys.argv[1] not in ['geo','pixel'] or (len(sys.argv)==5 and sys.argv[4]!='--allow-extrapolation'):raise SystemExit('Usage: query.py geo LONGITUDE LATITUDE | query.py pixel X Y [--allow-extrapolation]')
p=list(map(float,sys.argv[2:4]))
if sys.argv[1]=='geo':
    if not(-180<=p[0]<=180 and -90<=p[1]<=90):raise SystemExit('Invalid geographic range')
    geo=p;value=r.forward(model,[p])[0];label='Estimated bitmap XY'
else:
    if not(0<=p[0]<8192 and 0<=p[1]<3616):raise SystemExit('Pixel outside bitmap')
    value=r.inverse(model,[p])[0];geo=value.tolist();label='Estimated WGS84 lon lat'
outside=not r.in_support(model,geo)
if outside and len(sys.argv)!=5:raise SystemExit('Outside fitted convex-hull support. Refused by default; use --allow-extrapolation only for explicit diagnostics.')
print(json.dumps(dict(result_type=label,estimate=value.tolist(),outside_fit_support=outside,model='R5 geographic_axes local empirical',
    warning='Coarse Baltic/Polish region calibration, not a world projection or a political attribution. Four reserved physical points: mean2.08px, max3.19px; no guaranteed interval between points. Check domain/extrapolation in TRANSFORMATIONS.json.'),ensure_ascii=False,indent=2))
