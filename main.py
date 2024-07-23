from fastapi import FastAPI, Depends, HTTPException, status
from app import models, schemas
from address import model, schema
from app.database import engine, SessionLocal
from address.database import engines, SessionLocals
from sqlalchemy.orm import Session
import re
from fastapi.responses import JSONResponse
import json

app = FastAPI()
#TO run this code:
#Use~~ uvicorn main:app --host 26.243.124.232 --port 8080 --reload 
#To See the output use this link : http://26.243.124.232:8080/docs#/default/
# Create database tables
models.Base.metadata.create_all(engine)
model.Base.metadata.create_all(engine)
# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def gets_db():
    db = SessionLocals()
    try:
        yield db
    finally:
        db.close()
# admin authentication
@app.post("/admin")
async def check_admin(request: schemas.admin, db: Session = Depends(get_db)):
    user = db.query(models.admin).filter(models.admin.email == request.email, models.admin.pass_word == request.pass_word).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user Not Found")
    else:
        return {'status': 200, 'message': 'Login Successful'}

# Create user
@app.post("/user_create")
async def create_user(request: schemas.user, db: Session = Depends(get_db)):
    new_user = models.user(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'status': 200, 'message': 'user Created'}

# Update user details
@app.put("/user_update/{id}")
async def update_user(id: int, request: schemas.user, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user Not Found")
    for attr, value in request.dict(exclude_unset=True).items():
        setattr(user, attr, value)
    db.commit()
    db.refresh(user)
    return {'status': 200, 'message': 'user Updated'}

# Get all users
@app.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.user).all()
    return {'status':200,'data':users,'message':'Success'}

# Get user by id
@app.get("/user/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user Not Found")
    return {'status':200,'data':user,'message':'Success'}

# Delete user
@app.delete("/user_delete/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.user).filter(models.user.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user Not Found")
    db.delete(user)
    db.commit()
    return {'status': 204, 'message': 'user Deleted'}

# Get all applications
@app.get("/applications")
async def get_all_applications(db: Session = Depends(get_db)):
    applications = db.query(models.Application).all()
    return applications

