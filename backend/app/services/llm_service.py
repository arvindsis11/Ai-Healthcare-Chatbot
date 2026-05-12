from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from typing import List, Optional
import json
import re
from ..models.chat import SymptomAnalysis, RiskLevel, ReportSection

# Default timeouts per provider (seconds). Applied when llm_timeout_seconds=0.
_PROVIDER_TIMEOUTS: dict[str, int] = {
    "openai": 30,     # Cloud API — a hang almost always means an error
    "lm-studio": 120, # Local inference can be slow, especially on first run
    "ollama": 120,
}


class LLMService:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
        base_url: Optional[str] = None,
        provider: str = "openai",
        timeout_seconds: int = 0,
    ):
        self.api_key = api_key
        self.provider = provider
        self.llm = None

        effective_timeout = timeout_seconds or _PROVIDER_TIMEOUTS.get(provider, 30)

        # Local providers (lm-studio, ollama) expose an OpenAI-compatible API,
        # so ChatOpenAI works for all of them — only the base_url and api_key
        # differ.  A dummy key is used when no real key is required.
        effective_key = api_key or ("local" if provider != "openai" else "")
        if effective_key:
            kwargs = dict(
                openai_api_key=effective_key,
                model=model,
                temperature=0.3,  # Lower temperature for medical advice
                max_tokens=1500,
                request_timeout=effective_timeout,
            )
            if base_url:
                kwargs["openai_api_base"] = base_url
            self.llm = ChatOpenAI(**kwargs)

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

        {{
            "symptoms": ["list", "of", "identified", "symptoms"],
            "severity_score": <number 1-10, where 1 is mild and 10 is life-threatening>,
            "risk_level": "<low|medium|high>",
            "possible_conditions": ["list", "of", "possible", "general", "conditions"],
            "urgency_recommendation": "<recommendation for when to seek medical help>"
        }}

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
        if not self.llm:
            severity = 2 if len(symptoms) <= 1 else 5
            risk = RiskLevel.LOW if severity <= 3 else RiskLevel.MEDIUM
            return SymptomAnalysis(
                symptoms=symptoms,
                severity_score=severity,
                risk_level=risk,
                possible_conditions=["General symptom pattern - clinical evaluation needed"],
                urgency_recommendation="Monitor symptoms and consult a healthcare professional if they worsen or persist."
            )

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
                # Normalise risk_level to lowercase — some models return "LOW"/"HIGH"
                if "risk_level" in analysis_data:
                    analysis_data["risk_level"] = analysis_data["risk_level"].lower()
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

        if not self.llm:
            context_hint = ""
            if context:
                context_hint = "\n\nRelevant context snippets:\n- " + "\n- ".join(context[:2])

            risk_hint = ""
            if symptom_analysis:
                risk_hint = (
                    f"\n\nEstimated triage risk: {symptom_analysis.risk_level.value.upper()} "
                    f"(severity {symptom_analysis.severity_score}/10)."
                )

            return (
                "I can provide general health information, but an OpenAI API key is not configured in this environment, "
                "so I am using a limited fallback response mode. "
                "Please consult a licensed healthcare professional for diagnosis and treatment." +
                risk_hint +
                context_hint +
                "\n\nMedical disclaimer: This is not medical advice."
            )

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

    def generate_report_data(self, chat_history: List[dict]) -> ReportSection:
        """Generate a structured health report from conversation history."""
        if not chat_history:
            return ReportSection(
                symptoms_detected=[],
                possible_conditions=[],
                suggested_precautions=["Maintain a healthy lifestyle", "Stay hydrated", "Get adequate rest"],
                when_to_consult_doctor="Consult a healthcare professional if you experience any concerning symptoms.",
                summary="No conversation history available to generate a health report.",
            )

        conversation_text = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history
        )

        if not self.llm:
            user_messages = [m["content"] for m in chat_history if m["role"] == "user"]
            combined = " ".join(user_messages).lower()
            keywords = [
                "fever", "headache", "nausea", "dizziness", "cough", "pain",
                "fatigue", "vomiting", "rash", "shortness of breath", "chest pain",
                "sore throat", "runny nose", "abdominal pain", "back pain",
            ]
            found = [kw for kw in keywords if kw in combined]
            return ReportSection(
                symptoms_detected=found if found else ["No specific symptoms identified"],
                possible_conditions=["Unable to determine without LLM — consult a healthcare professional"],
                suggested_precautions=[
                    "Rest and stay hydrated",
                    "Monitor your symptoms",
                    "Avoid self-medication without professional guidance",
                ],
                when_to_consult_doctor="Please consult a healthcare professional for a proper evaluation.",
                summary="Health report generated from conversation. An OpenAI API key is required for a detailed analysis.",
            )

        report_prompt = """Analyze the following patient-chatbot conversation and extract health information.
Return ONLY a JSON object with this exact structure:

{{
    "symptoms_detected": ["list of symptoms mentioned by the patient"],
    "possible_conditions": ["list of possible general conditions — do not diagnose, only suggest possibilities"],
    "suggested_precautions": ["list of self-care measures and precautions"],
    "when_to_consult_doctor": "clear guidance on urgency and when to seek professional help",
    "summary": "2-3 sentence summary of the patient health concern and key findings",
    "severity_score": <integer 1-10 representing overall severity, where 1 is mild and 10 is life-threatening>,
    "risk_level": "<low|medium|high>"
}}

Severity scoring guidelines:
- 1-3: Mild, manageable at home
- 4-6: Moderate, should see a doctor within days
- 7-10: Severe, requires prompt or immediate medical attention

Be conservative, accurate, and do not make definitive diagnoses.
Conversation:
"""

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(report_prompt + "{conversation}"),
            HumanMessagePromptTemplate.from_template("Generate the health report JSON."),
        ])

        chain = prompt | self.llm | StrOutputParser()
        try:
            response = chain.invoke({"conversation": conversation_text})
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return ReportSection(**data)
        except Exception as e:
            print(f"Error generating report data: {e}")

        return ReportSection(
            symptoms_detected=["Unable to extract symptoms"],
            possible_conditions=["Unable to determine — consult a healthcare professional"],
            suggested_precautions=["Rest and stay hydrated", "Monitor symptoms", "Seek medical advice if symptoms worsen"],
            when_to_consult_doctor="Please consult a healthcare professional for a proper evaluation.",
            summary="Health report could not be fully generated. Please consult a healthcare professional.",
        )

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