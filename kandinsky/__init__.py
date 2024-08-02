from .kandinsky_api import KandinskyAPI

def create_kandinsky_api(url, api_key, secret_key):
    return KandinskyAPI(url, api_key, secret_key)
