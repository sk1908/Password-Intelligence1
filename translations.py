"""
Module for managing translations for the password analyzer.
This provides translations for password feedback in multiple languages.
"""

# Dictionary of translations by language code
TRANSLATIONS = {
    'en': {  # English (default)
        'vulnerability_patterns': {
            'short_length': 'Short length makes it vulnerable to brute force attacks',
            'lacks_uppercase': 'Lacks uppercase letters',
            'lacks_numbers': 'Lacks numbers',
            'lacks_special': 'Lacks special characters',
            'common_password': 'This is a commonly used password that appears in data breaches',
            'dictionary_attack': 'Could be vulnerable to dictionary or brute force attacks'
        },
        'reasoning': {
            'default': 'This password has been improved by adding complexity while maintaining some recognizable elements.',
            'add_length': 'Increase length to at least 12 characters',
            'add_lowercase': 'Add lowercase letters',
            'add_uppercase': 'Add uppercase letters',
            'add_numbers': 'Add numbers',
            'add_special': 'Add special characters'
        },
        'strength_labels': {
            'very_weak': 'Very Weak',
            'weak': 'Weak',
            'moderate': 'Moderate',
            'strong': 'Strong',
            'very_strong': 'Very Strong'
        },
        'time_units': {
            'seconds': 'seconds',
            'minutes': 'minutes',
            'hours': 'hours',
            'days': 'days',
            'months': 'months',
            'years': 'years',
            'centuries': 'centuries'
        },
        'ui': {
            'loading': 'Our AI security advisor is analyzing your password...',
            'error': 'Could not load suggestions at this time.',
            'improved_heading': 'Suggested Improvement',
            'vulnerability_heading': 'Vulnerabilities Identified',
            'reason_heading': 'Why This Is Better'
        }
    },
    'es': {  # Spanish
        'vulnerability_patterns': {
            'short_length': 'La longitud corta lo hace vulnerable a ataques de fuerza bruta',
            'lacks_uppercase': 'Carece de letras mayúsculas',
            'lacks_numbers': 'Carece de números',
            'lacks_special': 'Carece de caracteres especiales',
            'common_password': 'Esta es una contraseña de uso común que aparece en filtraciones de datos',
            'dictionary_attack': 'Podría ser vulnerable a ataques de diccionario o fuerza bruta'
        },
        'reasoning': {
            'default': 'Esta contraseña se ha mejorado añadiendo complejidad mientras se mantienen algunos elementos reconocibles.',
            'add_length': 'Aumentar la longitud a al menos 12 caracteres',
            'add_lowercase': 'Añadir letras minúsculas',
            'add_uppercase': 'Añadir letras mayúsculas',
            'add_numbers': 'Añadir números',
            'add_special': 'Añadir caracteres especiales'
        },
        'strength_labels': {
            'very_weak': 'Muy Débil',
            'weak': 'Débil',
            'moderate': 'Moderada',
            'strong': 'Fuerte',
            'very_strong': 'Muy Fuerte'
        },
        'time_units': {
            'seconds': 'segundos',
            'minutes': 'minutos',
            'hours': 'horas',
            'days': 'días',
            'months': 'meses',
            'years': 'años',
            'centuries': 'siglos'
        },
        'ui': {
            'loading': 'Nuestro asesor de seguridad IA está analizando tu contraseña...',
            'error': 'No se pudieron cargar sugerencias en este momento.',
            'improved_heading': 'Mejora Sugerida',
            'vulnerability_heading': 'Vulnerabilidades Identificadas',
            'reason_heading': 'Por Qué Es Mejor'
        }
    },
    'fr': {  # French
        'vulnerability_patterns': {
            'short_length': 'Sa courte longueur le rend vulnérable aux attaques par force brute',
            'lacks_uppercase': 'Manque de lettres majuscules',
            'lacks_numbers': 'Manque de chiffres',
            'lacks_special': 'Manque de caractères spéciaux',
            'common_password': "C'est un mot de passe couramment utilisé qui apparaît dans les fuites de données",
            'dictionary_attack': 'Pourrait être vulnérable aux attaques par dictionnaire ou force brute'
        },
        'reasoning': {
            'default': 'Ce mot de passe a été amélioré en ajoutant de la complexité tout en conservant certains éléments reconnaissables.',
            'add_length': 'Augmenter la longueur à au moins 12 caractères',
            'add_lowercase': 'Ajouter des lettres minuscules',
            'add_uppercase': 'Ajouter des lettres majuscules',
            'add_numbers': 'Ajouter des chiffres',
            'add_special': 'Ajouter des caractères spéciaux'
        },
        'strength_labels': {
            'very_weak': 'Très Faible',
            'weak': 'Faible',
            'moderate': 'Modéré',
            'strong': 'Fort',
            'very_strong': 'Très Fort'
        },
        'time_units': {
            'seconds': 'secondes',
            'minutes': 'minutes',
            'hours': 'heures',
            'days': 'jours',
            'months': 'mois',
            'years': 'années',
            'centuries': 'siècles'
        },
        'ui': {
            'loading': 'Notre conseiller en sécurité IA analyse votre mot de passe...',
            'error': 'Impossible de charger les suggestions pour le moment.',
            'improved_heading': 'Amélioration Suggérée',
            'vulnerability_heading': 'Vulnérabilités Identifiées',
            'reason_heading': 'Pourquoi C\'est Mieux'
        }
    },
    'de': {  # German
        'vulnerability_patterns': {
            'short_length': 'Kurze Länge macht es anfällig für Brute-Force-Angriffe',
            'lacks_uppercase': 'Enthält keine Großbuchstaben',
            'lacks_numbers': 'Enthält keine Zahlen',
            'lacks_special': 'Enthält keine Sonderzeichen',
            'common_password': 'Dies ist ein häufig verwendetes Passwort, das in Datenlecks vorkommt',
            'dictionary_attack': 'Könnte anfällig für Wörterbuch- oder Brute-Force-Angriffe sein'
        },
        'reasoning': {
            'default': 'Dieses Passwort wurde verbessert, indem Komplexität hinzugefügt wurde, während einige erkennbare Elemente erhalten blieben.',
            'add_length': 'Erhöhen Sie die Länge auf mindestens 12 Zeichen',
            'add_lowercase': 'Fügen Sie Kleinbuchstaben hinzu',
            'add_uppercase': 'Fügen Sie Großbuchstaben hinzu',
            'add_numbers': 'Fügen Sie Zahlen hinzu',
            'add_special': 'Fügen Sie Sonderzeichen hinzu'
        },
        'strength_labels': {
            'very_weak': 'Sehr Schwach',
            'weak': 'Schwach',
            'moderate': 'Mittel',
            'strong': 'Stark',
            'very_strong': 'Sehr Stark'
        },
        'time_units': {
            'seconds': 'Sekunden',
            'minutes': 'Minuten',
            'hours': 'Stunden',
            'days': 'Tage',
            'months': 'Monate',
            'years': 'Jahre',
            'centuries': 'Jahrhunderte'
        },
        'ui': {
            'loading': 'Unser KI-Sicherheitsberater analysiert Ihr Passwort...',
            'error': 'Vorschläge konnten derzeit nicht geladen werden.',
            'improved_heading': 'Vorgeschlagene Verbesserung',
            'vulnerability_heading': 'Identifizierte Schwachstellen',
            'reason_heading': 'Warum Dies Besser Ist'
        }
    },
    'zh': {  # Chinese (Simplified)
        'vulnerability_patterns': {
            'short_length': '长度短使其容易受到暴力攻击',
            'lacks_uppercase': '缺少大写字母',
            'lacks_numbers': '缺少数字',
            'lacks_special': '缺少特殊字符',
            'common_password': '这是一个常用密码，出现在数据泄露中',
            'dictionary_attack': '可能容易受到字典或暴力攻击'
        },
        'reasoning': {
            'default': '通过增加复杂性同时保留一些可识别的元素，此密码已得到改进。',
            'add_length': '将长度增加到至少12个字符',
            'add_lowercase': '添加小写字母',
            'add_uppercase': '添加大写字母',
            'add_numbers': '添加数字',
            'add_special': '添加特殊字符'
        },
        'strength_labels': {
            'very_weak': '非常弱',
            'weak': '弱',
            'moderate': '中等',
            'strong': '强',
            'very_strong': '非常强'
        },
        'time_units': {
            'seconds': '秒',
            'minutes': '分钟',
            'hours': '小时',
            'days': '天',
            'months': '月',
            'years': '年',
            'centuries': '世纪'
        },
        'ui': {
            'loading': '我们的AI安全顾问正在分析您的密码...',
            'error': '目前无法加载建议。',
            'improved_heading': '建议改进',
            'vulnerability_heading': '已识别的漏洞',
            'reason_heading': '为什么这更好'
        }
    },
    'ja': {  # Japanese
        'vulnerability_patterns': {
            'short_length': '短い長さによりブルートフォース攻撃に弱いです',
            'lacks_uppercase': '大文字がありません',
            'lacks_numbers': '数字がありません',
            'lacks_special': '特殊文字がありません',
            'common_password': 'これはデータ漏洩で見られる一般的なパスワードです',
            'dictionary_attack': '辞書攻撃やブルートフォース攻撃に弱い可能性があります'
        },
        'reasoning': {
            'default': 'このパスワードは、認識可能な要素を維持しながら複雑さを追加することで改善されました。',
            'add_length': '長さを少なくとも12文字に増やす',
            'add_lowercase': '小文字を追加する',
            'add_uppercase': '大文字を追加する',
            'add_numbers': '数字を追加する',
            'add_special': '特殊文字を追加する'
        },
        'strength_labels': {
            'very_weak': '非常に弱い',
            'weak': '弱い',
            'moderate': '普通',
            'strong': '強い',
            'very_strong': '非常に強い'
        },
        'time_units': {
            'seconds': '秒',
            'minutes': '分',
            'hours': '時間',
            'days': '日',
            'months': '月',
            'years': '年',
            'centuries': '世紀'
        },
        'ui': {
            'loading': 'AIセキュリティアドバイザーがパスワードを分析しています...',
            'error': '現在、提案を読み込むことができません。',
            'improved_heading': '提案された改善',
            'vulnerability_heading': '特定された脆弱性',
            'reason_heading': 'なぜこれが良いのか'
        }
    },
    'ru': {  # Russian
        'vulnerability_patterns': {
            'short_length': 'Короткая длина делает его уязвимым для атак методом перебора',
            'lacks_uppercase': 'Отсутствуют заглавные буквы',
            'lacks_numbers': 'Отсутствуют цифры',
            'lacks_special': 'Отсутствуют специальные символы',
            'common_password': 'Это часто используемый пароль, который встречается в утечках данных',
            'dictionary_attack': 'Может быть уязвим для словарных атак или атак методом перебора'
        },
        'reasoning': {
            'default': 'Этот пароль был улучшен путем добавления сложности при сохранении некоторых узнаваемых элементов.',
            'add_length': 'Увеличьте длину до не менее 12 символов',
            'add_lowercase': 'Добавьте строчные буквы',
            'add_uppercase': 'Добавьте заглавные буквы',
            'add_numbers': 'Добавьте цифры',
            'add_special': 'Добавьте специальные символы'
        },
        'strength_labels': {
            'very_weak': 'Очень Слабый',
            'weak': 'Слабый',
            'moderate': 'Средний',
            'strong': 'Сильный',
            'very_strong': 'Очень Сильный'
        },
        'time_units': {
            'seconds': 'секунд',
            'minutes': 'минут',
            'hours': 'часов',
            'days': 'дней',
            'months': 'месяцев',
            'years': 'лет',
            'centuries': 'веков'
        },
        'ui': {
            'loading': 'Наш ИИ-консультант по безопасности анализирует ваш пароль...',
            'error': 'Не удалось загрузить предложения в данный момент.',
            'improved_heading': 'Предлагаемое Улучшение',
            'vulnerability_heading': 'Выявленные Уязвимости',
            'reason_heading': 'Почему Это Лучше'
        }
    }
}

def get_translation(text_key, category, language='en'):
    """
    Get the translation for a specific text key in the given language.
    
    Args:
        text_key: The key of the text to translate
        category: The category of text (vulnerability_patterns, reasoning, etc.)
        language: Language code (default: 'en')
        
    Returns:
        Translated text string
    """
    # If the language is not supported, fall back to English
    if language not in TRANSLATIONS:
        language = 'en'
        
    # Get the translation category
    category_dict = TRANSLATIONS[language].get(category, {})
    
    # Return the translated text or the key itself if not found
    return category_dict.get(text_key, text_key)

def localize_suggestions(suggestions, language='en'):
    """
    Localize the suggestions data structure to the specified language.
    
    Args:
        suggestions: Dictionary with suggestion data
        language: Language code (default: 'en')
        
    Returns:
        Dictionary with localized suggestion data
    """
    if not suggestions:
        return suggestions
        
    # Create a new dictionary for localized suggestions
    localized = {
        "improved_password": suggestions.get("improved_password", ""),
        "reasoning": "",
        "vulnerability_details": []
    }
    
    # Try to translate the reasoning
    reasoning = suggestions.get("reasoning", "")
    if reasoning:
        # Check if reasoning matches any known patterns
        matched = False
        for key, text in TRANSLATIONS['en']['reasoning'].items():
            if reasoning.lower().startswith(text.lower()):
                localized["reasoning"] = get_translation(key, 'reasoning', language)
                matched = True
                break
                
        # If no match, use the original reasoning
        if not matched:
            localized["reasoning"] = reasoning
    
    # Try to translate vulnerability details
    for detail in suggestions.get("vulnerability_details", []):
        translated = False
        for key, text in TRANSLATIONS['en']['vulnerability_patterns'].items():
            if detail.lower() == text.lower():
                localized["vulnerability_details"].append(get_translation(key, 'vulnerability_patterns', language))
                translated = True
                break
                
        # If no match, use the original detail
        if not translated:
            localized["vulnerability_details"].append(detail)
            
    return localized

def get_ui_text(key, language='en'):
    """
    Get UI text in the specified language.
    
    Args:
        key: UI text key
        language: Language code (default: 'en')
        
    Returns:
        Translated UI text
    """
    return get_translation(key, 'ui', language)

def get_strength_label(strength, language='en'):
    """
    Get localized password strength label based on strength score.
    
    Args:
        strength: Strength score (0-100)
        language: Language code (default: 'en')
        
    Returns:
        Localized strength label
    """
    if strength < 20:
        label = 'very_weak'
    elif strength < 40:
        label = 'weak'
    elif strength < 60:
        label = 'moderate'
    elif strength < 80:
        label = 'strong'
    else:
        label = 'very_strong'
        
    return get_translation(label, 'strength_labels', language)

def get_time_unit(unit, language='en'):
    """
    Get localized time unit.
    
    Args:
        unit: Time unit key (seconds, minutes, hours, etc.)
        language: Language code (default: 'en')
        
    Returns:
        Localized time unit
    """
    return get_translation(unit, 'time_units', language)