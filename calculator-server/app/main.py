
from fastapi import FastAPI
from app.routers import calculator, history
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Mini Calculator API")

app.include_router(calculator.router)
app.include_router(history.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



