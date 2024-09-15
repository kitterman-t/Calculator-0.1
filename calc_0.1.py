"""
Calculator With Unlimited Precision and History Logging

This script provides a command-line calculator that handles simple mathematical
expressions with arbitrary precision. It supports basic math operators (+, -, *, /)
and uses the Decimal class for unlimited precision. Additionally, it logs all
interactions to a history file, maintaining the file size under 50MB.

Author: Tim Kitterman
Date: 15 Sept 2024
"""

import os
from decimal import Decimal
from datetime import datetime
from pathlib import Path

# Constants
HISTORY_FILE = Path(__file__).parent / "calculator_history.txt"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes

# Basic text formatting
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

def log_to_history(content):
    """
    Logs content to the history file, maintaining the file size under MAX_FILE_SIZE.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {content}\n"
    
    try:
        # Read existing content if file exists
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r') as f:
                lines = f.readlines()
        else:
            lines = []

        # Add new log entry
        lines.append(log_entry)

        # Remove oldest entries if necessary
        while sum(len(line) for line in lines) > MAX_FILE_SIZE:
            lines.pop(0)

        # Write updated content back to file
        with open(HISTORY_FILE, 'w') as f:
            f.writelines(lines)
    except IOError as e:
        print(f"Error writing to history file: {e}")

def calculate(expression):
    """
    Calculates the simple mathematical expression and returns the answer.
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
    Displays calculator instructions with improved formatting.
    """
    instructions = f"""
{BOLD}===== Calculator Instructions ====={END}

Enter your calculation in the format:
    {UNDERLINE}number operator number{END}

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
    log_to_history("Displayed instructions")

def main():
    """
    Main function to run the calculator.
    """
    welcome_message = f"{BOLD}Welcome to the Unlimited Precision Calculator!{END}"
    print(welcome_message)
    log_to_history("Started calculator")
    
    display_instructions()

    while True:
        user_input = input(f"\n{BOLD}Enter a calculation (or 'quit' to exit): {END}").strip().lower()
        log_to_history(f"User Input: {user_input}")
        
        if user_input == 'quit':
            goodbye_message = f"{BOLD}Thank you for using the calculator. Goodbye!{END}"
            print(goodbye_message)
            log_to_history("Closed calculator")
            break
        elif user_input == 'help':
            display_instructions()
        else:
            result = calculate(user_input)
            print(result)
            log_to_history(f"Calculation: {user_input} = {result}")

if __name__ == "__main__":
    main()