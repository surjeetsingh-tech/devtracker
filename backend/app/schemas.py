from pydantic import BaseModel, EmailStr
from datetime import  datetime
from typing import Optional

#User request Base
class UserBase(BaseModel):
    username: str
    email: EmailStr

#Signup input data shape
class UserCreate(UserBase):
    password: str

#API output response shape (Protects sensitive hashed password)
class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

#Token response schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
        user_id: Optional[int] = None

#Task Base defination
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"
    github_link: Optional[str] = None

#Input data shape when creating a task
class TaskCreate(TaskBase):
    pass

#Input data when update
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    github_link: Optional[str] = None

#Output API response 
class TaskOut(TaskBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardMetrics(BaseModel):
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int










        
















