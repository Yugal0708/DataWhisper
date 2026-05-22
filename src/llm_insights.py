import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ── Rate limiting constants ───────────────────────────────────────────────
MIN_DELAY_BETWEEN_CALLS = 2  # seconds between consecutive API calls

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.1
    )

def _is_rate_limited():
    """Check if enough time has passed since last API call."""
    last_call = st.session_state.get("last_ai_call_time", 0)
    return (time.time() - last_call) < MIN_DELAY_BETWEEN_CALLS

def _mark_call():
    """Mark the current time as last API call."""
    st.session_state["last_ai_call_time"] = time.time()

def _is_in_flight():
    """Check if an AI request is already in progress."""
    return st.session_state.get("ai_in_flight", False)

def _safe_invoke(chain, payload):
    """Invoke chain with rate limit + in-flight guard."""
    if _is_in_flight():
        return "⏳ Please wait — another AI request is already in progress."
    if _is_rate_limited():
        return "⏳ Please wait a moment before making another AI request."

    st.session_state["ai_in_flight"] = True
    _mark_call()
    try:
        response = chain.invoke(payload)
        return response.content
    except Exception as e:
        err = str(e)
        if "rate_limit" in err.lower() or "429" in err:
            return "⚠️ Groq rate limit reached. Please wait 30 seconds before trying again."
        return f"AI Error: {err}"
    finally:
        st.session_state["ai_in_flight"] = False

def generate_insights(df_summary, column_names, dtypes, missing_values, correlations, task="General Analysis"):
    llm = get_llm()
    if not llm:
        return "AI temporarily unavailable. Please check your GROQ_API_KEY in the .env file."

    prompt = ChatPromptTemplate.from_template("""
    You are a professional data analyst.
    Your specific objective is: {task}
    Dataset Context:
    - Columns: {column_names}
    - Types: {dtypes}
    - Summary Stats: {summary_stats}
    - Missing Values: {missing_values}
    - Correlations: {correlations}
    Tasks:
    1. Focus on the requested objective: {task}.
    2. Give 3–5 key insights.
    3. Suggest 2 actionable recommendations.
    Rules: Use bullet points. Reference specific column names. No Hallucinations.
    """)

    return _safe_invoke(prompt | llm, {
        "task": task,
        "column_names": column_names,
        "dtypes": dtypes,
        "summary_stats": df_summary,
        "missing_values": missing_values,
        "correlations": correlations
    })

def generate_auto_summary(df_info_str):
    llm = get_llm()
    if not llm:
        return "AI unavailable for summary."

    prompt = ChatPromptTemplate.from_template("""
    You are an expert data analyst. Based on this dataset summary, provide 3-5 concise executive insights as bullet points.
    Data Summary: {info}
    Insights:
    """)

    return _safe_invoke(prompt | llm, {"info": df_info_str})

def explain_chart(chart_info, data_context=None):
    llm = get_llm()
    if not llm:
        return "AI unavailable for chart explanation."

    context_str = f"\nAdditional Data Context: {data_context}" if data_context else ""

    prompt = ChatPromptTemplate.from_template("""
    You are an AI data assistant. Explain this chart in simple terms.
    Chart Metadata:
    - Type: {chart_type}
    - Columns: {columns}{context}
    Keep it to 2-3 sentences max.
    """)

    return _safe_invoke(prompt | llm, {
        "chart_type": chart_info['type'],
        "columns": chart_info['columns'],
        "context": context_str
    })