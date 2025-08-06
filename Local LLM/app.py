import streamlit as st

from streamlit import session_state
from streamlit import text_input
from streamlit import button
from streamlit import markdown
from streamlit import write
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

st.title("Chatbot Web UI")

# Session state for history
if "context" not in st.session_state:
    st.session_state.context = ""

# Show chat history
if st.session_state.context:
    st.markdown("**Conversation History:**")
    st.write(st.session_state.context)

# User input
user_input = st.text_input("You:", key="input")
if st.button("Send") and user_input:
    with st.spinner("AI is typing..."):
        result = chain.invoke({"context": st.session_state.context, "question": user_input})
    st.write("**Bot:**", result)
    st.session_state.context += f"\nUser: {user_input}\nAI: {result}"
