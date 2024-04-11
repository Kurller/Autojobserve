from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from app.database import Base, engine
from datetime import datetime
class Scrape(Base):
    __tablename__ = 'scrape1'
    job_id = Column(Integer, primary_key=True)
    company_Names = Column(String, nullable=False)
    job_titles = Column(String, nullable=False)
    posted_time =Column(TIMESTAMP)
    #user_id = Column(Integer, ForeignKey('user.id'))
    #user = relationship("User", back_populates="scrapes")
    Location = Column(String)
#Base.metadata.create_all(engine)