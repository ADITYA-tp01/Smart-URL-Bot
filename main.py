import streamlit as st
from rag import generate_answer, process_urls
import time

# Set page configuration
st.set_page_config(
    page_title="Smart URL Answer Bot", 
    page_icon="🔗", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        padding: 10px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    .url-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .answer-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .sources-card {
        background: #fff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
        margin-top: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    
    .status-info {
        background: #d1ecf1;
        color: #0c5460;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 0.5rem 0;
    }
    
    .question-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'urls_processed' not in st.session_state:
    st.session_state.urls_processed = False
if 'processed_urls' not in st.session_state:
    st.session_state.processed_urls = []

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🔗 Smart URL Answer Bot</h1>
    <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">Extract insights and get answers from web content using AI</p>
</div>
""", unsafe_allow_html=True)

# Create main layout with columns
col1, col2 = st.columns([1, 2])

# Sidebar - URL Input Section
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>📥 URL Processing</h2>
        <p>Add up to 3 URLs to analyze</p>
    </div>
    """, unsafe_allow_html=True)
    
    # URL inputs with better labels
    st.markdown("### 🌐 Enter URLs")
    url1 = st.text_input('First URL', placeholder="https://example.com/article1", help="Enter the first URL you want to analyze")
    url2 = st.text_input('Second URL (Optional)', placeholder="https://example.com/article2", help="Enter a second URL (optional)")
    url3 = st.text_input('Third URL (Optional)', placeholder="https://example.com/article3", help="Enter a third URL (optional)")
    
    st.markdown("---")
    
    # Process button
    process_button = st.button('🚀 Process URLs', help="Click to process the URLs and create the knowledge base")
    
    # Status indicator
    if st.session_state.urls_processed:
        st.success("✅ URLs processed successfully!")
        st.info(f"📊 Processed {len(st.session_state.processed_urls)} URL(s)")
        
        with st.expander("📋 View Processed URLs"):
            for i, url in enumerate(st.session_state.processed_urls, 1):
                st.write(f"{i}. {url}")
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### 📖 How to use:
    1. **Enter URLs** in the fields above
    2. **Click Process URLs** to analyze content
    3. **Ask questions** in the main area
    4. **Get AI-powered answers** with sources
    """)

# Main content area
with col2:
    # Status messages area
    status_container = st.container()
    
    # Process URLs logic
    if process_button:
        urls = [url.strip() for url in (url1, url2, url3) if url.strip()]
        
        if not urls:
            status_container.error("⚠️ Please enter at least one valid URL.")
        else:
            with status_container:
                st.info("🔄 Processing URLs... Please wait.")
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Process URLs with status updates
                    for i, status in enumerate(process_urls(urls)):
                        status_text.markdown(f'<div class="status-info">{status}</div>', unsafe_allow_html=True)
                        progress_bar.progress((i + 1) / 6)  # Assuming 6 steps
                        time.sleep(0.5)  # Small delay for better UX
                    
                    # Success state
                    st.session_state.urls_processed = True
                    st.session_state.processed_urls = urls
                    progress_bar.progress(1.0)
                    status_text.markdown('<div class="status-success">✅ All URLs processed successfully!</div>', unsafe_allow_html=True)
                    
                    st.balloons()  # Celebration effect
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error processing URLs: {str(e)}")

# Question and Answer Section
st.markdown("---")

# Question input container
st.markdown("""
<div class="question-container">
    <h2 style="color: #333; margin-bottom: 1rem;">💬 Ask Your Question</h2>
    <p style="color: #666; margin-bottom: 1.5rem;">Type your question below and get AI-powered answers based on the processed content.</p>
</div>
""", unsafe_allow_html=True)

# Question input with better styling
query = st.text_input(
    "",
    placeholder="What would you like to know about the content from your URLs?",
    help="Ask any question about the content from the URLs you've processed",
    label_visibility="collapsed"
)

# Enhanced question suggestions
if not st.session_state.urls_processed:
    st.info("💡 **Tip:** Process some URLs first, then you can ask questions about their content!")
else:
    st.markdown("""
    **💡 Example questions you can ask:**
    - What are the main topics discussed?
    - Can you summarize the key points?
    - What are the latest trends mentioned?
    - Compare the different viewpoints presented
    """)

# Answer generation and display
if query and st.session_state.urls_processed:
    with st.spinner("🤔 Analyzing content and generating answer..."):
        try:
            answer, sources = generate_answer(query)
            
            # Display answer in styled container
            st.markdown("""
            <div class="answer-card">
                <h3 style="color: #333; margin-bottom: 1rem;">🧠 AI Answer</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(answer)

            # Display sources if available
            if sources and sources.strip():
                st.markdown("""
                <div class="sources-card">
                    <h4 style="color: #333; margin-bottom: 1rem;">📚 Sources & References</h4>
                </div>
                """, unsafe_allow_html=True)
                
                source_list = [source.strip() for source in sources.strip().split("\n") if source.strip()]
                for i, source in enumerate(source_list, 1):
                    st.markdown(f"**{i}.** {source}")
            
            # Add feedback section
            st.markdown("---")
            st.markdown("### 📝 Was this answer helpful?")
            col_feedback1, col_feedback2, col_feedback3 = st.columns(3)
            
            with col_feedback1:
                if st.button("👍 Yes, very helpful"):
                    st.success("Thank you for your feedback!")
            
            with col_feedback2:
                if st.button("👎 Needs improvement"):
                    st.info("Thanks! We'll work on improving our answers.")
            
            with col_feedback3:
                if st.button("🔄 Try different question"):
                    st.info("Feel free to ask another question!")
                    
        except RuntimeError as e:
            st.error("⚠️ Please process the URLs first before asking a question.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

elif query and not st.session_state.urls_processed:
    st.warning("⚠️ Please process some URLs first before asking questions!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>• 🤖 Powered by AI •</p>
</div>
""", unsafe_allow_html=True)