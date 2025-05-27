import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

def init_session_state():
    if "files_processed" not in st.session_state:
        st.session_state.files_processed = False
    if "file_info" not in st.session_state:
        st.session_state.file_info = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "clear_conversation" not in st.session_state:
        st.session_state.clear_conversation = False
    # Initialize raw_prompt if it doesn't exist
    if "raw_prompt" not in st.session_state:
        st.session_state.raw_prompt = ""
    # Add example trigger state
    if "example_triggered" not in st.session_state:
        st.session_state.example_triggered = False

def configure_gemini():
    """Configure Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    else:
        st.error("Google API Key not found. Please set the GOOGLE_API_KEY environment variable.")
        return False

def get_system_prompt():
    return """You are MetaPromptor, an expert AI prompt engineer built on Google's Gemini framework. Your goal is to take any user-provided "raw" prompt and transform it into a clear, detailed, and highly structured prompt that elicits the best possible response from downstream language models.

When you receive a raw prompt, follow these steps exactly:

**Analyze the User's Intent**
- Identify the primary objective: what the user ultimately wants to achieve.
- Note any secondary objectives such as tone, style, format, or special requirements.

**Spot Ambiguities and Insert Clarifications**
- If any part of the user's request is unclear, add a placeholder for a clarifying question in square brackets.
- Example: [Clarifying Question: "Should the summary be under 100 words or under 200 words?"]

**Break the Task into Core Components**
- Context: Describe any background information the model needs to know.
- Role: Specify the persona or expertise the model should adopt (e.g., "an experienced science teacher").
- Task: State exactly what the model must do (e.g., "Explain the concept using analogies").
- Constraints: List any limitations (word count, vocabulary level, formatting rules, prohibited topics).
- Examples: If helpful, provide a brief input/output example to illustrate the desired style or structure.

**Add Meta-Instructions for Self-Reflection**
- Prompt the model to think step by step ("List your sub-tasks before generating").
- Instruct it to verify completeness ("After drafting, check that every objective is addressed").
- Encourage consistency checks ("Ensure tone and formatting are uniform throughout").

**Organize the Final Prompt in Plain English**
- Use clear headings or bullet lists to delineate each component.
- Write as a cohesive system message that can be pasted directly into any LLM setup.

**Output Only the Ready-to-Use Prompt**
- Do not include any commentary, analysis, or explanation—only the polished prompt itself.

Example Transformation:

Raw Prompt from User:
"Explain quantum computing in simple terms for a 10-year-old."

Your Transformed System Prompt:

You are an experienced STEM educator who excels at making complex ideas simple and engaging for young children.

Context:
- Audience: A curious 10-year-old with no background in physics or computing.

Task:
- Explain what quantum computing is, using everyday analogies.
- Keep sentences short and lively.

Constraints:
- Use language appropriate for a 10-year-old.
- Limit the explanation to around 150 words.
- Avoid technical jargon; if you must use a new term, define it immediately.

Meta-Instructions:
- Think step by step: first introduce the idea of bits, then describe how quantum bits differ.
- After writing, review each sentence to ensure clarity and simplicity.

Output Format:
- A single, engaging paragraph that reads like a story a child would understand."""

def generate_structured_prompt(raw_prompt):
    """Generate structured prompt using Gemini"""
    try:
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Combine system prompt with user's raw prompt
        full_prompt = f"{get_system_prompt()}\n\nNow transform this raw prompt:\n\n{raw_prompt}"
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
    except Exception as e:
        st.error(f"Error generating structured prompt: {str(e)}")
        return None

def create_copy_button(text_to_copy):
    """Create a simple copy mechanism using Streamlit components"""
    import streamlit.components.v1 as components
    import time
    
    # Create a unique ID for this instance
    unique_id = str(int(time.time() * 1000))
    
    # Enhanced HTML with better styling for dark theme
    copy_component = f"""
    <div id="copy-container-{unique_id}" style="margin: 10px 0;">
        <button id="copy-btn-{unique_id}" 
                onclick="copyToClipboard{unique_id}()" 
                style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 12px;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 14px;
                    width: 100%;
                    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
                    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    min-height: 48px;
                "
                onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 24px rgba(102, 126, 234, 0.4)'"
                onmouseout="this.style.transform='translateY(0px)'; this.style.boxShadow='0 8px 16px rgba(102, 126, 234, 0.3)'"
                >
            <span style="font-size: 16px;">📋</span>
            <span>Copy to Clipboard</span>
        </button>
        
        <textarea id="copy-text-{unique_id}" 
                  style="position: absolute; left: -9999px; opacity: 0;"
                  readonly>{text_to_copy}</textarea>
    </div>

    <script>
        function copyToClipboard{unique_id}() {{
            const button = document.getElementById('copy-btn-{unique_id}');
            const textArea = document.getElementById('copy-text-{unique_id}');
            
            try {{
                // Method 1: Modern clipboard API
                if (navigator.clipboard && window.isSecureContext) {{
                    navigator.clipboard.writeText(textArea.value).then(() => {{
                        button.innerHTML = '<span style="font-size: 16px;">✅</span><span>Copied!</span>';
                        button.style.background = 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)';
                        button.style.transform = 'scale(0.95)';
                        setTimeout(() => {{
                            button.innerHTML = '<span style="font-size: 16px;">📋</span><span>Copy to Clipboard</span>';
                            button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                            button.style.transform = 'scale(1)';
                        }}, 2000);
                    }}).catch(() => {{
                        fallbackCopy{unique_id}();
                    }});
                }} else {{
                    fallbackCopy{unique_id}();
                }}
            }} catch (err) {{
                fallbackCopy{unique_id}();
            }}
        }}
        
        function fallbackCopy{unique_id}() {{
            const button = document.getElementById('copy-btn-{unique_id}');
            const textArea = document.getElementById('copy-text-{unique_id}');
            
            try {{
                textArea.style.position = 'static';
                textArea.style.opacity = '1';
                textArea.select();
                textArea.setSelectionRange(0, 99999);
                
                const successful = document.execCommand('copy');
                
                textArea.style.position = 'absolute';
                textArea.style.opacity = '0';
                
                if (successful) {{
                    button.innerHTML = '<span style="font-size: 16px;">✅</span><span>Copied!</span>';
                    button.style.background = 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)';
                    setTimeout(() => {{
                        button.innerHTML = '<span style="font-size: 16px;">📋</span><span>Copy to Clipboard</span>';
                        button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    }}, 2000);
                }} else {{
                    throw new Error('Copy command failed');
                }}
            }} catch (err) {{
                button.innerHTML = '<span style="font-size: 16px;">⚠️</span><span>Manual Copy Needed</span>';
                button.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
                setTimeout(() => {{
                    button.innerHTML = '<span style="font-size: 16px;">📋</span><span>Copy to Clipboard</span>';
                    button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                }}, 3000);
            }}
        }}
    </script>
    """
    
    return copy_component

def inject_dark_theme_css():
    """Inject CSS to force dark theme and ensure proper styling"""
    st.markdown("""
    <style>
    /* Force dark theme detection and set base colors */
    .stApp {
        background-color: #0e1117 !important;
        color: #fafafa !important;
    }
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Set dark theme variables */
    :root {
        --background-color: rgba(30, 41, 59, 0.8) !important;
        --border-color: #374151 !important;
        --text-color: #f1f5f9 !important;
        --card-bg: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(55, 65, 81, 0.6) 100%) !important;
        --info-bg: rgba(59, 130, 246, 0.15) !important;
        --warning-bg: rgba(245, 158, 11, 0.15) !important;
        --error-bg: rgba(239, 68, 68, 0.15) !important;
        --success-bg: rgba(16, 185, 129, 0.15) !important;
        --divider-shadow: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background-color: #0e1117 !important;
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #f1f5f9 !important;
    }
    
    .main-header .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header .emoji {
        color: initial !important;
        -webkit-text-fill-color: initial !important;
        background: none !important;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #94a3b8 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Card-like containers - Force dark theme */
    .input-card, .output-card {
        background: rgba(30, 41, 59, 0.8) !important;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid #374151 !important;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .input-card {
        border-left: 4px solid #667eea !important;
    }
    
    .output-card {
        border-left: 4px solid #38ef7d !important;
    }
    
    /* Section Headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.25rem;
        color: #f1f5f9 !important;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Text areas - Force dark styling */
    .stTextArea > div > div > textarea {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 2px solid #374151 !important;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        transition: border-color 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px -4px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }
    
    .stInfo > div {
        color: #f1f5f9 !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15) !important;
        border: 1px solid #f59e0b !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }
    
    .stWarning > div {
        color: #f1f5f9 !important;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }
    
    .stError > div {
        color: #f1f5f9 !important;
    }
    
    .stSuccess {
        background: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid #10b981 !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
    }
    
    .stSuccess > div {
        color: #f1f5f9 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #374151 !important;
        color: #f1f5f9 !important;
    }
    
    .streamlit-expanderContent {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid #374151 !important;
        border-top: none !important;
        color: #f1f5f9 !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 12px !important;
        background-color: #1e293b !important;
    }
    
    .stCodeBlock > div {
        border-radius: 12px !important;
        background-color: #1e293b !important;
    }
    
    .stCodeBlock code {
        color: #f1f5f9 !important;
        background-color: #1e293b !important;
    }
    
    /* Custom divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
        border: none;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.1);
    }
    
    /* Feature highlight boxes */
    .feature-box {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(55, 65, 81, 0.6) 100%) !important;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        color: #f1f5f9 !important;
        backdrop-filter: blur(5px);
    }
    
    /* All text elements should be light colored */
    .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
    .stText, .stCaption, p, div, span {
        color: #f1f5f9 !important;
    }
    
    /* Column background */
    .stColumn > div {
        background-color: transparent !important;
    }
    
    /* Fix any remaining dark text */
    * {
        color: #f1f5f9 !important;
    }
    
    /* Exception for buttons and special elements */
    .stButton > button,
    .stButton > button *,
    .copy-btn,
    .copy-btn * {
        color: white !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .input-card, .output-card {
            padding: 1rem;
        }
        
        .section-header {
            font-size: 1.1rem;
        }
    }
    
    /* Smooth transitions */
    * {
        transition: background-color 0.3s ease, border-color 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def apply_custom_css():
    """Apply enhanced dark theme CSS"""
    inject_dark_theme_css()

def set_example_prompt(example_text):
    """Helper function to set example prompt"""
    # Use a query parameter approach to trigger the change
    st.query_params["example"] = example_text
    st.rerun()

def main():
    # Initialize session state
    init_session_state()
    
    # Set page configuration with dark theme
    st.set_page_config(
        page_title="Deathstroke Prompt Engineer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply dark theme CSS immediately
    apply_custom_css()
    
    # Configure Gemini API
    if not configure_gemini():
        return
    
    # Check for example query parameter
    query_params = st.query_params
    if "example" in query_params:
        example_text = query_params["example"]
        # Clear the query parameter and set the session state
        st.query_params.clear()
        if "raw_prompt" in st.session_state:
            del st.session_state["raw_prompt"]
        st.session_state.raw_prompt = example_text
        st.rerun()
    
    # Header with enhanced styling
    st.markdown('<h1 class="main-header"><span class="emoji">🤖</span><span class="gradient-text">Deathstroke Prompt Engineer</span></h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your raw prompts into structured, effective prompts for AI models</p>', unsafe_allow_html=True)
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Main interface with improved layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        # Input section with card styling
        st.markdown("""
        <div class="input-card">
            <h3 class="section-header">📝 Raw Prompt</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Use the session state value directly without trying to update it
        raw_prompt = st.text_area(
            "Enter your raw prompt here:",
            height=250,
            placeholder="Example: Explain machine learning to a beginner in simple terms...",
            key="raw_prompt",
            help="Enter any basic instruction or question you want to improve"
        )
        
        # Generate button with enhanced styling
        col1a, col1b, col1c = st.columns([1, 2, 1])
        with col1b:
            transform_clicked = st.button("🚀 Transform Prompt", type="primary", use_container_width=True)
        
        if transform_clicked:
            if raw_prompt.strip():
                with st.spinner("✨ Crafting your enhanced prompt..."):
                    structured_prompt = generate_structured_prompt(raw_prompt)
                    if structured_prompt:
                        st.session_state.structured_prompt = structured_prompt
                        st.success("✅ Prompt transformed successfully!")
            else:
                st.warning("⚠️ Please enter a raw prompt first!")
    
    with col2:
        # Output section with card styling
        st.markdown("""
        <div class="output-card">
            <h3 class="section-header">✨ Structured Prompt</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'structured_prompt'):
            # Display the structured prompt
            st.text_area(
                "Your transformed prompt:",
                value=st.session_state.structured_prompt,
                height=350,
                key="structured_output",
                help="This is your enhanced, structured prompt ready to use"
            )
            
            # Enhanced copy functionality
            col2a, col2b = st.columns([2, 1])
            
            with col2b:
                # Working copy button with better styling
                copy_button_html = create_copy_button(st.session_state.structured_prompt)
                st.components.v1.html(copy_button_html, height=80)
            
            with col2a:
                # Manual copy backup with better presentation
                with st.expander("📋 Manual Copy (Backup Method)", expanded=False):
                    st.code(st.session_state.structured_prompt, language=None)
                    st.caption("💡 Select all text above and use Ctrl+C (Windows/Linux) or Cmd+C (Mac)")
            
        else:
            st.info("🎯 Your structured prompt will appear here after transformation.")
            
            # Show example while waiting
            st.markdown("""
            <div class="feature-box">
                <strong>💡 What you'll get:</strong><br>
                • Clear role definition for the AI<br>
                • Detailed context and constraints<br>
                • Step-by-step instructions<br>
                • Quality verification prompts
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced instructions section
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    # Quick examples section
    st.markdown("### 🌟 Quick Examples")
    example_cols = st.columns(3)
    
    with example_cols[0]:
        if st.button("📚 Educational Content", use_container_width=True):
            set_example_prompt("Explain photosynthesis to middle school students")
    
    with example_cols[1]:
        if st.button("📧 Marketing Copy", use_container_width=True):
            set_example_prompt("Write a marketing email for a new fitness app")
    
    with example_cols[2]:
        if st.button("🎨 Creative Writing", use_container_width=True):
            set_example_prompt("Write a short story about time travel")
    
    # Detailed instructions
    with st.expander("📖 How to Use This Tool", expanded=False):
        st.markdown("""
        ### 🚀 Getting Started
        
        **Step 1:** Enter your basic prompt in the left text area
        - Can be as simple as "explain climate change" or "write a poem"
        - Don't worry about being detailed - that's what we'll fix!
        
        **Step 2:** Click the "Transform Prompt" button
        - Our AI will analyze your intent and create a comprehensive prompt
        - This usually takes 3-10 seconds
        
        **Step 3:** Copy and use your enhanced prompt
        - Use the copy button for quick copying
        - Manual copy option available as backup
        
        ### ✨ What Makes Prompts Better?
        
        **Before:** "Write about dogs"
        
        **After:** "You are a professional pet writer with expertise in animal behavior. Write an engaging 300-word article about dogs that includes their loyalty traits, training tips, and health benefits of pet ownership. Use a friendly, informative tone suitable for general readers. Include specific examples and actionable advice."
        
        ### 💡 Pro Tips
        - Be specific about your audience (beginners, experts, children, etc.)
        - Mention desired length or format
        - Include any style preferences
        - The tool works with any type of content request!
        """)
    
    # Action buttons at bottom
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    
    col_action1, col_action2, col_action3 = st.columns([1, 1, 1])
    
    with col_action2:
        if st.button("🔄 Clear All", type="secondary", use_container_width=True):
            # Clear session state properly
            if hasattr(st.session_state, 'structured_prompt'):
                del st.session_state.structured_prompt
            # Remove the widget key from session state
            if "raw_prompt" in st.session_state:
                del st.session_state["raw_prompt"]
            st.rerun()

if __name__ == "__main__":
    main()