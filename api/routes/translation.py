"""
Translation endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from api.models import (
    TranslationRequest,
    TranslationResponse,
    BatchTranslationRequest,
    BatchTranslationResponse,
    ErrorResponse,
    LanguageCode,
    EmailTranslationRequest,
    EmailTranslationResponse,
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


@router.post("/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Translate text using the multi-agent translation pipeline

    This endpoint processes text through multiple AI agents:
    - Translator Agent: Initial high-quality translation
    - Cultural Advisor: Cultural context and localization
    - Review Agent: Linguistic refinement and error correction
    - Quality Assessor: Comprehensive quality evaluation
    - MQM Framework: Multidimensional quality metrics
    - ISO Standards: ISO 17100:2015 compliance validation
    - Final Translator Agent: Ultimate translation refinement based on all analyses
    """
    try:
        # Validate text length
        if len(request.source_text) > settings.MAX_TEXT_LENGTH:
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

        # Process translation
        result = await service.translate(request)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@router.post("/translate/email", response_model=EmailTranslationResponse)
async def translate_email(
    request: EmailTranslationRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Translate individual email fields and return only those translated fields.
    """
    try:
        # Map string language to existing enum if possible; otherwise, raise.
        lang_str = request.output_language.strip().lower()
        if lang_str not in settings.SUPPORTED_LANGUAGES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported target language. Supported languages: {settings.SUPPORTED_LANGUAGES}",
            )
        try:
            target_lang = LanguageCode(lang_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid language code")

        # Helper to translate a single string using minimal pipeline
        async def translate_text_only(text: str) -> str:
            result = await service.translate(
                TranslationRequest(
                    source_text=text,
                    target_language=target_lang,
                    include_quality_analysis=False,
                    include_cultural_analysis=False,
                    include_mqm_analysis=False,
                    include_iso_compliance=False,
                )
            )
            return (
                result.refined_translation.final_translation
                if result.refined_translation
                else result.initial_translation.translation
            )

        subject = await translate_text_only(request.subject)
        subject_prefix = await translate_text_only(request.subject_prefix)
        preheader = await translate_text_only(request.preheader)
        preheader_prefix = await translate_text_only(request.preheader_prefix)
        opening = await translate_text_only(request.opening)
        closing = await translate_text_only(request.closing)

        return EmailTranslationResponse(
            subject=subject,
            subject_prefix=subject_prefix,
            preheader=preheader,
            preheader_prefix=preheader_prefix,
            opening=opening,
            closing=closing,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Email translation failed: {str(e)}"
        )


@router.post("/translate/batch", response_model=BatchTranslationResponse)
async def translate_batch(
    request: BatchTranslationRequest,
    service: TranslationService = Depends(get_translation_service),
):
    """
    Translate multiple texts in batch

    Process multiple translation requests efficiently with optional parallel processing.
    """
    try:
        # Validate batch size
        if len(request.translations) > 10:
            raise HTTPException(
                status_code=400,
                detail="Batch size too large. Maximum 10 translations per batch",
            )

        # Validate each request
        for i, translation_request in enumerate(request.translations):
            if len(translation_request.source_text) > settings.MAX_TEXT_LENGTH:
                raise HTTPException(
                    status_code=400,
                    detail=f"Text too long in request {i+1}. Maximum length is {settings.MAX_TEXT_LENGTH} characters",
                )

            if (
                translation_request.target_language.value
                not in settings.SUPPORTED_LANGUAGES
            ):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported target language in request {i+1}. Supported languages: {settings.SUPPORTED_LANGUAGES}",
                )

        # Process batch translation
        result = await service.translate_batch(request.translations)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Batch translation failed: {str(e)}"
        )


@router.get("/languages")
async def get_supported_languages(
    service: TranslationService = Depends(get_translation_service),
):
    """
    Get list of supported languages and their configurations
    """
    try:
        languages = service.get_supported_languages()
        return {
            "supported_languages": languages,
            "default_language": settings.DEFAULT_LANGUAGE,
            "max_text_length": settings.MAX_TEXT_LENGTH,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get supported languages: {str(e)}"
        )


@router.get("/translate/{request_id}")
async def get_translation_status(request_id: str):
    """
    Get translation status by request ID

    Note: This is a placeholder for future implementation with persistent storage
    """
    return {
        "message": "Translation status tracking not yet implemented",
        "request_id": request_id,
        "status": "completed",
    }
