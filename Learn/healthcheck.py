import requests

def llama_health_check():
    health = requests.get('http://127.0.0.1:8080/health') 
    return health 


def api_health_check():
    health = requests.get('http://0.0.0.0:8000/health')
    return health



if __name__ == "__main__":
    llama_check=llama_health_check()
    api_check=api_health_check()
    print(f"llama: {llama_check} , api: {api_check}")
else :
    print("failed")




