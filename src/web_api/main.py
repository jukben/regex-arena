from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum
import uuid

app = FastAPI()


# Enums and Models
class AgentStatus(str, Enum):
    PENDING = "pending"
    EVALUATING = "evaluating"
    COMPLETED = "completed"


class Agent(BaseModel):
    id: str
    status: AgentStatus
    regex: Optional[str] = None
    score: Optional[float] = None
    failures: Optional[List[str]] = None


class TestCases(BaseModel):
    valid: List[str]
    invalid: List[str]


class Iteration(BaseModel):
    number: int
    testCases: TestCases
    agents: List[Agent]


class GenerationState(BaseModel):
    userInput: str
    isGenerating: bool
    currentIteration: int
    maxIterations: int
    iterations: List[Iteration]
    showResults: bool


class ArenaInitRequest(BaseModel):
    input: str


# In-memory storage for generation states
generation_states: Dict[str, GenerationState] = {}


@app.post("/initializeArena")
async def initialize_arena(request: ArenaInitRequest):
    # Generate a unique ID for this run
    run_id = str(uuid.uuid4())

    # Create initial state
    initial_state = GenerationState(
        userInput=request.input,
        isGenerating=True,
        currentIteration=0,
        maxIterations=5,  # Default value, can be adjusted
        iterations=[],
        showResults=False,
    )

    # Store the state
    generation_states[run_id] = initial_state

    return {"runId": run_id}


@app.get("/getArenaStatus/{run_id}")
async def get_arena_status(run_id: str) -> GenerationState:
    if run_id not in generation_states:
        raise HTTPException(status_code=404, detail="Arena run not found")

    return generation_states[run_id]


def run_server():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_server()
