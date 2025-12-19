from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from agno.db.sqlite import SqliteDb
from transcription_reader import get_creator_transcriptions, list_available_creators
from dotenv import load_dotenv

from agno.os import AgentOS 
import os

load_dotenv()

copy = Agent(
    model=Gemini(id='gemini-2.5-flash', api_key=os.getenv("GOOGLE_API_KEY")),
    name="copywriter",
    num_history_sessions=4,
    add_history_to_context=True,
    db=SqliteDb(session_table="agent_sessions", db_file="tmp/storage.db"),
    tools=[TavilyTools(), get_creator_transcriptions, list_available_creators],
    instructions=open(os.path.join(os.path.dirname(__file__), "prompts", "copywriter.md"), encoding="utf-8").read()
)

agent_os = AgentOS(
    name="Agente de Copy",
    agents=[copy]
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="agent:app", reload=True, reload_delay=1)