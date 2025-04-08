import os
import logging
import random
import json
from groq import Groq
from translations import localize_suggestions

logger = logging.getLogger(__name__)

# Use Groq's LLama model for better performance
MODEL = "llama3-70b-8192"

# Initialize Groq client with the provided API key
GROQ_API_KEY = "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"
# Create Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

def get_ai_suggestions(password, analysis_results, language='en'):
    """
    Get AI-generated suggestions for improving a password
    
    Args:
        password: The password to improve
        analysis_results: The analysis results from the password analyzer
        language: Language code for the response (default: 'en')
        
    Returns:
        Dictionary with suggestions and reasoning, localized to the specified language
    """
    try:
        # Build a prompt based on the analysis results
        prompt = _build_prompt(password, analysis_results, language)
        
        # Make the API call with Groq
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a password security expert. Your task is to analyze passwords and suggest improvements. "
                    "Always respond with a JSON object containing fields for 'improved_password', 'reasoning', and 'vulnerability_details'."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse the response
        suggestions = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Sometimes the model adds extra text before or after the JSON
            # Find the JSON part that starts with { and ends with }
            json_start = suggestions.find('{')
            json_end = suggestions.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = suggestions[json_start:json_end]
                json_suggestions = json.loads(json_content)
                
                # If the language is English, return as is
                if language == 'en':
                    return json_suggestions
                    
                # For other languages, try to get a multilingual version using our AI model
                if language != 'en' and json_suggestions and 'vulnerability_details' in json_suggestions:
                    try:
                        # If the language is not English and the Groq model supports it,
                        # we could ask it directly to translate, but for now we'll use our translations
                        return localize_suggestions(json_suggestions, language)
                    except Exception as translation_error:
                        logger.warning(f"Error translating to {language}: {translation_error}")
                        # Fall back to English if there's an error
                        return json_suggestions
                else:
                    return json_suggestions
            else:
                # If no JSON found, create a structured response manually
                structured_response = _create_structured_response(password, analysis_results, suggestions)
                return localize_suggestions(structured_response, language)
        except json.JSONDecodeError:
            logger.warning("Response is not valid JSON, creating structured response")
            structured_response = _create_structured_response(password, analysis_results, suggestions)
            return localize_suggestions(structured_response, language)
        
    except Exception as e:
        logger.error(f"Error getting AI suggestions: {e}")
        fallback_suggestions = _get_fallback_suggestions(password, analysis_results)
        return localize_suggestions(fallback_suggestions, language)

def _create_structured_response(password, analysis_results, ai_text):
    """
    Create a structured response from unstructured AI text output
    """
    # Extract potential suggestions from the text
    improved_password = password
    reasoning = ""
    vulnerability_details = []
    
    # Try to find an improved password suggestion in the text
    if "improved password" in ai_text.lower():
        lines = ai_text.split('\n')
        for line in lines:
            if ":" in line and ("improved" in line.lower() or "suggestion" in line.lower()):
                parts = line.split(':', 1)
                if len(parts) > 1 and parts[1].strip():
                    improved_password = parts[1].strip().replace('"', '').replace("'", "")
                    # Remove any trailing punctuation
                    if improved_password and improved_password[-1] in '.,;':
                        improved_password = improved_password[:-1]
                    break
    
    # Try to find reasoning
    reasoning_section = False
    for line in ai_text.split('\n'):
        if reasoning_section and line.strip() and not line.lower().startswith(("vulnerability", "attack", "weakness")):
            reasoning += line.strip() + " "
        if "reason" in line.lower() or "why" in line.lower() or "better" in line.lower():
            reasoning_section = True
            # Extract content after colon if present
            if ":" in line:
                reasoning += line.split(':', 1)[1].strip() + " "
    
    # Try to find vulnerability details
    vulnerability_section = False
    for line in ai_text.split('\n'):
        if vulnerability_section and line.strip():
            if line.strip().startswith(("-", "•", "*", "1.", "2.", "3.")):
                vulnerability_details.append(line.strip()[1:].strip())
            elif not any(x in line.lower() for x in ["improved", "suggest", "better", "complex"]):
                if not vulnerability_details:
                    vulnerability_details.append(line.strip())
                else:
                    # Append to the last vulnerability if it doesn't look like a new entry
                    vulnerability_details[-1] += " " + line.strip()
        if any(x in line.lower() for x in ["vulnerab", "attack", "weakness", "problem"]):
            vulnerability_section = True
            # Extract content after colon if present
            if ":" in line and len(line.split(':', 1)[1].strip()) > 10:
                vulnerability_details.append(line.split(':', 1)[1].strip())
    
    # If we couldn't find any of these in the AI output, use fallback logic
    if not improved_password or improved_password == password:
        fallback = _get_fallback_suggestions(password, analysis_results)
        improved_password = fallback["improved_password"]
    
    if not reasoning:
        reasoning = "This password has been improved by adding complexity while maintaining some recognizable elements."
    
    if not vulnerability_details:
        # Extract basic vulnerabilities from analysis results
        features = analysis_results.get('features', {})
        patterns = analysis_results.get('patterns', [])
        
        if len(password) < 12:
            vulnerability_details.append("Short length makes it vulnerable to brute force attacks")
        
        if not features.get('has_uppercase', False):
            vulnerability_details.append("Lacks uppercase letters")
        
        if not features.get('has_digit', False):
            vulnerability_details.append("Lacks numbers")
            
        if not features.get('has_special', False):
            vulnerability_details.append("Lacks special characters")
            
        for pattern in patterns:
            if "only" in pattern or "common" in pattern:
                vulnerability_details.append(f"{pattern.capitalize()}")
    
    # Remove duplicates from vulnerability details
    if vulnerability_details:
        vulnerability_details = list(dict.fromkeys(vulnerability_details))
    
    return {
        "improved_password": improved_password,
        "reasoning": reasoning.strip(),
        "vulnerability_details": vulnerability_details if vulnerability_details else ["Could be vulnerable to dictionary or brute force attacks"]
    }

def _build_prompt(password, analysis, language='en'):
    """
    Build a prompt for the AI based on password analysis
    
    Args:
        password: The password to analyze
        analysis: Dictionary with analysis results
        language: Language code (default: 'en')
        
    Returns:
        Prompt string to send to the AI
    """
    entropy = analysis.get('entropy', 0)
    patterns = analysis.get('patterns', [])
    is_common = analysis.get('is_common', False)
    features = analysis.get('features', {})
    
    # Base prompt in English
    prompt = f"""
    Analyze this password: {password}
    
    Analysis results:
    - Entropy: {entropy} bits
    - Identified patterns: {', '.join(patterns)}
    - Common password: {'Yes' if is_common else 'No'}
    - Length: {len(password)}
    - Has lowercase: {features.get('has_lowercase', False)}
    - Has uppercase: {features.get('has_uppercase', False)}
    - Has digits: {features.get('has_digit', False)}
    - Has special chars: {features.get('has_special', False)}
    
    Based on this analysis, please:
    1. Suggest an improved version of this password that maintains some recognizable elements but is significantly stronger
    2. Explain why the original password is vulnerable and how your suggestion improves it
    3. Provide specific details about potential attack vectors for the original password
    
    Return your response in JSON format with these fields:
    - improved_password: your suggested improvement
    - reasoning: explanation of why your suggestion is better
    - vulnerability_details: specific vulnerabilities in the original password
    """
    
    # For certain languages, we can ask Groq to respond directly in that language
    # Note: Only do this for languages Groq is known to handle well
    if language in ['es', 'fr', 'de']:
        language_names = {
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
        
        prompt += f"""
        Please respond in {language_names[language]}. Ensure your response is a valid JSON object.
        """
    
    return prompt

def _get_fallback_suggestions(password, analysis_results):
    """
    Generate fallback suggestions when the AI API is not available
    """
    # Basic improvements based on analysis
    improvements = []
    vulnerability_details = []
    
    # Check password length
    if len(password) < 12:
        improvements.append("Increase length to at least 12 characters")
        vulnerability_details.append("Short passwords are vulnerable to brute force attacks")
    
    # Check character types
    features = analysis_results.get('features', {})
    if not features.get('has_lowercase', True):
        improvements.append("Add lowercase letters")
    if not features.get('has_uppercase', False):
        improvements.append("Add uppercase letters")
        vulnerability_details.append("Lacks uppercase letters which reduces complexity")
    if not features.get('has_digit', False):
        improvements.append("Add numbers")
        vulnerability_details.append("Lacks numbers which reduces complexity")
    if not features.get('has_special', False):
        improvements.append("Add special characters")
        vulnerability_details.append("Lacks special characters which reduces complexity")
    
    # Check for common patterns
    patterns = analysis_results.get('patterns', [])
    for pattern in patterns:
        if "only" in pattern:
            vulnerability_details.append(f"Uses {pattern}")
        elif "common" in pattern:
            vulnerability_details.append("Uses a predictable pattern")
    
    # Check if it's a common password
    if analysis_results.get('is_common', False):
        vulnerability_details.append("This is a commonly used password that appears in data breaches")
    
    # Generate improved password suggestion
    improved = password
    
    # Add uppercase if missing
    if not features.get('has_uppercase', False):
        if len(improved) > 0:
            improved = improved[0].upper() + improved[1:]
    
    # Add numbers if missing
    if not features.get('has_digit', False):
        improved += "123"
    
    # Add special chars if missing
    if not features.get('has_special', False):
        improved += "!"
    
    # Ensure minimum length
    while len(improved) < 12:
        improved += str(random.randint(0, 9))
    
    # Replace some characters to add complexity
    char_map = {'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$', 't': '+'}
    for char, replacement in char_map.items():
        if char in improved.lower():
            improved = improved.replace(char, replacement, 1)
    
    reasoning = "The improved password is stronger because it "
    if improvements:
        reasoning += ", ".join(improvements).lower()
    else:
        reasoning += "adds complexity while maintaining memorability"
    
    return {
        "improved_password": improved,
        "reasoning": reasoning,
        "vulnerability_details": vulnerability_details if vulnerability_details else ["Generic password that could be susceptible to dictionary attacks"]
    }