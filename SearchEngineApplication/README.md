# AI-Powered Search Engine with Chat Interface

A modern search engine application powered by OpenAI's ChatGPT with a beautiful Streamlit frontend and a robust FastAPI backend.

## 🚀 Features

- **Real-time Chat**: Powered by OpenAI's ChatGPT with streaming responses
- **Search Interface**: Clean, modern UI for product search
- **Response Tracking**: Uses OpenAI Responses API for conversation continuity
- **Comprehensive Logging**: Detailed logging for development and debugging
- **Error Handling**: Robust error handling with user-friendly messages
- **Modular Architecture**: Clean separation of concerns across frontend and backend

## 📁 Project Structure

```
SearchEngineApplication/
├── backend/
│   ├── models.py          # Pydantic data models
│   ├── config.py          # Configuration and logging setup
│   ├── client.py          # OpenAI client singleton
│   ├── helpers.py         # Business logic and utility functions
│   ├── routes.py          # API route handlers
│   ├── main.py            # FastAPI app setup
│   ├── run_server.py      # Server startup script
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Environment variables template
├── components/
│   ├── chat.py            # Chat interface component
│   ├── search_interface.py # Search form component
│   └── search_results.py  # Product results component
├── utils.py               # API communication utilities
├── data.py                # Sample product data
├── app.py                 # Main Streamlit application
└── README.md              # This file
```

## 🔧 Setup Instructions

### 1. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Start the backend server:
```bash
python run_server.py
```

### 2. Frontend Setup

In the main directory, run the Streamlit app:
```bash
streamlit run app.py
```

## 🔌 API Endpoints

### Core Chat Endpoints
- `POST /chat/start` - Start a new chat session with search query
- `POST /chat/message` - Send a message to existing session
- `GET /chat/{session_id}` - Retrieve session details
- `DELETE /chat/{session_id}` - Delete a chat session

### Management Endpoints
- `GET /` - Health check
- `GET /chat/sessions/list` - List all chat sessions
- `GET /chat/{session_id}/responses` - Get conversation responses

## 🌟 Key Improvements Made

### Backend Architecture
- **Modular Structure**: Separated models, routes, helpers, and configuration
- **OpenAI Responses API**: Implemented proper response tracking and conversation continuity
- **Singleton Client**: Efficient OpenAI client management
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Error Handling**: Robust error handling with proper HTTP status codes

### Frontend Architecture
- **Component-Based**: Separated chat, search, and results into individual components
- **Streaming Responses**: Restored word-by-word streaming effect for better UX
- **Error Management**: Removed fallback messages, added proper error handling
- **Logging**: Added frontend logging for better development experience

### Developer Experience
- **No Fallback Logic**: Clean error handling without confusing fallback behaviors
- **Comprehensive Logging**: Both backend and frontend log important events
- **Modular Code**: Easy to maintain and extend
- **Type Safety**: Proper Pydantic models for data validation

## 🔍 Usage

1. **Start Search**: Enter your search query on the homepage
2. **AI Response**: Get an intelligent response about your search from ChatGPT
3. **Continue Chatting**: Ask follow-up questions in the chat interface
4. **View Results**: Browse product results in the right panel
5. **Product Details**: Click "View Details" on any product card

## 🛠️ Development

### Backend Development
- All business logic is in `helpers.py`
- API routes are in `routes.py`
- Data models are in `models.py`
- Configuration is centralized in `config.py`

### Frontend Development
- Main app logic is in `app.py`
- UI components are in `components/`
- API utilities are in `utils.py`
- Sample data is in `data.py`

### Logging
- Backend logs to both console and `backend.log` file
- Frontend logs to browser console
- Configurable log levels via environment variables

## 📝 Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Weaviate Configuration (optional)
WEAVIATE_URL=your_weaviate_cluster_url
WEAVIATE_API_KEY=your_weaviate_api_key

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Development Settings
DEBUG=True
LOG_LEVEL=INFO
```

## 🚨 Troubleshooting

1. **Backend not starting**: Check OpenAI API key in `.env` file
2. **Frontend can't connect**: Ensure backend is running on port 8000
3. **Chat not working**: Verify OpenAI API key has sufficient credits
4. **Import errors**: Ensure all dependencies are installed correctly

## 📊 API Documentation

Once the backend is running, visit:
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc