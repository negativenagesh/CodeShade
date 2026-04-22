from fastapi import FastAPI
from backend.games.mines.router import router as mines_router

app = FastAPI()

app.include_router(mines_router, prefix="/api/mines", tags=["mines"])

@app.get("/api/games")
def list_games():
    return {"games": ["Mines"]}

@app.get("/health")
def health():
    return {"status": "ok"}
