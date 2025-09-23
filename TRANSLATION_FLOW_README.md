# Translation Multi-Agent Flow

## Overview

The translation system uses a **6-agent pipeline** to provide professional-grade translations with comprehensive quality assurance, cultural adaptation, and industry compliance validation.

## Agent Flow Sequence

```
Source Text → Translator → Cultural Advisor → Reviewer → Quality Assessor → MQM Framework → ISO Standards → Final Response
```

## Agent Details

### 1. **Translator Agent**

**Purpose**: Initial high-quality translation

- **Input Parameters**:
  - `source_text`: Original English text
  - `target_language`: "swedish" or "dutch"
- **Key Considerations**:
  - Native linguistic patterns
  - Grammar and syntax rules
  - Cultural nuances
  - Technical terminology
  - V2 word order (Swedish) / SOV word order (Dutch)
  - Definite articles (-en, -et, -na for Swedish / de/het for Dutch)
  - Formal vs informal register
- **Output**: Translation with confidence score, notes, difficulty level, key decisions

### 2. **Cultural Advisor**

**Purpose**: Cultural context analysis and localization recommendations

- **Input Parameters**:
  - `source_text`: Original English text
  - `initial_translation`: Translation from Translator Agent
  - `target_language`: Target language code
- **Key Considerations**:
  - **Swedish**: Lagom philosophy, Jantelagen, Allemansrätten, workplace equality
  - **Dutch**: Directness, pragmatism, tolerance, consensus building (poldermodel)
  - Regional variations (Stockholm/Göteborg vs Amsterdam/Rotterdam)
  - Business vs consumer context
  - Age and generational differences
  - Cultural sensitivities and risks
- **Output**: Cultural appropriateness, adaptations, regional notes, register recommendations

### 3. **Reviewer Agent**

**Purpose**: Linguistic refinement and error correction

- **Input Parameters**:
  - `source_text`: Original English text
  - `initial_translation`: Translation from Translator Agent
  - `cultural_analysis`: Results from Cultural Advisor
  - `target_language`: Target language code
- **Key Considerations**:
  - Grammatical accuracy (morphology, syntax, agreement)
  - Lexical choices and terminology consistency
  - Stylistic appropriateness and register
  - Cultural adaptation and localization
  - Natural flow and readability
  - Completeness and fidelity to source meaning
  - **Critical**: NO addition of disclaimers or content not in original
- **Output**: Final refined translation, review comments, changes made, quality grade

### 4. **Quality Assessor**

**Purpose**: Comprehensive quality evaluation using industry standards

- **Input Parameters**:
  - `source_text`: Original English text
  - `final_translation`: Refined translation from Reviewer Agent
  - `target_language`: Target language code
- **Key Considerations**:
  - **Fluency (0-100)**: Natural language flow, readability
  - **Grammar (0-100)**: Correct morphology, syntax, agreement, punctuation
  - **Accuracy (0-100)**: Faithful meaning preservation, no omissions/additions
  - **Naturalness (0-100)**: Sounds like native speaker, not translated text
  - **Vocabulary (0-100)**: Appropriate word choices, terminology, register
  - **Colloquial Usage (0-100)**: Natural expressions, idioms, cultural adaptation
- **Industry Benchmarks**:
  - 95-100%: Exceptional (publication ready)
  - 85-94%: Professional (meets industry standards)
  - 70-84%: Acceptable (minor revisions needed)
  - Below 70%: Poor (major revisions required)
- **Output**: Overall score, detailed scores, strengths, areas for improvement, error metrics

### 5. **MQM Framework**

**Purpose**: Multidimensional Quality Metrics analysis

- **Input Parameters**:
  - `source_text`: Original English text
  - `final_translation`: Final translation
  - `quality_assessment`: Results from Quality Assessor
- **Key Considerations**:
  - **Accuracy errors**: mistranslation, omission, addition
  - **Fluency errors**: grammar, spelling, punctuation, register
  - **Style errors**: awkward, unnatural, inconsistent
  - **Terminology errors**: incorrect technical terms
  - Error categorization by severity (minor, major, critical)
  - Errors per 1000 words metric
- **Output**: Total MQM score, error details, error summary, industry compliance status

### 6. **ISO Standards**

**Purpose**: ISO 17100:2015 compliance validation

- **Input Parameters**:
  - All previous agent results (complete translation pipeline data)
- **Key Considerations**:
  - **Translation process compliance**: Proper translation methodology
  - **Review process compliance**: Quality assurance procedures
  - **Competence requirements**: Translator qualifications
  - **Project management**: Process documentation
  - **Quality assurance**: Error detection and correction
  - **Client communication**: Professional standards
- **Output**: Compliance status, detailed scores by area, recommendations

## Request Configuration

Control which agents run using these flags:

```json
{
  "source_text": "Your text here",
  "target_language": "swedish",
  "include_quality_analysis": true, // Enables Reviewer + Quality Assessor
  "include_cultural_analysis": true, // Enables Cultural Advisor
  "include_mqm_analysis": true, // Enables MQM Framework
  "include_iso_compliance": true // Enables ISO Standards
}
```

## Response Structure

The system returns a comprehensive response containing:

- **Initial Translation**: Basic translation result
- **Cultural Analysis**: Cultural appropriateness and localization insights
- **Refined Translation**: Polished final translation
- **Quality Assessment**: Detailed quality scores and metrics
- **MQM Analysis**: Error analysis and industry compliance
- **ISO Compliance**: Professional standards validation
- **Processing Time**: Performance metrics
- **Metadata**: Request ID, timestamps, etc.

## Key Features

- **Sequential Processing**: Each agent builds upon previous results
- **Error Handling**: System continues even if individual agents fail
- **Async Processing**: Optimized for performance
- **Industry Standards**: MQM and ISO compliance ensure professional quality
- **Cultural Adaptation**: Ensures appropriate localization
- **Comprehensive Analysis**: Multiple quality perspectives


