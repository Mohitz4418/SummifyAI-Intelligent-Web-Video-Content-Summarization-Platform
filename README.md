# SummifyAI: Intelligent Web & Video Content Summarization Platform

The SummifyAI is a versatile application built with Streamlit that enables users to generate concise summaries of web content from two primary sources: websites and YouTube videos. The application extracts content from these sources and processes it through a language model to create informative summaries, making it easier for users to quickly understand the main points without having to read or watch the entire content.


## 🚀 Features

- **Dual Content Sources**: Summarize both websites and YouTube video transcripts
- **Interactive UI**: Clean Streamlit interface with sidebar navigation
- **AI-Powered Summaries**: Generate concise, informative summaries with state-of-the-art language models
- **YouTube Integration**: Automatic transcript extraction from YouTube videos
- **Robust Error Handling**: Comprehensive validation and error management

## 📋 Requirements

- Python 3.10
- Groq API Key ([Get one here](https://console.groq.com/))

## 🧰 How It Works

### Technology Stack

The application leverages the Groq API's high-performance inference capabilities to deliver fast and efficient summarization through their optimized language model infrastructure.

### Core Components

- **Frontend Framework**: Streamlit
- **Language Model**: Groq-hosted Gemma 2 (9B parameters, instruction-tuned)
- **LLM Integration**: LangChain for seamless orchestration
- **API Integration**: Groq API for accessing state-of-the-art language models

### Libraries and Tools

- **Content Extraction**:
  - UnstructuredURLLoader (for website content extraction)
  - YouTube Transcript API (for caption/transcript extraction)
  
- **Processing Pipeline**:
  - LangChain's summarization chains for structured processing
  - Custom prompt templates for optimized summary generation

## 📝 Notes

- YouTube summarization requires videos to have available transcripts/captions
- Website summarization works best on text-heavy pages with clear content structure
- Summary quality depends on content clarity and the language model's capabilities