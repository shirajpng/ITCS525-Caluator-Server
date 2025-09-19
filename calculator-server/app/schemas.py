from pydantic import BaseModel
from datetime import datetime

class BaseExpression(BaseModel):
	expr: str

class ExpressionIn(BaseModel):
	expr: str

class ExpressionOut(BaseModel):
	timestamp: datetime | None
	expr: str
	result: float

class Expression(ExpressionIn):
	pass

class CalculatorLog(ExpressionOut):
	pass
