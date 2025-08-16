from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./payments.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


class PaymentEvent(Base):
    __tablename__ = "payment_events"

    event_id = Column(String, primary_key=True, index=True)
    payment_id = Column(String, index=True)
    event_type = Column(String, index=True)
    received_at = Column(DateTime, default=datetime.utcnow)
    payload = Column(JSON)


Base.metadata.create_all(bind=engine)
