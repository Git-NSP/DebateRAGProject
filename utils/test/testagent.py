from utils.retriever import Retriever
from agent import DebateAgent

topic = "Spring Boot is better than Django."

retriever = Retriever("pro")

docs = retriever.retrieve(
    topic,
    top_k=5
)

agent = DebateAgent("Pro")

argument = agent.generate_argument(
    topic,
    docs
)

print(argument)

