from langchain_core.tools import tool 


global ec 
ec = False 
@tool 
def end_chat():
    '''ends chat with the user.''' 
    print('[Tool]Ending Chat ... ')
    global ec 
    ec = True
    return ec

def get_ec():
    return ec
