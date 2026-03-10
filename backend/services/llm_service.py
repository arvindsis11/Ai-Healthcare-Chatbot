"""
Async LLM Service for FastAPI backend
Integrates with existing LLM service for voice interactions
"""

import os
import logging
from typing import List, Dict, Any, Optional
import asyncio

try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    from langchain.schema import StrOutputParser
    from langchain.schema.runnable import RunnablePassthrough
    import json
    import re
except ImportError as e:
    logging.error(f"Missing LangChain dependencies: {e}")
    raise

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    """Async LLM Service for healthcare chatbot"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model="gpt-3.5-turbo",
            temperature=0.3,  # Lower temperature for medical advice
            max_tokens=1500
        )

        # Medical system prompt
        self.medical_system_prompt = """
        You are a medical assistant AI. You provide helpful, accurate information about health and symptoms,
        but you ALWAYS emphasize that you are not a substitute for professional medical advice.

        Key principles:
        1. Never diagnose conditions
        2. Always recommend consulting healthcare professionals
        3. Provide general information only
        4. Be empathetic and supportive
        5. Include appropriate medical disclaimers

        When discussing symptoms, focus on:
        - General information about possible causes
        - When to seek medical attention
        - Basic self-care measures
        - Preventive measures
        """

    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return bool(self.api_key)

    async def generate_response(self, message: str) -> Dict[str, Any]:
        """
        Generate a medical response to user message

        Args:
            message: User's message

        Returns:
            Dict containing response message and optional symptom analysis
        """
        try:
            logger.info(f"Generating response for: {message[:50]}...")

            # Create prompt template
            template = f"""{self.medical_system_prompt}

User Message: {{message}}

Provide a helpful, empathetic response that:
1. Acknowledges the user's concern
2. Provides general health information
3. Gives appropriate self-care advice
4. Strongly recommends professional medical consultation
5. Ends with a medical disclaimer

Keep your response conversational and supportive.

Response:"""

            prompt = ChatPromptTemplate.from_template(template)
            chain = prompt | self.llm | StrOutputParser()

            # Generate response
            response_text = await asyncio.get_event_loop().run_in_executor(
                None, chain.invoke, {"message": message}
            )

            # Check if message contains symptoms for analysis
            symptom_keywords = [
                'pain', 'ache', 'hurt', 'sore', 'fever', 'cough', 'nausea',
                'headache', 'dizzy', 'fatigue', 'tired', 'sick', 'ill',
                'symptom', 'feeling', 'stomach', 'chest', 'throat'
            ]

            has_symptoms = any(keyword in message.lower() for keyword in symptom_keywords)

            result = {
                "message": response_text.strip(),
                "symptom_analysis": None
            }

            if has_symptoms:
                # Perform symptom analysis
                analysis = await self._analyze_symptoms_async(message)
                result["symptom_analysis"] = analysis

            return result

        except Exception as e:
            logger.error(f"LLM response generation failed: {e}")
            return {
                "message": "I'm sorry, I'm having trouble processing your request right now. Please try again or consult a healthcare professional for medical advice.",
                "symptom_analysis": None
            }

    async def _analyze_symptoms_async(self, message: str) -> Optional[Dict[str, Any]]:
        """Analyze symptoms from user message"""
        try:
            analysis_prompt = """
Analyze the symptoms mentioned in this message and provide a structured assessment.
Return your response as a JSON object with this exact structure:

{
    "severity_score": <number 1-10>,
    "risk_level": "<low|medium|high>",
    "possible_conditions": ["condition1", "condition2"],
    "urgency_recommendation": "<recommendation text>"
}

Guidelines:
- Severity 1-3: Mild, routine care
- Severity 4-6: Moderate, see doctor within days
- Severity 7-10: Severe, immediate attention
- Be conservative with high scores

Message: {message}
"""

            prompt = ChatPromptTemplate.from_template(analysis_prompt)
            chain = prompt | self.llm | StrOutputParser()

            response = await asyncio.get_event_loop().run_in_executor(
                None, chain.invoke, {"message": message}
            )

            # Extract JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
                return analysis_data

        except Exception as e:
            logger.error(f"Symptom analysis failed: {e}")

        return None