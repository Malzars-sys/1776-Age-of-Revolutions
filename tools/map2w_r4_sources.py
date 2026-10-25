"""Bounded public-source retrieval for R4, never a bulk geographic download."""
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
import xml.etree.ElementTree as ET

OUT=Path(__file__).resolve().parents[1]/'docs/reports/map/MAP2W/R4/EVIDENCE'
URL='https://geoservices.bayern.de/wfs/v1/ogc_atkis_basisdlm.cgi'
# Orientation windows, NOT accepted exact mouth coordinates. Control extraction
# must inspect the returned network and distinguish banks, axes and side arms.
WINDOWS={
 'ILLER':(9.965,48.36,10.015,48.405),
 'LECH':(10.90,48.71,10.95,48.76),
 'ISAR':(12.95,48.78,13.01,48.83),
 'INN':(13.44,48.55,13.50,48.60),
 'SALZACH':(12.90,48.18,12.96,48.24),
}
def main():
    import sys
    kind='AX_Gewaesserstationierungsachse' if '--station' in sys.argv else 'AX_Gewaesserachse'
    log=[]
    for name,bounds in WINDOWS.items():
        p=OUT/(name+('_STATION_4326.gml' if '--station' in sys.argv else '_AXES_4326.gml'))
        # The service advertises EPSG:4326, with its formal lat/lon axis order;
        # CRS84 is not advertised. Explicit namespace fixes its BBOX parser.
        lon0,lat0,lon1,lat1=bounds
        params=dict(service='WFS',version='2.0.0',request='GetFeature',typenames='adv:'+kind,count=1000,srsName='urn:ogc:def:crs:EPSG::4326',namespaces='xmlns(adv,http://www.adv-online.de/namespaces/adv/gid/7.1)',bbox=','.join(map(str,[lat0,lon0,lat1,lon1]))+',urn:ogc:def:crs:EPSG::4326')
        url=URL+'?'+urlencode(params)
        if not p.exists():
            with urlopen(url,timeout=40) as r:p.write_bytes(r.read())
        root=ET.fromstring(p.read_bytes())
        error=root.tag.endswith('ExceptionReport')
        row=dict(name=name,url=url,file=p.name,bytes=p.stat().st_size,error=error,number_returned=root.get('numberReturned'),number_matched=root.get('numberMatched'))
        log.append(row);print(row,flush=True)
    (OUT/('STATION_REQUESTS_4326.json' if '--station' in sys.argv else 'AXES_REQUESTS_4326.json')).write_text(json.dumps(log,indent=2)+'\n',encoding='utf8')

def context():
    names=['Lech','Isar','Inn','Salzach','Donau','Iller','Regen','Naab']
    clauses=''.join('<fes:PropertyIsEqualTo><fes:ValueReference>adv:name</fes:ValueReference><fes:Literal>'+n+'</fes:Literal></fes:PropertyIsEqualTo>' for n in names)
    f='<fes:Filter xmlns:fes="http://www.opengis.net/fes/2.0" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:adv="http://www.adv-online.de/namespaces/adv/gid/7.1"><fes:And><fes:BBOX><fes:ValueReference>adv:position</fes:ValueReference><gml:Envelope srsName="urn:ogc:def:crs:EPSG::4326"><gml:lowerCorner>47 9.7</gml:lowerCorner><gml:upperCorner>49.3 14</gml:upperCorner></gml:Envelope></fes:BBOX><fes:Or>'+clauses+'</fes:Or></fes:And></fes:Filter>'
    params=dict(service='WFS',version='2.0.0',request='GetFeature',typenames='adv:AX_Gewaesserstationierungsachse',count=10000,srsName='urn:ogc:def:crs:EPSG::4326',Filter=f)
    url=URL+'?'+urlencode(params);p=OUT/'MAJOR_RIVERS_CONTEXT.gml'
    if not p.exists():
        with urlopen(url,timeout=50) as r:p.write_bytes(r.read())
    root=ET.fromstring(p.read_bytes());row=dict(url=url,file=p.name,bytes=p.stat().st_size,number_returned=root.get('numberReturned'),error=root.tag.endswith('ExceptionReport'),names=names)
    (OUT/'CONTEXT_REQUEST.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf8');print(row,flush=True)
if __name__=='__main__':
    import sys
    context() if '--context' in sys.argv else main()
