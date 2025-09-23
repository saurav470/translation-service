"""
Quality assessment endpoints
"""

import time
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from api.models import (
    QualityAssessment,
    MQMAnalysis,
    ISOCompliance,
    QualityAssessmentRequest,
    MQMAnalysisRequest,
    ISOComplianceRequest,
    CombinedAnalysisRequest,
    CombinedAnalysisResponse,
)
from core.translation_service import TranslationService
from core.config import settings

router = APIRouter()


def get_translation_service() -> TranslationService:
    """Dependency to get translation service instance"""
    from main import translation_service

    if translation_service is None:
        raise HTTPException(status_code=503, detail="Translation service not available")
    return translation_service


@router.get("/quality/standards")
async def get_quality_standards():
    """
    Get quality standards and thresholds
    """
    return {
        "quality_thresholds": {
            "minimum_quality": settings.MIN_QUALITY_SCORE,
            "professional_quality": settings.PROFESSIONAL_QUALITY_SCORE,
            "publication_quality": settings.PUBLICATION_QUALITY_SCORE,
        },
        "supported_frameworks": [
            "MQM (Multidimensional Quality Metrics)",
            "ISO 17100:2015 Translation Services",
            "Custom Quality Assessment",
        ],
        "assessment_criteria": {
            "fluency": "Natural language flow and readability",
            "grammar": "Correct morphology, syntax, and punctuation",
            "accuracy": "Faithful conveyance of source meaning",
            "naturalness": "Sounds like native language",
            "vocabulary": "Appropriate word choices and terminology",
            "colloquial_usage": "Natural expressions and cultural adaptation",
        },
    }


@router.get("/quality/mqm/info")
async def get_mqm_info():
    """
    Get MQM framework information
    """
    return {
        "framework": "Multidimensional Quality Metrics (MQM)",
        "description": "Industry-standard framework for translation quality evaluation",
        "error_categories": {
            "accuracy": ["mistranslation", "omission", "addition", "untranslated"],
            "fluency": ["grammar", "spelling", "punctuation", "register"],
            "style": ["awkward", "unnatural", "inconsistent_style"],
            "terminology": ["inconsistent_term", "wrong_term"],
        },
        "severity_levels": ["minor", "major", "critical"],
        "grading_scale": {
            "A": "90-100% (Excellent)",
            "B": "80-89% (Good)",
            "C": "70-79% (Acceptable)",
            "D": "60-69% (Poor)",
            "F": "Below 60% (Failing)",
        },
    }


@router.get("/quality/iso/info")
async def get_iso_info():
    """
    Get ISO 17100:2015 information
    """
    return {
        "standard": "ISO 17100:2015 Translation Services Requirements",
        "description": "International standard for translation services",
        "compliance_areas": {
            "translation_competence": "Linguistic, cultural, and domain expertise",
            "quality_assurance": "Review processes and error detection",
            "project_management": "Process documentation and resource allocation",
            "technical_resources": "Tools usage and terminology management",
            "client_requirements": "Requirements analysis and target audience fit",
        },
        "compliance_threshold": 85,
        "benefits": [
            "Industry recognition",
            "Quality assurance",
            "Professional credibility",
            "Client confidence",
        ],
    }


@router.get("/quality/metrics/explanation")
async def get_quality_metrics_explanation():
    """
    Get detailed explanation of quality metrics
    """
    return {
        "overall_score": {
            "description": "Weighted average of all quality dimensions",
            "calculation": "Sum of (dimension_score * weight) for all dimensions",
            "range": "0-100%",
            "thresholds": {
                "excellent": "95-100%",
                "professional": "85-94%",
                "acceptable": "70-84%",
                "poor": "Below 70%",
            },
        },
        "detailed_scores": {
            "fluency": {
                "description": "Natural language flow and readability",
                "weight": 0.20,
                "evaluation": "Assesses how naturally the translation reads in the target language",
            },
            "grammar": {
                "description": "Correct morphology, syntax, and punctuation",
                "weight": 0.20,
                "evaluation": "Checks for grammatical errors and proper language structure",
            },
            "accuracy": {
                "description": "Faithful conveyance of source meaning",
                "weight": 0.25,
                "evaluation": "Ensures the translation preserves the original meaning",
            },
            "naturalness": {
                "description": "Sounds like native language",
                "weight": 0.15,
                "evaluation": "Measures how native-like the translation sounds",
            },
            "vocabulary": {
                "description": "Appropriate word choices and terminology",
                "weight": 0.10,
                "evaluation": "Assesses word choice appropriateness and consistency",
            },
            "colloquial_usage": {
                "description": "Natural expressions and cultural adaptation",
                "weight": 0.10,
                "evaluation": "Evaluates use of natural expressions and cultural context",
            },
        },
        "error_metrics": {
            "error_count": "Total number of errors detected",
            "errors_per_1000_words": "Error density metric for quality assessment",
        },
    }


# Individual Agent Endpoints


@router.post("/quality/assess", response_model=QualityAssessment)
async def assess_quality(
    request: QualityAssessmentRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Assess translation quality using the Quality Assessor agent only

    This endpoint provides detailed quality analysis including:
    - Overall quality score (0-100)
    - Detailed scores for fluency, grammar, accuracy, naturalness, vocabulary, colloquial usage
    - Industry benchmark compliance
    - Error metrics and improvement recommendations
    """
    try:
        # Validate text length
        if (
            len(request.source_text) > settings.MAX_TEXT_LENGTH
            or len(request.final_translation) > settings.MAX_TEXT_LENGTH
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Maximum length is {settings.MAX_TEXT_LENGTH} characters",
            )

        # Validate target language
        if request.target_language.value not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported target language. Supported languages: {settings.SUPPORTED_LANGUAGES}",
            )

        # Run quality assessment
        start_time = time.time()
        quality_result = await service._run_agent_async(
            service.quality_assessor.assess,
            request.source_text,
            request.final_translation,
            request.target_language.value,
        )

        processing_time = time.time() - start_time

        return QualityAssessment(
            overall_score=quality_result["overall_score"],
            detailed_scores=quality_result["detailed_scores"],
            assessment_notes=quality_result.get("assessment_notes", []),
            strengths=quality_result.get("strengths", []),
            areas_for_improvement=quality_result.get("areas_for_improvement", []),
            industry_benchmark_met=quality_result.get("industry_benchmark_met", False),
            error_count=quality_result.get("error_count", 0),
            errors_per_1000_words=quality_result.get("errors_per_1000_words", 0),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Quality assessment failed: {str(e)}"
        )


@router.post("/quality/mqm", response_model=MQMAnalysis)
async def analyze_mqm(
    request: MQMAnalysisRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Analyze translation using MQM (Multidimensional Quality Metrics) framework only

    This endpoint provides comprehensive error analysis including:
    - MQM total score and grade
    - Detailed error categorization (accuracy, fluency, style, terminology)
    - Error severity levels (minor, major, critical)
    - Industry compliance status
    - Error summary statistics
    """
    try:
        # Validate text length
        if (
            len(request.source_text) > settings.MAX_TEXT_LENGTH
            or len(request.final_translation) > settings.MAX_TEXT_LENGTH
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Maximum length is {settings.MAX_TEXT_LENGTH} characters",
            )

        # Run MQM analysis
        start_time = time.time()
        mqm_result = await service._run_agent_async(
            service.mqm_framework.analyze,
            request.source_text,
            request.final_translation,
            request.quality_assessment.dict() if request.quality_assessment else {},
        )

        processing_time = time.time() - start_time

        return MQMAnalysis(
            total_score=mqm_result["total_score"],
            word_count=mqm_result["word_count"],
            errors=mqm_result.get("errors", []),
            error_summary=mqm_result["error_summary"],
            mqm_grade=mqm_result["mqm_grade"],
            industry_compliance=mqm_result["industry_compliance"],
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MQM analysis failed: {str(e)}")


@router.post("/quality/iso", response_model=ISOCompliance)
async def check_iso_compliance(
    request: ISOComplianceRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Check ISO 17100:2015 compliance for translation process only

    This endpoint validates compliance with international translation standards including:
    - Translation competence evaluation
    - Quality assurance process validation
    - Project management standards
    - Technical resource utilization
    - Client requirements fulfillment
    """
    try:
        # Validate text length
        if (
            len(request.source_text) > settings.MAX_TEXT_LENGTH
            or len(request.final_translation) > settings.MAX_TEXT_LENGTH
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Maximum length is {settings.MAX_TEXT_LENGTH} characters",
            )

        # Validate target language
        if request.target_language.value not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported target language. Supported languages: {settings.SUPPORTED_LANGUAGES}",
            )

        # Prepare results for ISO validation
        results = {
            "source_text": request.source_text,
            "final_translation": request.final_translation,
            "target_language": request.target_language.value,
        }

        if request.quality_assessment:
            results["quality_assessment"] = request.quality_assessment.dict()
        if request.cultural_analysis:
            results["cultural_analysis"] = request.cultural_analysis.dict()
        if request.mqm_analysis:
            results["mqm_analysis"] = request.mqm_analysis.dict()

        # Run ISO compliance check
        start_time = time.time()
        iso_result = await service._run_agent_async(
            service.iso_standards.validate, results
        )

        processing_time = time.time() - start_time

        return ISOCompliance(
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

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ISO compliance check failed: {str(e)}"
        )


@router.post("/quality/combined", response_model=CombinedAnalysisResponse)
async def combined_quality_analysis(
    request: CombinedAnalysisRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Combined quality analysis endpoint for third-party use

    This endpoint provides all three quality analyses in one request:
    - Quality Assessment (detailed scoring)
    - MQM Analysis (error analysis)
    - ISO Compliance (professional standards)

    Perfect for third-party integrations that need comprehensive quality evaluation.
    """
    try:
        # Validate text length
        if (
            len(request.source_text) > settings.MAX_TEXT_LENGTH
            or len(request.final_translation) > settings.MAX_TEXT_LENGTH
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Text too long. Maximum length is {settings.MAX_TEXT_LENGTH} characters",
            )

        # Validate target language
        if request.target_language.value not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported target language. Supported languages: {settings.SUPPORTED_LANGUAGES}",
            )

        start_time = time.time()
        request_id = str(uuid.uuid4())

        # Run all three analyses in parallel
        import asyncio

        # Quality Assessment
        quality_task = service._run_agent_async(
            service.quality_assessor.assess,
            request.source_text,
            request.final_translation,
            request.target_language.value,
        )

        # MQM Analysis (needs quality assessment result)
        quality_result = await quality_task
        mqm_task = service._run_agent_async(
            service.mqm_framework.analyze,
            request.source_text,
            request.final_translation,
            quality_result,
        )

        # ISO Compliance (needs all results)
        mqm_result = await mqm_task
        results = {
            "source_text": request.source_text,
            "final_translation": request.final_translation,
            "target_language": request.target_language.value,
            "quality_assessment": quality_result,
            "mqm_analysis": mqm_result,
        }

        iso_task = service._run_agent_async(service.iso_standards.validate, results)

        iso_result = await iso_task
        processing_time = time.time() - start_time

        return CombinedAnalysisResponse(
            request_id=request_id,
            source_text=request.source_text,
            target_language=request.target_language,
            final_translation=request.final_translation,
            quality_assessment=QualityAssessment(
                overall_score=quality_result["overall_score"],
                detailed_scores=quality_result["detailed_scores"],
                assessment_notes=quality_result.get("assessment_notes", []),
                strengths=quality_result.get("strengths", []),
                areas_for_improvement=quality_result.get("areas_for_improvement", []),
                industry_benchmark_met=quality_result.get(
                    "industry_benchmark_met", False
                ),
                error_count=quality_result.get("error_count", 0),
                errors_per_1000_words=quality_result.get("errors_per_1000_words", 0),
            ),
            mqm_analysis=MQMAnalysis(
                total_score=mqm_result["total_score"],
                word_count=mqm_result["word_count"],
                errors=mqm_result.get("errors", []),
                error_summary=mqm_result["error_summary"],
                mqm_grade=mqm_result["mqm_grade"],
                industry_compliance=mqm_result["industry_compliance"],
            ),
            iso_compliance=ISOCompliance(
                compliant=iso_result["compliant"],
                score=iso_result["score"],
                compliance_areas=iso_result["compliance_areas"],
                detailed_scores=iso_result["detailed_scores"],
                recommendations=iso_result.get("recommendations", []),
                iso_standard=iso_result.get("iso_standard", "ISO 17100:2015"),
                assessment_date=iso_result.get(
                    "assessment_date", datetime.now().isoformat()
                ),
            ),
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Combined quality analysis failed: {str(e)}"
        )
