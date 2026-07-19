from openai import OpenAI
from src.config import OPENAI_API_KEY
from src.database import query_historic_facts
from src.search import get_live_news_context

def compile_quiz_data(sport, difficulty, num_questions=4, output_format="Text", history=None):
    # Create query to run against ChromaDB
    db_query = f"{sport} history cup championships rules records"
    db_matches = query_historic_facts(sport=sport, query_text=db_query, n_results=2)
    db_context = "\n".join(db_matches) if db_matches else "No offline historic data recorded."

    # Search the live web
    web_context = get_live_news_context(sport)

    # Combine historical and web contexts
    unified_context = f"=== HISTORICAL FACTS ===\n{db_context}\n\n=== LIVE INTERNET NEWS ===\n{web_context}"

    # Instantiate the API client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url="https://openrouter.ai/api/v1",

)

    # Constructing a structured system prompt
    system_instruction = (
        "You are an expert sports quiz creator. Your job is to write multiple-choice quizzes "
        "relying strictly on the provided Context. Avoid hallucinations. Do not use facts not "
        "found in the Context below. If facts are scarce, make do with what you have, "
        "but keep details completely accurate to the text context.\n"
        "IMPORTANT: When writing explanations, do NOT mention 'Web Source', 'historical facts provided', "
        "or 'the context states'. Write the explanation naturally as an authoritative trivia host.\n\n"
        f"CONTEXT DETAILS:\n{unified_context}"
    )

    if output_format.lower() == "json":
        format_instructions = (
            "Format the output strictly as a JSON array of objects, like this:\n"
            "[\n"
            "  {\n"
            '    "question": "Question text here",\n'
            '    "options": {\n'
            '      "A": "Option A",\n'
            '      "B": "Option B",\n'
            '      "C": "Option C",\n'
            '      "D": "Option D"\n'
            "    },\n"
            '    "correct_answer": "A",\n'
            '    "explanation": "Detailed explanation..."\n'
            "  }\n"
            "]"
        )
    elif output_format.lower() == "markdown":
        format_instructions = (
            "Format the output strictly in Markdown, like this:\n"
            "### Question: [Question text here]\n"
            "- **A)** [Option A]\n"
            "- **B)** [Option B]\n"
            "- **C)** [Option C]\n"
            "- **D)** [Option D]\n\n"
            "**Correct Answer:** [Single Letter, e.g., A]\n\n"
            "> **Explanation:** [Detailed explanation...]\n"
            "---\n"
        )
    else:
        format_instructions = (
            "Format each question exactly as follows so my program can parse it:\n"
            "Question: [Question text here]\n"
            "A) [Option A]\n"
            "B) [Option B]\n"
            "C) [Option C]\n"
            "D) [Option D]\n"
            "Correct Answer: [Single Letter, e.g., A]\n"
            "Explanation: [Detailed background reasoning quoting from the context details]\n"
            "---"
        )

    history_constraint = ""
    if history:
        history_constraint = "\nCRITICAL INSTRUCTION: Do NOT generate questions that are identical or highly similar to these previously asked questions:\n"
        for item in history[:3]: # Only look at the last 3 quizzes to save tokens
            history_constraint += f"- {item['output'][:200]}...\n"

    user_prompt = (
        f"Generate exactly {num_questions} unique multiple-choice questions for the sport: {sport}.\n"
        f"Difficulty target: {difficulty}.\n\n"
        f"{format_instructions}\n"
        f"{history_constraint}"
    )

    # Make API call
    response = client.chat.completions.create(
        # model="gpt-4o mini", # Or "gpt-4o"
        model="google/gemma-4-26b-a4b-it:free", # Or "gpt-4o"
        # model="openrouter/auto-beta", # Or "gpt-4o"
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content, unified_context