# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import auth, team, checkin
from app.api.core.exceptions import add_error_handlers


app = FastAPI(title="Marketing Campaign API")
add_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["auth"], prefix="/api")
app.include_router(team.router, tags=["teams"], prefix="/api")
app.include_router(checkin.router, tags=["checkins"], prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Marketing Campaign API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)