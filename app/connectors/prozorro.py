from datetime import datetime
from urllib.parse import urljoin
import httpx
from app.core import Tender
BASE='https://public-api.prozorro.gov.ua/api/2.5/tenders'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(countries=None,limit=250):
 out=[];seen=set();url=BASE;params={'limit':100,'descending':1}
 async with httpx.AsyncClient(timeout=40,follow_redirects=True) as c:
  while url and len(seen)<limit:
   r=await c.get(url,params=params);r.raise_for_status();body=r.json();params=None
   for row in body.get('data',[]):
    rid=row.get('id')
    if not rid or rid in seen:continue
    seen.add(rid);rr=await c.get(f'{BASE}/{rid}');rr.raise_for_status();x=rr.json().get('data',{});v=x.get('value') or {};p=x.get('tenderPeriod') or {};a=next((a for a in x.get('awards',[]) if a.get('status')=='active'),{});s=(a.get('suppliers') or [{}])[0];tid=x.get('tenderID',rid)
    out.append(Tender('prozorro:'+tid,'prozorro','UKR',x.get('title') or x.get('title_en') or tid,(x.get('procuringEntity') or {}).get('name',''),v.get('amount'),v.get('currency',''),dt(p.get('endDate')),x.get('status',''),f'https://prozorro.gov.ua/tender/{tid}',s.get('name',''),(a.get('value') or {}).get('amount'),dt(a.get('date')),x.get('description',''),tid))
    if len(seen)>=limit:break
   nxt=(body.get('next_page') or {}).get('uri');url=urljoin(BASE,nxt) if nxt else None
 return out
