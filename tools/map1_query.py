"""Read-only spatial search; all coordinates are game pixels, never GPS."""
import argparse,csv,sys
from map1_prepare import OUT,table

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--state'); p.add_argument('--owner'); p.add_argument('--toponym'); p.add_argument('--band')
    p.add_argument('--pixel',nargs=2,type=float,metavar=('X','Y'))
    p.add_argument('--bbox',nargs=4,type=float,metavar=('X0','Y0','X1','Y1'))
    p.add_argument('--limit',type=int,default=50)
    args=p.parse_args(); records=table(OUT/'MAP1_BASELINE_PROVINCE_INDEX.csv'); rows=[]
    if args.pixel:
        import numpy as np
        x,y=args.pixel; arr=np.load(OUT/'MAP1_GEOGRAPHIC_EVIDENCE/pixel_index.npz')['rgb']
        if not 0<=y<3616: p.error('Y must be in [0,3616)')
        pixel='x%06X'%int(arr[int(y),int(x)%8192])
    else: pixel=None
    for r in records:
        if args.state and r['State_ID']!=args.state: continue
        if args.owner and r['Owner_TAG']!=args.owner: continue
        if args.toponym and args.toponym.lower() not in (r['State_ID']+' '+r['Hub_Anchors']+' '+r['Owner_Name']).lower(): continue
        if args.band and r['Pixel_Band']!=args.band: continue
        if pixel and r['Province_ID']!=pixel: continue
        if args.bbox:
            a,b,c,d=args.bbox
            if float(r['Pixel_X_Max_Exclusive'])<=a or float(r['Pixel_X_Min'])>=c or float(r['Pixel_Y_Max_Exclusive'])<=b or float(r['Pixel_Y_Min'])>=d: continue
        rows.append(r)
    fields=['Province_ID','State_ID','Owner_TAG','Province_Pixels','Hub_Anchors','Pixel_Band','Known_Issue_IDs','Geographic_Confidence']
    sys.stdout.reconfigure(encoding='utf-8'); writer=csv.DictWriter(sys.stdout,fields,extrasaction='ignore'); writer.writeheader(); writer.writerows(rows[:args.limit])
    print(f'{len(rows)} attribution rows matched; output limited to {args.limit}. No historical match implied.',file=sys.stderr)
if __name__=='__main__': main()
