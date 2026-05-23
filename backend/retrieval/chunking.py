# from langchain_text_splitters import RecursiveCharacterTextSplitter


# def create_chunks(documents):

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=200,
#         chunk_overlap=50
#     )

#     chunks = splitter.split_documents(documents)

#     chunks = [
#         chunk for chunk in chunks
#         if chunk.page_content
#         and isinstance(chunk.page_content, str)
#         and len(chunk.page_content.strip()) > 10
#     ]

#     return chunks

from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    chunks = [
        chunk for chunk in chunks
        if chunk.page_content
        and isinstance(chunk.page_content, str)
        and len(chunk.page_content.strip()) > 10
    ]

    return chunks