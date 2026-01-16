"""
Calculator Backend Module
Handles basic arithmetic operations and full expression evaluation with PEMDAS.
"""

import re
import math


class Calculator:
    """Calculator with arithmetic operations and PEMDAS expression support."""

    def __init__(self):
        self.last_result = 0
        # Safe math context for expression evaluation
        self.math_context = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e,
        }

    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        result = a + b
        self.last_result = result
        return result

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        result = a - b
        self.last_result = result
        return result

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        result = a * b
        self.last_result = result
        return result

    def divide(self, a: float, b: float) -> float:
        """
        Divide a by b.

        Raises:
            ValueError: If attempting to divide by zero.
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.last_result = result
        return result

    def clear(self) -> None:
        """Reset the last result."""
        self.last_result = 0

    def calculate(self, a: float, operator: str, b: float) -> float:
        """
        Perform a calculation based on the operator.

        Args:
            a: First operand
            operator: One of '+', '-', '*', '/'
            b: Second operand

        Returns:
            The result of the calculation

        Raises:
            ValueError: If operator is invalid or division by zero
        """
        operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
        }

        if operator not in operations:
            raise ValueError(f"Invalid operator: {operator}")

        return operations[operator](a, b)

    def _prepare_expression(self, expression: str) -> str:
        """
        Prepare an expression string for evaluation.
        Converts user-friendly syntax to Python syntax.

        Args:
            expression: Raw expression string from user

        Returns:
            Python-evaluatable expression string
        """
        expr = expression.strip()

        # Replace ^ with ** for exponentiation
        expr = re.sub(r'\^', '**', expr)

        # Replace × with * and ÷ with /
        expr = expr.replace('×', '*').replace('÷', '/')

        # Handle implicit multiplication: 2(3+4) -> 2*(3+4), (2)(3) -> (2)*(3)
        expr = re.sub(r'(\d)(\()', r'\1*\2', expr)  # 2( -> 2*(
        expr = re.sub(r'(\))(\d)', r'\1*\2', expr)  # )2 -> )*2
        expr = re.sub(r'(\))(\()', r'\1*\2', expr)  # )( -> )*(

        return expr

    def _validate_expression(self, expression: str) -> bool:
        """
        Validate that an expression only contains allowed characters.

        Args:
            expression: Expression to validate

        Returns:
            True if valid, raises ValueError if invalid
        """
        # Allow: digits, operators, parentheses, decimal points, spaces, and math functions
        allowed_pattern = r'^[\d\+\-\*\/\^\(\)\.\s\,piePIesqrtabsroundminmax]+$'

        if not re.match(allowed_pattern, expression):
            # Find the invalid characters
            invalid = re.sub(r'[\d\+\-\*\/\^\(\)\.\s\,piePIesqrtabsroundminmax]', '', expression)
            raise ValueError(f"Invalid characters in expression: {invalid}")

        # Check for balanced parentheses
        paren_count = 0
        for char in expression:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            if paren_count < 0:
                raise ValueError("Unbalanced parentheses: extra closing parenthesis")

        if paren_count != 0:
            raise ValueError("Unbalanced parentheses: missing closing parenthesis")

        return True

    def evaluate_expression(self, expression: str) -> float:
        """
        Evaluate a mathematical expression following PEMDAS rules.

        Supports:
        - Parentheses: (2+3)*4
        - Exponents: 2^3 or 2**3
        - Multiplication/Division: 2*3, 6/2
        - Addition/Subtraction: 2+3, 5-2
        - Nested expressions: ((2+3)*4)^2

        Args:
            expression: Mathematical expression string

        Returns:
            The result of the evaluation

        Raises:
            ValueError: If expression is invalid or cannot be evaluated

        Examples:
            >>> calc.evaluate_expression("2+3*4")
            14.0
            >>> calc.evaluate_expression("(2+3)*4")
            20.0
            >>> calc.evaluate_expression("2^3+1")
            9.0
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")

        # Prepare the expression
        prepared = self._prepare_expression(expression)

        # Validate the expression
        self._validate_expression(expression)

        try:
            # Evaluate using Python's eval with restricted context
            # Python naturally follows PEMDAS (operator precedence)
            result = eval(prepared, {"__builtins__": {}}, self.math_context)

            if not isinstance(result, (int, float)):
                raise ValueError("Expression did not evaluate to a number")

            if math.isnan(result) or math.isinf(result):
                raise ValueError("Result is undefined (infinity or NaN)")

            self.last_result = float(result)
            return self.last_result

        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except SyntaxError:
            raise ValueError("Invalid expression syntax")
        except Exception as e:
            raise ValueError(f"Could not evaluate expression: {str(e)}")


if __name__ == "__main__":
    # Quick tests
    calc = Calculator()

    print("Basic operations:")
    print(f"  5 + 3 = {calc.add(5, 3)}")
    print(f"  10 - 4 = {calc.subtract(10, 4)}")
    print(f"  6 * 7 = {calc.multiply(6, 7)}")
    print(f"  15 / 3 = {calc.divide(15, 3)}")

    print("\nPEMDAS Expression tests:")
    tests = [
        ("2+3*4", 14),           # Multiplication before addition
        ("(2+3)*4", 20),         # Parentheses first
        ("2^3", 8),              # Exponent
        ("2^3+1", 9),            # Exponent before addition
        ("10-2*3", 4),           # Multiplication before subtraction
        ("(10-2)*3", 24),        # Parentheses first
        ("2+3*4-5/5", 13),       # Mixed operations
        ("((2+3)*2)^2", 100),    # Nested parentheses
        ("10/2/5", 1),           # Left to right for same precedence
        ("2^2^3", 256),          # Right to left for exponents (2^8)
        ("(1+2)*(3+4)", 21),     # Multiple parentheses groups
    ]

    for expr, expected in tests:
        result = calc.evaluate_expression(expr)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {expr} = {result} (expected {expected})")
