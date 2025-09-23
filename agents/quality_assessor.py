import json
import os
from openai import OpenAI
from config.agent_config import LANGUAGE_CONFIGS

class QualityAssessor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
    
    def assess(self, source_text, final_translation, target_language="swedish"):
        """Comprehensive quality assessment using industry standards"""
        
        lang_config = LANGUAGE_CONFIGS.get(target_language, LANGUAGE_CONFIGS["swedish"])
        lang_name = lang_config["name"]
        
        system_prompt = f"""You are a translation quality assessment expert specializing in English-{lang_name} translation evaluation.

        You evaluate translations based on these industry-standard criteria:
        
        1. FLUENCY (0-100): Natural {lang_name} language flow, readability, no awkward constructions
        2. GRAMMAR (0-100): Correct {lang_name} morphology, syntax, agreement, punctuation
        3. ACCURACY (0-100): Faithful conveyance of source meaning, no omissions/additions
        4. NATURALNESS (0-100): Sounds like native {lang_name}, not translated text
        5. VOCABULARY (0-100): Appropriate word choices, terminology, register
        6. COLLOQUIAL USAGE (0-100): Natural {lang_name} expressions, idioms, cultural adaptation
        
        Industry benchmarks:
        - 95-100%: Exceptional (publication ready)
        - 85-94%: Professional (meets industry standards)
        - 70-84%: Acceptable (minor revisions needed)
        - Below 70%: Poor (major revisions required)
        
        Use MQM (Multidimensional Quality Metrics) framework for error categorization:
        - Accuracy errors: mistranslation, omission, addition
        - Fluency errors: grammar, spelling, punctuation, register
        - Style errors: awkward, unnatural, inconsistent
        
        Provide assessment in JSON format:
        {{
            "overall_score": overall_percentage,
            "detailed_scores": {{
                "fluency": score,
                "grammar": score,
                "accuracy": score,
                "naturalness": score,
                "vocabulary": score,
                "colloquial_usage": score
            }},
            "assessment_notes": ["note1", "note2"],
            "strengths": ["strength1", "strength2"],
            "areas_for_improvement": ["area1", "area2"],
            "industry_benchmark_met": true_or_false,
            "error_count": number,
            "errors_per_1000_words": number
        }}"""
        
        user_prompt = f"""Assess the quality of this English to {lang_name} translation using professional standards:

        ORIGINAL ENGLISH:
        "{source_text}"
        
        {lang_name.upper()} TRANSLATION:
        "{final_translation}"
        
        Evaluate based on:
        1. Fluency - natural {lang_name} flow and readability
        2. Grammar - correct {lang_name} morphology and syntax
        3. Accuracy - faithful meaning preservation
        4. Naturalness - sounds like native {lang_name}
        5. Vocabulary - appropriate word choices and terminology
        6. Colloquial usage - natural {lang_name} expressions and cultural adaptation
        
        Calculate word count and errors per 1000 words metric.
        Determine if translation meets professional industry standards (85%+ overall score)."""
        
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
                "overall_score": 0,
                "detailed_scores": {
                    "fluency": 0,
                    "grammar": 0,
                    "accuracy": 0,
                    "naturalness": 0,
                    "vocabulary": 0,
                    "colloquial_usage": 0
                },
                "assessment_notes": [f"Assessment failed: {str(e)}"],
                "strengths": [],
                "areas_for_improvement": ["Quality assessment system error"],
                "industry_benchmark_met": False,
                "error_count": 999,
                "errors_per_1000_words": 999
            }
