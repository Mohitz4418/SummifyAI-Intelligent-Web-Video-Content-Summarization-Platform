import validators
import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
from urllib.parse import parse_qs, urlparse
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

# Page configuration
st.set_page_config(page_title="SummifyAI", page_icon="🦜", layout="wide")

# Sidebar for app options
with st.sidebar:
    st.title("🦜 SummifyAI: Intelligent Web & Video Content Summarization Platform")
    st.markdown("---")
    
    # API Key input
    groq_api_key = st.text_input("Enter Groq API Key", value="", type="password")
    
    st.markdown("---")
    
    # Navigation options
    option = st.radio(
        "Choose content type:",
        ["Website Summarization", "YouTube Video Summarization"]
    )
    
    st.markdown("---")
    st.markdown("Made with ❤️ using LangChain and Groq")

# Main content area title
st.title("")

# Function to summarize website content
def summarize_website(url):
    try:
        with st.spinner("Loading website content..."):
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/"
            }
            
            loader = UnstructuredURLLoader(
                urls=[url], 
                ssl_verify=False,
                headers=headers
            )
            
            docs = loader.load()
            
            if not docs:
                st.error("Could not extract content from the provided URL")
                return
            
            st.success("Website content loaded successfully!")
            
            with st.spinner("Generating summary..."):
                # Chain For Summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)
                
                st.markdown("### Summary")
                st.markdown(output_summary)
                
    except Exception as e:
        st.error(f"Error loading website content: {str(e)}")

# Function to summarize YouTube video
def summarize_youtube(url):
    try:
        with st.spinner("Loading YouTube transcript..."):
            # Extract video ID from URL
            if "youtube.com" in url:
                video_id = parse_qs(urlparse(url).query).get("v", [None])[0]
            else:  # youtu.be format
                video_id = urlparse(url).path.lstrip("/")
            
            if not video_id:
                st.error("Could not extract YouTube video ID from URL")
                return
            
            # Get video metadata
            try:
                # Get video title
                response = requests.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json")
                if response.status_code == 200:
                    video_info = response.json()
                    video_title = video_info.get("title", "Untitled YouTube Video")
                    
                    # Display video thumbnail
                    st.image(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg", caption=video_title)
                else:
                    video_title = "YouTube Video"
            except Exception:
                video_title = "YouTube Video"
            
            # Get transcript directly using youtube_transcript_api
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript_text = " ".join([entry["text"] for entry in transcript_list])
            
            # Create Document objects compatible with LangChain
            docs = [Document(
                page_content=transcript_text,
                metadata={"source": url, "title": video_title}
            )]
            
            st.success(f"Successfully loaded transcript from: {video_title}")
            
            with st.spinner("Generating summary..."):
                # Chain For Summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)
                
                st.markdown("### Summary")
                st.markdown(output_summary)
                
    except (TranscriptsDisabled, NoTranscriptFound) as te:
        st.error(f"No transcript available for this video: {te}")
    except Exception as e:
        st.error(f"Error processing YouTube video: {str(e)}")

# Initialize LLM
def initialize_llm(api_key):
    if not api_key.strip():
        st.warning("Please enter your Groq API key in the sidebar")
        return None
    
    try:
        return ChatGroq(model="gemma2-9b-it", groq_api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing LLM: {str(e)}")
        return None

# Define prompt template
prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Initialize LLM if API key is provided
llm = initialize_llm(groq_api_key) if groq_api_key else None

# Display content based on selected option
if option == "Website Summarization":
    st.header("Website Summarization")
    
    st.markdown("""
    Enter the URL of any website you want to summarize. 
    The system will extract the content and generate a concise summary.
    """)
    
    website_url = st.text_input("Website URL", placeholder="https://example.com")
    
    if st.button("Summarize Website"):
        if not validators.url(website_url):
            st.error("Please enter a valid website URL")
        elif llm is None:
            st.error("Please enter a valid Groq API key in the sidebar")
        else:
            summarize_website(website_url)

elif option == "YouTube Video Summarization":
    st.header("YouTube Video Summarization")
    
    st.markdown("""
    Enter the URL of any YouTube video.
    The system will extract the transcript and generate a concise summary.
    """)
    
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    if st.button("Summarize YouTube Video"):
        if not validators.url(youtube_url) or not ("youtube.com" in youtube_url or "youtu.be" in youtube_url):
            st.error("Please enter a valid YouTube URL")
        elif llm is None:
            st.error("Please enter a valid Groq API key in the sidebar")
        else:
            summarize_youtube(youtube_url)