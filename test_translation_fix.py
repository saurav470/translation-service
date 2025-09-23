#!/usr/bin/env python3
"""
Test script to verify the translation fix for medical disclaimers
"""

import asyncio
import json
from core.translation_service import TranslationService
from api.models import TranslationRequest, LanguageCode

async def test_medical_translation():
    """Test the medical text translation to ensure no disclaimers are added"""
    
    # Initialize the translation service
    service = TranslationService()
    
    # The problematic medical text from the user
    medical_text = """Thank you for making the time to attend our recent speaker program. CAMZYOS® (mavacamten), a first-in-class cardiac myosin inhibitor, has redefined the treatment landscape for NYHA Class II–III obstructive HCM since its FDA approval in 2022.1,2 With the longest available follow-up for cardiac myosin inhibitors, based on results from Week 180 in EXPLORER-LTE, CAMZYOS has been evaluated for its impact on patients' LVOT gradient, symptom burden, and cardiac biomarkers.3 In April 2025, the FDA updated echo monitoring requirements for eligible patients in the Maintenance Phase taking CAMZYOS based on long-term safety, clinical trial, and real-world REMS data.4,5 Consider joining the 3500 prescribers who have written a prescription for over 15,000 patients in the US.6"""
    
    # Create translation request
    request = TranslationRequest(
        source_text=medical_text,
        target_language=LanguageCode.SWEDISH,
        include_quality_analysis=True,
        include_cultural_analysis=True,
        include_mqm_analysis=True,
        include_iso_compliance=True
    )
    
    print("Testing medical text translation...")
    print(f"Original text length: {len(medical_text)} characters")
    print(f"Original text: {medical_text[:100]}...")
    print("\n" + "="*80 + "\n")
    
    try:
        # Perform translation
        result = await service.translate(request)
        
        # Get the final translation (refined if available, otherwise initial)
        final_translation = result.refined_translation.final_translation if result.refined_translation else result.initial_translation.translation
        
        print("TRANSLATION RESULT:")
        print(f"Translation length: {len(final_translation)} characters")
        print(f"Translation: {final_translation}")
        print("\n" + "="*80 + "\n")
        
        # Check for unwanted disclaimers
        unwanted_phrases = [
            "Endast för hälso- och sjukvårdspersonal",
            "Biverkningar ska rapporteras",
            "Läkemedelsverket",
            "FASS.se",
            "medicinsk information",
            "produktresumé",
            "varningar och försiktighet"
        ]
        
        found_unwanted = []
        for phrase in unwanted_phrases:
            if phrase.lower() in final_translation.lower():
                found_unwanted.append(phrase)
        
        if found_unwanted:
            print("❌ ISSUE FOUND: Unwanted disclaimers detected!")
            print("Found unwanted phrases:")
            for phrase in found_unwanted:
                print(f"  - {phrase}")
        else:
            print("✅ SUCCESS: No unwanted disclaimers found!")
            print("Translation appears to be faithful to the original text.")
        
        # Show quality metrics
        if result.quality_assessment:
            print(f"\nQuality Score: {result.quality_assessment.overall_score}/100")
            print(f"Confidence: {result.initial_translation.confidence}/100")
        
        return result
        
    except Exception as e:
        print(f"❌ ERROR: Translation failed: {str(e)}")
        return None

if __name__ == "__main__":
    asyncio.run(test_medical_translation())
