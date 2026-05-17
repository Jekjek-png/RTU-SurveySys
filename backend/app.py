from fastapi import FastAPI, Request
from backend.Endpoints import admin_auth, admin_getdashboard, user_getservice, user_postrespo

app = FastAPI()

# Include routers from each file
app.include_router(admin_auth.router)
app.include_router(admin_getdashboard.router)
app.include_router(user_postrespo.router)
app.include_router(get_res.router)
app.include_router(user_getservice.router)