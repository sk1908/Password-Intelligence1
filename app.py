import os
import logging
from flask import Flask, render_template, request, jsonify, session
from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from ai_suggestions import get_ai_suggestions
from translations import get_strength_label, get_time_unit, get_ui_text

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "password-guardian-secret")

# Initialize password analyzer and generator
password_analyzer = PasswordAnalyzer()
password_generator = PasswordGenerator()

# List of supported languages
SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'zh', 'ja', 'ru']

@app.route('/')
def index():
    """Render the main application page"""
    # Get language from the query parameter or default to English
    language = request.args.get('lang', 'en')
    if language not in SUPPORTED_LANGUAGES:
        language = 'en'
    
    # Store the language in session for subsequent requests
    session['language'] = language
    
    return render_template('index.html', language=language)

@app.route('/about')
def about():
    """Render the about page"""
    language = session.get('language', 'en')
    return render_template('about.html', language=language)

@app.route('/analyze_password', methods=['POST'])
def analyze_password():
    """Analyze the submitted password and return detailed feedback"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        language = data.get('language', session.get('language', 'en'))
        
        # Ensure language is supported
        if language not in SUPPORTED_LANGUAGES:
            language = 'en'
        
        if not password:
            return jsonify({'error': 'No password provided'}), 400
        
        # Get the basic analysis results
        results = password_analyzer.analyze(password)
        
        # Localize strength labels
        results['strength_label'] = get_strength_label(results.get('score', 0), language)
        
        # Localize time to crack units if present
        if 'crack_time' in results and 'unit' in results['crack_time']:
            results['crack_time']['unit'] = get_time_unit(results['crack_time']['unit'], language)
        
        # Get AI-powered improvement suggestions with language support
        suggestions = get_ai_suggestions(password, results, language)
        
        # Combine the results
        complete_results = {**results, 'suggestions': suggestions}
        
        # Add UI text in the selected language
        complete_results['ui_text'] = {
            'loading': get_ui_text('loading', language),
            'error': get_ui_text('error', language),
            'improved_heading': get_ui_text('improved_heading', language),
            'vulnerability_heading': get_ui_text('vulnerability_heading', language),
            'reason_heading': get_ui_text('reason_heading', language)
        }
        
        return jsonify(complete_results)
    except Exception as e:
        logger.error(f"Error analyzing password: {e}")
        return jsonify({'error': 'Failed to analyze password'}), 500

@app.route('/generate_password', methods=['POST'])
def generate_password():
    """Generate a strong password based on user preferences"""
    try:
        data = request.get_json()
        length = int(data.get('length', 16))
        include_uppercase = data.get('include_uppercase', True)
        include_lowercase = data.get('include_lowercase', True)
        include_numbers = data.get('include_numbers', True)
        include_symbols = data.get('include_symbols', True)
        min_entropy = int(float(data.get('min_entropy', 80)))
        language = data.get('language', session.get('language', 'en'))
        
        # Ensure language is supported
        if language not in SUPPORTED_LANGUAGES:
            language = 'en'
        
        password = password_generator.generate(
            length=length,
            include_uppercase=include_uppercase,
            include_lowercase=include_lowercase,
            include_numbers=include_numbers,
            include_symbols=include_symbols,
            min_entropy=min_entropy
        )
        
        # Analyze the generated password
        analysis = password_analyzer.analyze(password)
        
        # Localize strength labels
        analysis['strength_label'] = get_strength_label(analysis.get('score', 0), language)
        
        # Localize time to crack units if present
        if 'crack_time' in analysis and 'unit' in analysis['crack_time']:
            analysis['crack_time']['unit'] = get_time_unit(analysis['crack_time']['unit'], language)
        
        return jsonify({
            'password': password,
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error generating password: {e}")
        return jsonify({'error': 'Failed to generate password'}), 500

@app.route('/languages')
def get_languages():
    """Get the list of supported languages"""
    return jsonify({
        'languages': [
            {'code': 'en', 'name': 'English'},
            {'code': 'es', 'name': 'Español (Spanish)'},
            {'code': 'fr', 'name': 'Français (French)'},
            {'code': 'de', 'name': 'Deutsch (German)'},
            {'code': 'zh', 'name': '中文 (Chinese)'},
            {'code': 'ja', 'name': '日本語 (Japanese)'},
            {'code': 'ru', 'name': 'Русский (Russian)'}
        ],
        'current': session.get('language', 'en')
    })

@app.route('/set_language', methods=['POST'])
def set_language():
    """Set the user's preferred language"""
    data = request.get_json()
    language = data.get('language', 'en')
    
    if language not in SUPPORTED_LANGUAGES:
        language = 'en'
    
    session['language'] = language
    return jsonify({'success': True, 'language': language})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
