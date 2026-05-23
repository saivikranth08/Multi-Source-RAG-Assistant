from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from backend.llm.groq_client import load_llm
from backend.llm.prompts import RAG_PROMPT
from backend.retrieval.vectorstore import rerank_results

# =========================================================
# STATE
# =========================================================
class RAGState(TypedDict):
    query: str
    context: str
    chat_history: str
    prompt: str
    answer: str

llm = load_llm()

# =========================================================
# NODES
# =========================================================
def retrieve_node(state: RAGState, retriever):
    print(f"--- NODE: RETRIEVE (Query: {state['query']}) ---")
    # Hybrid search — get 5 chunks
    results = retriever.invoke(state["query"])
    # Rerank — pick best 3
    reranked = rerank_results(state["query"], results, top_n=3)
    context = "\n\n".join([
        f"[Source: {r.metadata.get('source', 'Unknown')}]\n{r.page_content}"
        for r in reranked
    ])
    return {"context": context}


def prompt_node(state: RAGState):
    print("--- NODE: BUILD PROMPT ---")
    formatted_prompt = RAG_PROMPT.format(
        context=state["context"],
        chat_history=state["chat_history"],
        query=state["query"]
    )
    return {"prompt": formatted_prompt}


def generate_node(state: RAGState):
    print("--- NODE: GENERATE ANSWER ---")
    response = llm.invoke([HumanMessage(content=state["prompt"])])
    return {"answer": response.content}


# =========================================================
# BUILD GRAPH
# =========================================================
def build_rag_graph(retriever):
    def retrieve(state):
        return retrieve_node(state, retriever)

    workflow = StateGraph(RAGState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("prompt", prompt_node)
    workflow.add_node("generate", generate_node)

    workflow.set_entry_point("retrieve")
    
    workflow.add_edge("retrieve", "prompt")
    workflow.add_edge("prompt", "generate")
    workflow.add_edge("generate", END)
    return workflow.compile()