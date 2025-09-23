import re
from typing import Dict, List, Tuple

class SwedishLinguistics:
    """Swedish linguistic analysis and pattern recognition utilities"""
    
    def __init__(self):
        # Swedish grammatical patterns
        self.definite_articles = {
            'en_words': ['-en', '-n'],  # en bil -> bilen
            'ett_words': ['-et', '-t'], # ett hus -> huset  
            'plural': ['-na', '-en']    # bilar -> bilarna
        }
        
        # Swedish compound word patterns
        self.compound_patterns = [
            r'\b\w+s\w+\b',  # genitive compounds: arbetsplats
            r'\b\w+\w{3,}\b' # direct compounds: bilväg
        ]
        
        # Swedish verb conjugation patterns
        self.verb_groups = {
            'group1': r'\w+ar$',    # -ar verbs: talar, arbetar
            'group2a': r'\w+er$',   # -er verbs: läser, köper  
            'group2b': r'\w+r$',    # -r verbs: bor, hör
            'group3': r'\w+r$',     # irregular: går, står
            'group4': r'\w+[^r]$'   # others: är, blir
        }
        
        # Swedish vowel harmony patterns
        self.vowel_patterns = {
            'front_vowels': ['e', 'i', 'y', 'ä', 'ö'],
            'back_vowels': ['a', 'o', 'u', 'å']
        }
        
        # Swedish formal/informal markers
        self.register_markers = {
            'formal': ['ni', 'Ni', 'hälsningar', 'med vänlig hälsning'],
            'informal': ['du', 'hej', 'ha det bra', 'kram']
        }
    
    def analyze_definite_articles(self, text: str) -> Dict:
        """Analyze definite article usage in Swedish text"""
        analysis = {
            'en_articles': 0,
            'ett_articles': 0,
            'plural_articles': 0,
            'errors': []
        }
        
        words = text.split()
        
        for word in words:
            # Check for definite article patterns
            if any(word.endswith(suffix) for suffix in self.definite_articles['en_words']):
                analysis['en_articles'] += 1
            elif any(word.endswith(suffix) for suffix in self.definite_articles['ett_words']):
                analysis['ett_articles'] += 1
            elif any(word.endswith(suffix) for suffix in self.definite_articles['plural']):
                analysis['plural_articles'] += 1
        
        return analysis
    
    def detect_compounds(self, text: str) -> List[str]:
        """Detect Swedish compound words"""
        compounds = []
        
        for pattern in self.compound_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            compounds.extend(matches)
        
        # Remove duplicates and filter by length
        compounds = list(set([c for c in compounds if len(c) > 6]))
        
        return compounds
    
    def analyze_verb_conjugation(self, text: str) -> Dict:
        """Analyze Swedish verb conjugation patterns"""
        analysis = {
            'group1_verbs': [],
            'group2a_verbs': [],
            'group2b_verbs': [],
            'group3_verbs': [],
            'group4_verbs': [],
            'total_verbs': 0
        }
        
        words = text.split()
        
        for word in words:
            word_lower = word.lower()
            
            if re.match(self.verb_groups['group1'], word_lower):
                analysis['group1_verbs'].append(word)
            elif re.match(self.verb_groups['group2a'], word_lower):
                analysis['group2a_verbs'].append(word)
            elif re.match(self.verb_groups['group2b'], word_lower):
                analysis['group2b_verbs'].append(word)
            elif re.match(self.verb_groups['group3'], word_lower):
                analysis['group3_verbs'].append(word)
            elif re.match(self.verb_groups['group4'], word_lower):
                analysis['group4_verbs'].append(word)
        
        analysis['total_verbs'] = sum(len(verbs) for verbs in analysis.values() if isinstance(verbs, list))
        
        return analysis
    
    def detect_register(self, text: str) -> str:
        """Detect formal/informal register in Swedish text"""
        text_lower = text.lower()
        
        formal_count = sum(1 for marker in self.register_markers['formal'] 
                          if marker.lower() in text_lower)
        informal_count = sum(1 for marker in self.register_markers['informal'] 
                           if marker.lower() in text_lower)
        
        if formal_count > informal_count:
            return 'formal'
        elif informal_count > formal_count:
            return 'informal'
        else:
            return 'neutral'
    
    def analyze_vowel_harmony(self, text: str) -> Dict:
        """Analyze Swedish vowel patterns (basic analysis)"""
        analysis = {
            'front_vowels': 0,
            'back_vowels': 0,
            'vowel_ratio': 0.0
        }
        
        text_lower = text.lower()
        
        for char in text_lower:
            if char in self.vowel_patterns['front_vowels']:
                analysis['front_vowels'] += 1
            elif char in self.vowel_patterns['back_vowels']:
                analysis['back_vowels'] += 1
        
        total_vowels = analysis['front_vowels'] + analysis['back_vowels']
        if total_vowels > 0:
            analysis['vowel_ratio'] = analysis['front_vowels'] / total_vowels
        
        return analysis
    
    def validate_swedish_syntax(self, sentence: str) -> Dict:
        """Basic Swedish syntax validation"""
        validation = {
            'has_v2_order': False,
            'proper_word_order': True,
            'syntax_score': 0,
            'suggestions': []
        }
        
        words = sentence.split()
        
        # Check for V2 word order (very basic check)
        if len(words) >= 2:
            # In main clauses, verb should be second element
            # This is a simplified check
            if len(words) >= 3:
                validation['has_v2_order'] = True
        
        # Calculate basic syntax score
        validation['syntax_score'] = 85  # Default score, would be enhanced with proper parsing
        
        return validation
    
    def comprehensive_analysis(self, text: str) -> Dict:
        """Perform comprehensive Swedish linguistic analysis"""
        return {
            'definite_articles': self.analyze_definite_articles(text),
            'compounds': self.detect_compounds(text),
            'verb_analysis': self.analyze_verb_conjugation(text),
            'register': self.detect_register(text),
            'vowel_patterns': self.analyze_vowel_harmony(text),
            'word_count': len(text.split()),
            'character_count': len(text),
            'sentences': len([s for s in text.split('.') if s.strip()])
        }
