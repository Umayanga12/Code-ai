import asyncio
import json
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain.messages import HumanMessage
from langgraph.types import Command

# from agent.requirment.server_graph import (
#     RequirementSystemState,
# )
from agent.requirment.server_graph import (
    server_graph as requirment_system_graph,
)

app = FastAPI()

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store client states
client_states = {}


def new_state():
    return {"messages": [], "requirements": None, "itinerary": None}


active_threads = {}  # thread_id → state
# waiting_futures = {}        # REMOVED: No longer needed for non-blocking interrupt


# 🟦 MAIN WEBSOCKET ENDPOINT
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"DEBUG: New websocket connection request")
    await websocket.accept()
    print(f"DEBUG: Websocket connection accepted")

    client_id = str(uuid4())
    print(f"DEBUG: Assigned client_id: {client_id}")
    client_states[client_id] = new_state()

    # Initialize thread state for this client
    active_threads[client_id] = client_states[client_id]

    try:
        while True:
            data = await websocket.receive_text()
            print(f"DEBUG: Received message from {client_id}: {data}")

            # Parse the incoming message
            try:
                message_data = json.loads(data)
                user_content = message_data.get("message", data)
                message_type = message_data.get("type", "message")
            except json.JSONDecodeError:
                user_content = data
                message_type = "message"

            print(
                f"DEBUG: Parsed message type: {message_type}, content: {user_content}"
            )

            # Handle interrupt response
            if message_type == "response":
                print(f"DEBUG: Handling interrupt response for {client_id}")
                await run_agent(websocket, client_id, resume_value=user_content)
                continue

            # Add user message to state
            print(f"DEBUG: Appending user message to state for {client_id}")
            active_threads[client_id]["messages"].append(
                HumanMessage(content=user_content)
            )

            # Run the agent with streaming
            print(f"DEBUG: Starting run_agent for {client_id}")
            await run_agent(websocket, client_id)
            print(f"DEBUG: Finished run_agent for {client_id}")

    except WebSocketDisconnect:
        print(f"DEBUG: Client {client_id} disconnected")
        if client_id in client_states:
            del client_states[client_id]
        if client_id in active_threads:
            del active_threads[client_id]


# 🟩 STREAM AGENT EVENTS USING LangGraph
async def run_agent(ws: WebSocket, thread_id: str, resume_value=None):
    print(
        f"DEBUG: run_agent started for thread_id: {thread_id}, resume: {resume_value is not None}"
    )

    if resume_value:
        input_data = Command(resume=resume_value)
    else:
        input_data = active_threads[thread_id]

    async for step in requirment_system_graph.astream(
        input_data, {"configurable": {"thread_id": thread_id}}
    ):
        event_type = list(step.keys())[0]
        payload = step[event_type]
        print(f"DEBUG: Stream event: {event_type}")

        # INTERRUPT
        if event_type == "__interrupt__":
            interrupt_value = payload[0].value
            print(f"DEBUG: Processing interrupt event: {interrupt_value}")
            await ws.send_json({"type": "interrupt", "message": interrupt_value})

            # Return to allow websocket loop to receive response
            return

        # STREAMED TOKEN
        if event_type == "stream":
            # print(f"DEBUG: Token received: {payload}") # Commented out to avoid too much noise
            await ws.send_json({"type": "token", "token": payload})
            continue

        # REGULAR AI MESSAGE
        if event_type == "agent":
            print(f"DEBUG: Agent message received: {payload}")
            await ws.send_json({"type": "agent_message", "message": payload})
            continue

        # Update state with latest from step
        if isinstance(payload, dict) and "messages" in payload:
            print(f"DEBUG: Updating state from step payload")
            pass

    print(f"DEBUG: run_agent sending 'done' message")
    await ws.send_json({"type": "done"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
