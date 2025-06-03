from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from model import Feedback

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount static files directory (for CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Serve feedback form HTML on root route
@app.get("/")
def read_form(request: Request):
    return templates.TemplateResponse("feedback.html", {"request": request})

# CREATE feedback entry (HTML form submission)
@app.post("/feedback")
def create_feedback(
    request: Request,
    name: str = Form(...),
    CName: str = Form(None),
    email: str = Form(...),
    service: str = Form(...),
    satisfaction: int = Form(...),
    onTime: str = Form(...),
    communication: int = Form(...),
    recommend: str = Form(...),
    liked: str = Form(None),
    improve: str = Form(None),
    comments: str = Form(None),
    db: Session = Depends(get_db)
):
    feedback = Feedback(
        name=name,
        CName=CName,
        email=email,
        service=service,
        satisfaction=satisfaction,
        onTime=onTime,
        communication=communication,
        recommend=recommend,
        liked=liked,
        improve=improve,
        comments=comments,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    # Redirect back to form with success query param
    return RedirectResponse(url="/?submitted=true", status_code=303)

# READ all feedback entries
@app.get("/feedbacks")
def read_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).all()

# READ single feedback by ID
@app.get("/feedbacks/{feedback_id}")
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

# UPDATE feedback entry by ID
@app.put("/feedbacks/{feedback_id}")
def update_feedback(
    feedback_id: int,
    name: str = Form(...),
    CName: str = Form(None),
    email: str = Form(...),
    service: str = Form(...),
    satisfaction: int = Form(...),
    onTime: str = Form(...),
    communication: int = Form(...),
    recommend: str = Form(...),
    liked: str = Form(None),
    improve: str = Form(None),
    comments: str = Form(None),
    db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    feedback.name = name
    feedback.CName = CName
    feedback.email = email
    feedback.service = service
    feedback.satisfaction = satisfaction
    feedback.onTime = onTime
    feedback.communication = communication
    feedback.recommend = recommend
    feedback.liked = liked
    feedback.improve = improve
    feedback.comments = comments

    db.commit()
    db.refresh(feedback)
    return {"message": "Feedback updated", "feedback": feedback}

# DELETE feedback entry by ID
@app.delete("/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(feedback)
    db.commit()
    return {"message": "Feedback deleted"}
