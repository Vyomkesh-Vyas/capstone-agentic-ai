from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

vectorstore = Chroma(
    collection_name="hospital_cases",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)


def retrieve_similar_cases(query: str):
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([d.page_content for d in docs])


def save_case(case_id: str, summary: str):
    vectorstore.add_texts(
        texts=[summary],
        metadatas=[{"case_id": case_id}]
    )
