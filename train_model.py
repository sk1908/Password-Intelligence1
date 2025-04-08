import os
import pickle
import logging
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_rockyou_dataset(file_path='data/rockyou_sample.txt', max_passwords=10000):
    """Load passwords from the RockYou dataset"""
    logger.info(f"Loading passwords from {file_path}")
    
    passwords = []
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='latin-1', errors='ignore') as f:
                for line in f:
                    password = line.strip()
                    if password:
                        passwords.append(password)
                        if len(passwords) >= max_passwords:
                            break
        else:
            logger.warning(f"File {file_path} not found. Using a small sample set.")
            # Use a small set of common passwords as fallback
            passwords = [
                "123456", "password", "12345678", "qwerty", "123456789",
                "12345", "1234", "111111", "1234567", "dragon",
                "123123", "baseball", "abc123", "football", "monkey"
            ]
    except Exception as e:
        logger.error(f"Error loading passwords: {e}")
        passwords = ["password", "123456", "qwerty"]
    
    logger.info(f"Loaded {len(passwords)} passwords")
    return passwords

def generate_strong_passwords(count=1000):
    """Generate strong passwords for training data"""
    strong_passwords = []
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    for _ in range(count):
        # Generate a random strong password (12-20 chars, mixed character types)
        length = random.randint(12, 20)
        password = ''.join(random.choice(chars) for _ in range(length))
        strong_passwords.append(password)
    
    return strong_passwords

def assign_labels(passwords):
    """Assign strength labels to passwords"""
    labels = []
    
    for password in passwords:
        # Criteria for password strength
        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        # Calculate a score based on these criteria
        score = 0
        
        # Length contribution (up to 5 points)
        score += min(5, length / 2)
        
        # Character type contribution
        if has_lower:
            score += 1
        if has_upper:
            score += 2
        if has_digit:
            score += 2
        if has_special:
            score += 3
        
        # Assign label based on score
        if score < 6:
            labels.append(0)  # Weak
        elif score < 10:
            labels.append(1)  # Medium
        else:
            labels.append(2)  # Strong
    
    return labels

def train_model():
    """Train a password strength prediction model"""
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # 1. Load and prepare data
    weak_passwords = load_rockyou_dataset()
    strong_passwords = generate_strong_passwords(min(1000, len(weak_passwords)))
    
    # Combine datasets
    all_passwords = weak_passwords + strong_passwords
    
    # Assign labels (0=weak, 1=medium, 2=strong)
    labels = assign_labels(all_passwords)
    
    # 2. Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        all_passwords, labels, test_size=0.2, random_state=42
    )
    
    # 3. Feature extraction
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
    X_train_features = vectorizer.fit_transform(X_train)
    X_test_features = vectorizer.transform(X_test)
    
    # 4. Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_features, y_train)
    
    # 5. Evaluate the model
    y_pred = model.predict(X_test_features)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Model accuracy: {accuracy:.2f}")
    logger.info(f"Classification report:\n{classification_report(y_test, y_pred)}")
    
    # 6. Save the model and vectorizer
    with open('data/password_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('data/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    logger.info("Model and vectorizer saved to data directory")

if __name__ == "__main__":
    train_model()
