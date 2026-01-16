"""
Grapher Backend Module
Handles function parsing and generating plot data for f(x) format functions.
"""

import math
import re
from typing import Tuple, List, Optional


class Grapher:
    """
    Parses mathematical functions in f(x)= format and generates plot data.

    Supported operations:
    - Basic arithmetic: +, -, *, /
    - Power: ^ or **
    - Trigonometric: sin, cos, tan
    - Square root: sqrt
    - Constants: pi, e
    """

    def __init__(self):
        # Math functions available for evaluation
        self.math_context = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'abs': abs,
            'pi': math.pi,
            'e': math.e,
        }

    def parse_function(self, func_string: str) -> str:
        """
        Parse a function string into an evaluatable Python expression.

        Args:
            func_string: Function in format "f(x)=expression" or just "expression"

        Returns:
            Cleaned expression ready for evaluation
        """
        # Remove "f(x)=" prefix if present
        expression = func_string.strip()
        if expression.lower().startswith('f(x)'):
            expression = expression[4:].lstrip('=').strip()

        # Replace ^ with ** for power operations
        expression = expression.replace('^', '**')

        # Handle implicit multiplication: 2x -> 2*x, 3sin(x) -> 3*sin(x)
        # Number followed by x
        expression = re.sub(r'(\d)([x])', r'\1*\2', expression)
        # Number followed by function
        expression = re.sub(r'(\d)(sin|cos|tan|sqrt)', r'\1*\2', expression)
        # x followed by (
        expression = re.sub(r'([x])(\()', r'\1*\2', expression)
        # ) followed by x or (
        expression = re.sub(r'(\))([x\(])', r'\1*\2', expression)
        # ) followed by number
        expression = re.sub(r'(\))(\d)', r'\1*\2', expression)

        return expression

    def evaluate(self, expression: str, x_value: float) -> Optional[float]:
        """
        Evaluate an expression for a given x value.

        Args:
            expression: Mathematical expression with x as variable
            x_value: The value to substitute for x

        Returns:
            The result of the evaluation, or None if evaluation fails
        """
        try:
            # Create evaluation context with x value
            context = self.math_context.copy()
            context['x'] = x_value

            # Evaluate the expression safely
            result = eval(expression, {"__builtins__": {}}, context)

            # Check for valid numeric result
            if isinstance(result, (int, float)) and not math.isnan(result) and not math.isinf(result):
                return float(result)
            return None

        except (ValueError, ZeroDivisionError, OverflowError, SyntaxError, NameError):
            return None

    def generate_plot_data(
        self,
        func_string: str,
        x_min: float = -10,
        x_max: float = 10,
        num_points: int = 500
    ) -> Tuple[List[float], List[float]]:
        """
        Generate x and y coordinates for plotting a function.

        Args:
            func_string: Function in format "f(x)=expression"
            x_min: Minimum x value for the domain
            x_max: Maximum x value for the domain
            num_points: Number of points to generate

        Returns:
            Tuple of (x_values, y_values) lists

        Raises:
            ValueError: If the function cannot be parsed
        """
        expression = self.parse_function(func_string)

        x_values = []
        y_values = []

        step = (x_max - x_min) / (num_points - 1)

        for i in range(num_points):
            x = x_min + i * step
            y = self.evaluate(expression, x)

            if y is not None:
                x_values.append(x)
                y_values.append(y)

        if not x_values:
            raise ValueError(f"Could not evaluate function: {func_string}")

        return x_values, y_values


if __name__ == "__main__":
    # Quick tests
    grapher = Grapher()

    # Test parsing
    print("Parsing tests:")
    print(f"  'f(x)=x^2' -> '{grapher.parse_function('f(x)=x^2')}'")
    print(f"  '2x+1' -> '{grapher.parse_function('2x+1')}'")
    print(f"  'sin(x)' -> '{grapher.parse_function('sin(x)')}'")

    # Test evaluation
    print("\nEvaluation tests:")
    expr = grapher.parse_function("f(x)=x^2")
    print(f"  x^2 at x=3: {grapher.evaluate(expr, 3)}")

    expr = grapher.parse_function("f(x)=sin(x)")
    print(f"  sin(x) at x=0: {grapher.evaluate(expr, 0)}")
    print(f"  sin(x) at x=pi/2: {grapher.evaluate(expr, math.pi/2)}")

    # Test plot data generation
    print("\nPlot data test:")
    x_vals, y_vals = grapher.generate_plot_data("f(x)=x^2", -5, 5, 11)
    print(f"  x^2 from -5 to 5: {len(x_vals)} points")
    print(f"  First 5 points: {list(zip(x_vals[:5], y_vals[:5]))}")
