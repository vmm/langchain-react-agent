# react_agent/tools.py
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()

# Set up API Keys
openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_api_key)

# Initialize Tavily client
tavily_client = TavilyClient(api_key=tavily_api_key)

@tool
def search_tool(query: str) -> str:
    """Searches the web for the query using Tavily."""
    try:
        search_result = tavily_client.search(query)
        # Extract and format the results
        results = []
        for item in search_result['results'][:3]:  # Get top 3 results
            results.append(f"- {item['title']}: {item['content'][:200]}...")

        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search error: {e}"

@tool
def calculator_tool(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time. Optionally specify a timezone (default: UTC)."""
    now = datetime.now()
    return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')} {timezone}"

@tool
def weather_tool(city: str) -> str:
    """Get current weather for a city using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Weather in {city}: {description}, Temperature: {temp}°C"
        return f"Error getting weather: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error: {e}"

@tool
def summarize_text(text: str) -> str:
    """Summarize a piece of text using the configured LLM."""
    try:
        response = llm.invoke(f"Please summarize this text concisely: {text}")
        return response.content
    except Exception as e:
        return f"Error summarizing text: {e}"

@tool
def convert_units(query: str) -> str:
    """
    Convert between different units. Example query: '5 km to miles' or '100 kg to lbs'
    """
    # Simple conversion factors
    conversions = {
        ('km', 'miles'): 0.621371,
        ('miles', 'km'): 1.60934,
        ('kg', 'lbs'): 2.20462,
        ('lbs', 'kg'): 0.453592,
        ('celsius', 'fahrenheit'): lambda x: (x * 9/5) + 32,
        ('fahrenheit', 'celsius'): lambda x: (x - 32) * 5/9
    }

    try:
        # Parse query (very basic parsing)
        parts = query.lower().split()
        if len(parts) != 4 or parts[2] != 'to':
            return "Please use format: '5 km to miles'"

        value = float(parts[0])
        from_unit = parts[1]
        to_unit = parts[3]

        # Find conversion
        conversion = conversions.get((from_unit, to_unit))
        if conversion is None:
            return f"Unsupported conversion: {from_unit} to {to_unit}"

        # Calculate result
        if callable(conversion):
            result = conversion(value)
        else:
            result = value * conversion

        return f"{value} {from_unit} = {result:.2f} {to_unit}"
    except Exception as e:
        return f"Error in conversion: {e}"

@tool
def store_note(input_str: str) -> str:
    """
    Store a note in a simple key-value format.
    Format: 'key: value' or 'key: multi-line value'
    """
    try:
        notes_file = "notes.json"
        # Load existing notes
        notes = {}
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as f:
                notes = json.load(f)

        # Parse input
        if ': ' not in input_str:
            return "Please use format 'key: value'"

        key, value = input_str.split(': ', 1)
        notes[key] = value

        # Save notes
        with open(notes_file, 'w') as f:
            json.dump(notes, f)

        return f"Stored note with key: {key}"
    except Exception as e:
        return f"Error storing note: {e}"

@tool
def retrieve_note(key: str) -> str:
    """Retrieve a stored note by its key."""
    try:
        notes_file = "notes.json"
        if not os.path.exists(notes_file):
            return "No notes found"

        with open(notes_file, 'r') as f:
            notes = json.load(f)

        return notes.get(key, f"No note found with key: {key}")
    except Exception as e:
        return f"Error retrieving note: {e}"

@tool
def process_data(data: str) -> str:
    """Process and analyze data, combining multiple operations."""
    # ... implementation ...

@tool
def manage_notes(action: str, data: dict) -> str:
    """Unified tool for note operations (store, retrieve, list, delete)."""
    # ... implementation ...
