import streamlit as st
from src.generator import compile_quiz_data
from src.database import setup_and_populate_db

# 1. Warm-up and initialize the vector DB with our offline facts on startup
@st.cache_resource
def prepare_knowledge_base():
    setup_and_populate_db()

prepare_knowledge_base()

# 2. Set Page configurations
st.set_page_config(page_title="Sports Quiz Agent", page_icon="🏆", layout="centered")

st.title("🏆 AI-Powered Sports Quiz Generator")
st.write("Challenge yourself or generate engaging social media content! Powered by RAG (ChromaDB + Web Search).")

# 3. Sidebar inputs
st.sidebar.header("Quiz Settings")
sport_choice = st.sidebar.selectbox("Select Sport", ["Cricket", "Football", "Badminton", "Tennis", "Basketball", "Formula 1", "Baseball"])
difficulty = st.sidebar.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of Questions", min_value=3, max_value=5, value=4)
output_format = st.sidebar.selectbox("Output Format", ["Text", "JSON", "Markdown"])

# 4. Initialize session state to remember quizzes across page interactions
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
    st.session_state.quiz_context = None
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []

# Button to trigger compilation pipeline
if st.sidebar.button("Generate Fresh Quiz", use_container_width=True):
    with st.spinner("Fetching historical facts & scouring the live web..."):
        try:
            quiz_text, context_used = compile_quiz_data(sport_choice, difficulty, num_questions, output_format)
            st.session_state.quiz_output = quiz_text
            st.session_state.quiz_context = context_used
            
            # Save to history
            st.session_state.quiz_history.insert(0, {
                "sport": sport_choice,
                "difficulty": difficulty,
                "output": quiz_text,
                "format": output_format,
                "context": context_used
            })
            
            st.success("Quiz created successfully!")
        except Exception as e:
            st.error(f"Failed to generate quiz: {e}")

# 5. Display the generated quiz
if st.session_state.quiz_output:
    st.subheader(f"Current Quiz: {sport_choice} ({difficulty})")
    # st.markdown("### Generated Quiz Output")
    
    # # Render the output visually based on format
    # if output_format == "JSON":
    #     try:
    #         import json
    #         st.json(json.loads(st.session_state.quiz_output))
    #     except Exception:
    #         # Fallback if LLM didn't return perfectly parsable JSON
    #         st.code(st.session_state.quiz_output, language="json")
    # elif output_format == "Markdown":
    #     st.markdown(st.session_state.quiz_output)
    # else:
    #     st.text(st.session_state.quiz_output)

    # Determine appropriate file extension and MIME type for download/copying
    if output_format == "JSON":
        file_ext = "json"
        mime_type = "application/json"
        language_format = "json"
    elif output_format == "Markdown":
        file_ext = "md"
        mime_type = "text/markdown"
        language_format = "markdown"
    else:
        file_ext = "txt"
        mime_type = "text/plain"
        language_format = "text"
        
    with st.expander("📝 Generated Quiz Output"):
        st.code(st.session_state.quiz_output, language=language_format)
    
    # st.download_button(
    #     label=f"💾 Download as .{file_ext}",
    #     data=st.session_state.quiz_output,
    #     file_name=f"quiz_output.{file_ext}",
    #     mime=mime_type,
    #     use_container_width=True
    # )

    # Expandable window showcasing the "ground truth context" for audit purposes
    with st.expander("🔍 Inspect Ground Truth (RAG Context Used)"):
        st.code(st.session_state.quiz_context, language="markdown")

# 6. Display Quiz History
# if st.session_state.quiz_history:
#     st.divider()
#     st.header("📜 Quiz History")
#     for idx, history_item in enumerate(st.session_state.quiz_history):
#         with st.expander(f"Quiz #{len(st.session_state.quiz_history) - idx}: {history_item['sport']} - {history_item['difficulty']} ({history_item['format']})"):
#             language_format = "json" if history_item['format'] == "JSON" else "markdown" if history_item['format'] == "Markdown" else "text"
#             st.code(history_item['output'], language=language_format)