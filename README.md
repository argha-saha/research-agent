# AI Research Agent

A research assistant that uses AI models to perform comprehensive research on any topic. The agent leverages multiple tools including web search, Wikipedia, and can save research results to files.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/argha-saha/research-agent.git
   cd research-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

## Usage

Run the research agent:

```bash
python src/main.py
```

The agent will prompt you to enter a research query, then perform comprehensive research using available tools.

### CLI Options

The research agent supports several command-line options to control output verbosity:

```bash
# Basic usage
python src/main.py

# Show detailed LLM thought process
python src/main.py --verbose
# or
python src/main.py -v

# Show tools used during research
python src/main.py --tools
# or
python src/main.py -t

# Show everything
python src/main.py --all
# or
python src/main.py -a

# Combine options
python src/main.py -v -t
```

**Output Modes:**
- **Default (clean)**: Shows only research results and sources
- **Verbose**: Shows LLM thought process and reasoning
- **Tools**: Shows which tools were used during research
- **All**: Shows everything 

### Using Different Models

You can specify different models when initializing the agent:

```python
agent = ResearchAgent(model="o3")
```
```python
agent = ResearchAgent(model="claude-sonnet-4-20250514")
```

## Configuration

### Model Configuration

Edit `src/models/llm_models.json` to add or modify available models (or use specific versions):

```json
{
    "openai": {
        "model_name": "model_identifier"
    },
    "anthropic": {
        "model_name": "model_identifier"
    }
}
```

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key is required when using OpenAI models such as gpt-4o
- `ANTHROPIC_API_KEY`: Anthropic API key is required when using Anthropic models such as Claude Sonnet 4

### Getting API Keys
- **OpenAI**: [OpenAI Platform](https://platform.openai.com/)
- **Anthropic**: [Anthropic Console](https://console.anthropic.com/)