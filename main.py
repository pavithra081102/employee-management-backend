from fastapi import FastAPI
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
# from auth.jwt_bearar import JWTBearer

from routers import dep, position, attendance, admin, login, emp
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Employee Management API")

app.include_router(dep.router)
app.include_router(position.router)
app.include_router(attendance.router)
app.include_router(admin.router)
# app.include_router(login.router)
app.include_router(emp.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify list of origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.get("/")
# def root():

#     return {"message": "Welcome to the Employee Management API"}

# @app.get("/profile", dependencies=[Depends(JWTBearer())])
# def profile():
#     return {"message": "You are logged in and can view your profile!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000, reload=True)
