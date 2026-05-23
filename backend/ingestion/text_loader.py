# from langchain_community.document_loaders import TextLoader

# def load_text(path):
#     loader = TextLoader(path)
#     return loader.load()

from langchain_community.document_loaders import TextLoader

def load_text(path):
    loader = TextLoader(path, encoding="utf-8")
    return loader.load()