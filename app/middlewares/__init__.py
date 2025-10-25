from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["localhost"], # Allow requests from localhost
        allow_credentials=True, # Allow credentials (cookies, etc.)
        allow_methods=["GET", "POST", "PUT", "DELETE"], # Allow these methods
        allow_headers=["content-type", "authorization"], # Allow these headers
    )