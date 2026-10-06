import hashlib,re,unicodedata
from datetime import timedelta

def norm(v):
 v=unicodedata.normalize('NFKD',str(v or '')).encode('ascii','ignore').decode().lower()
 return re.sub(r'[^a-z0-9]+',' ',v).strip()

def ids(t):
 text=' '.join([t.id,t.url,t.title,t.description])
 patterns=[r'\b\d{4}/s\s*\d{3}-\d{6}\b',r'\b\d{6}-\d{4}\b',r'\bocds-[a-z0-9-]+\b']
 out=set()
 for p in patterns:out.update(re.findall(p,text.lower()))
 return out

def fingerprint(t):
 day=(t.deadline.date().isoformat() if t.deadline else '')
 base='|'.join([t.country,norm(t.buyer),norm(t.title)[:180],day,str(round(t.value or 0,2)),t.currency])
 return hashlib.sha256(base.encode()).hexdigest()

def duplicate(a,b):
 if ids(a)&ids(b):return True,'external-id'
 if fingerprint(a)==fingerprint(b):return True,'fingerprint'
 if a.country!=b.country:return False,''
 title_a=set(norm(a.title).split());title_b=set(norm(b.title).split())
 sim=len(title_a&title_b)/max(1,len(title_a|title_b))
 buyer=norm(a.buyer)==norm(b.buyer) and bool(norm(a.buyer))
 deadline=not a.deadline or not b.deadline or abs((a.deadline-b.deadline).days)<=2
 value=(not a.value or not b.value or abs(a.value-b.value)<=max(1,0.01*max(a.value,b.value)))
 return (sim>=0.86 and buyer and deadline and value),'fuzzy' if sim>=0.86 and buyer and deadline and value else ''

def merge(existing,incoming):
 # Prefer a national record for richer local detail, but retain TED provenance.
 primary=incoming if incoming.source!='ted' and existing.source=='ted' else existing
 sources=set(getattr(existing,'sources',[]) or [existing.source])|set(getattr(incoming,'sources',[]) or [incoming.source])
 primary.sources=sorted(sources);primary.duplicate_sources=sorted(sources- {primary.source})
 return primary
