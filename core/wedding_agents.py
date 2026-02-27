from langchain.agents import create_agent
from langchain_tavily import TavilySearch

flight_agent = create_agent(
    model="gpt-5-nano", tools=[TavilySearch(max_results=3, topics="flights")]
)

venue_agent = create_agent(
    model="gpt-5-nano", tools=[TavilySearch(max_results=3, topics="venues")]
)

music_agent = create_agent(
    model="gpt-5-nano", tools=[TavilySearch(max_results=15, topics="music")]
)

