from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

from core.wedding_agents import flight_agent, music_agent, venue_agent


@tool
def call_flight_agent(runtime: ToolRuntime) -> str:
    """Call the flight agent to get flight information"""
    try:
        current_location = runtime.state["current_location"]
        destination = runtime.state["destination"]
        response = flight_agent.invoke(
            {
                "messages": HumanMessage(
                    content=f"Find the best flight options from {current_location} to {destination}."
                )
            }
        )
        return response["messages"][-1].content

    except KeyError:
        return "Current location or destination is missing in the state. Please ask before calling this tool."


@tool
def call_venue_agent(runtime: ToolRuntime) -> str:
    """Call the venue agent to get venue information"""
    try:
        destination = runtime.state["destination"]
        guest_count = runtime.state["guest_count"]
        response = venue_agent.invoke(
            {
                "messages": HumanMessage(
                    content=f"Find the best venues for wedding in {destination} with capacity for {guest_count} guests."
                )
            }
        )

        return response["messages"][-1].content
    
    except KeyError:
        return "Destination and guest_count are missing in the state. Please ask before calling this tool."


@tool
def call_music_agent(runtime: ToolRuntime) -> str:
    """Call the music agent to get music information"""
    try:
        theme = runtime.state["theme"]
    except KeyError:
        return "Theme is missing in the state. Please ask before calling this tool."
    
    response = music_agent.invoke(
        {
            "messages": HumanMessage(
                content=f"Find and list the best music events for a wedding with theme of {theme}."
            )
        }
    )

    return response["messages"][-1].content


@tool
def update_wedding_state(
    runtime: ToolRuntime,
    current_location: str,
    destination: str,
    theme: str,
    music: list[str],
    budget: int,
    venues: str,
    date: str,
    guest_count: int,
) -> Command:
    """Update the wedding state when you know all of values for the state"""
    return Command(
        update={
            "current_location": current_location,
            "destination": destination,
            "theme": theme,
            "music": music,
            "budget": budget,
            "venues": venues,
            "date": date,
            "guest_count": guest_count,
            "messages": [
                ToolMessage(
                    "Wedding state updated successfully.",
                    tool_call_id=runtime.tool_call_id,
                )
            ]
        }
    )
