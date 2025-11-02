from pydantic import BaseModel, EmailStr

class FarmerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class FarmerLogin(BaseModel):
    email: EmailStr
    password: str

class FarmerResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
