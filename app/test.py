import langchain  # This import isn't needed unless you use something from it.
from langchain_openai import AzureChatOpenAI
import os 
from dotenv import load_dotenv
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent

load_dotenv() 

ak = os.getenv('AZURE_OPENAI_API_KEY')
av = os.getenv('API_VERSION')
ep = os.getenv('ENDPOINT_URL')
dn = os.getenv('DEPLOYMENT_NAME')
llm = AzureChatOpenAI(
    api_key=SecretStr(ak) if ak else None, 
    api_version=av, 
    azure_endpoint=ep,
    azure_deployment=dn,
)


response  = llm.invoke('hi')
print(response.content)
print(type(response.content))