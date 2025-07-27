# backend/app/routers/event_router.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..data.database import supabase_client

router = APIRouter()

# Pydantic models for request/response bodies
class EventCreate(BaseModel):
    event_name: str
    event_type: str
    event_date: str # YYYY-MM-DD
    number_of_guests: int
    budget: float

class EventUpdate(BaseModel):
    event_name: Optional[str] = None
    event_type: Optional[str] = None
    event_date: Optional[str] = None
    number_of_guests: Optional[int] = None
    budget: Optional[float] = None

class Event(EventCreate):
    id: int

@router.post("/", response_model=Event)
def create_event(event: EventCreate):
    """
    Creates a new event record in the database.
    """
    try:
        response = supabase_client.from_('events').insert(event.dict()).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=500, detail="Failed to create event.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating event: {e}")

@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int):
    """
    Retrieves a specific event by ID.
    """
    try:
        response = supabase_client.from_('events').select('*').filter('id', 'eq', event_id).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=404, detail="Event not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving event: {e}")

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate):
    """
    Updates an existing event record.
    """
    try:
        response = supabase_client.from_('events').update(event.dict(exclude_unset=True)).filter('id', 'eq', event_id).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=500, detail="Failed to update event.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating event: {e}")

@router.delete("/{event_id}")
def delete_event(event_id: int):
    """
    Deletes an event record.
    """
    try:
        response = supabase_client.from_('events').delete().filter('id', 'eq', event_id).execute()
        if response.data:
            return {"message": "Event deleted successfully."}
        raise HTTPException(status_code=404, detail="Event not found or failed to delete.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting event: {e}")