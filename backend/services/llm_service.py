from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import StrOutputParser, BaseMessage
from langchain.schema.runnable import RunnablePassthrough
from typing import List, Dict, Any, Optional
import json
import re
from ..models.chat import SymptomAnalysis, RiskLevel

class LLMService:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=0.3,  # Lower temperature for medical advice
            max_tokens=1500
        )

        # System prompts for different functionalities
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

        self.symptom_analysis_prompt = """
        Analyze the following symptoms and provide a structured assessment.
        Return your response as a JSON object with this exact structure:

        {
            "symptoms": ["list", "of", "identified", "symptoms"],
            "severity_score": <number 1-10, where 1 is mild and 10 is life-threatening>,
            "risk_level": "<low|medium|high>",
            "possible_conditions": ["list", "of", "possible", "general", "conditions"],
            "urgency_recommendation": "<recommendation for when to seek medical help>"
        }

        Guidelines for scoring:
        - Severity 1-3: Mild symptoms, can usually wait for routine care
        - Severity 4-6: Moderate symptoms, should see doctor within days
        - Severity 7-10: Severe symptoms, seek immediate medical attention

        Risk levels:
        - LOW: Non-urgent, can be managed at home
        - MEDIUM: Should see healthcare provider within days
        - HIGH: Requires immediate medical attention

        Be conservative with high severity scores. When in doubt, err on the side of caution.
        """

    def analyze_symptoms(self, symptoms: List[str], user_description: str = "") -> SymptomAnalysis:
        """Analyze symptoms and return structured assessment."""
        symptoms_text = ", ".join(symptoms)
        full_description = f"Symptoms: {symptoms_text}\nDescription: {user_description}"

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.symptom_analysis_prompt),
            HumanMessagePromptTemplate.from_template("Please analyze these symptoms: {symptoms}")
        ])

        chain = prompt | self.llm | StrOutputParser()

        try:
            response = chain.invoke({"symptoms": full_description})
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
                return SymptomAnalysis(**analysis_data)
            else:
                # Fallback analysis
                return SymptomAnalysis(
                    symptoms=symptoms,
                    severity_score=5,
                    risk_level=RiskLevel.MEDIUM,
                    possible_conditions=["Unknown - please consult a doctor"],
                    urgency_recommendation="Please consult a healthcare professional for proper evaluation."
                )
        except Exception as e:
            print(f"Error in symptom analysis: {e}")
            return SymptomAnalysis(
                symptoms=symptoms,
                severity_score=5,
                risk_level=RiskLevel.MEDIUM,
                possible_conditions=["Unable to analyze - consult a doctor"],
                urgency_recommendation="Please seek medical attention for proper evaluation."
            )

    def generate_medical_response(self, query: str, context: Optional[List[str]] = None, symptom_analysis: Optional[SymptomAnalysis] = None) -> str:
        """Generate a medical response using RAG with symptom analysis."""

        # Build context
        context_text = ""
        if context:
            context_text = "\n\n".join(context)

        # Add symptom analysis if available
        analysis_text = ""
        if symptom_analysis:
            analysis_text = f"""
            Symptom Analysis:
            - Identified Symptoms: {', '.join(symptom_analysis.symptoms)}
            - Severity Score: {symptom_analysis.severity_score}/10
            - Risk Level: {symptom_analysis.risk_level.value.upper()}
            - Possible General Conditions: {', '.join(symptom_analysis.possible_conditions)}
            - Urgency: {symptom_analysis.urgency_recommendation}
            """

        template = f"""{self.medical_system_prompt}

        Context Information:
        {{context}}

        Symptom Analysis:
        {{analysis}}

        User Query: {{question}}

        Provide a helpful response that:
        1. Acknowledges the user's symptoms/concerns
        2. Provides general information based on the context
        3. Includes the symptom analysis insights
        4. Gives appropriate precautions and self-care advice
        5. Strongly recommends professional medical consultation
        6. Ends with the medical disclaimer

        Response:"""

        prompt = ChatPromptTemplate.from_template(template)

        chain = (
            {
                "context": lambda x: context_text,
                "analysis": lambda x: analysis_text,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(query)

    def generate_response(self, query: str, context: Optional[List[str]] = None) -> str:
        """Legacy method for backward compatibility."""
        return self.generate_medical_response(query, context)

    def summarize_context(self, documents: List[str]) -> str:
        """Summarize retrieved documents for context."""
        if not documents:
            return ""

        template = """Summarize the following healthcare information concisely, focusing on key symptoms, causes, and general advice:

{documents}

Summary:"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()

        docs_text = "\n\n".join(documents[:3])  # Limit to top 3
        return chain.invoke({"documents": docs_text})