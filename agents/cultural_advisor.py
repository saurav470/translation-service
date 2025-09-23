import json
import os
from openai import OpenAI
from config.agent_config import LANGUAGE_CONFIGS


class CulturalAdvisor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"

    def analyze(self, source_text, initial_translation, target_language="swedish"):
        """Analyze cultural context and provide localization recommendations"""

        lang_config = LANGUAGE_CONFIGS.get(target_language, LANGUAGE_CONFIGS["swedish"])
        lang_name = lang_config["name"]
        cultural_aspects = lang_config["cultural_aspects"]
        regions = lang_config["regions"]

        if target_language == "swedish":
            system_prompt = """You are a Swedish cultural and linguistic expert specializing in localization and cultural adaptation.

            Your expertise includes:
            - Swedish cultural norms, values, and social conventions
            - Regional variations across Sweden (Stockholm, Göteborg, Malmö, Northern Sweden)
            - Business culture and communication styles
            - Swedish humor, idioms, and colloquialisms
            - Historical and contemporary Swedish society
            - Consumer behavior and market preferences
            - Legal and regulatory considerations
            - Swedish language register and formality levels
            
            Swedish Cultural Context Considerations:
            1. Lagom philosophy (moderation, balance)
            2. Jantelagen (law of Jante) - modesty and equality
            3. Allemansrätten (right to roam)
            4. Workplace equality and consensus culture
            5. Environmental consciousness
            6. Technology adoption and digitalization
            7. Seasonal and geographic variations
            8. Age and generational differences
            
            Language Considerations:
            - Formal vs informal address (ni/du)
            - Regional dialect influences
            - Loan words vs native Swedish terms
            - Business vs casual register
            - Swedish compound word preferences
            
        Provide analysis in JSON format:
        {
            "cultural_appropriateness": "high|medium|low",
            "adaptations": ["adaptation1", "adaptation2"],
            "regional_notes": ["note1", "note2"],
            "register_recommendations": "formal|informal|neutral",
            "localization_suggestions": ["suggestion1", "suggestion2"],
            "cultural_risks": ["risk1", "risk2"],
            "target_audience_fit": "excellent|good|fair|poor"
        }
            
            """
        else:  # Dutch
            system_prompt = """You are a Dutch cultural and linguistic expert specializing in localization and cultural adaptation.

            Your expertise includes:
            - Dutch cultural norms, values, and social conventions
            - Regional variations across Netherlands and Belgium (Amsterdam, Rotterdam, Utrecht, The Hague, Flanders)
            - Business culture and communication styles
            - Dutch humor, idioms, and colloquialisms
            - Historical and contemporary Dutch society
            - Consumer behavior and market preferences
            - Legal and regulatory considerations
            - Dutch language register and formality levels
            
            Dutch Cultural Context Considerations:
            1. Directness and honesty in communication
            2. Pragmatism and efficiency
            3. Tolerance and liberal values
            4. Consensus building (poldermodel)
            5. Work-life balance importance
            6. Egalitarian society
            7. Regional differences (Netherlands vs Belgium)
            8. Multicultural integration
            
            Language Considerations:
            - Formal vs informal address (u/je, jij)
            - Regional dialect influences (Flemish vs Dutch)
            - English loanwords vs native Dutch terms
            - Business vs casual register
            - Dutch compound word preferences
            
        Provide analysis in JSON format:
        {
            "cultural_appropriateness": "high|medium|low",
            "adaptations": ["adaptation1", "adaptation2"],
            "regional_notes": ["note1", "note2"],
            "register_recommendations": "formal|informal|neutral",
            "localization_suggestions": ["suggestion1", "suggestion2"],
            "cultural_risks": ["risk1", "risk2"],
            "target_audience_fit": "excellent|good|fair|poor"
        }"""

        user_prompt = f"""Analyze the cultural appropriateness of this English to {lang_name} translation:

        ORIGINAL ENGLISH TEXT:
        "{source_text}"
        
        {lang_name.upper()} TRANSLATION:
        "{initial_translation}"
        
        Analyze:
        1. Cultural context and appropriateness for {lang_name} audience
        2. Register and formality level suitability
        3. Regional considerations (if any specific region targeted)
        4. Business vs consumer context appropriateness
        5. Potential cultural sensitivities or misunderstandings
        6. Localization opportunities for better {lang_name} market fit
        7. Age group and demographic considerations
        
        Consider {lang_name} cultural values like {', '.join(cultural_aspects)}.
        Recommend adaptations for authentic {lang_name} communication style."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if content is None:
                raise ValueError("No content received from OpenAI API")
            result = json.loads(content)
            return result

        except Exception as e:
            return {
                "cultural_appropriateness": "low",
                "adaptations": [f"Cultural analysis failed: {str(e)}"],
                "regional_notes": [],
                "register_recommendations": "neutral",
                "localization_suggestions": [],
                "cultural_risks": ["Unable to assess cultural context"],
                "target_audience_fit": "poor",
            }
