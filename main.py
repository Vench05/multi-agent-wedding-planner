from dotenv import load_dotenv

load_dotenv()

from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from core.agent_tools import (call_flight_agent, call_music_agent,
                              call_venue_agent)


class WeddingSchema(AgentState):
    current_location: str
    destination: str
    music: list[str]
    budget: int
    venues: str
    date: str
    guest_count: int


main_system_prompt = """You are a wedding planner assistant. You can help the user plan their wedding by providing information about flights
        to the wedding destination, venues to visit in the wedding destination, and music events happening in the wedding destination. You can use the following tools to get this information:
        - call_flight_agent: Call the flight agent to get flight information
        - call_venue_agent: Call the venue agent to get venue information
        - call_music_agent: Call the music agent to get music information
        Tell the user current data with WeddingSchema and ask if they want to update any of the data. 
        If they do, update the data and call the appropriate tool to get the information they need. 
        If they don't, provide them with the information they need based on the current data in WeddingSchema."""


def main():
    main_agent = create_agent(
        model="gpt-5-nano",
        tools=[call_flight_agent, call_venue_agent, call_music_agent],
        checkpointer=InMemorySaver(),
        state_schema=WeddingSchema,
        system_prompt=main_system_prompt,
    )

    current_location = input("User: What is your current location? \n> ")
    user_input = f"lets plan my wedding! My current location is {current_location}. tell me what is next step to plan my wedding."
        
    while True:
        response = main_agent.invoke({"messages": [HumanMessage(content=user_input)]},
                                     {"configurable": {"thread_id": "1"}})
        print(response["messages"][-1].content, end="\n\n")
        
        user_input = input(f"(type 'exit' to quit) User: \n> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
