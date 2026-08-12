import sys
from pathlib import Path

import streamlit as st


# --------------------------------------------------
# SETUP PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

sys.path.append(str(SRC_DIR))

from generate_hybrid import generate_hybrid_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ProductOps AI",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        max-width: 900px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem 0 1.5rem 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }

    .answer-card {
        padding: 1.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        margin-top: 1.5rem;
    }

    .architecture {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
        color: #6b7280;
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HERO
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">ProductOps AI</div>
        <div class="hero-subtitle">
            AI-powered product knowledge assistant
        </div>
        <p>
            Ask questions across product requirements,
            payment documentation and customer policies.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# QUESTION INPUT
# --------------------------------------------------

question = st.text_input(
    "Ask a question",
    placeholder="e.g. How long does a refund take?"
)

ask_button = st.button(
    "Ask ProductOps AI",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# GENERATE ANSWER
# --------------------------------------------------

if ask_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching product knowledge..."):

            try:

                answer = generate_hybrid_answer(question)

                st.markdown(
                    """
                    <div class="answer-card">
                        <strong>ANSWER</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(answer)

            except Exception as error:

                st.error(
                    f"Unable to generate an answer: {error}"
                )


# --------------------------------------------------
# ARCHITECTURE FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="architecture">
        <strong>Retrieval architecture:</strong>
        Hybrid Search · Vector Retrieval + BM25 · Reciprocal Rank Fusion
        <br>
        Grounded answers with source citations and abstention guardrails.
    </div>
    """,
    unsafe_allow_html=True
)
