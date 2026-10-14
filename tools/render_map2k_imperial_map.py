"""Render a data-driven map of frozen RGB rights, not a political-owner map."""
import json,re,struct
import numpy as np
from PIL import Image
from map2k_work import ROOT,GAME,OUT
from map2c_work import source_bitmap
from map2l_registry import active_registry_path
def render():
 ledger=json.loads(active_registry_path().read_text(encoding='utf-8'))
 im=Image.open(source_bitmap()).convert('RGB');a=np.asarray(im,dtype=np.uint32)
 packed=(a[:,:,0]<<16)|(a[:,:,1]<<8)|a[:,:,2]
 rights=np.array([int(r['rgb'][1:],16) for r in ledger],dtype=np.uint32)
 imperial=np.isin(packed,rights)
 ys,xs=np.nonzero(imperial);box=(max(0,int(xs.min())-35),max(0,int(ys.min())-35),min(im.width,int(xs.max())+36),min(im.height,int(ys.max())+36))
 x0,y0,x1,y1=box;p=packed[y0:y1,x0:x1];inside=imperial[y0:y1,x0:x1]
 terrain=ROOT/'map_data/province_terrains.txt'
 if not terrain.exists():terrain=GAME/'map_data/province_terrains.txt'
 sea=np.array([int(rgb,16) for rgb,t in re.findall(r'x([0-9A-Fa-f]{6})\s*=\s*"([^"]+)"',terrain.read_text(encoding='utf-8-sig')) if t in {'ocean','sea','lake'}],dtype=np.uint32)
 water=np.isin(p,sea);rgba=np.zeros((*p.shape,4),dtype=np.uint8);rgba[:]=[86,89,91,255];rgba[water]=[31,58,74,255];rgba[inside]=[238,202,64,255]
 edge=np.zeros(p.shape,dtype=bool);edge[:,1:]|=p[:,1:]!=p[:,:-1];edge[1:,:]|=p[1:,:]!=p[:-1,:]
 rgba[edge&~water]=[43,44,44,255]
 # Keep native bitmap proportions; never stretch geography to fill the widget.
 fitted=Image.fromarray(rgba)
 scale=min(1000/fitted.width,740/fitted.height)
 fitted=fitted.resize((round(fitted.width*scale),round(fitted.height*scale)),Image.Resampling.NEAREST)
 out=Image.new('RGBA',(1000,740),(31,58,74,255));out.paste(fitted,((1000-fitted.width)//2,(740-fitted.height)//2))
 folder=ROOT/'gfx/interface/journal_entries';folder.mkdir(parents=True,exist_ok=True)
 source=ROOT/'workshop_assets/source/map2k_hre_registered_map.png';out.save(source)
 levels=[];w,h=out.size
 while True:
  pixels=np.asarray(out.resize((w,h),Image.Resampling.LANCZOS),dtype=np.uint8)
  levels.append(pixels[:,:,[2,1,0,3]].tobytes())
  if w==h==1:break
  w=max(1,w//2);h=max(1,h//2)
 header=bytearray(128);header[:4]=b'DDS '
 for off,val in [(4,124),(8,0x2100f),(12,740),(16,1000),(20,4000),(28,len(levels)),(76,32),(80,0x41),(88,32),(92,0xff0000),(96,0xff00),(100,0xff),(104,0xff000000),(108,0x401008)]:struct.pack_into('<I',header,off,val)
 (folder/'aor1776_hre_registered_map.dds').write_bytes(header+b''.join(levels))
 report=dict(provinces=len(ledger),crop=box,size=[1000,740],water_RGBs=len(sea),basis='Frozen imperial RGB registry; independent of current owner; this is a journal map, NOT a new main-map painting mode')
 (OUT/'FEEDBACK_MAP_VALIDATION.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(report)
if __name__=='__main__':render()
