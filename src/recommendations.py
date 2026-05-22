import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )

def generate_recommendations(df_info):
    llm = get_llm()
    if not llm:
        return "AI temporarily unavailable. Check GROQ_API_KEY."

    # Reuse same in-flight guard from session state
    if st.session_state.get("ai_in_flight", False):
        return "⏳ Please wait — another AI request is already in progress."

    last_call = st.session_state.get("last_ai_call_time", 0)
    if (time.time() - last_call) < 2:
        return "⏳ Please wait a moment before making another AI request."

    prompt = ChatPromptTemplate.from_template("""
    You are an expert data science assistant. Based on the following dataset info,
    provide 3-5 high-priority actionable recommendations for data preprocessing.
    Rules:
    - START DIRECTLY with recommendations. No introductions.
    - Use clear markdown subheadings for each point.
    - Be specific (e.g., "Use One-Hot Encoding for column X").
    Dataset Info: {info}
    """)

    st.session_state["ai_in_flight"] = True
    st.session_state["last_ai_call_time"] = time.time()
    try:
        response = (prompt | llm).invoke({"info": df_info})
        return response.content
    except Exception as e:
        err = str(e)
        if "rate_limit" in err.lower() or "429" in err:
            return "⚠️ Groq rate limit reached. Please wait 30 seconds before trying again."
        return f"Error generating recommendations: {err}"
    finally:
        st.session_state["ai_in_flight"] = False