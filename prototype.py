import gradio as gr
import requests
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import bingsearch
from googletrans import Translator

# Constants for calling the Azure OpenAI service
openai_api_type = "azure"
gpt_endpoint = "https://sspopenaisouthcentralus.openai.azure.com/"            # Your endpoint will look something like this: https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/
gpt_api_key = "397b74073028455584fafd40c55095fa"                               # Your key will look something like this: 00000000000000000000000000000000
gpt_deployment_name="gpt-35-turbo-0301"
bing_endpoint = "https://api.bing.microsoft.com/v7.0/search"
# bing_api_key = "<Bing Key>"

# Create instance to call GPT model
gpt = AzureChatOpenAI(
    openai_api_base=gpt_endpoint,
    openai_api_version="2023-03-15-preview",
    deployment_name=gpt_deployment_name,
    openai_api_key=gpt_api_key,
    openai_api_type = openai_api_type,
)

def call_gpt_model(rag_from_bing, message, language):
    system_template="You are a professional, helpful assistant to provide resources to combat childhood hunger.  \n"
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    user_prompt=PromptTemplate(
        template="## Context \n {rag_from_bing} \n" +
                "## Instructions \n Using the above context, answer the question below in {language}.\n" +
                "## Question \n {message} \n",
        input_variables=["rag_from_bing", "message", "language"],
    )
    human_message_prompt = HumanMessagePromptTemplate(prompt=user_prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Get formatted messages for the chat completion
    messages = chat_prompt.format_prompt(rag_from_bing={rag_from_bing}, message={message}, language={language}).to_messages()
    print("Messages")
    print(messages)

    # Call the model
    output = gpt(messages)
    print("Output")
    print(output)
    return output.content

def scrape(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the HTML content of the response
        print(response.text)
        # TODO: consider stripping html tags or any extra tokens?  
        return response.text
    else:
        # Print an error message
        print(f"Request failed with status code {response.status_code}")


def chat(message, history):

    # Get location
    location = get_location()
    print("Location")
    print(location)
    
    # TODO: table storage logic here
    # TODO: use scrape function above to get content

    # Get information from trusted sources
    # TODO
    # TODO - use the location above to get localized info for that location
    # TODO - do we need logic here to see if we have sufficient trusted source data, or whether we even need to call Bing?  

    for val in location.values():
        if val is None:
            print("I'm sorry, I can't find your location. Please try again later.")
            query = "Am I eligible for SNAP - Supplemental Nutrition Assistance Program (Food Stamps), WIC - Women, Infants and Children, SFSP and SSO (summer food services for kids)?"
        else:
            query =  "If I live in " + location["city"] + ", " + location["region"] + ", am I eligibile for SNAP - Supplemental Nutrition Assistance Program (Food Stamps), WIC - Women, Infants and Children, SFSP and SSO (summer food services for kids)?"
    print(query)
    # Call Bing to get context
    # bing_response = bingsearch.call_search_api(query, bing_endpoint, bing_api_key)
    # rag_from_bing = bing_response
    rag_from_bing = ""
    
    langauge = "spanish"
    
    # Call GPT model with context from Bing
    model_response = call_gpt_model(rag_from_bing, message, langauge)
    return model_response


# Gets the ip address of the request (user)
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

# Fetches the location of the user based on the ip address
def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data


# UI components (using Gradio - https://gradio.app)
chatbot = gr.Chatbot(bubble_full_width = False)
chat_interface = gr.ChatInterface(fn=chat, 
                 chatbot=chatbot)

chat_interface.launch()
chatbot = gr.Chatbot(bubble_full_width = False)

def translate_to_spanish(text):
    try:
        # Initialize the translator
        translator = Translator()
        # Detect the source language (English in this case)
        detected_lang = translator.detect(text).lang
        # If the detected language is not Spanish ('es'), translate it to Spanish
        if detected_lang != 'es':
            translation = translator.translate(text, src='en', dest='es')
            translated_text = translation.text
        else:
            # If the text is already in Spanish, no need to translate
            translated_text = text
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
   

def translate_to_english(text):
    try:
        # Initialize the translator
        translator = Translator()
        # Detect the source language (Spanish in this case)
        detected_lang = translator.detect(text).lang
        print(detected_lang)
        # If the detected language is not English ('en'), translate it to English
        if detected_lang != 'en':
            translation = translator.translate(text, src='es', dest='en')
            translated_text = translation.text
        else:
            # If the text is already in English, no need to translate
            translated_text = text
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

with gr.Blocks() as chatbot:
    with gr.Row():
        chat_interface = gr.ChatInterface(fn=chat,
        #                 title="Title here",
        #                 description="Description here",
                        chatbot=chatbot)
    with gr.Row():
        btnSpanish = gr.Button("Translate to Spanish")
        btnEnglish = gr.Button("Translate to English")

chatbot.launch()