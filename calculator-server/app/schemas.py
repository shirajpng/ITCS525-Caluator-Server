from pydantic import BaseModel
from datetime import datetime

class BaseExpression(BaseModel):
	expr: str

class ExpressionIn(BaseExpression):
	pass

class ExpressionOut(BaseExpression):
	timestamp: datetime | None
	result: float

class Expression(ExpressionIn):
	pass

class CalculatorLog(ExpressionOut):
	pass
