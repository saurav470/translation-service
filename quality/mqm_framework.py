import json
import os
from openai import OpenAI

class MQMFramework:

    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-5"
        

        self.error_categories = {
            "accuracy": {
                "mistranslation": {"minor": -1, "major": -5, "critical": -25},
                "omission": {"minor": -1, "major": -5, "critical": -25},
                "addition": {"minor": -1, "major": -5, "critical": -25},
                "untranslated": {"minor": -1, "major": -5, "critical": -25}
            },
            "fluency": {
                "grammar": {"minor": -0.5, "major": -2, "critical": -5},
                "spelling": {"minor": -0.25, "major": -1, "critical": -5},
                "punctuation": {"minor": -0.1, "major": -0.5, "critical": -2},
                "register": {"minor": -0.5, "major": -2, "critical": -5}
            },
            "style": {
                "awkward": {"minor": -0.25, "major": -1, "critical": -3},
                "unnatural": {"minor": -0.5, "major": -2, "critical": -5},
                "inconsistent_style": {"minor": -0.25, "major": -1, "critical": -3}
            },
            "terminology": {
                "inconsistent_term": {"minor": -0.5, "major": -2, "critical": -10},
                "wrong_term": {"minor": -1, "major": -5, "critical": -15}
            }
        }
    
    def analyze(self, source_text, translation, quality_assessment):
        """Perform MQM analysis on the translation"""
        
        system_prompt = f"""You are an MQM (Multidimensional Quality Metrics) expert for translation evaluation.

        MQM Framework Error Categories:
        
        ACCURACY ERRORS:
        - Mistranslation: Wrong meaning conveyed
        - Omission: Source content missing in translation  
        - Addition: Extra content not in source
        - Untranslated: Source text left untranslated
        
        FLUENCY ERRORS:
        - Grammar: Morphology, syntax, agreement errors
        - Spelling: Incorrect word spelling
        - Punctuation: Wrong punctuation usage
        - Register: Inappropriate formality level
        
        STYLE ERRORS:
        - Awkward: Unnatural phrasing but understandable
        - Unnatural: Does not sound like native Swedish
        - Inconsistent style: Mixed registers or styles
        
        TERMINOLOGY ERRORS:
        - Inconsistent term: Same concept translated differently
        - Wrong term: Incorrect technical/domain term used
        
        Severity Levels:
        - MINOR: Slight impact on quality/understanding
        - MAJOR: Noticeable impact, may cause confusion
        - CRITICAL: Severe impact, meaning substantially affected
        
        Error Penalty System:
        {json.dumps(self.error_categories, indent=2)}
        
        Provide MQM analysis in JSON format:
        {{
            "total_score": calculated_score_out_of_100,
            "word_count": number_of_words,
            "errors": [
                {{
                    "category": "accuracy|fluency|style|terminology",
                    "subcategory": "specific_error_type",
                    "severity": "minor|major|critical",
                    "description": "error description",
                    "penalty": negative_number,
                    "location": "text segment with error"
                }}
            ],
            "error_summary": {{
                "total_errors": number,
                "accuracy_errors": number,
                "fluency_errors": number,
                "style_errors": number,
                "terminology_errors": number
            }},
            "mqm_grade": "A|B|C|D|F",
            "industry_compliance": true_or_false
        }}"""
        
        user_prompt = f"""Perform MQM (Multidimensional Quality Metrics) analysis on this translation:

        SOURCE TEXT (English):
        "{source_text}"
        
        TRANSLATION (Swedish):
        "{translation}"
        
        QUALITY ASSESSMENT CONTEXT:
        {json.dumps(quality_assessment, ensure_ascii=False, indent=2)}
        
        Instructions:
        1. Identify all errors according to MQM categories
        2. Assign severity levels (minor/major/critical)
        3. Calculate penalty points for each error
        4. Determine total MQM score (start at 100, subtract penalties)
        5. Assign MQM grade: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
        6. Assess industry compliance (>= 85 score = compliant)
        
        Be thorough but fair in error detection. Focus on errors that actually impact quality."""
        
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
            
            # Validate and ensure reasonable scoring
            if result.get("total_score", 0) > 100:
                result["total_score"] = 100
            elif result.get("total_score", 0) < 0:
                result["total_score"] = 0
                
            return result
            
        except Exception as e:
            return {
                "total_score": 0,
                "word_count": len(source_text.split()),
                "errors": [
                    {
                        "category": "system",
                        "subcategory": "analysis_failure", 
                        "severity": "critical",
                        "description": f"MQM analysis failed: {str(e)}",
                        "penalty": -100,
                        "location": "system error"
                    }
                ],
                "error_summary": {
                    "total_errors": 1,
                    "accuracy_errors": 0,
                    "fluency_errors": 0,
                    "style_errors": 0,
                    "terminology_errors": 0
                },
                "mqm_grade": "F",
                "industry_compliance": False
            }
