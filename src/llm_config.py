from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import ResearchResponse

def create_openai_llm(model: str = "o4-mini") -> ChatOpenAI:
    return ChatOpenAI(model=model)


def create_anthropic_llm(model: str = "claude-sonnet-4-20250514") -> ChatAnthropic:
    return ChatAnthropic(model=model)


def create_parser() -> PydanticOutputParser:
    return PydanticOutputParser(pydantic_object=ResearchResponse)


def create_prompt(parser: PydanticOutputParser) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research assistant that will help generate a research paper.
                Answer the query and use necessary tools to get the information.
                Wrap the output in this format and provide no other text\n{format_instructions}
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions()) 