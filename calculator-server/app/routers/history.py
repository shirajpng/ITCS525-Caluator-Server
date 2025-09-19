from fastapi import APIRouter, Depends
from schemas import CalculatorLog
from dependencies import get_history
from typing import Annotated
router = APIRouter()

@router.get("/history", response_model=list[CalculatorLog])
async def return_history(limit: int | None = None, get_history: dict= Depends(get_history) ):
    return list(reversed(get_history))[:limit] if limit else list(reversed(get_history))


@router.delete("/history")
async def del_history(history: dict =Depends(get_history)):
    history.clear()
    return {"ok": True, "cleared": True}
