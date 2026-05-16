from fastapi import FastAPI
from backend.Endpoints import adminAuth, admin_sum, post_res, get_res, get_service

app = FastAPI()

# Include routers from each file
app.include_router(adminAuth.router)
app.include_router(admin_sum.router)
app.include_router(post_res.router)
app.include_router(get_res.router)
app.include_router(get_service.router)