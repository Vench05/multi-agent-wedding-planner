from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain_mcp_adapters.client import MultiServerMCPClient
from core.prompts import flight_system_prompt

kiwi_travel_tools = None

def get_travel_tools():
    global kiwi_travel_tools
    if kiwi_travel_tools is None:
        kiwi_travel_client = MultiServerMCPClient(
            {
                "travel_server": {
                        "transport": "streamable_http",
                        "url": "https://mcp.kiwi.com"
                    }
            }
        )
        kiwi_travel_tools = kiwi_travel_client.get_tools()
    return kiwi_travel_tools


flight_agent = create_agent(
    model="gpt-5-nano", 
    tools=[get_travel_tools()],
    system_prompt=flight_system_prompt
)

venue_agent = create_agent(
    model="gpt-5-nano", tools=[TavilySearch(max_results=3, topics="venues")]
)

music_agent = create_agent(
    model="gpt-5-nano", tools=[TavilySearch(max_results=15, topics="music")]
)

