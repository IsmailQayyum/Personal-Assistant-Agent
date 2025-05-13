import langchain 
from langchain_openai import AzureChatOpenAI
import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage , AIMessage
from langgraph.prebuilt import create_react_agent

load_dotenv() 

ak = os.getenv('AZURE_OPENAI_API_KEY')
av= os.getenv('API_VERSION')
ep = os.getenv('ENDPOINT_URL')
dn = os.getenv('DEPLOYMENT_NAME')

llm = AzureChatOpenAI(
    api_key=ak , 
    api_version=av , 
    azure_endpoint=ep,
    azure_deployment=dn,
)

pt = PromptTemplate(
    template='Give a 3 line summary on {topic}',
)

chain = pt | llm

from tools import end_chat, load_document, ask_about_document
agent_tools = [end_chat, load_document, ask_about_document]


agent = create_react_agent(llm , agent_tools )

def chat():
    messages = [
        SystemMessage(content=(
            'You are a very helpful personal assistant. '
            'Greet user in the beggining'
            'You talk to your user, and give him appropriate reply.'
            'End the chat if you feel like user has ended the chat.'

            'You can load a document using the "load_document" tool if the user provides a file path.' 
            'Then, you can use the "ask_about_document" tool to answer questions based on that document.'
        )    )
    ]

    import tools 
    greet = agent.invoke({'messages':messages})['messages'][-1].content
    print('Assistant: ',greet)
    messages.append(AIMessage(content=(greet)))
    chat_active=True 
    while chat_active:
        user_input= input('User: ')
        messages.append(HumanMessage(content=(user_input)))
        response= agent.invoke({'messages':messages})
        print('Assistant: ',response['messages'][-1].content)
        if tools.ec:
            break
        messages.append(AIMessage(content=(response['messages'][-1].content)))


if __name__ == '__main__':
    chat()
