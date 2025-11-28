# app.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from validate import validate_tool_call

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.get_template("index.html").render({"request": request})

@app.post("/validate")
async def validate(json_input: str = Form(...)):
    try:
        payload = json.loads(json_input)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}

    clean, errors = validate_tool_call(payload)
    return {
        "clean": clean if clean else None,
        "errors": errors
    }