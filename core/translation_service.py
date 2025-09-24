"""
Core translation service with multi-agent architecture
"""

import asyncio
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from agents.translator_agent import TranslatorAgent
from agents.reviewer_agent import ReviewerAgent
from agents.quality_assessor import QualityAssessor
from agents.cultural_advisor import CulturalAdvisor
from quality.mqm_framework import MQMFramework
from quality.iso_standards import ISOStandards
from api.models import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationResponse,
    TranslationResult,
    CulturalAnalysis,
    ReviewResult,
    QualityAssessment,
    MQMAnalysis,
    ISOCompliance,
    ErrorResponse,
)


class TranslationService:
    """Main translation service orchestrating multiple AI agents"""

    def __init__(self):
        """Initialize the translation service with all agents"""
        self.translator = TranslatorAgent()
        self.reviewer = ReviewerAgent()
        self.quality_assessor = QualityAssessor()
        self.cultural_advisor = CulturalAdvisor()
        self.mqm_framework = MQMFramework()
        self.iso_standards = ISOStandards()

    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Process a single translation request through the multi-agent pipeline"""
        start_time = time.time()
        request_id = str(uuid.uuid4())

        try:
            # Step 1: Initial Translation
            initial_result = await self._run_agent_async(
                self.translator.translate,
                request.source_text,
                request.target_language.value,
            )

            # Convert to response model
            initial_translation = TranslationResult(
                translation=initial_result["translation"],
                confidence=initial_result["confidence"],
                translation_notes=initial_result.get("translation_notes", []),
                difficulty_level=initial_result.get("difficulty_level", "medium"),
                key_decisions=initial_result.get("key_decisions", []),
            )

            results = {
                "initial_translation": initial_result,
                "request_id": request_id,
                "source_text": request.source_text,
                "target_language": request.target_language.value,
            }

            # Step 2: Cultural Analysis (if requested)
            cultural_analysis = None
            if request.include_cultural_analysis:
                cultural_result = await self._run_agent_async(
                    self.cultural_advisor.analyze,
                    request.source_text,
                    initial_result["translation"],
                    request.target_language.value,
                )

                cultural_analysis = CulturalAnalysis(
                    cultural_appropriateness=cultural_result[
                        "cultural_appropriateness"
                    ],
                    adaptations=cultural_result.get("adaptations", []),
                    regional_notes=cultural_result.get("regional_notes", []),
                    register_recommendations=cultural_result.get(
                        "register_recommendations", "neutral"
                    ),
                    localization_suggestions=cultural_result.get(
                        "localization_suggestions", []
                    ),
                    cultural_risks=cultural_result.get("cultural_risks", []),
                    target_audience_fit=cultural_result.get(
                        "target_audience_fit", "fair"
                    ),
                )

                results["cultural_analysis"] = cultural_result

            # Step 3: Review and Refinement
            refined_translation = None
            if request.include_quality_analysis:
                review_result = await self._run_agent_async(
                    self.reviewer.review,
                    request.source_text,
                    initial_result["translation"],
                    results.get("cultural_analysis", {}),
                    request.target_language.value,
                )

                refined_translation = ReviewResult(
                    final_translation=review_result["final_translation"],
                    review_comments=review_result.get("review_comments", []),
                    changes_made=review_result.get("changes_made", []),
                    confidence_improvement=review_result.get(
                        "confidence_improvement", 0
                    ),
                    quality_grade=review_result.get("quality_grade", "C"),
                )

                results["refined_translation"] = review_result

            # Step 4: Quality Assessment
            quality_assessment = None
            if request.include_quality_analysis:
                final_text = (
                    refined_translation.final_translation
                    if refined_translation
                    else initial_result["translation"]
                )
                quality_result = await self._run_agent_async(
                    self.quality_assessor.assess,
                    request.source_text,
                    final_text,
                    request.target_language.value,
                )

                quality_assessment = QualityAssessment(
                    overall_score=quality_result["overall_score"],
                    detailed_scores=quality_result["detailed_scores"],
                    assessment_notes=quality_result.get("assessment_notes", []),
                    strengths=quality_result.get("strengths", []),
                    areas_for_improvement=quality_result.get(
                        "areas_for_improvement", []
                    ),
                    industry_benchmark_met=quality_result.get(
                        "industry_benchmark_met", False
                    ),
                    error_count=quality_result.get("error_count", 0),
                    errors_per_1000_words=quality_result.get(
                        "errors_per_1000_words", 0
                    ),
                )

                results["quality_assessment"] = quality_result

            # Step 5: MQM Analysis
            mqm_analysis = None
            if request.include_mqm_analysis and quality_assessment:
                mqm_result = await self._run_agent_async(
                    self.mqm_framework.analyze,
                    request.source_text,
                    (
                        refined_translation.final_translation
                        if refined_translation
                        else initial_result["translation"]
                    ),
                    results.get("quality_assessment", {}),
                )

                mqm_analysis = MQMAnalysis(
                    total_score=mqm_result["total_score"],
                    word_count=mqm_result["word_count"],
                    errors=mqm_result.get("errors", []),
                    error_summary=mqm_result["error_summary"],
                    mqm_grade=mqm_result["mqm_grade"],
                    industry_compliance=mqm_result["industry_compliance"],
                )

                results["mqm_analysis"] = mqm_result

            # Step 6: ISO Compliance Check
            iso_compliance = None
            if request.include_iso_compliance:
                iso_result = await self._run_agent_async(
                    self.iso_standards.validate, results
                )

                iso_compliance = ISOCompliance(
                    compliant=iso_result["compliant"],
                    score=iso_result["score"],
                    compliance_areas=iso_result["compliance_areas"],
                    detailed_scores=iso_result["detailed_scores"],
                    recommendations=iso_result.get("recommendations", []),
                    iso_standard=iso_result.get("iso_standard", "ISO 17100:2015"),
                    assessment_date=iso_result.get(
                        "assessment_date", datetime.now().isoformat()
                    ),
                )

                results["iso_compliance"] = iso_result

            processing_time = time.time() - start_time

            return TranslationResponse(
                request_id=request_id,
                source_text=request.source_text,
                target_language=request.target_language,
                initial_translation=initial_translation,
                cultural_analysis=cultural_analysis,
                refined_translation=refined_translation,
                quality_assessment=quality_assessment,
                mqm_analysis=mqm_analysis,
                iso_compliance=iso_compliance,
                processing_time=processing_time,
                timestamp=datetime.now().isoformat(),
            )

        except Exception as e:
            processing_time = time.time() - start_time
            raise Exception(f"Translation failed: {str(e)}")

    async def translate_batch(
        self, requests: list[TranslationRequest]
    ) -> BatchTranslationResponse:
        """Process multiple translation requests"""
        start_time = time.time()
        batch_id = str(uuid.uuid4())

        # Process translations in parallel
        tasks = [self.translate(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Separate successful and failed results
        successful_results = []
        error_count = 0

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_count += 1
                # Create error response for failed translation
                error_response = TranslationResponse(
                    request_id=str(uuid.uuid4()),
                    source_text=requests[i].source_text,
                    target_language=requests[i].target_language,
                    initial_translation=TranslationResult(
                        translation=f"Translation failed: {str(result)}",
                        confidence=0,
                        translation_notes=["Error in translation process"],
                        difficulty_level="error",
                        key_decisions=[],
                    ),
                    processing_time=0,
                    timestamp=datetime.now().isoformat(),
                )
                successful_results.append(error_response)
            else:
                successful_results.append(result)

        total_processing_time = time.time() - start_time

        return BatchTranslationResponse(
            request_id=batch_id,
            results=successful_results,
            total_processing_time=total_processing_time,
            success_count=len(requests) - error_count,
            error_count=error_count,
            timestamp=datetime.now().isoformat(),
        )

    async def _run_agent_async(self, agent_func, *args, **kwargs):
        """Run agent function asynchronously"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, agent_func, *args, **kwargs)

    def get_supported_languages(self) -> Dict[str, Any]:
        """Get list of supported languages and their configurations"""
        from config.agent_config import LANGUAGE_CONFIGS

        return LANGUAGE_CONFIGS

    def get_health_status(self) -> Dict[str, Any]:
        """Get service health status"""
        return {
            "status": "healthy",
            "agents_initialized": all(
                [
                    self.translator is not None,
                    self.reviewer is not None,
                    self.quality_assessor is not None,
                    self.cultural_advisor is not None,
                    self.mqm_framework is not None,
                    self.iso_standards is not None,
                ]
            ),
            "supported_languages": list(self.get_supported_languages().keys()),
            "timestamp": datetime.now().isoformat(),
        }
