from src.vector_base import get_pdf_text, get_text_chunks, get_vectorstore
from src.model import get_conversation_chain

def lmm_response_pdf(file, question):

    # get pdf text
    raw_text = get_pdf_text(file)

    # get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # create vector store
    vectorstore = get_vectorstore(text_chunks)

    chat_chain = get_conversation_chain(vectorstore)

    response = chat_chain({"question": question})
    return response["answer"]
