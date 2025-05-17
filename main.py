import json
import re

def generate_crossword_prompt(theme, language):
    prompt = f"""
You are an AI crossword generator. Your task is to create a thematic crossword puzzle in JSON format. The theme is '{theme}' and the language is '{language}'.

Please adhere strictly to the following JSON structure:

{{
  "cols": 13,
  "rows": 13,
  "cells": [
    "R","E","Y","","H","I","J","O","N","","","","",
    "","","","A","B","C","","D","E","F","","","","",
    ...
  ],
  "words": [
    "0,1,2",
    "4,5,6,7",
    ...
  ],
  "questions": [
    "I have set my ___ upon Zion",
    "My ___ you are",
    ...
  ]
}}

Guidelines:
- 'cols' and 'rows' must be integers between 10 and 15.
- 'cells' must be a list of length 'cols' × 'rows', containing uppercase letters or empty strings ("").
- Each entry in 'words' must be a string of comma-separated integers representing consecutive positions in 'cells' (either horizontal or vertical).
- 'questions' must be a list of clues corresponding to each word in 'words'.
- The lengths of 'words' and 'questions' must be equal.

Ensure that the JSON is syntactically valid and all fields meet the specified criteria.
"""
    return prompt.strip()

def validate_crossword_json(crossword_json):
    try:
        data = json.loads(crossword_json)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    cols = data.get("cols")
    rows = data.get("rows")
    cells = data.get("cells")
    words = data.get("words")
    questions = data.get("questions")

    if not isinstance(cols, int) or not isinstance(rows, int):
        return False, "Cols and rows must be integers."

    if not (10 <= cols <= 15) or not (10 <= rows <= 15):
        return False, "Cols and rows must be between 10 and 15."

    if not isinstance(cells, list) or len(cells) != cols * rows:
        return False, "Cells must be a list of length cols × rows."

    if not all(isinstance(cell, str) and (cell.isupper() or cell == "") for cell in cells):
        return False, "Each cell must be an uppercase letter or an empty string."

    if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
        return False, "Words must be a list of strings."

    if not isinstance(questions, list) or not all(isinstance(q, str) for q in questions):
        return False, "Questions must be a list of strings."

    if len(words) != len(questions):
        return False, "The number of words and questions must be equal."

    for word in words:
        positions = list(map(int, word.split(',')))
        if not positions:
            return False, "Each word must have at least one position."

        # Check if positions are consecutive horizontally or vertically
        diffs = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
        if all(diff == 1 for diff in diffs):
            continue  # Horizontal
        elif all(diff == cols for diff in diffs):
            continue  # Vertical
        else:
            return False, f"Word positions {positions} are not consecutive horizontally or vertically."

    return True, "Valid crossword JSON."

def main():
    theme = input("Enter the theme of the crossword puzzle: ")
    language = input("Enter the language of the crossword puzzle: ")

    prompt = generate_crossword_prompt(theme, language)
    print("\nGenerated Prompt:\n")
    print(prompt)

    # The user would input the generated JSON from Claude here
    crossword_json = input("\nPaste the generated crossword JSON here:\n")

    is_valid, message = validate_crossword_json(crossword_json)
    if is_valid:
        print("\nThe generated crossword JSON is valid.")
    else:
        print(f"\nValidation Error: {message}")

if __name__ == "__main__":
    main()
