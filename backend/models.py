from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

from .settings import settings

Base = declarative_base()

class Monitor(Base):
    __tablename__ = "monitors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, nullable=True)  # Keyword.com project identifier
    keyword_id = Column(String, nullable=True)  # Keyword.com keyword identifier
    keyword = Column(String, nullable=False)
    target_url = Column(Text, nullable=False)
    location = Column(String, default="United States")
    device = Column(String, default="desktop")
    notes = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('keyword', 'target_url', 'location', 'device', name='uniq_monitor'),)

    history = relationship("RankHistory", back_populates="monitor", cascade="all, delete-orphan")

class RankHistory(Base):
    __tablename__ = "rank_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    monitor_id = Column(Integer, ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
    position = Column(Integer, nullable=True)  # 1..100, or None if not ranked
    found_url = Column(Text, nullable=True)    # The url that matched (domain or exact path)
    serp_sample = Column(Text, nullable=True)  # JSON-serialized subset of SERP rows inspected

    monitor = relationship("Monitor", back_populates="history")

engine = create_engine(settings.SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)