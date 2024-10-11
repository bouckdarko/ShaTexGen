# ShaTexGen

**ShaTexGen** est un générateur de variations de texte qui permet de créer automatiquement des déclinaisons d'un mot ou d'une phrase, avec des options personnalisables telles que les caractères spéciaux, les abréviations courantes, les synonymes, et bien plus encore.

## Fonctionnalités

- **Leet Speak (1337)** : Convertit des lettres en leur équivalent Leet (ex. : "a" devient "4", "e" devient "3").
- **Variations de casse** : Génère des variations en majuscule, minuscule, camelCase, etc.
- **Abréviations courantes** : Remplace des expressions par leurs abréviations (ex. : "par exemple" devient "p.ex.").
- **Synonymes** : Remplace certains mots par leurs synonymes.
- **Caractères spéciaux** : Ajoute des caractères spéciaux avant ou après les mots/phrases.
- **Redoublement de lettres** : Crée des variations avec des lettres doublées ou triplées.
- **Suppression des voyelles** : Génère des versions abrégées en supprimant les voyelles.
- **Accents** : Ajoute ou enlève des accents sur certaines lettres.
- **Chiffres aléatoires** : Ajoute des chiffres au début ou à la fin du texte.
- **Inversion des mots dans une phrase** : Retourne l'ordre des mots dans une phrase.

## Prérequis

Ce projet fonctionne avec Python 3.6 ou supérieur. Aucun package externe n'est requis pour exécuter le script principal.

## Installation

1. Clonez le dépôt GitHub :

```bash
git clone https://github.com/tonutilisateur/ShaTexGen.git
cd ShaTexGen
python sha_tex_gen.py "votre texte ici" -o variations.txt -n variations