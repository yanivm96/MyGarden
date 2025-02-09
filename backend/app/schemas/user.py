from pydantic import BaseModel

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    username: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  
