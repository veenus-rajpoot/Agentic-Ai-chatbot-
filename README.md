# Agentic AI Chatbot

A powerful, agentic conversational AI chatbot built with LangGraph, Streamlit, and Google's Gemini API. This chatbot features real-time tool execution, persistent conversation history, and multi-threaded conversation management.

## Features

 **Agentic Architecture** - Leverages LangGraph's StateGraph for intelligent multi-step reasoning and tool execution

🔧 **Built-in Tools**:
- **Web Search** - Real-time information retrieval using DuckDuckGo
- **Stock Price Lookup** - Fetch current stock prices via Alpha Vantage API
- **Calculator** - Perform arithmetic operations (add, subtract, multiply, divide)

**Conversation Management**:
- Multiple concurrent conversations with unique thread IDs
- Persistent storage using SQLite
- Automatic conversation titles based on first user message
- Easy switching between conversation threads

 **Interactive UI** - Streamlit-based frontend with:
- Real-time message streaming
- Sidebar navigation for conversation history
- Clean chat interface with message history

**Intelligent Message Handling**:
- Support for complex message structures
- Stream-based response generation
- Automatic content parsing

## Tech Stack

- **Backend**: LangGraph, LangChain, Google Generative AI (Gemini 3.5 Flash)
- **Frontend**: Streamlit
- **Storage**: SQLite with LangGraph's SqliteSaver
- **APIs**: 
  - Google Generative AI (Gemini)
  - Alpha Vantage (Stock Prices)
  - DuckDuckGo (Web Search)

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/veenus-rajpoot/Agentic-Ai-chatbot-.git
cd Agentic-Ai-chatbot-
```

2. **Create a virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
Create a `.env` file in the project root with:
```env
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
```

## Usage

1. **Start the Streamlit application**:
```bash
streamlit run streamlit_frontend.py
```

2. **Access the chatbot**:
- Open your browser and navigate to `http://localhost:8501`
- The Streamlit interface will load with the chatbot UI

3. **Interact with the chatbot**:
- Type your message in the chat input field
- The chatbot will intelligently use tools (search, calculator, stock prices) as needed
- View your conversation history in the left sidebar
- Create new conversations with the "New Chat" button
- Switch between saved conversations by clicking on them in the sidebar

## Project Structure

```
Agentic-Ai-chatbot-/
├── langgraph_backend.py      # Core chatbot logic with LangGraph
├── streamlit_frontend.py     # Streamlit UI and user interface
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── chatbot.db              # SQLite database (auto-generated)
```

## How It Works

### Backend (`langgraph_backend.py`)

1. **LLM Configuration**: Uses Google's Gemini 3.5 Flash model for intelligent reasoning
2. **Tool Integration**: Binds search, stock price, and calculator tools to the LLM
3. **State Management**: Implements `ChatState` TypedDict to manage conversation state with message history
4. **Graph Architecture**:
   - `chat_node`: Processes user queries and generates responses
   - `tools`: Executes tool calls when needed
   - Conditional routing based on tool requirements
5. **Persistence**: Uses SQLite with LangGraph's SqliteSaver for conversation persistence

### Frontend (`streamlit_frontend.py`)

1. **Session Management**: Manages thread IDs and message history in Streamlit session state
2. **Conversation Threads**: Display and switch between multiple conversation threads
3. **Message Streaming**: Real-time streaming of AI responses for better UX
4. **Dynamic Updates**: Automatic rerun when new conversations are created

## Available Tools

### Web Search
Search the web for current information using DuckDuckGo:
```
"What are the latest news about AI?"
"Find information about Python 3.12"
```

### Stock Price
Fetch current stock prices:
```
"What's the price of AAPL?"
"Get me Tesla stock price"
```

### Calculator
Perform arithmetic calculations:
```
"Calculate 100 + 50"
"What is 25 multiplied by 4?"
```

## API Keys Required

1. **Google API Key** (Required):
   - Get from [Google AI Studio](https://aistudio.google.com/apikey)
   - Add to `.env` as `GOOGLE_API_KEY`

2. **Alpha Vantage API Key** (Pre-configured):
   - Already included in the code (hardcoded for demo)
   - For production, move to `.env`

## Database

The chatbot uses SQLite to persist conversations:
- **File**: `chatbot.db` (auto-generated)
- **Storage**: Thread IDs, messages, and conversation history
- **Access**: Automatically managed by LangGraph's SqliteSaver

## Future Enhancements

- [ ] Add more tools (weather, news aggregation, etc.)
- [ ] Implement user authentication
- [ ] Add conversation export/download functionality
- [ ] Support for custom LLM models
- [ ] Web UI improvements (dark mode, themes)
- [ ] Conversation analytics and insights

## Troubleshooting

**Issue: "Module not found" errors**
- Solution: Ensure all dependencies in `requirements.txt` are installed
- Run: `pip install -r requirements.txt --upgrade`

**Issue: API key errors**
- Solution: Verify `.env` file exists and contains valid API keys
- Check: `GOOGLE_API_KEY` is correctly set

**Issue: Database locked errors**
- Solution: Delete `chatbot.db` and restart the application
- The database will be recreated automatically

**Issue: Streamlit not loading**
- Solution: Ensure port 8501 is available
- Try: `streamlit run streamlit_frontend.py --logger.level=debug`

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests

## License

This project is open source and available under the MIT License.

## Author

**Veenus Rajpoot** - [GitHub Profile](https://github.com/veenus-rajpoot)

## Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based orchestration
- [LangChain](https://github.com/langchain-ai/langchain) - AI framework
- [Streamlit](https://streamlit.io/) - UI framework
- [Google Generative AI](https://ai.google.dev/) - LLM provider
