from datetime import datetime
import httpx
from app.core import Tender
URL='https://api.ted.europa.eu/v3/notices/search'
def first(v):
 if isinstance(v,dict):
  for k in ('eng','pol','ukr','deu','fra'):
   if k in v:return first(v[k])
  return first(next(iter(v.values()),''))
 if isinstance(v,list):return first(v[0]) if v else ''
 return str(v or '')
def dt(v):
 try:return datetime.fromisoformat(first(v)[:10])
 except:return None
def num(v):
 try:return float(first(v))
 except:return None
async def fetch(countries=None,limit=200):
 fields=['publication-number','notice-title','buyer-name','buyer-country','total-value','total-value-cur','publication-date','deadline','classification-cpv','description-proc','description-lot']
 queries=['FT~"SSD" OR FT~"NVMe" OR FT~"DDR4" OR FT~"DDR5" OR FT~"memory card" OR FT~"flash drive"','classification-cpv IN (30233100 30233130 30234100 30236100 30237200)'];err=''
 async with httpx.AsyncClient(timeout=45,follow_redirects=True) as c:
  for q in queries:
   r=await c.post(URL,json={'query':q,'fields':fields,'page':1,'limit':min(limit,200),'scope':'ALL','paginationMode':'PAGE_NUMBER','onlyLatestVersions':True})
   if r.status_code==200:break
   err=f'HTTP {r.status_code}: {r.text[:700]}'
  else:raise RuntimeError('TED API: '+err)
 out=[]
 for x in r.json().get('notices',[]):
  country=first(x.get('buyer-country'))[:3] or 'EU'
  if countries and country not in set(countries):continue
  n=first(x.get('publication-number'));out.append(Tender('ted:'+n,'ted',country,first(x.get('notice-title')) or n,first(x.get('buyer-name')),num(x.get('total-value')),first(x.get('total-value-cur')),dt(x.get('deadline')),'active',f'https://ted.europa.eu/en/notice/-/detail/{n}',description=first(x.get('description-proc')) or first(x.get('description-lot')),procurement_id=n))
 return out
