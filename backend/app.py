from fastapi import FastAPI
from backend.Endpoints import post_res, service, admin_sum
from backend.Endpoints import get_res

app = FastAPI()

# Include routers from each file
app.include_router(service.router)
app.include_router(post_res.router)
app.include_router(admin_sum.router)
app.include_router(get_res.router)