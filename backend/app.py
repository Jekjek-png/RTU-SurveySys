from fastapi import FastAPI, Request
from backend.Endpoints import admin_auth, admin_respo, post_res, get_res, get_service

app = FastAPI()

# Include routers from each file
app.include_router(admin_auth.router)
app.include_router(admin_respo.router)
app.include_router(post_res.router)
app.include_router(get_res.router)
app.include_router(get_service.router)