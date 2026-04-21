import random
import uuid
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .maths import calculate_multiplier

router = APIRouter()

# Temporary memory store for active games
MINES_GAMES: Dict[str, dict] = {}

class StartMinesRequest(BaseModel):
    bet: float
    bombs: int

class PickMinesRequest(BaseModel):
    game_id: str
    index: int  # 0 to 24

class CashoutRequest(BaseModel):
    game_id: str

@router.post("/start")
def start_mines(req: StartMinesRequest):
    if req.bombs < 1 or req.bombs > 24:
        raise HTTPException(status_code=400, detail="Bombs must be between 1 and 24")
    
    game_id = str(uuid.uuid4())
    board = ["safe"] * 25
    bomb_indices = random.sample(range(25), req.bombs)
    for i in bomb_indices:
        board[i] = "bomb"
        
    MINES_GAMES[game_id] = {
        "bet": req.bet,
        "bombs": req.bombs,
        "board": board,
        "hits": 0,
        "picked": [],
        "active": True,
        "current_multiplier": 1.0
    }
    
    return {
        "game_id": game_id,
        "multiplier": 1.0,
        "next_multiplier": calculate_multiplier(req.bombs, 1)
    }

@router.post("/pick")
def pick_mine(req: PickMinesRequest):
    if req.game_id not in MINES_GAMES:
        raise HTTPException(status_code=404, detail="Game not found")
        
    game = MINES_GAMES[req.game_id]
    
    if not game["active"]:
        raise HTTPException(status_code=400, detail="Game already ended")
        
    if req.index < 0 or req.index > 24 or req.index in game["picked"]:
        raise HTTPException(status_code=400, detail="Invalid pick")
        
    game["picked"].append(req.index)
    
    if game["board"][req.index] == "bomb":
        game["active"] = False
        return {
            "status": "boom",
            "board": game["board"], # reveal all
            "picked": game["picked"]
        }
        
    # Safe pick
    game["hits"] += 1
    new_mult = calculate_multiplier(game["bombs"], game["hits"])
    game["current_multiplier"] = new_mult
    
    # Auto win if they hit all safe tiles
    if game["hits"] == (25 - game["bombs"]):
        game["active"] = False
        return {
            "status": "cashout",
            "winnings": game["bet"] * new_mult,
            "multiplier": new_mult,
            "board": game["board"],
            "picked": game["picked"]
        }
        
    next_mult = calculate_multiplier(game["bombs"], game["hits"] + 1)
    
    return {
        "status": "safe",
        "multiplier": new_mult,
        "next_multiplier": next_mult,
        "picked": game["picked"]
    }

@router.post("/cashout")
def cashout_mines(req: CashoutRequest):
    if req.game_id not in MINES_GAMES:
        raise HTTPException(status_code=404, detail="Game not found")
        
    game = MINES_GAMES[req.game_id]
    
    if not game["active"] or game["hits"] == 0:
        raise HTTPException(status_code=400, detail="Cannot cashout")
        
    game["active"] = False
    winnings = game["bet"] * game["current_multiplier"]
    
    return {
        "status": "cashed_out",
        "winnings": winnings,
        "multiplier": game["current_multiplier"],
        "board": game["board"],
        "picked": game["picked"]
    }
