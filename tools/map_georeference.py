"""Local read-only georeferencing workbench and reusable MAP command line."""
import argparse
import hashlib
import io
import json
import math
import mimetypes
from pathlib import Path
import re
import threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
import numpy as np
from PIL import Image,ImageDraw
from georeference.model import fit,forward,inverse,evaluate,grid_lines

ROOT=Path(__file__).resolve().parents[1]
ASSETS=Path(__file__).resolve().parent/'georeference'
DEFAULT=ASSETS/'controls.example.json'
GAME=Path('C:/Games/Victoria 3/game')

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def output_path(path,inputs=()):
    """Diagnostic outputs only: never overwrite game/mod assets or inputs."""
    target=Path(path).resolve()
    if target in [Path(p).resolve() for p in inputs]:raise ValueError('Un résultat ne peut pas remplacer sa source.')
    if not target.is_relative_to(ROOT):raise ValueError('Exporter dans le dépôt, sous tools/georeference ou docs/reports.')
    if not any(target.is_relative_to(base) for base in [ASSETS,ROOT/'docs/reports']):
        raise ValueError('Sortie limitée aux dossiers de diagnostic ; fichiers de jeu protégés.')
    if target.exists():raise ValueError('La sortie existe déjà : choisir un nouveau nom pour préserver les résultats.')
    target.parent.mkdir(parents=True,exist_ok=True)
    return target

def make_model(payload):
    if not isinstance(payload,dict):raise ValueError('Objet JSON requis.')
    rows=payload.get('controls',load(DEFAULT)['controls'])
    if len(rows)>200:raise ValueError('200 points maximum.')
    return fit(rows,payload.get('kind','miller_affine'),(8192,3616))

def render_grid(model,spacing=1,clip_domain=True):
    image=Image.new('RGBA',tuple(model['dimensions']),(0,0,0,0));draw=ImageDraw.Draw(image)
    w,h=image.size
    for line in grid_lines(model,spacing,clip_domain):
        # Clip individual segments through Pillow's raster boundary handling.
        points=line['pixels'];color=(30,105,220,190) if line['axis']=='lon' else (195,70,40,190)
        for a,b in zip(points,points[1:]):
            if max(a[0],b[0])<0 or min(a[0],b[0])>=w or max(a[1],b[1])<0 or min(a[1],b[1])>=h:continue
            draw.line([tuple(a),tuple(b)],fill=color,width=1)
    return image

def warp_raster(image,source_model,target_model,box):
    """Explicit geographic chain, for later historical scan profiles (no owner)."""
    x0,y0,x1,y1=map(int,box)
    if not (0<x1-x0<=4096 and 0<y1-y0<=4096):raise ValueError('Zone de warp maximale 4096×4096.')
    mesh=[];step=16
    for y in range(0,y1-y0,step):
        for x in range(0,x1-x0,step):
            right=min(x+step,x1-x0);bottom=min(y+step,y1-y0)
            dest=[[x+x0,y+y0],[x+x0,bottom+y0],[right+x0,bottom+y0],[right+x0,y+y0]]
            src=forward(source_model,inverse(target_model,dest)).reshape(-1).tolist()
            mesh.append(((x,y,right,bottom),src))
    return image.convert('RGBA').transform((x1-x0,y1-y0),Image.Transform.MESH,mesh,resample=Image.Resampling.BILINEAR)

class Workbench:
    def __init__(self,bitmap):
        self.bitmap=Path(bitmap).resolve()
        self.image=Image.open(self.bitmap).convert('RGB')
        if self.image.size!=(8192,3616):raise ValueError('Bitmap 8192×3616 requis pour cet exemple Victoria 3.')
        self.bitmap_hash=digest(self.bitmap)
        self.lock=threading.Lock()
        self.controls=load(DEFAULT)
    def handler(self):
        workspace=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def send(self,status,data,content='application/json',filename=None):
                if content=='application/json':data=json.dumps(data,ensure_ascii=False,allow_nan=False).encode('utf-8')
                self.send_response(status);self.send_header('Content-Type',content);self.send_header('Content-Length',str(len(data)))
                self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store')
                self.send_header('Content-Security-Policy',"default-src 'self'; img-src 'self' blob: data:; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
                if filename:self.send_header('Content-Disposition','attachment; filename="'+filename+'"')
                self.end_headers();self.wfile.write(data)
            def do_GET(self):
                if self.headers.get('Host','').split(':')[0] not in ['127.0.0.1','localhost']:return self.send(403,{'error':'Hôte refusé.'})
                try:
                    parsed=urlparse(self.path)
                    if parsed.path=='/api/session':
                        return self.send(200,{**workspace.controls,'bitmap_sha256':workspace.bitmap_hash,'dimensions':[8192,3616],
                            'bitmap_name':workspace.bitmap.name,'native_equator_y':3616*.58,'native_equator_note':'Repère graphique officiel, pas une preuve de projection exacte.'})
                    if parsed.path=='/api/bitmap':
                        query=parse_qs(parsed.query);raw=query.get('box',['0,0,8192,3616'])[0]
                        box=list(map(int,raw.split(',')))
                        if len(box)!=4 or not (0<=box[0]<box[2]<=8192 and 0<=box[1]<box[3]<=3616):raise ValueError('Découpe hors bitmap.')
                        with workspace.lock:im=workspace.image.crop(tuple(box))
                        im.thumbnail((1600,1100),Image.Resampling.NEAREST)
                        stream=io.BytesIO();im.save(stream,format='PNG');return self.send(200,stream.getvalue(),'image/png')
                    if parsed.path=='/':target=ASSETS/'index.html'
                    elif parsed.path in ['/app.js','/style.css']:target=ASSETS/parsed.path[1:]
                    else:return self.send(404,{'error':'Ressource inconnue.'})
                    return self.send(200,target.read_bytes(),mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
                except (ValueError,KeyError,TypeError) as e:self.send(400,{'error':str(e)})
            def do_POST(self):
                # Same-origin POST only. The server never writes uploaded files.
                origin=self.headers.get('Origin');host=self.headers.get('Host','')
                if origin and origin!='http://'+host:return self.send(403,{'error':'Origine refusée.'})
                if host.split(':')[0] not in ['127.0.0.1','localhost']:return self.send(403,{'error':'Hôte refusé.'})
                try:
                    length=int(self.headers.get('Content-Length','0'))
                    if not 0<length<=300000:raise ValueError('Corps JSON trop volumineux.')
                    body=json.loads(self.rfile.read(length));model=make_model(body)
                    if self.path=='/api/fit':
                        return self.send(200,{'model':model,'evaluation':evaluate(model),
                            'grid':grid_lines(model,float(body.get('spacing',1)),not body.get('extrapolate',False))})
                    if self.path=='/api/convert':
                        direction=body.get('direction','geo_to_pixel');point=body['point']
                        if not isinstance(point,list) or len(point)!=2:raise ValueError('Deux coordonnées requises.')
                        result=forward(model,[point])[0] if direction=='geo_to_pixel' else inverse(model,[point])[0]
                        if direction not in ['geo_to_pixel','pixel_to_geo']:raise ValueError('Direction inconnue.')
                        return self.send(200,{'result':result.tolist(),'status':model['status']})
                    if self.path=='/api/export':
                        grid=render_grid(model,float(body.get('spacing',1)),not body.get('extrapolate',False))
                        stream=io.BytesIO();grid.save(stream,format='PNG')
                        return self.send(200,stream.getvalue(),'image/png','geographic-grid-8192x3616.png')
                    return self.send(404,{'error':'Action inconnue.'})
                except (ValueError,TypeError,KeyError,np.linalg.LinAlgError,json.JSONDecodeError) as e:self.send(400,{'error':str(e)})
        return Handler

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    serve=sub.add_parser('serve');serve.add_argument('--port',type=int,default=8766);serve.add_argument('--bitmap',type=Path,default=ROOT/'map_data/provinces.png')
    calibrate=sub.add_parser('calibrate');calibrate.add_argument('--controls',type=Path,default=DEFAULT);calibrate.add_argument('--kind',choices=['miller_affine','geographic_affine','miller_axes','native_miller_hypothesis'],default='miller_affine');calibrate.add_argument('--output',type=Path,required=True)
    convert=sub.add_parser('convert');convert.add_argument('--profile',type=Path,required=True);convert.add_argument('--inverse',action='store_true');convert.add_argument('a',type=float);convert.add_argument('b',type=float)
    export=sub.add_parser('grid');export.add_argument('--profile',type=Path,required=True);export.add_argument('--spacing',type=float,default=1);export.add_argument('--extrapolate',action='store_true');export.add_argument('--output',type=Path,required=True)
    warp=sub.add_parser('warp');warp.add_argument('--image',type=Path,required=True);warp.add_argument('--source-profile',type=Path,required=True);warp.add_argument('--target-profile',type=Path,required=True);warp.add_argument('--box',required=True);warp.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='serve':
        work=Workbench(args.bitmap);server=ThreadingHTTPServer(('127.0.0.1',args.port),work.handler());server.daemon_threads=True
        print('Géoréférencement : http://127.0.0.1:'+str(server.server_port)+' — bitmap en lecture seule',flush=True)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
        finally:server.server_close()
    elif args.command=='calibrate':
        target=output_path(args.output,[args.controls]);doc=load(args.controls);model=fit(doc['controls'],args.kind,doc.get('dimensions',[8192,3616]))
        result={'model':model,'evaluation':evaluate(model),'source_controls_sha256':digest(args.controls)}
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'fit':result['evaluation']['fit'],'check':result['evaluation']['check'],'accuracy':result['evaluation']['accuracy_status']},ensure_ascii=False))
    elif args.command=='convert':
        doc=load(args.profile);model=doc.get('model',doc);fn=inverse if args.inverse else forward
        print(json.dumps(fn(model,[[args.a,args.b]])[0].tolist()))
    elif args.command=='grid':
        target=output_path(args.output,[args.profile])
        doc=load(args.profile);model=doc.get('model',doc)
        render_grid(model,args.spacing,not args.extrapolate).save(target);print('PNG transparent',target)
    else:
        destination=output_path(args.output,[args.image,args.source_profile,args.target_profile])
        source=load(args.source_profile);target=load(args.target_profile)
        warp_raster(Image.open(args.image),source.get('model',source),target.get('model',target),list(map(int,args.box.split(',')))).save(destination)

if __name__=='__main__':main()
