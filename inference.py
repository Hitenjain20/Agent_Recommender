import os
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import SimpleDirectoryReader
from llama_index.core import SimpleKeywordTableIndex, VectorStoreIndex
from custome_retriever import CustomRetriever
from dotenv import load_dotenv
from llama_index.core import StorageContext
from llama_index.core.retrievers import (
    VectorIndexRetriever,
    KeywordTableSimpleRetriever,
)
from llama_index.core.prompts import PromptTemplate
from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
import nest_asyncio

load_dotenv()

class Inference:
    def __init__(self):


        self.llm = Gemini(api_key= os.getenv('GOOGLE_API_KEY'))
        self.embed_model = GeminiEmbedding(model_name= "models/embedding-001", api_key= os.getenv('GOOGLE_API_KEY'))
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

        # self.node_parser = MarkdownElementNodeParser(llm = OpenAI(model = "gpt-3.5-turbo-0125"), num_workers=8)

    def load_docs(self):
        nest_asyncio.apply()

        documents = SimpleDirectoryReader('data').load_data()
        return documents

    def get_chunks(self, documents):
        nodes = Settings.node_parser.get_nodes_from_documents(documents)
        return nodes

    def _query_engine(self, ques):
        nest_asyncio.apply()

        docs = self.load_docs()

        nodes = self.get_chunks(docs)

        storage_context = StorageContext.from_defaults()
        storage_context.docstore.add_documents(nodes)

        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
        keyword_index = SimpleKeywordTableIndex(nodes, storage_context=storage_context)

        vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=2)
        keyword_retriever = KeywordTableSimpleRetriever(index=keyword_index)

        # custom retriever => combine vector and keyword retriever

        custom_retriever = CustomRetriever(vector_retriever, keyword_retriever)

        # define response synthesizer
        response_synthesizer = get_response_synthesizer()

        # custom_query_engine = RetrieverQueryEngine(
        #     retriever=custom_retriever,
        #     response_synthesizer=response_synthesizer,
        # )

        reranker = FlagEmbeddingReranker(
            top_n=5,
            model="BAAI/bge-reranker-large",
        )

        custom_query_engine = RetrieverQueryEngine(
            retriever=custom_retriever,
            node_postprocessors=[reranker],
            response_synthesizer=response_synthesizer,
        )

        agent_rag_template = """
        Context information is below.
        ---------------------
        {context_str}
        ---------------------
        Given the context information and not prior knowledge, \
        give the best fit agent based on the query. \


        Query: {query_str}
        Answer: \
        """

        qa_prompt_template = PromptTemplate(template=agent_rag_template)

        custom_query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_template})

        response = custom_query_engine.query(ques)


        return response


# inference = Inference()
#
# ques = "Looking for help with organizing a large corporate event."
#
# response = inference._query_engine(ques)
#
# print(response)