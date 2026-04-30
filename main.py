from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas
import csv
from fastapi import UploadFile, File
import io
models.Base.metadata.create_all(bind=engine)  # Table না থাকলে বানাবে

app = FastAPI()

# সব posts পাও
@app.get("/posts", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# একটা post তৈরি করো
@app.post("/posts", response_model=schemas.PostResponse)
def create_post(title: str, content: str, db: Session = Depends(get_db)):
    new_post = models.Post(title=title, content=content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
@app.delete("/posts/{post_id}", response_model=schemas.PostResponse)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}
@app.get("/leads", response_model=list[schemas.LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    return leads
@app.post("/leads/upload-csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    
    leads = []
    for row in reader:
        lead = models.Lead(
            business_name=row["name"],
            phone=row["phone"],
            address=row["address"],
            city=row["city"],
            category=row["category"],
            rating=None
        )
        leads.append(lead)
    
    db.add_all(leads)
    db.commit()
    return {"message": f"{len(leads)} leads inserted"}