import json
import os
from openai import OpenAI
from config.agent_config import LANGUAGE_CONFIGS
from utils.GLOSSARY.dutch import dutch


class TranslatorAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
        self.glossary = dutch

    def translate(self, source_text, target_language="swedish"):
        """Perform high-quality English to target language translation"""

        lang_config = LANGUAGE_CONFIGS.get(target_language, LANGUAGE_CONFIGS["swedish"])
        lang_name = lang_config["name"]

        if target_language == "swedish":
            system_prompt = """You are a professional English to Swedish translator with expertise in:
            - Native Swedish linguistic patterns
            - Cultural nuances and context adaptation
            - Technical terminology and colloquial expressions
            - Swedish grammar and syntax rules
            
            CRITICAL TRANSLATION RULES:
            1. Translate ONLY what is provided in the source text
            2. Do NOT add disclaimers, regulatory information, or legal text not present in the original
            3. Do NOT add medical warnings, side effect information, or contact details
            4. Do NOT add references to external websites or regulatory bodies
            5. Preserve the exact structure and content of the original text
            6. If the original text lacks disclaimers, the translation should also lack them
            
            Your task is to provide accurate, fluent, and culturally appropriate Swedish translations that are faithful to the source content.
            Consider Swedish linguistic features like:
            - V2 word order in main clauses
            - Definite article suffixes (-en, -et, -na)
            - Swedish vowel system and pronunciation
            - Formal vs informal register (du/ni)
            - Swedish compound word formation
            
            Provide your response in JSON format with the following structure:
            {
                "translation": "Swedish translation here",
                "confidence": confidence_score_0_to_100,
                "translation_notes": ["note1", "note2"],
                "difficulty_level": "easy|medium|hard",
                "key_decisions": ["decision1", "decision2"]
            }"""
        
        else:  # Dutch
            system_prompt = """You are a professional English to Dutch translator with expertise in:
            - Native Dutch linguistic patterns
            - Cultural nuances and context adaptation
            - Technical terminology and colloquial expressions
            - Dutch grammar and syntax rules
            
            CRITICAL TRANSLATION RULES:
            1. Translate ONLY what is provided in the source text
            2. Do NOT add disclaimers, regulatory information, or legal text not present in the original
            3. Do NOT add medical warnings, side effect information, or contact details
            4. Do NOT add references to external websites or regulatory bodies
            5. Preserve the exact structure and content of the original text
            6. If the original text lacks disclaimers, the translation should also lack them
            
            Your task is to provide accurate, fluent, and culturally appropriate Dutch translations that are faithful to the source content.
            Consider Dutch linguistic features like:
            - SOV word order in subordinate clauses
            - Definite articles (de/het system)
            - Dutch vowel system and diphthongs
            - Formal vs informal register (u/je, jij)
            - Dutch compound word formation
            - Diminutive forms (-je, -tje endings)
            
            Provide your response in JSON format with the following structure:
            {
                "translation": "Dutch translation here",
                "confidence": confidence_score_0_to_100,
                "translation_notes": ["note1", "note2"],
                "difficulty_level": "easy|medium|hard",
                "key_decisions": ["decision1", "decision2"]
            }"""

        user_prompt = f"""Translate this English text to {lang_name} with professional quality:

        "{source_text}"
        
        IMPORTANT: Translate ONLY the content provided above. Do NOT add any disclaimers, regulatory information, medical warnings, or contact details that are not present in the original text.
        
        Focus on:
        1. Accurate meaning preservation
        2. Natural {lang_name} flow and rhythm
        3. Appropriate register and tone
        4. Cultural context adaptation
        5. {lang_name} linguistic conventions
        6. Faithful reproduction of the original content structure"""

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
            if target_language == "dutch":
                original_translation = result["translation"]
                result["translation"] = self._apply_glossary(original_translation)
            
                # TODO: uncomment it Track if glossary was applied 
                # if original_translation != result["translation"]:
                #     result["translation_notes"].append("Glossary terms applied")
                    
            return result

        except Exception as e:
            return {
                "translation": f"Translation failed: {str(e)}",
                "confidence": 0,
                "translation_notes": ["Error in translation process"],
                "difficulty_level": "error",
                "key_decisions": [],
            }

    def _apply_glossary(self, text):
        # Same logic as DeepL system
        for en_term, nl_term in sorted(self.glossary.items(), key=lambda x: -len(x[0])):
            text = text.replace(en_term, nl_term)
        return text