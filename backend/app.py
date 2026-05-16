from fastapi import FastAPI
<<<<<<< HEAD
from backend.Endpoints import adminAuth, service, submit_res

app = FastAPI()

# Include routers from each file
app.include_router(service.router)
app.include_router(submit_res.router)
app.include_router(adminAuth.router)
=======
from backend.Endpoints import get_service, post_res, admin_sum, get_res

app = FastAPI()

app.include_router(get_service.router)
app.include_router(post_res.router)
app.include_router(admin_sum.router)
app.include_router(get_res.router)
>>>>>>> origin/backend/services
