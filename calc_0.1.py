"""
Simple Calculator With Unlimited Precision

This basic command-line calculator handles simple mathematical expressions with arbitrary precision. 
It works with basic math operators (+, -, *, /) and uses the Decimal class for unlimited precision. 
"""

from decimal import Decimal

def calculate(expression):
    """
    Calculates the simple mathematical expression and returns the answer
    """
    try:
        # Split the string on spaces into numbers and operators
        parts = expression.split()
        if len(parts) != 3:
            return "Entry Error: Please enter the math problem in this format: (number operator number)"

        # Assign the expressions factors to 
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
                return "Error: Can't divide by zero."
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
    Calculator Instructions.
    """
    print("\n----- Calculator Instructions -----")
    print("Enter your calculation in the format:")
    print("  number operator number")
    print("Supported operators: +, -, *, /")
    print("Examples:")
    print("  5 + 3")
    print("  10.5 - 2.7")
    print("  4 * 6")
    print("  15 / 3")
    print("Enter 'quit' to exit the calculator.")
    print("-----------------------------------")

# Main loop
if __name__ == "__main__":
    print("Welcome to the Simple Unlimited Precision Calculator!")
    display_instructions()

    while True:
        user_input = input("\nEnter a calculation (or 'quit' to exit): ").strip().lower()
        if user_input == 'quit':
            print("Closing calculator. Goodbye!")
            break
        print(calculate(user_input))