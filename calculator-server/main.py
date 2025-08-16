from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from asteval import Interpreter

app = FastAPI()

# CORS middleware (still needed if you're calling this from JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

aeavl = Interpreter()
print(aeavl("10*3"))

# To return a response with HTML directly from FastAPI, use HTMLResponse.
@app.get('/', response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>ITCS525</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """

