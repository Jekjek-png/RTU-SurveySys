from fastapi import FastAPI
from backend.Endpoints import adminAuth, service, submit_res

app = FastAPI()

# Include routers from each file
app.include_router(service.router)
app.include_router(submit_res.router)
app.include_router(adminAuth.router)
