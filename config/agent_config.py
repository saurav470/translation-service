"""
Configuration settings for the multi-agent translation system
"""

# Agent Model Configuration
AGENT_MODELS = {
    "translator": "gpt-5",  # Primary translation agent
    "reviewer": "gpt-5",    # Review and refinement agent  
    "quality_assessor": "gpt-5",  # Quality assessment agent
    "cultural_advisor": "gpt-5"   # Cultural adaptation agent
}

# Quality Thresholds
QUALITY_THRESHOLDS = {
    "professional_grade": 85,      # Minimum for professional use
    "publication_ready": 95,       # Publication quality threshold
    "iso_compliance": 85,          # ISO 17100:2015 compliance
    "mqm_passing": 80,             # MQM framework passing score
    "errors_per_1000_words": 10    # Maximum errors per 1000 words
}

# MQM Framework Configuration
MQM_CONFIG = {
    "error_weights": {
        "critical": -25,
        "major": -5, 
        "minor": -1
    },
    "categories": [
        "accuracy",
        "fluency", 
        "style",
        "terminology"
    ]
}

# Multi-Language Configuration
LANGUAGE_CONFIGS = {
    "swedish": {
        "name": "Swedish",
        "code": "sv",
        "flag": "🇸🇪",
        "regions": ["Stockholm", "Göteborg", "Malmö", "Northern Sweden"],
        "register_levels": ["formal", "informal", "neutral"],
        "cultural_aspects": [
            "lagom",
            "jantelagen", 
            "allemansrätten",
            "consensus_culture",
            "environmental_consciousness"
        ]
    },
    "dutch": {
        "name": "Dutch",
        "code": "nl", 
        "flag": "🇳🇱",
        "regions": ["Amsterdam", "Rotterdam", "Utrecht", "The Hague", "Flanders"],
        "register_levels": ["formal", "informal", "neutral"],
        "cultural_aspects": [
            "directness",
            "pragmatism",
            "tolerance", 
            "consensus_building",
            "work_life_balance"
        ]
    }
}

# Default language (for backward compatibility)
SWEDISH_CONFIG = LANGUAGE_CONFIGS["swedish"]

# Translation Process Settings
PROCESS_CONFIG = {
    "enable_parallel_processing": True,
    "max_retry_attempts": 3,
    "timeout_seconds": 120,
    "enable_caching": True
}

# Quality Assessment Weights
ASSESSMENT_WEIGHTS = {
    "fluency": 0.20,
    "grammar": 0.20,
    "accuracy": 0.25,
    "naturalness": 0.15,
    "vocabulary": 0.10,
    "colloquial_usage": 0.10
}

# Industry Standards Compliance
ISO_17100_REQUIREMENTS = {
    "translator_competence": 0.25,
    "quality_assurance": 0.25,
    "project_management": 0.20,
    "technical_resources": 0.15,
    "client_requirements": 0.15
}
