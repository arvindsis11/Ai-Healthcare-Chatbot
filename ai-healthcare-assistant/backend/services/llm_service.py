from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from typing import List, Dict, Any, Optional
import os

class LLMService:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=1000
        )

    def generate_response(self, query: str, context: Optional[List[str]] = None) -> str:
        """Generate a response using the LLM with optional context."""
        if context:
            # RAG prompt
            template = """You are a helpful healthcare assistant. Use the following context to answer the user's question.
If you cannot find the answer in the context, provide general healthcare advice but recommend consulting a doctor.

Context:
{context}

Question: {question}

Answer:"""

            prompt = ChatPromptTemplate.from_template(template)

            # Combine context
            context_text = "\n\n".join(context)

            chain = (
                {"context": lambda x: context_text, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )

            return chain.invoke(query)
        else:
            # Basic chat
            template = """You are a helpful healthcare assistant. Answer the user's question about health and wellness.
Always recommend consulting a healthcare professional for medical advice.

Question: {question}

Answer:"""

            prompt = ChatPromptTemplate.from_template(template)
            chain = prompt | self.llm | StrOutputParser()

            return chain.invoke(query)

    def summarize_context(self, documents: List[str]) -> str:
        """Summarize retrieved documents for context."""
        if not documents:
            return ""

        template = """Summarize the following healthcare information concisely:

{documents}

Summary:"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()

        docs_text = "\n\n".join(documents[:3])  # Limit to top 3
        return chain.invoke({"documents": docs_text})