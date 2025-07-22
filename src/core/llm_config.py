import json
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models.research_response import ResearchResponse

def load_models_from_json() -> dict:
    json_path = os.path.join(os.path.dirname(__file__), "models", "llm_models.json")
    
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Models file not found at {json_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in {json_path}")
    except Exception as e:
        raise Exception(f"Error loading models from {json_path}: {e}")


def get_default_openai_model() -> str:
    models_config = load_models_from_json()
    return models_config["openai"]["o4-mini"]


def get_default_anthropic_model() -> str:
    models_config = load_models_from_json()
    return models_config["anthropic"]["Claude Sonnet 4"]


def create_openai_llm(model: str = None) -> ChatOpenAI:
    if model is None:
        model = get_default_openai_model()
    return ChatOpenAI(model=model)


def create_anthropic_llm(model: str = None) -> ChatAnthropic:
    if model is None:
        model = get_default_anthropic_model()
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