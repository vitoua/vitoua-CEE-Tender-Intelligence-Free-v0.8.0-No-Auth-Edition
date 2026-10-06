from fastapi import FastAPI,Form,Request,HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer,BadSignature
from app.core import store,active,analytics
from app.config import settings
from app.i18n import tr
from app.sources import COUNTRIES,sources_for
app=FastAPI(version='0.8.0');app.mount('/static',StaticFiles(directory='app/static'),name='static');tpl=Jinja2Templates(directory='app/templates');sign=URLSafeSerializer(settings.secret_key,'session')
def lang(r):return r.cookies.get('lang') or settings.app_language
def auth(r):
 try:return sign.loads(r.cookies.get('session',''))=='admin'
 except BadSignature:return False
def c(r,x=None):return {'request':r,'t':tr(lang(r)),**(x or {})}
@app.get('/health')
def health():return {'status':'ok','version':'0.8.0','tenders':len(store.data)}
@app.get('/lang/{code}')
def sl(code,request:Request):
 r=RedirectResponse(request.headers.get('referer') or '/',303);r.set_cookie('lang',code if code in ('uk','pl','en') else 'uk');return r
@app.get('/login',response_class=HTMLResponse)
def lp(request:Request):return tpl.TemplateResponse('login.html',c(request))
@app.post('/login')
def login(email:str=Form(),password:str=Form()):
 if email!=settings.admin_email or password!=settings.admin_password:return HTMLResponse('Invalid credentials',400)
 r=RedirectResponse('/',303);r.set_cookie('session',sign.dumps('admin'),httponly=True,secure=True,samesite='lax');return r
@app.get('/logout')
def logout():r=RedirectResponse('/login',303);r.delete_cookie('session');return r
@app.get('/',response_class=HTMLResponse)
def home(request:Request,country:str='',q:str='',active_only:int=1):
 if not auth(request):return RedirectResponse('/login',303)
 rows=list(store.data.values());rows=[x for x in rows if (not active_only or active(x)) and (not country or x.country==country) and (not q or q.lower() in ' '.join([x.title,x.buyer,x.description]).lower())]
 return tpl.TemplateResponse('index.html',c(request,{'rows':rows,'runs':store.runs,'countries':store.countries(),'available_countries':COUNTRIES,'country':country,'q':q,'active_only':active_only}))
@app.post('/refresh')
async def refresh(request:Request,countries:list[str]=Form(default=[])):
 if not auth(request):raise HTTPException(401)
 if not countries:countries=list(COUNTRIES)
 for src,scope in sources_for(countries):
  try:
   if src=='ted':from app.connectors.ted import fetch;rows=await fetch(scope)
   elif src=='prozorro':from app.connectors.prozorro import fetch;rows=await fetch(scope)
   elif src=='germany':from app.connectors.germany import fetch;rows=await fetch(scope)
   elif src=='poland':from app.connectors.poland import fetch;rows=await fetch(scope)
   else:raise RuntimeError(f'Unsupported source: {src}')
   store.add(src,rows)
  except Exception as e:store.error(src,e)
 return RedirectResponse('/',303)
@app.get('/analytics',response_class=HTMLResponse)
def report(request:Request,sort_by:str='wins',order:str='desc'):
 if not auth(request):raise HTTPException(401)
 rows=analytics(store.data.values());key={'wins':'wins','value':'total'}.get(sort_by,'wins');rows.sort(key=lambda x:x[key],reverse=order!='asc')
 return tpl.TemplateResponse('analytics.html',c(request,{'rows':rows,'sort_by':sort_by,'order':order}))
