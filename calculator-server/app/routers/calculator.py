from asteval import Interpreter
from datetime import datetime
from fastapi import APIRouter, Depends
from schemas import Expression
from dependencies import expand_percent, get_history
import math
from typing import Annotated

router = APIRouter()


# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})
ExpandDep = Annotated[dict, Depends(expand_percent)]

@router.post("/calculate")
def calculate(expr_obj: Expression, expand_percent: dict = Depends(expand_percent), get_history: dict = Depends(get_history)):
    try:
        # code = expand_percent(expr)
        result = aeval(expand_percent)
        print(expr_obj)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr_obj.expr, "result": "", "error": msg}
        get_history.append({"timestamp": datetime.now(), "expr": expr_obj.expr, "result": result})
        return {"ok": True, "expr": expr_obj.expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr_obj.expr, "error": str(e)}