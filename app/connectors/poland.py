from datetime import datetime
import httpx
from app.core import Tender
URL='https://ezamowienia.gov.pl/mo-board/api/v1/notice'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
def pick(x,*keys):
 for k in keys:
  if x.get(k) not in (None,''):return x.get(k)
 return ''
async def fetch(countries=None,limit=200):
 async with httpx.AsyncClient(timeout=45,follow_redirects=True,headers={'Accept':'application/json'}) as c:
  r=await c.get(URL,params={'PageSize':limit,'PageNumber':1});r.raise_for_status();body=r.json()
 rows=body if isinstance(body,list) else body.get('items') or body.get('data') or body.get('results') or []
 out=[]
 for x in rows[:limit]:
  rid=str(pick(x,'noticeNumber','noticeId','id'))
  title=str(pick(x,'orderObject','title','noticeTitle'))
  buyer=pick(x,'organizationName','contractingAuthorityName','buyerName')
  out.append(Tender('pl:'+rid,'poland','POL',title or rid,str(buyer),None,'PLN',dt(pick(x,'submissionDeadline','deadline')),str(pick(x,'noticeStatus','status') or 'active'),str(pick(x,'noticeUrl','url')),description=str(pick(x,'description','shortDescription')),procurement_id=rid))
 return out
