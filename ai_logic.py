# backend/app/core/ai_logic.py
import os
import google.generativeai as genai
from ..data.database import supabase_client
import json

class EventPlanningAgent:
    def __init__(self):
        """
        Initializes the agent by configuring the Google Gemini client.
        This establishes the connection to the AI model.
        """
        try:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not found.")
            
            genai.configure(api_key=api_key)
            
            generation_config = {"response_mime_type": "application/json"}
            
            # Using Gemini 1.5 Flash for its speed, capability, and generous free tier.
            self.model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=generation_config
            )
            print("Expert Indian Wedding Planner (Gemini) client initialized successfully.")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to initialize Google Gemini client: {e}")
            self.model = None

    def _build_enhanced_prompt(self, user_query: str) -> str:
        """
        Dynamically builds a highly detailed and context-aware prompt.
        This is the core logic that makes the AI an "expert".
        """
        # 1. Establish the Expert Persona and Core Instructions
        base_prompt = """
        You are an expert Indian Wedding Planner AI. Your task is to create a detailed, practical, and culturally relevant wedding plan based on user requests. All budgetary figures must be in Indian Rupees (INR).

        You must provide the plan ONLY in the following structured JSON format. Do not include any other text, explanations, or markdown formatting like ```json.
        {
            "event_name": "string",
            "event_type": "string (e.g., Rajasthani Royal Wedding, Intimate Kerala Wedding)",
            "event_date": "YYYY-MM-DD (or a suggested month/season if not specified)",
            "number_of_guests": "integer",
            "budget": "float (in INR)",
            "required_components": [
                {"component_type": "Venue", "details": "string (e.g., Palace Hotel in Udaipur, Beach Resort in Goa)", "preferences": "string"},
                {"component_type": "Caterer", "details": "string (e.g., Authentic Punjabi cuisine, South Indian Sadhya)", "preferences": "string"},
                {"component_type": "Decorator", "details": "string (e.g., Marigold and Gota Patti theme, Modern minimalist theme)", "preferences": "string"},
                {"component_type": "Mehendi Artist", "details": "string", "preferences": "string"},
                {"component_type": "Photographer/Videographer", "details": "string (e.g., Candid and traditional mix)", "preferences": "string"},
                {"component_type": "Entertainment", "details": "string (e.g., Bollywood DJ, Live Sangeet band, Dhol players)", "preferences": "string"},
                {"component_type": "Pandit/Priest", "details": "string", "preferences": "string"},
                {"component_type": "Wedding Choreographer", "details": "string (for Sangeet performances)", "preferences": "string"}
            ],
            "action_items": ["string (a detailed list of tasks to be done)"]
        }
        """

        # 2. Add Dynamic Context based on Keywords in the User's Query
        contextual_hints = ""
        query_lower = user_query.lower()
        
        # This dictionary makes the logic clean and easily extensible
        keyword_map = {
            "rajasthan": "\nHint: For a Rajasthani wedding, suggest palace or fort venues, folk dancers like Ghoomar or Kalbelia, and a 'Gota Patti' decor theme.",
            "udaipur": "\nHint: For a Rajasthani wedding, suggest palace or fort venues, folk dancers like Ghoomar or Kalbelia, and a 'Gota Patti' decor theme.",
            "jaipur": "\nHint: For a Rajasthani wedding, suggest palace or fort venues, folk dancers like Ghoomar or Kalbelia, and a 'Gota Patti' decor theme.",
            "kerala": "\nHint: For a Kerala wedding, suggest backwater resort venues, a traditional Sadhya feast on banana leaves, and Chenda Melam percussionists.",
            "goa": "\nHint: For a Goan wedding, suggest beach resort venues, a seaside ceremony, and a mix of Goan and continental cuisine. Mention options for both church weddings and Hindu ceremonies.",
            "punjabi": "\nHint: For a Punjabi wedding, suggest farmhouse venues, high-energy Dhol players and a Jaggo night, and a rich menu with lots of tandoori items and chaat stalls.",
            "delhi": "\nHint: For a Delhi wedding, suggest luxury banquet halls or farmhouses in Chattarpur. The style can be very grand and modern.",
            "mumbai": "\nHint: For a Mumbai wedding, suggest luxury hotels or rooftop bars. The style is often chic, modern, and space-conscious."
        }
        
        for keyword, hint in keyword_map.items():
            if keyword in query_lower:
                contextual_hints += hint
                break # Stop after the first match to avoid conflicting hints

        # 3. Combine everything into the final prompt
        final_prompt = f"{base_prompt}\n{contextual_hints}\n\nNow, generate a complete plan for the following user request:\n---_USER_REQUEST_---\n{user_query}"
        
        return final_prompt

    async def generate_event_plan(self, user_query: str, existing_details: dict = None) -> dict:
        """
        Generates a comprehensive Indian wedding plan using the Gemini model.
        This function orchestrates the prompt building and API call.
        """
        if not self.model:
            return {"error": "Critical: Gemini client is not initialized. Please check the server logs and API key."}

        try:
            # Build the intelligent, context-aware prompt
            enhanced_prompt = self._build_enhanced_prompt(user_query)
            
            # Asynchronously generate the content
            print("Sending enhanced prompt to Gemini...")
            response = await self.model.generate_content_async(enhanced_prompt)
            
            # Extract and parse the JSON response
            plan_json = response.text
            print("Received plan from Gemini. Parsing JSON.")
            return json.loads(plan_json)
        
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to parse JSON from Gemini response. Raw response: {response.text}. Error: {e}")
            return {"error": "The AI returned an invalid format. Please try rephrasing your request."}
        except Exception as e:
            print(f"ERROR: An unexpected error occurred while generating event plan: {e}")
            return {"error": f"An unexpected error occurred: {e}"}

    # --- Database Functions ---
    # These functions remain synchronous as they perform simple lookups.
    # Their docstrings are updated for context.

    def get_all_venues(self) -> list:
        """
        Fetches all wedding venues from the database.
        In a real app, this would be filtered by city, capacity, and type (e.g., Palace, Farmhouse).
        """
        response = supabase_client.from_('venues').select('*').execute()
        return response.data if response.data else []

    def recommend_caterers(self, cuisine_type: str, budget_per_plate: int) -> list:
        """
        Recommends caterers based on cuisine type and budget.
        A real implementation would filter the database query with these parameters.
        """
        response = supabase_client.from_('caterers').select('*').execute()
        return response.data if response.data else []

    def get_all_decorators(self) -> list:
        """
        Fetches all wedding decorators from the database.
        Future logic could filter by specialization (e.g., traditional, modern).
        """
        response = supabase_client.from_('decorators').select('*').execute()
        return response.data if response.data else []

    def get_all_event_services_providers(self) -> list:
        """
        Fetches all miscellaneous event service providers, like choreographers, mehendi artists, etc.
        """
        response = supabase_client.from_('event_services_providers').select('*').execute()
        return response.data if response.data else []