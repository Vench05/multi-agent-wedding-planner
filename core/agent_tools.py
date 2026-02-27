from langchain.messages import HumanMessage
from langchain.tools import tool

from core.wedding_agents import flight_agent, music_agent, venue_agent


@tool
def call_flight_agent(current_location: str, destination: str) -> str:
    """Call the flight agent to get flight information"""
    response = flight_agent.invoke(
        {
            "messages": HumanMessage(
                content=f"What are the best flight options from {current_location} to {destination}?"
            )
        }
    )

    return response["messages"][-1].content


@tool
def call_venue_agent(destination: str) -> str:
    """Call the venue agent to get venue information"""
    response = venue_agent.invoke(
        {
            "messages": HumanMessage(
                content=f"What are the best venues to visit in {destination}?"
            )
        }
    )

    return response["messages"][-1].content


@tool
def call_music_agent(destination: str) -> str:
    """Call the music agent to get music information"""
    response = music_agent.invoke(
        {
            "messages": HumanMessage(
                content=f"What are the best music events happening in {destination}?"
            )
        }
    )

    return response["messages"][-1].content
