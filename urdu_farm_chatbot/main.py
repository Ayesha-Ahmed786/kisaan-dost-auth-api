from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database
from .routers import auth, finance
from .schemas import farmer as farmer_schema
from .models import farmer as farmer_model
from .database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(finance.router, prefix="/finance", tags=["Finance"])

# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Signup Endpoint
# -----------------------
@app.post("/signup", response_model=farmer_schema.FarmerResponse)
def signup(farmer_data: farmer_schema.FarmerCreate, db: Session = Depends(get_db)):
    # Check for empty fields
    if not farmer_data.name.strip() or not farmer_data.email.strip() or not farmer_data.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name, email, and password are required."
        )

    # Check if email already exists
    db_farmer = db.query(farmer_model.Farmer).filter(farmer_model.Farmer.email == farmer_data.email).first()
    if db_farmer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    # Hash password and save
    hashed_pw = auth.hash_password(farmer_data.password)
    new_farmer = farmer_model.Farmer(
        name=farmer_data.name,
        email=farmer_data.email,
        password=hashed_pw
    )
    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)

    return new_farmer


# -----------------------
# Login Endpoint
# -----------------------
@app.post("/login")
def login(credentials: farmer_schema.FarmerLogin, db: Session = Depends(get_db)):
    # Check for empty fields
    if not credentials.email.strip() or not credentials.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )

    # Fetch user
    db_farmer = db.query(farmer_model.Farmer).filter(farmer_model.Farmer.email == credentials.email).first()
    if not db_farmer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Verify password
    if not auth.verify_password(credentials.password, db_farmer.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password."
        )

    # Create access token
    token = auth.create_access_token(data={"sub": db_farmer.email})
    return {
        "access_token": token,
        "token_type": "bearer",
        "message": "Login successful"
    }
