import random
import string
import math
import logging

logger = logging.getLogger(__name__)

class PasswordGenerator:
    """Generates secure passwords based on user preferences"""
    
    def __init__(self):
        self.lowercase_chars = string.ascii_lowercase
        self.uppercase_chars = string.ascii_uppercase
        self.digit_chars = string.digits
        self.symbol_chars = string.punctuation
    
    def generate(self, length=16, include_uppercase=True, include_lowercase=True, 
                 include_numbers=True, include_symbols=True, min_entropy=80):
        """
        Generate a strong password based on given parameters
        
        Args:
            length: The length of the password (default: 16)
            include_uppercase: Whether to include uppercase letters (default: True)
            include_lowercase: Whether to include lowercase letters (default: True)
            include_numbers: Whether to include numbers (default: True)
            include_symbols: Whether to include symbols (default: True)
            min_entropy: Minimum entropy required (default: 80)
            
        Returns:
            A generated password string
        """
        # Ensure at least one character type is selected
        if not any([include_uppercase, include_lowercase, include_numbers, include_symbols]):
            include_lowercase = True
        
        # Build character pool
        char_pool = ""
        if include_lowercase:
            char_pool += self.lowercase_chars
        if include_uppercase:
            char_pool += self.uppercase_chars
        if include_numbers:
            char_pool += self.digit_chars
        if include_symbols:
            char_pool += self.symbol_chars
        
        # Calculate minimum length needed for the required entropy
        pool_size = len(char_pool)
        min_length = math.ceil(min_entropy / math.log2(pool_size))
        
        # Adjust length if necessary
        actual_length = max(length, min_length)
        
        # Generate the password
        for attempt in range(5):  # Try up to 5 times to meet requirements
            password = self._generate_random_password(char_pool, actual_length)
            
            # Check if the password meets character type requirements
            meets_requirements = True
            if include_lowercase and not any(c in self.lowercase_chars for c in password):
                meets_requirements = False
            if include_uppercase and not any(c in self.uppercase_chars for c in password):
                meets_requirements = False
            if include_numbers and not any(c in self.digit_chars for c in password):
                meets_requirements = False
            if include_symbols and not any(c in self.symbol_chars for c in password):
                meets_requirements = False
            
            if meets_requirements:
                return password
        
        # If we couldn't generate a password that meets all requirements naturally,
        # generate one with forced character types
        return self._generate_password_with_requirements(
            actual_length, include_lowercase, include_uppercase, 
            include_numbers, include_symbols
        )
    
    def _generate_random_password(self, char_pool, length):
        """Generate a random password from the given character pool"""
        return ''.join(random.choice(char_pool) for _ in range(length))
    
    def _generate_password_with_requirements(self, length, include_lowercase, 
                                            include_uppercase, include_numbers, 
                                            include_symbols):
        """Generate a password that meets all specified requirements"""
        # Determine how many of each character type we need
        char_types = []
        if include_lowercase:
            char_types.append(self.lowercase_chars)
        if include_uppercase:
            char_types.append(self.uppercase_chars)
        if include_numbers:
            char_types.append(self.digit_chars)
        if include_symbols:
            char_types.append(self.symbol_chars)
        
        # Make sure we have at least one of each required character type
        password_chars = []
        for char_type in char_types:
            password_chars.append(random.choice(char_type))
        
        # Fill the rest with random characters from the full pool
        full_pool = ''.join(char_types)
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choice(full_pool) for _ in range(remaining_length))
        
        # Shuffle the characters to avoid predictable patterns
        random.shuffle(password_chars)
        
        return ''.join(password_chars)
