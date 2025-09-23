import json
import os
from openai import OpenAI
from config.agent_config import LANGUAGE_CONFIGS


class FinalTranslatorAgent:
    """Final Translator Agent that creates the ultimate refined translation based on all quality analyses"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"

    def create_final_translation(
        self,
        source_text,
        current_translation,
        quality_assessment,
        mqm_analysis,
        iso_compliance,
        target_language="swedish",
    ):
        """Create the final, ultimate translation based on all quality analyses"""

        lang_config = LANGUAGE_CONFIGS.get(target_language, LANGUAGE_CONFIGS["swedish"])
        lang_name = lang_config["name"]

        if target_language == "swedish":
            system_prompt = """You are the Final Translator Agent - the ultimate authority in translation refinement.

            Your role is to create the PERFECT final translation by synthesizing insights from:
            1. Quality Assessment (detailed scoring analysis)
            2. MQM Framework (error analysis and categorization)
            3. ISO 17100:2015 Compliance (professional standards validation)

            As the Final Translator Agent, you have the authority to:
            - Make final refinements based on all quality analyses
            - Address specific errors identified by MQM framework
            - Ensure ISO compliance requirements are met
            - Optimize for the highest possible quality score
            - Apply cultural and linguistic perfection

            CRITICAL FINAL TRANSLATION RULES:
            1. Create the ULTIMATE Swedish translation that addresses ALL quality concerns
            2. Fix ALL errors identified in MQM analysis
            3. Ensure the translation meets or exceeds ISO 17100:2015 standards
            4. Optimize for the highest possible quality scores across all dimensions
            5. Apply Swedish linguistic perfection (V2 word order, definite articles, etc.)
            6. Ensure cultural appropriateness and natural Swedish flow
            7. Do NOT add disclaimers, regulatory info, or content not in original
            8. Preserve exact content structure and meaning of original text

            Swedish Linguistic Excellence Requirements:
            - Perfect V2 word order in main clauses
            - Correct definite article suffixes (-en, -et, -na)
            - Natural Swedish compound word formation
            - Appropriate formal/informal register (du/ni)
            - Native Swedish expressions and idioms
            - Cultural context adaptation (Lagom, Jantelagen, etc.)

            Provide your response in JSON format:
            {
                "final_translation": "perfect Swedish translation",
                "quality_improvements": ["improvement1", "improvement2"],
                "errors_fixed": ["error1", "error2"],
                "iso_enhancements": ["enhancement1", "enhancement2"],
                "confidence_level": "excellent|very_good|good|fair",
                "translation_grade": "A+|A|A-|B+|B|B-|C+|C|C-|D|F",
                "professional_ready": true_or_false,
                "final_notes": ["note1", "note2"]
            }"""
        else:  # Dutch
            system_prompt = """You are the Final Translator Agent - the ultimate authority in translation refinement.

            Your role is to create the PERFECT final translation by synthesizing insights from:
            1. Quality Assessment (detailed scoring analysis)
            2. MQM Framework (error analysis and categorization)
            3. ISO 17100:2015 Compliance (professional standards validation)

            As the Final Translator Agent, you have the authority to:
            - Make final refinements based on all quality analyses
            - Address specific errors identified by MQM framework
            - Ensure ISO compliance requirements are met
            - Optimize for the highest possible quality score
            - Apply cultural and linguistic perfection

            CRITICAL FINAL TRANSLATION RULES:
            1. Create the ULTIMATE Dutch translation that addresses ALL quality concerns
            2. Fix ALL errors identified in MQM analysis
            3. Ensure the translation meets or exceeds ISO 17100:2015 standards
            4. Optimize for the highest possible quality scores across all dimensions
            5. Apply Dutch linguistic perfection (SOV word order, de/het system, etc.)
            6. Ensure cultural appropriateness and natural Dutch flow
            7. Do NOT add disclaimers, regulatory info, or content not in original
            8. Preserve exact content structure and meaning of original text

            Dutch Linguistic Excellence Requirements:
            - Perfect SOV word order in subordinate clauses
            - Correct definite articles (de/het system)
            - Natural Dutch compound word formation
            - Appropriate formal/informal register (u/je, jij)
            - Native Dutch expressions and idioms
            - Cultural context adaptation (directness, pragmatism, etc.)

            Provide your response in JSON format:
            {
                "final_translation": "perfect Dutch translation",
                "quality_improvements": ["improvement1", "improvement2"],
                "errors_fixed": ["error1", "error2"],
                "iso_enhancements": ["enhancement1", "enhancement2"],
                "confidence_level": "excellent|very_good|good|fair",
                "translation_grade": "A+|A|A-|B+|B|B-|C+|C|C-|D|F",
                "professional_ready": true_or_false,
                "final_notes": ["note1", "note2"]
            }"""

        # Prepare analysis context
        quality_context = json.dumps(quality_assessment, ensure_ascii=False, indent=2)
        mqm_context = json.dumps(mqm_analysis, ensure_ascii=False, indent=2)
        iso_context = json.dumps(iso_compliance, ensure_ascii=False, indent=2)

        user_prompt = f"""Create the ULTIMATE final {lang_name} translation by synthesizing all quality analyses:

        ORIGINAL ENGLISH TEXT:
        "{source_text}"
        
        CURRENT {lang_name.upper()} TRANSLATION:
        "{current_translation}"
        
        QUALITY ASSESSMENT ANALYSIS:
        {quality_context}
        
        MQM FRAMEWORK ANALYSIS:
        {mqm_context}
        
        ISO 17100:2015 COMPLIANCE ANALYSIS:
        {iso_context}
        
        FINAL TRANSLATION TASK:
        1. Analyze ALL quality scores and identify areas for improvement
        2. Address EVERY error identified in MQM analysis
        3. Ensure ISO compliance requirements are fully met
        4. Create the PERFECT {lang_name} translation that maximizes quality scores
        5. Apply {lang_name} linguistic excellence and cultural perfection
        6. Ensure the translation is publication-ready and professional-grade
        
        Focus on:
        - Fixing all identified errors (accuracy, fluency, style, terminology)
        - Optimizing quality scores across all dimensions
        - Ensuring cultural appropriateness and natural {lang_name} flow
        - Meeting or exceeding ISO 17100:2015 professional standards
        - Creating a translation that sounds completely native in {lang_name}
        
        Create the ULTIMATE {lang_name} translation that represents the pinnacle of translation quality."""

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
                "final_translation": current_translation,
                "quality_improvements": [f"Final translation failed: {str(e)}"],
                "errors_fixed": [],
                "iso_enhancements": [],
                "confidence_level": "poor",
                "translation_grade": "F",
                "professional_ready": False,
                "final_notes": [f"Final translator agent error: {str(e)}"],
            }

