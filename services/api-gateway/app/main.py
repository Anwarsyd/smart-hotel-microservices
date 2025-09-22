from fastapi import FastAPI
from app.routes import user_proxy

from app.middleware.cors_middleware import setup_cors
from app.middleware.logging_middleware import log_requests

app = FastAPI(title="Smart Hotel API Gateway")

# Include proxy routes
app.include_router(user_proxy.router, prefix="/users")

@app.get("/")
def root():
    return {"message": "Welcome to Smart Hotel API Gateway"}

setup_cors(app)
app.middleware("http")(log_requests)