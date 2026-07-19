# AI-Powered Sports Quiz Generation Agent 🏆

## Project Overview

This project is an AI-powered agent capable of generating engaging, sports-related multiple-choice quizzes. It is designed to create interactive social media content by utilizing **Retrieval-Augmented Generation (RAG)** to ensure factual accuracy and avoid hallucinations. 

The application combines offline historical facts from a **ChromaDB vector database** with real-time web search via **DuckDuckGo** to ground the AI's responses. A sleek **Streamlit** dashboard provides a user-friendly interface to configure and generate the quizzes on the fly.

## Features

- **Dynamic Quiz Generation**: Select a sport (Cricket, Football, Badminton) and a difficulty level to generate a custom quiz.
- **Customizable Output**: Choose between generating 3 to 5 questions, and format the output as plain Text, structured JSON, or Markdown.
- **Retrieval-Augmented Generation (RAG)**: 
  - **ChromaDB**: Efficiently searches and retrieves relevant historical sports facts from an offline database.
  - **Web Search**: Integrates live web search to pull the latest news and tournament results to keep quizzes fresh.
- **Explainable Answers**: Each quiz question includes the correct answer along with a brief explanation derived directly from the retrieved context.
- **Context Inspection**: The dashboard allows users to inspect the exact ground truth texts that were fed to the LLM to generate the quiz.

## Prerequisites

- Python 3.8+
- An API Key from OpenRouter/OpenAI for LLM inference.

## Setup Instructions

1. **Clone the repository** (if applicable) and navigate to the project folder:
   ```bash
   cd "Statupbox"
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On MacOS/Linux:
   source venv/bin/activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (if not already present) and add your API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Data Preparation**:
   Ensure your historic facts are located in `data/sports_facts.json`. The app will automatically initialize and populate the ChromaDB vector database upon startup.

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
2. **Access the Dashboard**: Open your web browser and navigate to `http://localhost:8501`.
3. **Configure the Quiz**: Use the sidebar to select your desired sport, difficulty, number of questions, and output format.
4. **Generate**: Click **Generate Fresh Quiz**. The app will fetch offline facts, scrape live web context, and present your quiz on the screen!

## Project Structure

- `app.py`: The main Streamlit application script.
- `src/generator.py`: Connects the RAG contexts to the LLM for quiz generation.
- `src/database.py`: Handles ChromaDB vector database initialization and query logic.
- `src/search.py`: Manages the live web search functionality.
- `src/config.py`: Loads environment configurations.
- `data/`: Directory for storing local JSON fact datasets.
- `chroma_db/`: Persistent storage directory for the vector database.
