import streamlit as st
from tavily import TavilyClient
from groq import Groq

# Streamlit app title and description
st.title("AI-Powered Search Assistant")
st.write("Enter your Tavily and Groq API keys below, then ask a question to get an AI-generated response based on web search results.")

# Input fields for API keys
tavily_api_key = st.text_input("Tavily API Key", type="password")
groq_api_key = st.text_input("Groq API Key", type="password")

# Input field for user query
query = st.text_input("Ask a question:")

# List of URLs to exclude from sources
EXCLUDED_URLS = [
    "https://www2.deloitte.com/us/en/insights/economy/asia-pacific/india-economic-outlook.html",
    "https://www.ibef.org/economy/indian-economy-overview"
]

# Function to perform search and generate response with filtered URLs and titles
def get_ai_response(tavily_key, groq_key, user_query):
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

        # Generate response using Groq
        prompt = f"Based on the following context, answer the question: {user_query}\n\nContext: {context}"
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
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
def generate_follow_up_questions(groq_key, original_query, answer):
    try:
        groq_client = Groq(api_key=groq_key)
        prompt = (
            f"Given the following question and answer, generate exactly three concise follow-up questions that a user might ask to explore the topic further.\n\n"
            f"Original Question: {original_query}\n"
            f"Answer: {answer}\n\n"
            f"Provide the questions in a numbered list (1., 2., 3.). Do not include any additional text or explanations."
        )
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
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
        with st.spinner("Searching and generating response..."):
            answer, sources = get_ai_response(tavily_api_key, groq_api_key, query)
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
                follow_ups = generate_follow_up_questions(groq_api_key, query, answer)
                st.subheader("Follow-Up Questions:")
                for follow_up in follow_ups:
                    # Clean up numbering if present (e.g., "1. " -> "")
                    follow_up_text = follow_up.lstrip("1234567890. ").strip()
                    st.write(follow_up_text)

# Footer
st.write("Powered by Tavily and Groq. Deployed on Streamlit Community Cloud.")