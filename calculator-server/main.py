import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent
from models import Expression, CalculatorLog

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr_obj: Expression):
    try:
        # code = expand_percent(expr)
        result = aeval(expr_obj.expand_percent())
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr_obj.expr, "result": "", "error": msg}
        history.append({"timestamp": datetime.now(), "expr": expr_obj.expr, "result": result})
        return {"ok": True, "expr": expr_obj.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr_obj.expr, "error": str(e)}

@app.get("/history", response_model=list[CalculatorLog])
def get_history(limit: int | None = None):
    return list(reversed(history))[:limit] if limit else list(reversed(history))


@app.delete("/history")
def del_history():
    history.clear()
    return {"ok": True, "cleared": True}
