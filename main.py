from dotenv import load_dotenv

load_dotenv()

from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

from core.agent_tools import (call_flight_agent, call_music_agent,
                              call_venue_agent)
from core.prompts import main_system_prompt


class WeddingSchema(AgentState):
    current_location: str
    destination: str
    theme: str
    music: list[str]
    budget: int
    venues: str
    date: str
    guest_count: int



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
