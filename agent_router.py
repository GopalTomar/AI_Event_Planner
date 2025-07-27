# backend/app/routers/agent_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.ai_logic import EventPlanningAgent

router = APIRouter()
event_planning_agent = EventPlanningAgent() # Initialize the agent

class UserQuery(BaseModel):
    query: str
    existing_details: dict = None

class EventPlanResponse(BaseModel):
    event_name: str
    event_type: str
    event_date: str
    number_of_guests: int
    budget: float
    required_components: list
    action_items: list

@router.post("/plan_event", response_model=EventPlanResponse)
async def plan_event(user_query: UserQuery):
    """
    Receives a user query and generates an event plan using the AI agent.
    """
    try:
        # This remains async because the underlying AI call is async
        plan = await event_planning_agent.generate_event_plan(user_query.query, user_query.existing_details)
        if "error" in plan:
            raise HTTPException(status_code=500, detail=plan["error"])
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate event plan: {e}")

@router.get("/venues", response_model=list)
def get_venues():
    """
    Fetches all available venues.
    """
    try:
        venues = event_planning_agent.get_all_venues()
        return venues
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch venues: {e}")

@router.get("/caterers", response_model=list)
def get_caterers():
    """
    Fetches all caterers.
    """
    try:
        caterers = event_planning_agent.get_all_caterers()
        return caterers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch caterers: {e}")

@router.get("/decorators", response_model=list)
def get_decorators():
    """
    Fetches all decorators.
    """
    try:
        decorators = event_planning_agent.get_all_decorators()
        return decorators
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch decorators: {e}")

@router.get("/service_providers", response_model=list)
def get_service_providers():
    """
    Fetches all event service providers.
    """
    try:
        service_providers = event_planning_agent.get_all_event_services_providers()
        return service_providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch service providers: {e}")