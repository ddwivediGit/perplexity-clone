import streamlit as st
from tavily import TavilyClient
from groq import Groq

# Streamlit app title and description
st.title("Unperplexed")
st.write("Enter your Tavily and Groq API keys below, then ask a question to get an AI-generated response based on web search results.")

# Input fields for API keys side by side
col1, col2 = st.columns(2)
with col1:
    tavily_api_key = st.text_input("Tavily API Key", type="password")
with col2:
    groq_api_key = st.text_input("Groq API Key", type="password")

# Model selection dropdown
model_options = [
    "mixtral-8x7b-32768",
    "llama-3.1-8b-instant",
    "qwen-2.5-32b",
    "gemma2-9b-it",
    "llama-3.2-11b-vision-preview"
]
selected_model = st.selectbox("Select Model:", model_options, index=0)  # Default to first model

# Processing mode dropdown
mode_options = ["Adapts to Question", "Think Hard"]
selected_mode = st.selectbox("Processing Mode:", mode_options, index=0)  # Default to first mode

# Input field for user query
query = st.text_input("Ask a question:")

# List of URLs to exclude from sources
EXCLUDED_URLS = [
    "https://www2.deloitte.com/us/en/insights/economy/asia-pacific/india-economic-outlook.html",
    "https://www.ibef.org/economy/indian-economy-overview"
]

# Function to perform search and generate response with filtered URLs and titles
def get_ai_response(tavily_key, groq_key, user_query, model, mode):
    try:
        # Initialize Tavily and Groq clients
        tavily_client = TavilyClient(api_key=tavily_key)
        groq_client = Groq(api_key=groq_key)

        # Perform search using Tavily
        search_results = tavily_client.search(user_query, max_results=5)
        context = " ".join([result["content"] for result in search_results["results"]])
        # Extract URLs and titles, excluding specific URLs
        sources = [
            {"title": result["title"], "url": result["url"]}
            for result in search_results["results"]
            if result["url"] not in EXCLUDED_URLS
        ]

        # Set prompt based on selected mode
        if mode == "Adapts to Question":
            prompt = f"Based on the following context, answer the question: {user_query}\n\nContext: {context}"
        else:  # Think Hard
            prompt = f"Take a deep breath and think carefully. Analyze the following context step-by-step and provide a well-reasoned answer to the question: {user_query}\n\nContext: {context}"

        # Generate response using Groq with selected model
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        answer = response.choices[0].message.content
        return answer, sources
    except Exception as e:
        return f"Error: {str(e)}", []

# Function to generate follow-up questions using Groq
def generate_follow_up_questions(groq_key, original_query, answer, model, mode):
    try:
        groq_client = Groq(api_key=groq_key)
        # Set prompt based on selected mode
        if mode == "Adapts to Question":
            prompt = (
                f"Given the following question and answer, generate exactly three concise follow-up questions that a user might ask to explore the topic further.\n\n"
                f"Original Question: {original_query}\n"
                f"Answer: {answer}\n\n"
                f"Provide the questions in a numbered list (1., 2., 3.). Do not include any additional text or explanations."
            )
        else:  # Think Hard
            prompt = (
                f"Take a deep breath and think carefully. Given the following question and answer, analyze them step-by-step and generate exactly three concise, well-thought-out follow-up questions that a user might ask to explore the topic further.\n\n"
                f"Original Question: {original_query}\n"
                f"Answer: {answer}\n\n"
                f"Provide the questions in a numbered list (1., 2., 3.). Do not include any additional text or explanations."
            )
        
        response = groq_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        # Parse the response into a list of questions
        questions_text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
        # Ensure we return exactly 3 questions, padding or trimming if necessary
        if len(questions) < 3:
            questions.extend([f"What else can you tell me about {original_query}?" for _ in range(3 - len(questions))])
        return questions[:3]
    except Exception as e:
        # Fallback questions in case of error
        return [
            f"What else can you tell me about {original_query}?",
            f"Why is {original_query} significant?",
            f"How does {original_query} affect us?"
        ]

# Button to trigger the search and response
if st.button("Get Answer"):
    if not tavily_api_key or not groq_api_key:
        st.error("Please provide both Tavily and Groq API keys.")
    elif not query:
        st.error("Please enter a question.")
    else:
        # Set spinner message based on selected mode
        spinner_message = "Searching and generating response..." if selected_mode == "Adapts to Question" else "Analyzing and reasoning..."
        with st.spinner(spinner_message):
            answer, sources = get_ai_response(tavily_api_key, groq_api_key, query, selected_model, selected_mode)
            st.subheader("Answer:")
            st.write(answer)
            if sources:
                # Limit to first 3 sources
                limited_sources = sources[:3]
                st.subheader("Sources:")
                # Display sources as plain text
                for source in limited_sources:
                    st.write(f"{source['title']}: {source['url']}")

            # Generate and display follow-up questions as plain text
            with st.spinner("Generating follow-up questions..."):
                follow_ups = generate_follow_up_questions(groq_api_key, query, answer, selected_model, selected_mode)
                st.subheader("Follow-Up Questions (copy and paste to explore):")
                for follow_up in follow_ups:
                    # Clean up numbering if present (e.g., "1. " -> "")
                    follow_up_text = follow_up.lstrip("1234567890. ").strip()
                    st.write(follow_up_text)

# Footer
st.write("Powered by Tavily and Groq. Deployed on Streamlit Community Cloud.")