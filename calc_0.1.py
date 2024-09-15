"""
Calculator With Unlimited Precision History Logging

This script provides a simple string based command line calculator with 
arbitrary precision. It supports basic math operations (+, -, *, /)
and uses the Decimal class for unlimited precision. It will log all the
interactions to a JSON-based calculator history file. This file will 
be maintained under 50MB and formatted for human readability.

Author: Tim Kitterman
Date: 15 Sept 2024
"""

import json
from decimal import Decimal
from datetime import datetime
from pathlib import Path

# Constants
HISTORY_FILE = Path(__file__).parent / "calculator_history.json"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes

# ANSI escape codes for text formatting
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

def manage_history(content_type, content):
    """
    Manages the JSON-based history file for the calculator.

    It loads existing history from JSON file or initializes an empty list if the file doesn't exist.
    Then it appends a new entry with timestamp, content type, and content.
    It ensures the history file stays under the MAX_FILE_SIZE by removing oldest entries if necessary.
    Saves the updated history back to the JSON file in a human-readable format.

    Args:
    content_type (str): The type of content being logged (e.g., "USER_INPUT", "CALCULATION").
    content (str): The actual content to be logged.

    Returns:
    list: The updated history list.
    """
    try:
        # Load existing history or create an empty list
        history = json.loads(HISTORY_FILE.read_text()) if HISTORY_FILE.exists() else []

        # Create and append new history entry
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "content_type": content_type,
            "content": content
        }
        history.append(new_entry)

        # Maintain file size limit by removing oldest entries if necessary
        while len(json.dumps(history, indent=2).encode('utf-8')) > MAX_FILE_SIZE and history:
            history.pop(0)

        # Save updated history in a human-readable JSON format
        HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False))

        return history
    except Exception as e:
        print(f"Error managing history file: {e}")
        return []

def calculate(expression):
    """
    Evaluates a simple mathematical expression and returns the result.

    Supports basic arithmetic operations (+, -, *, /) with arbitrary precision
    using the Decimal class.

    Args:
    expression (str): A string containing two numbers and an operator, space-separated.

    Returns:
    str: The result of the calculation or an error message.
    """
    try:
        parts = expression.split()
        if len(parts) != 3:
            return "Entry Error: Please enter the math problem in this format: (number operator number)"

        num1, operator, num2 = parts
        num1, num2 = Decimal(num1), Decimal(num2)

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Error: Cannot divide by zero."
            result = num1 / num2
        else:
            return f"Error: Unknown operator '{operator}'"

        return f"Result: {result}"
    except ValueError:
        return "Error: Invalid number format"
    except Exception as e:
        return f"Error: {str(e)}"

def display_instructions():
    """
    Displays formatted usage instructions for the calculator.
    
    Also logs the instructions to the history file.
    """
    instructions = f"""
{BOLD}===== Calculator Instructions ====={END}

Enter your calculation in the format:
    {UNDERLINE}number{END} {UNDERLINE}operator{END} {UNDERLINE}number{END}

Supported operators: +, -, *, /

Examples:
    5 + 3
    10.5 - 2.7
    4 * 6
    15 / 3

Type 'quit' to exit the calculator.
Type 'help' to see these instructions again.

{BOLD}==================================={END}
"""
    print(instructions)
    manage_history("INSTRUCTIONS", instructions)

def main():
    """
    Main function to run the calculator.

    Handles user input, performs calculations, and manages the program flow.
    All interactions are logged to the history file.
    """
    welcome_message = f"{BOLD}Welcome to the Unlimited Precision Calculator!{END}"
    print(welcome_message)
    manage_history("START", "Started calculator")
    
    display_instructions()

    while True:
        user_input = input(f"\n{BOLD}Enter a calculation (or 'quit' to exit): {END}").strip().lower()
        manage_history("USER_INPUT", user_input)
        
        if user_input in ('quit', 'exit'):
            goodbye_message = f"{BOLD}Thank you for using the calculator. Goodbye!{END}"
            print(goodbye_message)
            manage_history("END", "Closed calculator")
            break
        elif user_input == 'help':
            display_instructions()
        else:
            result = calculate(user_input)
            print(result)
            manage_history("CALCULATION", f"{user_input} = {result}")

if __name__ == "__main__":
    main()