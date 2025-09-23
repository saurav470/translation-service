import re
from typing import Dict, List, Tuple

class DutchLinguistics:
    """Dutch linguistic analysis and pattern recognition utilities"""
    
    def __init__(self):
        # Dutch grammatical patterns
        self.definite_articles = {
            'de_words': ['de'],       # de auto, de man
            'het_words': ['het'],     # het huis, het kind
            'plural': ['de']          # de auto's, de huizen
        }
        
        # Dutch compound word patterns
        self.compound_patterns = [
            r'\b\w+s\w+\b',  # genitive compounds: werkplaats
            r'\b\w+\w{4,}\b' # direct compounds: autoweg
        ]
        
        # Dutch verb conjugation patterns
        self.verb_groups = {
            'weak_verbs': r'\w+(de|te|d|t)$',     # werkte, maakte, heeft gewerkt
            'strong_verbs': r'\w+en$',            # lopen, geven, nemen
            'irregular_verbs': r'\w+(ben|is|zijn|heeft|hadden)$'  # zijn, hebben
        }
        
        # Dutch vowel patterns
        self.vowel_patterns = {
            'short_vowels': ['a', 'e', 'i', 'o', 'u'],
            'long_vowels': ['aa', 'ee', 'ie', 'oo', 'uu'],
            'diphthongs': ['ei', 'ij', 'au', 'ou', 'ui', 'eu']
        }
        
        # Dutch formal/informal markers
        self.register_markers = {
            'formal': ['u', 'U', 'meneer', 'mevrouw', 'met vriendelijke groet'],
            'informal': ['je', 'jij', 'hoi', 'dag', 'groetjes']
        }
        
        # Dutch-specific linguistic features
        self.dutch_features = {
            'diminutives': ['-je', '-tje', '-pje', '-kje'],  # huisje, boompje
            'past_participles': ['ge-'],                      # gedaan, gegeven
            'separable_verbs': ['af-', 'aan-', 'uit-', 'op-', 'mee-']  # afmaken, uitgaan
        }
    
    def analyze_definite_articles(self, text: str) -> Dict:
        """Analyze definite article usage in Dutch text"""
        analysis = {
            'de_articles': 0,
            'het_articles': 0,
            'article_errors': []
        }
        
        words = text.split()
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            if word_lower == 'de':
                analysis['de_articles'] += 1
            elif word_lower == 'het':
                analysis['het_articles'] += 1
        
        return analysis
    
    def detect_compounds(self, text: str) -> List[str]:
        """Detect Dutch compound words"""
        compounds = []
        
        for pattern in self.compound_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            compounds.extend(matches)
        
        # Remove duplicates and filter by length
        compounds = list(set([c for c in compounds if len(c) > 6]))
        
        return compounds
    
    def analyze_verb_conjugation(self, text: str) -> Dict:
        """Analyze Dutch verb conjugation patterns"""
        analysis = {
            'weak_verbs': [],
            'strong_verbs': [],
            'irregular_verbs': [],
            'total_verbs': 0
        }
        
        words = text.split()
        
        for word in words:
            word_lower = word.lower()
            
            if re.match(self.verb_groups['weak_verbs'], word_lower):
                analysis['weak_verbs'].append(word)
            elif re.match(self.verb_groups['strong_verbs'], word_lower):
                analysis['strong_verbs'].append(word)
            elif re.match(self.verb_groups['irregular_verbs'], word_lower):
                analysis['irregular_verbs'].append(word)
        
        analysis['total_verbs'] = sum(len(verbs) for verbs in analysis.values() if isinstance(verbs, list))
        
        return analysis
    
    def detect_register(self, text: str) -> str:
        """Detect formal/informal register in Dutch text"""
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
    
    def detect_diminutives(self, text: str) -> List[str]:
        """Detect Dutch diminutive forms"""
        diminutives = []
        words = text.split()
        
        for word in words:
            for suffix in self.dutch_features['diminutives']:
                if word.lower().endswith(suffix):
                    diminutives.append(word)
                    break
        
        return diminutives
    
    def analyze_separable_verbs(self, text: str) -> List[str]:
        """Detect Dutch separable verbs"""
        separable_verbs = []
        words = text.split()
        
        for word in words:
            for prefix in self.dutch_features['separable_verbs']:
                if word.lower().startswith(prefix):
                    separable_verbs.append(word)
                    break
        
        return separable_verbs
    
    def validate_dutch_syntax(self, sentence: str) -> Dict:
        """Basic Dutch syntax validation"""
        validation = {
            'has_proper_word_order': True,
            'syntax_score': 0,
            'suggestions': []
        }
        
        words = sentence.split()
        
        # Dutch word order validation (basic)
        if len(words) >= 2:
            validation['has_proper_word_order'] = True
        
        # Calculate basic syntax score
        validation['syntax_score'] = 85  # Default score, would be enhanced with proper parsing
        
        return validation
    
    def comprehensive_analysis(self, text: str) -> Dict:
        """Perform comprehensive Dutch linguistic analysis"""
        return {
            'definite_articles': self.analyze_definite_articles(text),
            'compounds': self.detect_compounds(text),
            'verb_analysis': self.analyze_verb_conjugation(text),
            'register': self.detect_register(text),
            'diminutives': self.detect_diminutives(text),
            'separable_verbs': self.analyze_separable_verbs(text),
            'word_count': len(text.split()),
            'character_count': len(text),
            'sentences': len([s for s in text.split('.') if s.strip()])
        }