# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv # Import the load_dotenv function

# Load environment variables from the .env file
load_dotenv()

from .routers import agent_router, event_router
from .data.database import initialize_supabase_client

app = FastAPI(
    title="Planiva AI Event Planner API",
    description="API for managing event planning, AI agent interactions, and database operations.",
    version="1.0.0",
)

# CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
# This will now successfully find the loaded environment variables
initialize_supabase_client()

# Include routers
app.include_router(agent_router.router, prefix="/api/agent", tags=["AI Agent"])
app.include_router(event_router.router, prefix="/api/events", tags=["Event Management"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Planiva AI Event Planner API!"}                     