# from langchain.memory import ConversationBufferMemory

# def load_memory():
#     memory = ConversationBufferMemory(
#         memory_key="history",
#         return_messages=False
#     )
#     return memory

from langchain.memory import ConversationBufferMemory

def load_memory():
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=False
    )
    return memory