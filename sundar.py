from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import requests
import os
from dotenv import load_dotenv
import base64



load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# NASA API base URL
NASA_API_URL = "https://api.nasa.gov/planetary/apod"

## Prompt Template

prompt = ChatPromptTemplate.from_messages([
    ("system", "I'm your space exploration assistant. Ask me anything about space!"),
    ("user", "Question: {question}")
])

## streamlit framework
st.set_page_config(layout="wide")

st.markdown("""
<style>
.big-font {
    font-size:100px !important;
            font-family:"Algerian";
            font-align:"center";
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white; size: 100px; face: algerian'>                                                                                                                                                                                     </h1>", unsafe_allow_html=True)

# Display header with image
page_by_img="""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://i.imgur.com/mqwZevX.jpeg");
background-size: cover; 

}

</style>
"""
st.markdown(page_by_img, unsafe_allow_html=True)  




st.markdown("<h1 style='text-align: left; color: white; size: 20px'>Ask me a question about space!!</h1>", unsafe_allow_html=True)

input_text = st.text_input("")

# Add css to make text bigger


# Ollama Llama2 LLM 
llm = Ollama(model="llama2")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
 
def get_nasa_data():
    # Fetch data from NASA API
    params = {
        'api_key': os.getenv("NASA_API_KEY")  # Provide your NASA API key
    }
    response = requests.get(NASA_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    if input_text:
        # Query the NASA API for relevant information
        nasa_data = get_nasa_data()
        if nasa_data:
            # Display NASA image of the day
            nasa_response = f"Today's space image is: {nasa_data['title']}. {nasa_data['explanation']}"            
            # Pass the input and NASA response through the chat chain
            response = chain.invoke({"question": input_text})
            st.write(response)

        else:
            st.write("Sorry, I couldn't fetch information from NASA API. Please try again later.")

