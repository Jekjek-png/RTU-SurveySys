from fastapi import FastAPI
from backend.Endpoints import get_service, post_res, admin_sum, get_res

app = FastAPI()

app.include_router(get_service.router)
app.include_router(post_res.router)
app.include_router(admin_sum.router)
app.include_router(get_res.router)