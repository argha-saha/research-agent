from langchain.agents import create_tool_calling_agent, AgentExecutor
from core.tools import save_tool, search_tool, wiki_tool

def get_tools():
    return [save_tool, search_tool, wiki_tool]


def create_agent(llm, prompt, tools):
    return create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )


def create_agent_executor(agent, tools, verbose: bool = False):
    return AgentExecutor(agent=agent, tools=tools, verbose=verbose) 