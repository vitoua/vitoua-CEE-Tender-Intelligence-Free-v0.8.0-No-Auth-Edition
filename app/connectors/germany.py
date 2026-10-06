import io,json,zipfile
from datetime import date,datetime,timedelta
import httpx
from app.core import Tender
URL='https://oeffentlichevergabe.de/api/notice-exports'
def dt(v):
 try:return datetime.fromisoformat(str(v).replace('Z','+00:00')).replace(tzinfo=None)
 except:return None
async def fetch(countries=None,days=3):
 out=[]
 async with httpx.AsyncClient(timeout=60,follow_redirects=True) as c:
  for offset in range(days):
   day=(date.today()-timedelta(days=offset)).isoformat();r=await c.get(URL,params={'pubDay':day,'format':'ocds.zip'})
   if r.status_code==404:continue
   r.raise_for_status()
   with zipfile.ZipFile(io.BytesIO(r.content)) as z:
    for name in z.namelist():
     pack=json.loads(z.read(name));rel=(pack.get('releases') or [{}])[0];t=rel.get('tender') or {};parties=rel.get('parties') or []
     buyer=next((p.get('name','') for p in parties if 'buyer' in p.get('roles',[])),'');supplier=next((p.get('name','') for p in parties if 'supplier' in p.get('roles',[])),'');val=t.get('value') or {};period=t.get('tenderPeriod') or {};ocid=rel.get('ocid') or rel.get('id') or name
     out.append(Tender('de:'+ocid,'germany','DEU',t.get('title') or ocid,buyer,val.get('amount'),val.get('currency','EUR'),dt(period.get('endDate')),t.get('status','active'),f'https://oeffentlichevergabe.de/ui/de/notices/{ocid}',supplier,None,dt(rel.get('date')),t.get('description',''),ocid))
 return out
