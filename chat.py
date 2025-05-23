import langchain 
from langchain_openai import AzureChatOpenAI
import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage , AIMessage
from langgraph.prebuilt import create_react_agent

load_dotenv() 

ak = os.getenv('AZURE_OPENAI_API_KEY')
av = os.getenv('API_VERSION')
ep = os.getenv('ENDPOINT_URL')
dn = os.getenv('DEPLOYMENT_NAME')

# Debug prints
print("Configuration check:")
print(f"API Version: {av}")
print(f"Endpoint URL: {ep}")
print(f"Deployment Name: {dn}")
print(f"API Key present: {'Yes' if ak else 'No'}")

if not all([ak, av, ep, dn]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

# Remove trailing slash from endpoint if present
if ep and ep.endswith('/'):
    ep = ep[:-1]

llm = AzureChatOpenAI(
    api_key=ak,
    api_version=av,
    azure_endpoint=ep,
    azure_deployment=dn,
    temperature=0.7,
)

pt = PromptTemplate(
    template='Give a 3 line summary on {topic}',
)

chain = pt | llm

from tools import end_chat, load_document, ask_about_document
agent_tools = [end_chat, load_document, ask_about_document]

agent = create_react_agent(llm, agent_tools)

def chat():
    messages = [
        SystemMessage(content=(
            'You are a very helpful personal assistant. '
            'Greet user in the beginning. '
            'You talk to your user, and give him appropriate reply.'
            'End the chat if you feel like user has ended the chat.'

            'You can load a document using the "load_document" tool if the user provides a file path.' 
            'Then, you can use the "ask_about_document" tool to answer questions based on that document.'
        ))
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
    # print('Covo=======--',messages)
    # print('specific====', messages[0])
    # print('specific2====', messages[1])
    # print('000000',messages)
    # print('Roleee:',messages[0].role )
if __name__ == '__main__':
    chat()
   
