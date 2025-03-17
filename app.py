import streamlit as st
from tavily import TavilyClient
from groq import Groq
import json

# Streamlit app title and description
st.title("AI-Powered Search Assistant")
st.write("Enter your Tavily and Groq API keys below, then ask a question to get an AI-generated response based on web search results.")

# Input fields for API keys
tavily_api_key = st.text_input("Tavily API Key", type="password")
groq_api_key = st.text_input("Groq API Key", type="password")

# Input field for user query
query = st.text_input("Ask a question:")

# Function to perform search and generate response
def get_ai_response(tavily_key, groq_key, user_query):
    try:
        # Initialize Tavily and Groq clients
        tavily_client = TavilyClient(api_key=tavily_key)
        groq_client = Groq(api_key=groq_key)

        # Perform search using Tavily
        search_results = tavily_client.search(user_query, max_results=5)
        context = " ".join([result["content"] for result in search_results["results"]])

        # Generate response using Groq
        prompt = f"Based on the following context, answer the question: {user_query}\n\nContext: {context}"
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # You can change this to another Groq model if desired
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Button to trigger the search and response
if st.button("Get Answer"):
    if not tavily_api_key or not groq_api_key:
        st.error("Please provide both Tavily and Groq API keys.")
    elif not query:
        st.error("Please enter a question.")
    else:
        with st.spinner("Searching and generating response..."):
            answer = get_ai_response(tavily_api_key, groq_api_key, query)
            st.subheader("Answer:")
            st.write(answer)

# Footer
st.write("Powered by Tavily and Groq. Deployed on Streamlit Community Cloud.")