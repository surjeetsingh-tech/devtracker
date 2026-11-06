from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import Base, engine, get_db
from app.models import User
from app.schemas import UserCreate ,UserOut, Token
from app import models
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from sqlalchemy.future import select
from sqlalchemy import func
from app.models import Task
from app.schemas import TaskCreate, TaskOut, TaskUpdate,DashboardMetrics

app = FastAPI(title="Devtracker", version="1.0") 

origins = [
    "http://localhost:3000",  
    "http://localhost:5173", 
    "https://devtracker-jet.vercel.app" 
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=False,           
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],
)

#Signup route
@app.post("/auth/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where((User.email == user_data.email)|(User.username == user_data.username)))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username or email alreday registered")
    new_user = User(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hash_password(user_data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

#Login route
@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db : AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"user_id": user.id})
    return{"access_token": access_token, "token_type": "bearer"}
    
#Protected route
@app.get("/users/me", response_model=UserOut)
async def get_logged_in_user(current_user: User = Depends(get_current_user)):
    return current_user

#Create Task
@app.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    new_task = Task(
        **task_data.model_dump(),
        user_id=current_user.id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

#Get all current user tasks
@app.get("/tasks", response_model=list[TaskOut])
async def get_all_user_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id))
    return result.scalars().all()

#Update task 
@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task_by_id(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    db_task = result.scalars().first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found or access unauthorized")
    update_dict = task_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_task,key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

#Delete task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    db_task = result.scalars().first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found or access unauthorized")
    await db.delete(db_task)
    await db.commit()
    return None

#Dashboard metrics
@app.get("/dashboard/metrics", response_model=DashboardMetrics)
async def get_dashboard_summary_metrics(
    db: AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)):
    result = await db.execute(
        select(Task.status, func.count(Task.id))
        .where(Task.user_id == current_user.id)
        .group_by(Task.status)
    )
    status_counts = dict(result.all())
    pending = status_counts.get("Pending", 0)
    in_progress = status_counts.get("In Progress", 0)
    completed = status_counts.get("Completed", 0)
    total = pending + in_progress + completed
    return {
        "total_tasks": total,
        "pending_tasks": pending,
        "in_progress_tasks": in_progress,
        "completed_tasks": completed
    }


#Create database tables
# @app.on_event("startup")# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_base_or_alter if hasattr(Base.metadata, 'create_base_or_alter') else Base.metadata.create_all)

# Create database tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return{
        "status" : "success",
        "message" : "welcome to Devtracker"
    }

@app.get("/health-check")
async def check_db_health(db : AsyncSession = Depends(get_db)):
    return {
        "status": "healthy",
        "database": "connected successfully"
    }
