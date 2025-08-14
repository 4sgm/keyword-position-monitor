from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
import pytz

from .settings import settings
from .models import SessionLocal, Monitor, RankHistory
from .keywordcom import KeywordComClient
from .utils import urls_match

def check_all_monitors():
    db: Session = SessionLocal()
    try:
        client = KeywordComClient()
        monitors = db.query(Monitor).all()
        for m in monitors:
            try:
                history = client.get_keyword_history(m.keyword_id)
                serp_rows = []
                if isinstance(history, dict):
                    serp_rows = history.get("serp", []) or history.get("results", []) or history.get("data", [])
                if not isinstance(serp_rows, list):
                    serp_rows = []

                position = None
                found_url = None

                for row in serp_rows:
                    pos = row.get("position") or row.get("rank") or row.get("ranking") or row.get("index")
                    url = row.get("url") or row.get("link") or row.get("result_url")
                    if pos is None or url is None:
                        continue
                    if urls_match(m.target_url, url):
                        position = int(pos)
                        found_url = url
                        break

                rh = RankHistory(
                    monitor_id=m.id,
                    position=position,
                    found_url=found_url,
                    serp_sample=str(serp_rows[:10])
                )
                db.add(rh)
                db.commit()
            except Exception as e:
                rh = RankHistory(monitor_id=m.id, position=None, found_url=None, serp_sample=str({"error": str(e)}))
                db.add(rh)
                db.commit()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.timezone(settings.TIMEZONE))
    # initial run shortly after startup, then cron
    scheduler.add_job(check_all_monitors, trigger='interval', seconds=2, id="startup-once", max_instances=1, replace_existing=True)
    scheduler.add_job(check_all_monitors, CronTrigger.from_crontab(settings.SCHEDULE_CRON), id="monitor-cron", replace_existing=True)
    scheduler.start()