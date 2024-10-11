import pytest
from ShaTexGen import generate_word_variations, generate_sentence_variations

@pytest.fixture
def default_options():
    return {
        'leet': True,
        'abbreviations': False,
        'synonyms': False,
        'special_chars': True,
        'case': True,
        'accents': True,
        'remove_vowels': True
    }

# Test de la génération de variations pour un mot simple
def test_generate_word_variations_basic(default_options):
    word = "test"
    variations = generate_word_variations(word, default_options)
    
    assert "Test" in variations
    assert "TEST" in variations
    assert "t3st" in variations  # Leet Speak
    assert "tst" in variations   # Suppression des voyelles
    assert "*test" in variations  # Caractères spéciaux

# Test de la gestion des accents
def test_generate_word_variations_accents(default_options):
    word = "facade"
    variations = generate_word_variations(word, default_options)
    
    assert "façade" in variations  # Ajout d'accents
    assert "facade" in variations  # Version sans accent

# Test de la génération avec des chiffres aléatoires
def test_generate_word_variations_with_numbers(default_options):
    word = "hello"
    variations = generate_word_variations(word, default_options)
    
    assert any(variation.startswith('hello') and variation[-2:].isdigit() for variation in variations)
    assert any(variation.endswith('hello') and variation[:2].isdigit() for variation in variations)

# Test de la génération de variations pour une phrase
def test_generate_sentence_variations_basic(default_options):
    sentence = "bonjour le monde"
    variations = generate_sentence_variations(sentence, default_options)
    
    assert "Bonjour Le Monde" in variations  # Variation de casse
    assert "b0nj0ur le monde" in variations  # Leet Speak
    assert "bonjour_le_monde" in variations  # Remplacement des espaces par underscores

# Test de la génération avec des abréviations
def test_generate_sentence_with_abbreviations():
    options = {
        'leet': False,
        'abbreviations': True,
        'synonyms': False,
        'special_chars': False,
        'case': False,
        'accents': False,
        'remove_vowels': False
    }
    sentence = "par exemple, s'il vous plaît"
    variations = generate_sentence_variations(sentence, options)
    
    assert "p.ex." in variations  # Abréviation de "par exemple"
    assert "svp" in variations    # Abréviation de "s'il vous plaît"

# Test de la génération avec des synonymes
def test_generate_sentence_with_synonyms():
    options = {
        'leet': False,
        'abbreviations': False,
        'synonyms': True,
        'special_chars': False,
        'case': False,
        'accents': False,
        'remove_vowels': False
    }
    sentence = "donne moi un exemple"
    variations = generate_sentence_variations(sentence, options)
    
    assert "donne moi une illustration" in variations  # Synonyme d'exemple
    assert "donne moi un exemple" in variations  # Version originale toujours présente

# Test pour les mots en camelCase
def test_generate_sentence_in_camel_case(default_options):
    sentence = "bonsoir tout le monde"
    variations = generate_sentence_variations(sentence, default_options)
    
    assert "BonsoirToutLeMonde" in variations  # camelCase

# Test des erreurs
def test_generate_with_invalid_input(default_options):
    with pytest.raises(ValueError):
        generate_word_variations("", default_options)
    
    with pytest.raises(ValueError):
        generate_word_variations(None, default_options)
