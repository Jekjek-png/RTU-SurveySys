from fastapi import FastAPI
from backend.Endpoints import service, submit_res, admin_sum

app = FastAPI()

# Include routers from each file
app.include_router(service.router)
app.include_router(submit_res.router)
app.include_router(admin_sum.router)