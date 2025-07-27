# backend/app/data/database.py
import os
from supabase import create_client, Client

supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase_client: Client = None

def initialize_supabase_client():
    """Initializes the Supabase client globally."""
    global supabase_client
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and Key must be set in environment variables.")
    supabase_client = create_client(supabase_url, supabase_key)
    print("Supabase client initialized successfully.")

# Example of how to use it in other modules:
# from .database import supabase_client
#
# async def get_data_from_table(table_name: str):
#     response = await supabase_client.from_(table_name).select('*').execute()
#     return response.data