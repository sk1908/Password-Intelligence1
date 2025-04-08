import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import logging

logger = logging.getLogger(__name__)

class PasswordStrengthModel:
    """Machine learning model for predicting password strength"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.model_path = os.path.join('data', 'password_model.pkl')
        self.vectorizer_path = os.path.join('data', 'vectorizer.pkl')
        self.load_model()
    
    def load_model(self):
        """Load the trained model if available, otherwise create a simple model"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                logger.info("Loaded pre-trained password strength model")
            else:
                logger.warning("Pre-trained model not found, using a simple model")
                self._create_simple_model()
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._create_simple_model()
    
    def _create_simple_model(self):
        """Create a simple model for fallback"""
        self.vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
        self.model = RandomForestClassifier()
        
        # Simple training data
        passwords = [
            "123456", "password", "qwerty", "admin", "welcome",  # Very weak
            "Password123", "Qwerty123", "Admin123!",  # Medium
            "C0mpl3x!P@ssw0rd", "Sup3rS3cur3P@55w0rd!"  # Strong
        ]
        
        strengths = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2]  # 0=weak, 1=medium, 2=strong
        
        # Fit the vectorizer and model
        X = self.vectorizer.fit_transform(passwords)
        self.model.fit(X, strengths)
    
    def predict_strength(self, password):
        """Predict the strength class of a password"""
        if not password:
            return 0
        
        # Feature extraction
        X = self.vectorizer.transform([password])
        
        # Predict strength (0=weak, 1=medium, 2=strong)
        strength_class = self.model.predict(X)[0]
        
        # Get prediction probabilities
        probs = self.model.predict_proba(X)[0]
        
        return {
            'strength_class': int(strength_class),
            'probabilities': probs.tolist()
        }
    
    def extract_features(self, password):
        """Extract features for a password to help determine why it's weak"""
        features = {}
        
        # Length-based features
        features['length'] = len(password)
        features['too_short'] = len(password) < 8
        
        # Character class features
        features['has_lowercase'] = any(c.islower() for c in password)
        features['has_uppercase'] = any(c.isupper() for c in password)
        features['has_digit'] = any(c.isdigit() for c in password)
        features['has_special'] = any(not c.isalnum() for c in password)
        
        # Pattern features
        features['only_letters'] = password.isalpha()
        features['only_digits'] = password.isdigit()
        features['starts_with_uppercase_ends_with_digit'] = (
            password and password[0].isupper() and password[-1].isdigit()
        )
        
        # Case features
        features['is_lowercase'] = password.islower()
        features['is_uppercase'] = password.isupper()
        
        # Repeating characters
        features['has_repeating_chars'] = any(
            password[i] == password[i+1] for i in range(len(password)-1)
        )
        
        return features
