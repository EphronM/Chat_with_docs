import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from mistralai.client import MistralClient
from langchain_mistralai.chat_models import ChatMistralAI


from langchain import PromptTemplate

DEFAULT_SYSTEM_PROMPT = """
You are a helpful, respectful and honest assistant.
Always answer as helpfully as possible, while being safe.
Your answers should not include any harmful, unethical,
racist, sexist, toxic, dangerous, or illegal content.
Please ensure that your responses are socially unbiased
and positive in nature.

If a question does not make any sense, or is not factually
 coherent, explain why instead of answering something
 not correct. If you don't know the answer to a question,
 please don't share false information.
""".strip()


def generate_prompt(
        prompt: str,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT
        ) -> str:
    return f"""
          [INST] <<SYS>> {system_prompt} <</SYS>>

          {prompt} [/INST]
          """.strip()

SYSTEM_PROMPT = """Use the following pieces of context to answer
 the question at the end. If you don't know the answer,
 just say that you don't know, don't try to make up an answer."""

template = generate_prompt(
           """
            {context}
            
            Question: {question}
            """,
                system_prompt=SYSTEM_PROMPT,
            )

prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
            )



def get_conversation_chain(vectorstore):

    try:
        api_key = os.environ['MISTRAL_API_KEY']
    except:
        raise ValueError("Either pass the mistral API key while instantiating this class or set 'MISTRAL_API_KEY' environment variable.")

    llm = ChatMistralAI(mistral_api_key=api_key, model="open-mistral-7b")


    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain