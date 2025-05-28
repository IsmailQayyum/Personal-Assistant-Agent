from langchain_openai import AzureChatOpenAI
import os 
from dotenv import load_dotenv
from pydantic import SecretStr
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

async def get_llm():
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
    return llm 

# async def get_llm_response(prompt)