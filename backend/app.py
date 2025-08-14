from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets

from .settings import settings
from .models import SessionLocal, init_db, Monitor, RankHistory
from .keywordcom import KeywordComClient
from .scheduler import start_scheduler

security = HTTPBasic()

app = FastAPI(title=settings.APP_NAME)

app.mount("/static", StaticFiles(directory="backend/static"), name="static")
templates = Jinja2Templates(directory="backend/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})
    return True

@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    monitors = db.query(Monitor).all()
    return templates.TemplateResponse("index.html", {"request": request, "monitors": monitors, "app_name": settings.APP_NAME})

@app.post("/monitors", response_class=RedirectResponse)
def create_monitor(
    keyword: str = Form(...),
    target_url: str = Form(...),
    location: str = Form("United States"),
    device: str = Form("desktop"),
    notes: str = Form(""),
    project_id: str = Form(""),
    keyword_id: str = Form(""),
    db: Session = Depends(get_db),
    _: bool = Depends(require_auth),
):
    if not keyword_id and project_id:
        client = KeywordComClient()
        try:
            add_resp = client.add_keywords(project_id=project_id, keywords=[keyword], location=location, device=device)
            if isinstance(add_resp, dict):
                keyword_id_candidate = (add_resp.get("data") or {}).get("id") or add_resp.get("id") or ""
                if keyword_id_candidate:
                    keyword_id = str(keyword_id_candidate)
        except Exception:
            pass

    m = Monitor(
        project_id=project_id or None,
        keyword_id=keyword_id or None,
        keyword=keyword,
        target_url=target_url,
        location=location,
        device=device,
        notes=notes,
    )
    db.add(m)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/run-now")
def run_now(_: bool = Depends(require_auth)):
    from .scheduler import check_all_monitors
    check_all_monitors()
    return {"status": "ok"}

@app.get("/monitors")
def list_monitors(db: Session = Depends(get_db)):
    ms = db.query(Monitor).all()
    return [{"id": m.id, "keyword": m.keyword, "target_url": m.target_url, "project_id": m.project_id, "keyword_id": m.keyword_id} for m in ms]

@app.get("/history/{monitor_id}")
def history(monitor_id: int, db: Session = Depends(get_db)):
    rows = db.query(RankHistory).filter(RankHistory.monitor_id == monitor_id).order_by(RankHistory.id.asc()).all()
    series = [{"t": str(r.checked_at), "position": r.position, "found_url": r.found_url} for r in rows]
    return {"monitor_id": monitor_id, "series": series}

@app.get("/keywordcom/projects")
def keywordcom_projects(_: bool = Depends(require_auth)):
    client = KeywordComClient()
    return client.list_projects()

@app.get("/keywordcom/{project_id}/keywords")
def keywordcom_project_keywords(project_id: str, _: bool = Depends(require_auth)):
    client = KeywordComClient()
    return client.list_project_keywords(project_id)