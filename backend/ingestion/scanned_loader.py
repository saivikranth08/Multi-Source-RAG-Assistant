# from llama_parse import LlamaParse
# from langchain.schema import Document

# def load_scanned_pdf(path, api_key, file_name):

#     parser = LlamaParse(
#         api_key=api_key,
#         result_type="markdown"
#     )

#     parsed = parser.load_data(path)

#     documents = [
#         Document(
#             page_content=doc.text,
#             metadata={"source": file_name}
#         )
#         for doc in parsed
#     ]

#     return documents

from llama_parse import LlamaParse
from langchain.schema import Document

def load_scanned_pdf(path, api_key, file_name):
    parser = LlamaParse(
        api_key=api_key,
        result_type="markdown"
    )

    parsed = parser.load_data(path)

    documents = [
        Document(
            page_content=doc.text,
            metadata={"source": file_name}
        )
        for doc in parsed
    ]

    return documents