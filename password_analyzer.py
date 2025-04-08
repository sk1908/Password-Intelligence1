import math
import hashlib
import re
import os
import logging
from models import PasswordStrengthModel
from collections import Counter

logger = logging.getLogger(__name__)

class PasswordAnalyzer:
    """Analyzes password strength and vulnerability"""
    
    def __init__(self):
        self.model = PasswordStrengthModel()
        self.common_passwords = self._load_common_passwords()
        
        # Map known patterns to their descriptions
        self.pattern_descriptions = {
            r'^[a-z]+$': 'lowercase letters only',
            r'^[A-Z]+$': 'uppercase letters only',
            r'^[0-9]+$': 'digits only',
            r'^[a-zA-Z]+$': 'letters only (no numbers or symbols)',
            r'^[a-z]+[0-9]+$': 'lowercase letters followed by numbers',
            r'^[A-Z][a-z]+[0-9]+$': 'capitalized word followed by numbers',
            r'^[A-Z][a-z]+[0-9]{1,4}$': 'capitalized word followed by 1-4 numbers (common pattern)',
            r'password': 'contains the word "password"',
            r'123': 'contains the sequence "123"',
            r'qwerty': 'contains the keyboard pattern "qwerty"',
            r'abc': 'contains the alphabet sequence "abc"',
        }
        
        # Define character sets for entropy calculation
        self.char_sets = {
            'lowercase': 26,   # a-z
            'uppercase': 26,   # A-Z
            'digits': 10,      # 0-9
            'symbols': 33      # Special characters
        }
    
    def _load_common_passwords(self):
        """Load a set of common passwords from the RockYou dataset sample"""
        common_passwords = set()
        try:
            file_path = os.path.join('data', 'rockyou_sample.txt')
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
                    for line in f:
                        password = line.strip()
                        if password:
                            common_passwords.add(password)
            else:
                # Fallback to a small list of common passwords
                common_passwords = {
                    "123456", "password", "12345678", "qwerty", "123456789",
                    "12345", "1234", "111111", "1234567", "dragon",
                    "123123", "baseball", "abc123", "football", "monkey",
                    "letmein", "shadow", "master", "666666", "qwertyuiop"
                }
        except Exception as e:
            logger.error(f"Error loading common passwords: {e}")
            # Fallback to a small list of common passwords
            common_passwords = {
                "123456", "password", "12345678", "qwerty", "123456789",
                "12345", "1234", "111111", "1234567", "dragon"
            }
        
        return common_passwords
    
    def analyze(self, password):
        """Perform a comprehensive analysis of password strength"""
        if not password:
            return {
                'score': 0,
                'strength': 'No password provided',
                'entropy': 0,
                'time_to_crack': '< 1 second',
                'patterns': ['No password provided'],
                'is_common': False,
                'features': {}
            }
        
        # Check if it's a common password
        is_common = password.lower() in self.common_passwords
        
        # Calculate entropy
        entropy = self._calculate_entropy(password)
        
        # Estimate time to crack
        time_to_crack = self._calculate_crack_time(entropy)
        
        # Get ML model prediction
        ml_results = self.model.predict_strength(password)
        strength_class = ml_results['strength_class']
        
        # Map strength class to label
        strength_labels = ['Weak', 'Medium', 'Strong']
        strength = strength_labels[strength_class]
        
        # Calculate numeric score (0-100)
        score = min(100, max(0, int(entropy * 3.3)))
        if is_common:
            score = min(score, 10)  # Cap score for common passwords
        
        # Extract features and patterns
        features = self.model.extract_features(password)
        patterns = self._identify_patterns(password)
        
        # Calculate character distribution
        char_distribution = self._analyze_character_distribution(password)
        
        return {
            'score': score,
            'strength': strength,
            'entropy': round(entropy, 2),
            'time_to_crack': time_to_crack,
            'patterns': patterns,
            'is_common': is_common,
            'features': features,
            'char_distribution': char_distribution,
            'length': len(password)
        }
    
    def _calculate_entropy(self, password):
        """Calculate the entropy (bits) of a password"""
        if not password:
            return 0
        
        # Count character types
        has_lowercase = any(c.islower() for c in password)
        has_uppercase = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        # Calculate character pool size
        char_pool_size = 0
        if has_lowercase:
            char_pool_size += self.char_sets['lowercase']
        if has_uppercase:
            char_pool_size += self.char_sets['uppercase']
        if has_digit:
            char_pool_size += self.char_sets['digits']
        if has_special:
            char_pool_size += self.char_sets['symbols']
        
        # Calculate base entropy
        if char_pool_size == 0:
            return 0
        
        base_entropy = len(password) * math.log2(char_pool_size)
        
        # Penalty for repeating characters
        char_counts = Counter(password)
        repeats = sum(count - 1 for count in char_counts.values() if count > 1)
        repeat_penalty = repeats * 0.5
        
        # Penalty for patterns
        pattern_penalty = len(self._identify_patterns(password)) * 4
        
        # Calculate final entropy
        final_entropy = max(0, base_entropy - repeat_penalty - pattern_penalty)
        
        return final_entropy
    
    def _calculate_crack_time(self, entropy):
        """Estimate the time it would take to crack a password with the given entropy"""
        # Assuming 10 billion guesses per second (modern hardware)
        guesses_per_second = 10_000_000_000
        
        # Calculate the total possible guesses needed (2^entropy)
        total_guesses = 2 ** entropy
        
        # Calculate seconds to crack
        seconds = total_guesses / guesses_per_second
        
        # Convert to human-readable format
        if seconds < 1:
            return "< 1 second"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        elif seconds < 31536000:
            return f"{int(seconds / 86400)} days"
        elif seconds < 31536000 * 100:
            return f"{int(seconds / 31536000)} years"
        else:
            return f"{int(seconds / 31536000)} years (effectively uncrackable)"
    
    def _identify_patterns(self, password):
        """Identify common patterns in the password"""
        patterns = []
        
        # Check for common patterns
        for pattern, description in self.pattern_descriptions.items():
            if re.search(pattern, password, re.IGNORECASE):
                patterns.append(description)
        
        # Check for sequential characters
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i]) + 2):
                patterns.append("sequential characters")
                break
        
        # Check for repeating characters
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                patterns.append("repeating characters")
                break
        
        # Check for keyboard patterns (horizontal)
        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm"
        ]
        
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                if row[i:i+3].lower() in password.lower():
                    patterns.append("keyboard pattern")
                    break
            if "keyboard pattern" in patterns:
                break
        
        # If no patterns found
        if not patterns and len(password) >= 12:
            patterns.append("no common patterns detected")
        
        return patterns
    
    def _analyze_character_distribution(self, password):
        """Analyze the distribution of characters in the password"""
        lowercase_count = sum(1 for c in password if c.islower())
        uppercase_count = sum(1 for c in password if c.isupper())
        digit_count = sum(1 for c in password if c.isdigit())
        special_count = sum(1 for c in password if not c.isalnum())
        
        total_len = len(password)
        if total_len == 0:
            return {
                'lowercase': 0,
                'uppercase': 0,
                'digits': 0,
                'special': 0
            }
        
        return {
            'lowercase': round(lowercase_count / total_len * 100),
            'uppercase': round(uppercase_count / total_len * 100),
            'digits': round(digit_count / total_len * 100),
            'special': round(special_count / total_len * 100)
        }
