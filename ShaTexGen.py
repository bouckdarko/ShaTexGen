"""
Ce script génère diverses variations d'un mot ou d'une phrase en fonction de plusieurs options 
(personnalisation de la casse, ajout de caractères spéciaux, remplacement par des abréviations ou des synonymes, etc.).

Fonctionnalités :
- Génère des variations avec Leet Speak (1337).
- Applique des abréviations courantes (ex. : "par exemple" devient "p.ex.").
- Remplace des mots par leurs synonymes.
- Ajoute des caractères spéciaux avant et après les mots.
- Supprime ou redouble certaines lettres pour créer des variantes uniques.
- Gère les accents (ajout ou suppression).
- Génère des variations en camelCase.
- Ajoute des chiffres aléatoires au début ou à la fin des mots.

Utilisation :
1. En ligne de commande avec une entrée directe :
   python script.py "mot" -o variations.txt -n ma_liste

2. En mode interactif (sans argument) :
   python script.py
   Le script vous demandera des informations pour générer les variations.

Exemple de sortie :
Pour l'entrée "mot", la liste de variations peut inclure :
[
    'Mot', 'M0t', 'mot_', '*mot', 'MotMot', 'm0t12', 'moT'
]
"""

import argparse
import re
import random
import concurrent.futures
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fonction pour appliquer les remplacements dans un mot ou une phrase
def apply_replacements(text, replacements):
    text_list = list(text)
    for i, char in enumerate(text_list):
        if char in replacements:
            text_list[i] = replacements[char]
    return ''.join(text_list)

# Fonction pour valider l'entrée utilisateur
def validate_input(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        raise ValueError("L'entrée doit être une chaîne de caractères non vide.")

# Fonction pour gérer les accents
def handle_accents(word):
    accents = {"e": "é", "a": "à", "u": "ù", "c": "ç"}
    variations = set()
    for letter, accented in accents.items():
        if letter in word:
            variations.add(word.replace(letter, accented))
        if accented in word:
            variations.add(word.replace(accented, letter))
    return variations

# Fonction pour gérer le Leet Speak
def handle_leet_speak(word):
    leet_map = {"a": "4", "e": "3", "s": "$", "o": "0"}
    return apply_replacements(word, leet_map)

# Fonction pour générer des variations d'un mot
def generate_word_variations(word, options):
    variations = set()
    
    # Ajout de préfixes et suffixes
    prefixes_suffixes = ["", " ", "\t", "\n"]
    for prefix in prefixes_suffixes:
        for suffix in prefixes_suffixes:
            variations.add(f"{prefix}{word}{suffix}")
    
    # Variations de casse
    if options['case']:
        variations.add(word.lower())
        variations.add(word.upper())
        variations.add(word.capitalize())
        variations.add(word.title())
    
    # Variations avec des fautes de frappe
    if 'l' in word or 'n' in word:
        if 'l' in word:
            variations.add(re.sub(r'l+', 'l', word))
        if 'n' in word:
            variations.add(re.sub(r'n+', 'n', word))
    
    # Ajout de caractères spéciaux
    if options['special_chars']:
        special_chars = ["#", "*", "@", "!"]
        for char in special_chars:
            variations.add(f"{char}{word}")
            variations.add(f"{word}{char}")
    
    # Redoublement de lettres
    if len(word) > 1:
        variations.add(word + word[-1] * 2)
    
    # Suppression des voyelles
    if options['remove_vowels']:
        variations.add(re.sub(r'[aeiouAEIOU]', '', word))
    
    # Ajout de chiffres aléatoires
    random_number = random.randint(0, 99)
    variations.add(f"{word}{random_number}")
    variations.add(f"{random_number}{word}")
    
    # Gestion des accents
    if options['accents']:
        variations.update(handle_accents(word))
    
    # Gestion du Leet Speak
    if options['leet']:
        variations.add(handle_leet_speak(word))
    
    return list(variations)

# Fonction pour générer des variations d'une phrase
def generate_sentence_variations(sentence, options):
    variations = set()
    
    # Ajout de préfixes et suffixes
    prefixes_suffixes = ["", " ", "\t", "\n"]
    for prefix in prefixes_suffixes:
        for suffix in prefixes_suffixes:
            variations.add(f"{prefix}{sentence}{suffix}")
    
    # Variations de casse
    if options['case']:
        variations.add(sentence.lower())
        variations.add(sentence.upper())
        variations.add(sentence.capitalize())
        variations.add(sentence.title())
    
    # Variations avec des abréviations
    if options['abbreviations']:
        abbreviations = {
            "par exemple": "p.ex.",
            "c'est-à-dire": "c.-à-d.",
            "s'il vous plaît": "svp"
        }
        for word, abbr in abbreviations.items():
            if word in sentence:
                variations.add(sentence.replace(word, abbr))
    
    # Remplacement des espaces par des caractères spéciaux
    if options['special_chars']:
        special_chars = ["_", "-", "|"]
        for char in special_chars:
            variations.add(sentence.replace(" ", char))
    
    # Utilisation des synonymes
    if options['synonyms']:
        synonyms = {
            "information": "donnée",
            "exemple": "illustration"
        }
        for word, synonym in synonyms.items():
            if word in sentence:
                variations.add(sentence.replace(word, synonym))
    
    # Suppression des espaces (camelCase)
    camel_case = ''.join(word.capitalize() for word in sentence.split())
    variations.add(camel_case)
    
    # Gestion du Leet Speak
    if options['leet']:
        variations.add(handle_leet_speak(sentence))
    
    return list(variations)

# Fonction pour afficher les variations de manière plus lisible
def display_variations(variations):
    print("Variations générées :")
    for variation in variations:
        print(f"- {variation}")

# Fonction pour paralléliser la génération des variations
def parallel_variation_generation(user_input, options):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_variations = []
        if " " in user_input:
            future_variations.append(executor.submit(generate_sentence_variations, user_input, options))
        else:
            future_variations.append(executor.submit(generate_word_variations, user_input, options))
        results = [f.result() for f in future_variations]
    return results[0] if results else []

# Fonction principale avec options interactives
def main():
    parser = argparse.ArgumentParser(description="Générateur de variations de mots ou de phrases.")
    parser.add_argument("input", type=str, nargs="?", help="Le mot ou la phrase à varier.")
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier de sortie (avec une liste Python).")
    parser.add_argument("-n", "--name", type=str, help="Nom de la liste Python à générer dans le fichier de sortie.")
    args = parser.parse_args()
    
    # Options interactives
    if not args.input:
        user_input = input("Entrez un mot ou une phrase : ")
        use_leet = input("Voulez-vous générer des variations avec Leet Speak (1337) ? (oui/non) : ").strip().lower() == "oui"
        use_abbreviations = input("Voulez-vous utiliser des abréviations courantes ? (oui/non) : ").strip().lower() == "oui"
        use_synonyms = input("Voulez-vous utiliser des synonymes ? (oui/non) : ").strip().lower() == "oui"
        use_special_chars = input("Voulez-vous ajouter des caractères spéciaux ? (oui/non) : ").strip().lower() == "oui"
        use_case = input("Voulez-vous générer des variations de casse ? (oui/non) : ").strip().lower() == "oui"
        use_accents = input("Voulez-vous gérer les accents ? (oui/non) : ").strip().lower() == "oui"
        use_remove_vowels = input("Voulez-vous supprimer les voyelles pour certaines variations ? (oui/non) : ").strip().lower() == "oui"
    else:
        user_input = args.input
        use_leet = True
        use_abbreviations = True
        use_synonyms = True
        use_special_chars = True
        use_case = True
        use_accents = True
        use_remove_vowels = True
    
    options = {
        'leet': use_leet,
        'abbreviations': use_abbreviations,
        'synonyms': use_synonyms,
        'special_chars': use_special_chars,
        'case': use_case,
        'accents': use_accents,
        'remove_vowels': use_remove_vowels
    }
    
    # Valider l'entrée
    try:
        validate_input(user_input)
    except ValueError as e:
        logger.error(e)
        return

    # Générer les variations avec parallélisation
    logger.info("Début de la génération des variations.")
    variations = parallel_variation_generation(user_input, options)
    logger.info("Génération terminée.")
    
    # Affichage des variations
    display_variations(variations)
    
    # Sauvegarde dans un fichier si l'option est activée
    if args.output:
        list_name = args.name if args.name else "variations"
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(f"{list_name} = {variations}\n")
        logger.info(f"Les variations ont été écrites dans le fichier {args.output}.")

if __name__ == "__main__":
    main()
