from langchain.agents import AgentState


class WeddingSchema(AgentState):
    current_location: str
    destination: str
    theme: str
    music: list[str]
    budget: int
    venues: str
    date: str
    guest_count: int
