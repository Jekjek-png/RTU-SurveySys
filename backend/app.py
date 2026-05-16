from fastapi import FastAPI
from backend.Endpoints import adminAuth, service, submit_res, post_res, get_res, service, admin_sum

app = FastAPI()

# Include routers from each file
app.include_router(service.router)
app.include_router(submit_res.router)
app.include_router(adminAuth.router)
app.include_router(post_res.router)
app.include_router(admin_sum.router)
app.include_router(get_res.router)
