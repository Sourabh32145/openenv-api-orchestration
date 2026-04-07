from fastapi import FastAPI
from models.action import Action
from api_env import APIEnv

app = FastAPI()
env = APIEnv()

@app.post("/reset")
async def reset():
    return await env.reset()

@app.post("/step")
async def step(action: Action):
    return await env.step(action.action)

@app.get("/state")
async def state():
    return env.state
