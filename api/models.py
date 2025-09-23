from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, validator
from enum import Enum


class LanguageCode(str, Enum):
    """Supported language codes"""

    SWEDISH = "swedish"
    DUTCH = "dutch"


class QualityGrade(str, Enum):
    """Quality grade levels"""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class SeverityLevel(str, Enum):
    """Error severity levels"""

    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


class CulturalAppropriateness(str, Enum):
    """Cultural appropriateness levels"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TargetAudienceFit(str, Enum):
    """Target audience fit levels"""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


# Request Models
class TranslationRequest(BaseModel):
    """Translation request model"""

    source_text: str = Field(
        ..., min_length=1, max_length=10000, description="Source text to translate"
    )
    target_language: LanguageCode = Field(
        default=LanguageCode.SWEDISH, description="Target language"
    )
    include_quality_analysis: bool = Field(
        default=True, description="Include quality analysis"
    )
    include_cultural_analysis: bool = Field(
        default=True, description="Include cultural analysis"
    )
    include_mqm_analysis: bool = Field(
        default=True, description="Include MQM framework analysis"
    )
    include_iso_compliance: bool = Field(
        default=True, description="Include ISO 17100:2015 compliance check"
    )

    @validator("source_text")
    def validate_source_text(cls, v):
        if not v.strip():
            raise ValueError("Source text cannot be empty")
        return v.strip()


class BatchTranslationRequest(BaseModel):
    """Batch translation request model"""

    translations: List[TranslationRequest] = Field(
        ..., min_items=1, max_items=10, description="List of translation requests"
    )
    process_parallel: bool = Field(
        default=True, description="Process translations in parallel"
    )


# Response Models
class TranslationResult(BaseModel):
    """Individual translation result"""

    translation: str = Field(..., description="Translated text")
    confidence: float = Field(
        ..., ge=0, le=100, description="Translation confidence score"
    )
    translation_notes: List[str] = Field(
        default_factory=list, description="Translation notes"
    )
    difficulty_level: Literal["easy", "medium", "hard", "error"] = Field(
        ..., description="Translation difficulty"
    )
    key_decisions: List[str] = Field(
        default_factory=list, description="Key translation decisions"
    )


class CulturalAnalysis(BaseModel):
    """Cultural analysis result"""

    cultural_appropriateness: CulturalAppropriateness = Field(
        ..., description="Cultural appropriateness level"
    )
    adaptations: List[str] = Field(
        default_factory=list, description="Cultural adaptations made"
    )
    regional_notes: List[str] = Field(
        default_factory=list, description="Regional considerations"
    )
    register_recommendations: Literal["formal", "informal", "neutral"] = Field(
        ..., description="Register recommendations"
    )
    localization_suggestions: List[str] = Field(
        default_factory=list, description="Localization suggestions"
    )
    cultural_risks: List[str] = Field(
        default_factory=list, description="Potential cultural risks"
    )
    target_audience_fit: TargetAudienceFit = Field(
        ..., description="Target audience fit"
    )


class ReviewResult(BaseModel):
    """Review and refinement result"""

    final_translation: str = Field(..., description="Final refined translation")
    review_comments: List[str] = Field(
        default_factory=list, description="Review comments"
    )
    changes_made: List[str] = Field(
        default_factory=list, description="Changes made during review"
    )
    confidence_improvement: float = Field(
        ..., ge=0, le=100, description="Confidence improvement percentage"
    )
    quality_grade: QualityGrade = Field(..., description="Quality grade")


class QualityScores(BaseModel):
    """Detailed quality scores"""

    fluency: float = Field(..., ge=0, le=100, description="Fluency score")
    grammar: float = Field(..., ge=0, le=100, description="Grammar score")
    accuracy: float = Field(..., ge=0, le=100, description="Accuracy score")
    naturalness: float = Field(..., ge=0, le=100, description="Naturalness score")
    vocabulary: float = Field(..., ge=0, le=100, description="Vocabulary score")
    colloquial_usage: float = Field(
        ..., ge=0, le=100, description="Colloquial usage score"
    )


class QualityAssessment(BaseModel):
    """Quality assessment result"""

    overall_score: float = Field(..., ge=0, le=100, description="Overall quality score")
    detailed_scores: QualityScores = Field(..., description="Detailed quality scores")
    assessment_notes: List[str] = Field(
        default_factory=list, description="Assessment notes"
    )
    strengths: List[str] = Field(
        default_factory=list, description="Translation strengths"
    )
    areas_for_improvement: List[str] = Field(
        default_factory=list, description="Areas for improvement"
    )
    industry_benchmark_met: bool = Field(
        ..., description="Whether industry benchmark is met"
    )
    error_count: int = Field(..., ge=0, description="Total error count")
    errors_per_1000_words: float = Field(..., ge=0, description="Errors per 1000 words")


class MQMError(BaseModel):
    """MQM error details"""

    category: Literal["accuracy", "fluency", "style", "terminology"] = Field(
        ..., description="Error category"
    )
    subcategory: str = Field(..., description="Error subcategory")
    severity: SeverityLevel = Field(..., description="Error severity")
    description: str = Field(..., description="Error description")
    penalty: float = Field(..., description="Penalty points")
    location: str = Field(..., description="Error location in text")


class ErrorSummary(BaseModel):
    """Error summary statistics"""

    total_errors: int = Field(..., ge=0, description="Total error count")
    accuracy_errors: int = Field(..., ge=0, description="Accuracy error count")
    fluency_errors: int = Field(..., ge=0, description="Fluency error count")
    style_errors: int = Field(..., ge=0, description="Style error count")
    terminology_errors: int = Field(..., ge=0, description="Terminology error count")


class MQMAnalysis(BaseModel):
    """MQM framework analysis result"""

    total_score: float = Field(..., ge=0, le=100, description="Total MQM score")
    word_count: int = Field(..., ge=0, description="Word count")
    errors: List[MQMError] = Field(default_factory=list, description="Detected errors")
    error_summary: ErrorSummary = Field(..., description="Error summary")
    mqm_grade: QualityGrade = Field(..., description="MQM grade")
    industry_compliance: bool = Field(..., description="Industry compliance status")


class ISOCompliance(BaseModel):
    """ISO 17100:2015 compliance result"""

    compliant: bool = Field(..., description="Overall compliance status")
    score: float = Field(..., ge=0, le=100, description="Compliance score")
    compliance_areas: Dict[str, bool] = Field(..., description="Compliance by area")
    detailed_scores: Dict[str, float] = Field(
        ..., description="Detailed compliance scores"
    )
    recommendations: List[str] = Field(
        default_factory=list, description="Compliance recommendations"
    )
    iso_standard: str = Field(
        default="ISO 17100:2015", description="ISO standard version"
    )
    assessment_date: str = Field(..., description="Assessment date")


class FinalTranslationResult(BaseModel):
    """Final translation result from the 7th agent"""

    final_translation: str = Field(..., description="Ultimate refined translation")
    quality_improvements: List[str] = Field(
        default_factory=list, description="Quality improvements made"
    )
    errors_fixed: List[str] = Field(
        default_factory=list, description="Errors that were fixed"
    )
    iso_enhancements: List[str] = Field(
        default_factory=list, description="ISO compliance enhancements"
    )
    confidence_level: Literal["excellent", "very_good", "good", "fair", "poor"] = Field(
        ..., description="Final confidence level"
    )
    translation_grade: Literal[
        "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"
    ] = Field(..., description="Final translation grade")
    professional_ready: bool = Field(
        ..., description="Whether translation is professional ready"
    )
    final_notes: List[str] = Field(
        default_factory=list, description="Final translation notes"
    )


class TranslationResponse(BaseModel):
    """Complete translation response"""

    request_id: str = Field(..., description="Unique request identifier")
    source_text: str = Field(..., description="Original source text")
    target_language: LanguageCode = Field(..., description="Target language")
    initial_translation: TranslationResult = Field(
        ..., description="Initial translation result"
    )
    cultural_analysis: Optional[CulturalAnalysis] = Field(
        None, description="Cultural analysis result"
    )
    refined_translation: Optional[ReviewResult] = Field(
        None, description="Refined translation result"
    )
    quality_assessment: Optional[QualityAssessment] = Field(
        None, description="Quality assessment result"
    )
    mqm_analysis: Optional[MQMAnalysis] = Field(None, description="MQM analysis result")
    iso_compliance: Optional[ISOCompliance] = Field(
        None, description="ISO compliance result"
    )
    final_translation: Optional[FinalTranslationResult] = Field(
        None, description="Final ultimate translation result from 7th agent"
    )
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: str = Field(..., description="Processing timestamp")


class BatchTranslationResponse(BaseModel):
    """Batch translation response"""

    request_id: str = Field(..., description="Batch request identifier")
    results: List[TranslationResponse] = Field(
        ..., description="Individual translation results"
    )
    total_processing_time: float = Field(
        ..., description="Total processing time in seconds"
    )
    success_count: int = Field(
        ..., ge=0, description="Number of successful translations"
    )
    error_count: int = Field(..., ge=0, description="Number of failed translations")
    timestamp: str = Field(..., description="Processing timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )
    request_id: Optional[str] = Field(
        None, description="Request identifier if available"
    )


class HealthResponse(BaseModel):
    """Health check response"""

    status: Literal["healthy", "degraded", "unhealthy"] = Field(
        ..., description="Service status"
    )
    version: str = Field(..., description="Service version")
    timestamp: str = Field(..., description="Check timestamp")
    uptime: float = Field(..., description="Service uptime in seconds")
    dependencies: Dict[str, bool] = Field(..., description="Dependency status")


# Individual Agent Request/Response Models
class QualityAssessmentRequest(BaseModel):
    """Request for quality assessment only"""

    source_text: str = Field(
        ..., min_length=1, max_length=10000, description="Source text"
    )
    final_translation: str = Field(
        ..., min_length=1, max_length=10000, description="Final translation to assess"
    )
    target_language: LanguageCode = Field(..., description="Target language")


class MQMAnalysisRequest(BaseModel):
    """Request for MQM analysis only"""

    source_text: str = Field(
        ..., min_length=1, max_length=10000, description="Source text"
    )
    final_translation: str = Field(
        ..., min_length=1, max_length=10000, description="Final translation to analyze"
    )
    quality_assessment: Optional[QualityAssessment] = Field(
        None, description="Optional quality assessment context"
    )


class ISOComplianceRequest(BaseModel):
    """Request for ISO compliance check only"""

    source_text: str = Field(
        ..., min_length=1, max_length=10000, description="Source text"
    )
    final_translation: str = Field(
        ..., min_length=1, max_length=10000, description="Final translation"
    )
    target_language: LanguageCode = Field(..., description="Target language")
    quality_assessment: Optional[QualityAssessment] = Field(
        None, description="Optional quality assessment"
    )
    cultural_analysis: Optional[CulturalAnalysis] = Field(
        None, description="Optional cultural analysis"
    )
    mqm_analysis: Optional[MQMAnalysis] = Field(
        None, description="Optional MQM analysis"
    )


class CombinedAnalysisRequest(BaseModel):
    """Request for combined quality analysis (third-party endpoint)"""

    source_text: str = Field(
        ..., min_length=1, max_length=10000, description="Source text"
    )
    final_translation: str = Field(
        ..., min_length=1, max_length=10000, description="Final translation"
    )
    target_language: LanguageCode = Field(..., description="Target language")


class CombinedAnalysisResponse(BaseModel):
    """Response for combined quality analysis"""

    request_id: str = Field(..., description="Unique request identifier")
    source_text: str = Field(..., description="Source text")
    target_language: LanguageCode = Field(..., description="Target language")
    final_translation: str = Field(..., description="Final translation")
    quality_assessment: QualityAssessment = Field(
        ..., description="Quality assessment result"
    )
    mqm_analysis: MQMAnalysis = Field(..., description="MQM analysis result")
    iso_compliance: ISOCompliance = Field(..., description="ISO compliance result")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: str = Field(..., description="Processing timestamp")


# Final Translator Agent Models


class EmailTranslationRequest(BaseModel):
    """Request model for translating email components"""

    subject: str = Field(..., description="Email subject")
    subject_prefix: str = Field(..., description="Email subject prefix")
    preheader: str = Field(..., description="Email preheader")
    preheader_prefix: str = Field(..., description="Email preheader prefix")
    opening: str = Field(..., description="Email opening text")
    closing: str = Field(..., description="Email closing text")
    output_language: str = Field(
        ..., description="Target language (e.g., 'swedish', 'dutch')"
    )
    market: str = Field(..., description="Market identifier")


class EmailTranslationResponse(BaseModel):
    """Response model for email component translations"""

    subject: str = Field(..., description="Translated email subject")
    subject_prefix: str = Field(..., description="Translated subject prefix")
    preheader: str = Field(..., description="Translated preheader")
    preheader_prefix: str = Field(..., description="Translated preheader prefix")
    opening: str = Field(..., description="Translated opening text")
    closing: str = Field(..., description="Translated closing text")
