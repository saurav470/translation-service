import json

class ISOStandards:
    """ISO 17100:2015 Translation Services Requirements compliance validator"""
    
    def __init__(self):
        # ISO 17100:2015 compliance criteria
        self.iso_requirements = {
            "translation_competence": {
                "weight": 0.25,
                "criteria": ["linguistic_competence", "cultural_competence", "domain_expertise"]
            },
            "quality_assurance": {
                "weight": 0.25, 
                "criteria": ["review_process", "error_detection", "quality_metrics"]
            },
            "project_management": {
                "weight": 0.20,
                "criteria": ["process_documentation", "resource_allocation", "delivery_standards"]
            },
            "technical_resources": {
                "weight": 0.15,
                "criteria": ["tools_usage", "terminology_management", "consistency_checks"]
            },
            "client_requirements": {
                "weight": 0.15,
                "criteria": ["requirements_analysis", "target_audience", "purpose_fitness"]
            }
        }
    
    def validate(self, translation_results):
        """Validate translation process against ISO 17100:2015 standards"""
        
        compliance_scores = {}
        total_weighted_score = 0
        
        # Evaluate Translation Competence
        translation_competence = self._evaluate_translation_competence(translation_results)
        compliance_scores["Translation Competence"] = translation_competence
        total_weighted_score += translation_competence * self.iso_requirements["translation_competence"]["weight"]
        
        # Evaluate Quality Assurance
        quality_assurance = self._evaluate_quality_assurance(translation_results)
        compliance_scores["Quality Assurance"] = quality_assurance
        total_weighted_score += quality_assurance * self.iso_requirements["quality_assurance"]["weight"]
        
        # Evaluate Project Management
        project_management = self._evaluate_project_management(translation_results)
        compliance_scores["Project Management"] = project_management
        total_weighted_score += project_management * self.iso_requirements["project_management"]["weight"]
        
        # Evaluate Technical Resources
        technical_resources = self._evaluate_technical_resources(translation_results)
        compliance_scores["Technical Resources"] = technical_resources
        total_weighted_score += technical_resources * self.iso_requirements["technical_resources"]["weight"]
        
        # Evaluate Client Requirements
        client_requirements = self._evaluate_client_requirements(translation_results)
        compliance_scores["Client Requirements"] = client_requirements  
        total_weighted_score += client_requirements * self.iso_requirements["client_requirements"]["weight"]
        
        # Calculate overall compliance
        overall_score = total_weighted_score * 100
        is_compliant = overall_score >= 85  # Industry standard for ISO compliance
        
        # Generate compliance report
        compliance_areas = {}
        recommendations = []
        
        for area, score in compliance_scores.items():
            compliance_areas[area] = score >= 0.85
            if score < 0.85:
                recommendations.append(f"Improve {area.lower()} to meet ISO 17100:2015 standards")
        
        return {
            "compliant": is_compliant,
            "score": overall_score,
            "compliance_areas": compliance_areas,
            "detailed_scores": compliance_scores,
            "recommendations": recommendations,
            "iso_standard": "ISO 17100:2015",
            "assessment_date": "2025-09-20"
        }
    
    def _evaluate_translation_competence(self, results):
        """Evaluate translator competence based on output quality"""
        competence_score = 0
        
        # Linguistic competence (40%)
        if results.get('quality_assessment', {}).get('detailed_scores', {}).get('grammar', 0) >= 85:
            competence_score += 0.4
        
        # Cultural competence (35%)
        cultural_analysis = results.get('cultural_analysis', {})
        if cultural_analysis.get('cultural_appropriateness') in ['high', 'medium']:
            competence_score += 0.35
        
        # Domain expertise (25%)
        overall_quality = results.get('quality_assessment', {}).get('overall_score', 0)
        if overall_quality >= 85:
            competence_score += 0.25
            
        return min(competence_score, 1.0)
    
    def _evaluate_quality_assurance(self, results):
        """Evaluate quality assurance processes"""
        qa_score = 0
        
        # Review process implemented (50%)
        if 'refined_translation' in results:
            qa_score += 0.5
        
        # Error detection capability (30%)
        mqm_analysis = results.get('mqm_analysis', {})
        if mqm_analysis.get('total_score', 0) >= 80:
            qa_score += 0.3
        
        # Quality metrics available (20%)
        if 'quality_assessment' in results:
            qa_score += 0.2
            
        return min(qa_score, 1.0)
    
    def _evaluate_project_management(self, results):
        """Evaluate project management standards"""
        pm_score = 0
        
        # Process documentation (40%)
        if len(results.get('refined_translation', {}).get('review_comments', [])) > 0:
            pm_score += 0.4
        
        # Resource allocation (30%) - Multi-agent approach
        agent_count = sum(1 for key in results.keys() 
                         if key in ['initial_translation', 'cultural_analysis', 'refined_translation', 'quality_assessment'])
        if agent_count >= 4:
            pm_score += 0.3
        
        # Delivery standards (30%)
        overall_quality = results.get('quality_assessment', {}).get('overall_score', 0)
        if overall_quality >= 85:
            pm_score += 0.3
            
        return min(pm_score, 1.0)
    
    def _evaluate_technical_resources(self, results):
        """Evaluate technical resource utilization"""
        tech_score = 0
        
        # Tools usage (40%) - AI-powered translation
        if 'initial_translation' in results:
            tech_score += 0.4
        
        # Terminology management (35%)
        quality_scores = results.get('quality_assessment', {}).get('detailed_scores', {})
        if quality_scores.get('vocabulary', 0) >= 85:
            tech_score += 0.35
        
        # Consistency checks (25%)
        if results.get('mqm_analysis', {}).get('error_summary', {}).get('terminology_errors', 999) <= 2:
            tech_score += 0.25
            
        return min(tech_score, 1.0)
    
    def _evaluate_client_requirements(self, results):
        """Evaluate client requirement fulfillment"""
        client_score = 0
        
        # Requirements analysis (40%) - Cultural adaptation
        if results.get('cultural_analysis', {}).get('target_audience_fit') in ['excellent', 'good']:
            client_score += 0.4
        
        # Target audience consideration (35%)
        cultural_analysis = results.get('cultural_analysis', {})
        if cultural_analysis.get('cultural_appropriateness') == 'high':
            client_score += 0.35
        
        # Purpose fitness (25%)
        overall_quality = results.get('quality_assessment', {}).get('overall_score', 0)
        if overall_quality >= 90:
            client_score += 0.25
        elif overall_quality >= 85:
            client_score += 0.15
            
        return min(client_score, 1.0)
