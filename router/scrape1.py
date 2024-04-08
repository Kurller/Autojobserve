from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Scrape as DBScrape
from app.database import get_db
#from router import oAuth
from pydantic import BaseModel
from typing import Optional
from app import models
#from app.models import User,Scrape
from sqlalchemy import func

router = APIRouter(prefix="/get_data", tags=['Scraped-Data'])

class ScrapeBase(BaseModel):
    company_Names: str
    job_titles: str
    Location:str

class ScrapeCreate(ScrapeBase):
    pass

@router.get("/")
def test_post(db: Session = Depends(get_db),limit:int = 10,skip:int = 0,search:Optional[str] =""):
    new_scrape = db.query(DBScrape).filter(DBScrape.company_Names.contains(search)).limit(limit).offset(skip).all()
    #return serialized_result
    return {"status": new_scrape}
@router.get("/{id}")
def get_data(id:int,db: Session=Depends(get_db)):
    new_data = db.query(DBScrape).filter(DBScrape.job_id ==id).first()
    return new_data
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(DBScrape).filter(DBScrape.job_id == id)
     
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    post.delete(synchronize_session=False)
    db.commit()
@router.post("/")
def create_post(data: ScrapeCreate, db: Session = Depends(get_db)):
    #user_id: int = Depends(oAuth.get_current_user))
    created_post = DBScrape(**data.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return {"data": created_post}

