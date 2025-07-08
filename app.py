import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Set Streamlit page config for blue background
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for blue gradient background, white bold fonts, and chat section styling
st.markdown(
    """
    <style>
    body, .stApp {
        background: linear-gradient(135deg, #1565c0 0%, #1e88e5 100%) !important;
        color: #fff !important;
        font-weight: bold !important;
    }
    .stApp {
        background: linear-gradient(135deg, #1565c0 0%, #1e88e5 100%) !important;
    }
    .main-chat-section {
        background: #5fa8f5 !important;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        color: #fff !important;
        font-weight: bold !important;
        box-shadow: 0 4px 24px rgba(21,101,192,0.15);
    }
    .sidebar .sidebar-content {
        color: #fff !important;
        font-weight: bold !important;
    }
    .css-1v0mbdj, .css-1v0mbdj * {
        color: #fff !important;
        font-weight: bold !important;
    }
    .stTextInput > div > input {
        background: #e3f2fd !important;
        color: #1565c0 !important;
        font-weight: bold !important;
    }
    .stButton > button {
        background: #1565c0 !important;
        color: #fff !important;
        font-weight: bold !important;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 AI Chatbot (Gemma 3 via Ollama)")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for chat history
def render_sidebar():
    st.sidebar.title("Chat History")
    if st.session_state.chat_history:
        for i, (user, bot) in enumerate(st.session_state.chat_history):
            st.sidebar.markdown(f"**You:** {user}")
            st.sidebar.markdown(f"**Bot:** {bot}")
    else:
        st.sidebar.info("No chat history yet.")

render_sidebar()

# User input
user_input = st.text_input("You:", "", key="user_input")

# Only load LLM and chain if needed
def get_chain():
    llm = Ollama(model="gemma3")
    memory = ConversationBufferMemory()
    chain = ConversationChain(llm=llm, memory=memory)
    return chain

if "chain" not in st.session_state:
    st.session_state.chain = get_chain()

if st.button("Send") and user_input.strip():
    # Get response from LLM
    response = st.session_state.chain.run(input=user_input)
    # Save to chat history
    st.session_state.chat_history.append((user_input, response))
    # Rerun to update sidebar and clear input
    st.rerun()

# Display the last exchange in the main area
if st.session_state.chat_history:
    user, bot = st.session_state.chat_history[-1]
    with st.container():
        st.markdown('<div class="main-chat-section">', unsafe_allow_html=True)
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Bot:** {bot}")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Start the conversation above!") 