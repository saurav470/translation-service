import streamlit as st
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from agents.translator_agent import TranslatorAgent
from agents.reviewer_agent import ReviewerAgent
from agents.quality_assessor import QualityAssessor
from agents.cultural_advisor import CulturalAdvisor
from agents.final_translator_agent import FinalTranslatorAgent
from quality.mqm_framework import MQMFramework
from quality.iso_standards import ISOStandards
from config.agent_config import LANGUAGE_CONFIGS

st.set_page_config(
    page_title="Professional AI Translation System - Multi-Language",
    page_icon="🌍",
    layout="wide"
)

def initialize_agents():
    """Initialize all AI agents"""
    if 'agents_initialized' not in st.session_state:
        st.session_state.translator = TranslatorAgent()
        st.session_state.reviewer = ReviewerAgent()
        st.session_state.quality_assessor = QualityAssessor()
        st.session_state.cultural_advisor = CulturalAdvisor()
        st.session_state.mqm_framework = MQMFramework()
        st.session_state.iso_standards = ISOStandards()
        st.session_state.final_translator = FinalTranslatorAgent()
        st.session_state.agents_initialized = True

def run_translation_pipeline(source_text, target_language="swedish"):
    """Run the complete multi-agent translation pipeline"""
    results = {}
    
    with st.spinner("Running multi-agent translation pipeline..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Initial Translation
        status_text.text("🤖 Agent 1: Performing initial translation...")
        progress_bar.progress(0.2)
        translation_result = st.session_state.translator.translate(source_text, target_language)
        results['initial_translation'] = translation_result
        
        # Step 2: Cultural Advisory
        status_text.text("🏛️ Agent 2: Analyzing cultural context...")
        progress_bar.progress(0.4)
        cultural_analysis = st.session_state.cultural_advisor.analyze(
            source_text, translation_result['translation'], target_language
        )
        results['cultural_analysis'] = cultural_analysis
        
        # Step 3: Review and Refinement
        status_text.text("📝 Agent 3: Reviewing and refining translation...")
        progress_bar.progress(0.6)
        refined_translation = st.session_state.reviewer.review(
            source_text, 
            translation_result['translation'],
            cultural_analysis,
            target_language
        )
        results['refined_translation'] = refined_translation
        
        # Step 4: Quality Assessment
        status_text.text("📊 Agent 4: Performing quality assessment...")
        progress_bar.progress(0.8)
        quality_assessment = st.session_state.quality_assessor.assess(
            source_text,
            refined_translation['final_translation'],
            target_language
        )
        results['quality_assessment'] = quality_assessment
        
        # Step 5: MQM Framework Analysis
        status_text.text("🎯 Generating MQM quality metrics...")
        progress_bar.progress(0.9)
        mqm_analysis = st.session_state.mqm_framework.analyze(
            source_text,
            refined_translation['final_translation'],
            quality_assessment
        )
        results['mqm_analysis'] = mqm_analysis
        
        # Step 6: ISO Compliance Check
        status_text.text("✅ Validating ISO 17100:2015 compliance...")
        progress_bar.progress(1.0)
        iso_compliance = st.session_state.iso_standards.validate(results)
        results['iso_compliance'] = iso_compliance
        
        # step 7: agent 7 final tarnslation after quality check
        status_text.text("🔄 Finalizing translation after quality checks...")
        final_translation = st.session_state.final_translator.create_final_translation(
            source_text,
            refined_translation['final_translation'],
            quality_assessment,
            mqm_analysis,
            iso_compliance,
            target_language
        )
        print(final_translation)
        results['updated_translation'] = final_translation
        status_text.text("✨ Translation pipeline completed!")
        
    return results

def display_quality_metrics(results):
    """Display comprehensive quality metrics"""
    st.subheader("📊 Quality Assessment Dashboard")
    
    # Overall Quality Score
    overall_score = results['quality_assessment']['overall_score']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Overall Quality Score",
            value=f"{overall_score:.1f}%",
            delta=f"{overall_score - 85:.1f}% vs Industry Standard"
        )
    
    with col2:
        iso_status = "✅ Compliant" if results['iso_compliance']['compliant'] else "❌ Non-Compliant"
        st.metric(
            label="ISO 17100:2015 Status",
            value=iso_status
        )
    
    with col3:
        mqm_score = results['mqm_analysis']['total_score']
        st.metric(
            label="MQM Framework Score",
            value=f"{mqm_score:.1f}/100"
        )
    
    # Detailed Quality Metrics
    st.subheader("🎯 Detailed Quality Breakdown")
    
    quality_data = results['quality_assessment']['detailed_scores']
    categories = list(quality_data.keys())
    scores = list(quality_data.values())
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        name='Translation Quality',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Translation Quality Assessment (MQM Framework)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Error Analysis
    if 'errors' in results['mqm_analysis']:
        st.subheader("🔍 Error Analysis")
        errors_df = pd.DataFrame(results['mqm_analysis']['errors'])
        if not errors_df.empty:
            st.dataframe(errors_df, use_container_width=True)
        else:
            st.success("No errors detected in the translation!")

def main():
    """Main application interface"""
    initialize_agents()
    
    st.title("🌍 Professional AI Translation System")
    st.subheader("English to Multiple Languages - Industry Standard Quality")
    
    st.markdown("""
    This professional translation system uses multiple AI agents to deliver industry-standard quality:
    - **Translator Agent**: Initial high-quality translation
    - **Cultural Advisor**: Swedish cultural context and localization
    - **Review Agent**: Linguistic refinement and error correction
    - **Quality Assessor**: Comprehensive quality evaluation using MQM framework
    """)
    
    # Input Section
    st.header("📝 Translation Input")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Language Selection
        language_options = {
            f"{config['flag']} {config['name']}": key 
            for key, config in LANGUAGE_CONFIGS.items()
        }
        
        selected_display = st.selectbox(
            "Select target language:",
            options=list(language_options.keys()),
            index=0
        )
        
        selected_language = language_options[selected_display]
        selected_config = LANGUAGE_CONFIGS[selected_language]
        
        source_text = st.text_area(
            "Enter English text to translate:",
            height=200,
            placeholder=f"Enter your English text here for professional {selected_config['name']} translation..."
        )
    
    with col2:
        st.markdown("**Quality Standards:**")
        st.markdown("✅ ISO 17100:2015 Compliant")
        st.markdown("✅ MQM Framework")
        st.markdown("✅ Professional Grade")
        st.markdown("✅ Cultural Adaptation")
        st.markdown("✅ Linguistic Excellence")
    
    if st.button("🚀 Start Professional Translation", type="primary"):
        if source_text.strip():
            results = run_translation_pipeline(source_text, selected_language)
            
            # Display Results
            st.header("📋 Translation Results")
            
            # Final Translation
            selected_config = LANGUAGE_CONFIGS[selected_language]
            st.subheader(f"🎯 Final {selected_config['name']} Translation")
            final_translation = results['refined_translation']['final_translation']
            st.markdown(f"**{final_translation}**")
            
            # after quality check final translation
            st.subheader(f"🏆 Finalized {selected_config['name']} Translation After Quality")
            st.markdown(f"""final_translation after quality checks considering MQM and ISO compliance""")
            updated_translation = results['updated_translation']['final_translation']
            st.markdown(f"**{updated_translation}**")
            
            # Quality Metrics
            display_quality_metrics(results)
            
            # Detailed Analysis Sections
            with st.expander("🔍 Translation Process Analysis"):
                st.subheader("Initial Translation")
                st.write(results['initial_translation']['translation'])
                st.write("**Confidence:**", f"{results['initial_translation']['confidence']:.1f}%")
                
                st.subheader("Cultural Analysis")
                cultural = results['cultural_analysis']
                st.write("**Cultural Adaptations:**", cultural['adaptations'])
                st.write("**Regional Considerations:**", cultural['regional_notes'])
                
                st.subheader("Review Comments")
                review = results['refined_translation']
                for comment in review['review_comments']:
                    st.write(f"• {comment}")
            
            with st.expander("📊 Quality Assessment Details"):
                qa = results['quality_assessment']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Fluency Score:**", f"{qa['detailed_scores']['fluency']:.1f}%")
                    st.write("**Grammar Score:**", f"{qa['detailed_scores']['grammar']:.1f}%")
                    st.write("**Accuracy Score:**", f"{qa['detailed_scores']['accuracy']:.1f}%")
                
                with col2:
                    st.write("**Naturalness Score:**", f"{qa['detailed_scores']['naturalness']:.1f}%")
                    st.write("**Vocabulary Score:**", f"{qa['detailed_scores']['vocabulary']:.1f}%")
                    st.write("**Colloquial Usage:**", f"{qa['detailed_scores']['colloquial_usage']:.1f}%")
                
                st.write("**Assessment Notes:**")
                for note in qa['assessment_notes']:
                    st.write(f"• {note}")
            
            with st.expander("🏅 ISO 17100:2015 Compliance Report"):
                iso = results['iso_compliance']
                st.write(f"**Compliance Status:** {'✅ Compliant' if iso['compliant'] else '❌ Non-Compliant'}")
                st.write(f"**Overall Score:** {iso['score']:.1f}%")
                
                st.write("**Compliance Areas:**")
                for area, status in iso['compliance_areas'].items():
                    status_icon = "✅" if status else "❌"
                    st.write(f"{status_icon} {area}")
                
                if iso['recommendations']:
                    st.write("**Recommendations:**")
                    for rec in iso['recommendations']:
                        st.write(f"• {rec}")
        
        else:
            st.error("Please enter text to translate.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    Professional AI Translation System | Industry Standards Compliant | Powered by Multi-Agent Architecture
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
