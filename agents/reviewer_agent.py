import json
import os
from openai import OpenAI
from config.agent_config import LANGUAGE_CONFIGS

class ReviewerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def review(self, source_text, initial_translation, cultural_analysis, target_language="swedish"):
        """Review and refine the initial translation based on linguistic and cultural analysis"""
        
        lang_config = LANGUAGE_CONFIGS.get(target_language, LANGUAGE_CONFIGS["swedish"])
        lang_name = lang_config["name"]
        
        if target_language == "swedish":
            system_prompt = """You are a Swedish language specialist and translation reviewer with expertise in:
            - Advanced Swedish grammar and syntax
            - Regional variations and dialectal preferences
            - Professional translation quality standards
            - Linguistic error detection and correction
            - Style and register optimization
            
            Your role is to review translations and provide refined, error-free Swedish text that meets professional standards.
            
            Review criteria:
            1. Grammatical accuracy (Swedish morphology, syntax, agreement)
            2. Lexical choices and terminology consistency
            3. Stylistic appropriateness and register
            4. Cultural adaptation and localization
            5. Natural flow and readability
            6. Completeness and fidelity to source meaning
            7. NO addition of disclaimers, regulatory info, or content not in original
            8. Preserve exact content structure and length of original text"""
        else:  # Dutch
            system_prompt = """You are a Dutch language specialist and translation reviewer with expertise in:
            - Advanced Dutch grammar and syntax
            - Regional variations and dialectal preferences (Netherlands vs Belgium)
            - Professional translation quality standards
            - Linguistic error detection and correction
            - Style and register optimization
            
            Your role is to review translations and provide refined, error-free Dutch text that meets professional standards.
            
            Review criteria:
            1. Grammatical accuracy (Dutch morphology, syntax, agreement)
            2. Lexical choices and terminology consistency
            3. Stylistic appropriateness and register
            4. Cultural adaptation and localization
            5. Natural flow and readability
            6. Completeness and fidelity to source meaning
            7. NO addition of disclaimers, regulatory info, or content not in original
            8. Preserve exact content structure and length of original text"""
        
        system_prompt += f"""
        
        Provide your response in JSON format:
        {{
            "final_translation": "refined {lang_name} translation",
            "review_comments": ["comment1", "comment2"],
            "changes_made": ["change1", "change2"],
            "confidence_improvement": improvement_percentage,
            "quality_grade": "A|B|C|D|F"
        }}"""
        
        cultural_context = json.dumps(cultural_analysis, ensure_ascii=False, indent=2)
        
        user_prompt = f"""Review and refine this English to {lang_name} translation:

        ORIGINAL ENGLISH:
        "{source_text}"
        
        INITIAL {lang_name.upper()} TRANSLATION:
        "{initial_translation}"
        
        CULTURAL ANALYSIS CONTEXT:
        {cultural_context}
        
        CRITICAL: Do NOT add any disclaimers, regulatory information, medical warnings, or contact details that are not present in the original English text. The translation should be faithful to the source content only.
        
        Please review the translation for:
        1. {lang_name} grammatical correctness
        2. Natural language flow
        3. Cultural appropriateness
        4. Terminology accuracy
        5. Style consistency
        6. Register appropriateness
        7. Faithful reproduction of original content (no additions)
        
        Provide an improved, refined {lang_name} translation that matches the original text's structure and content exactly."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("No content received from OpenAI API")
            result = json.loads(content)
            return result
            
        except Exception as e:
            return {
                "final_translation": initial_translation,
                "review_comments": [f"Review failed: {str(e)}"],
                "changes_made": [],
                "confidence_improvement": 0,
                "quality_grade": "F"
            }
