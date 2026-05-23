# from langchain_community.document_loaders import WebBaseLoader

# def load_web(url):
#     loader = WebBaseLoader(url)
#     return loader.load()

from langchain_community.document_loaders import WebBaseLoader

def load_web(url):
    loader = WebBaseLoader(url)
    return loader.load()