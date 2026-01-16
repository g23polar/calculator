#!/usr/bin/env python3
"""
Python Calculator with Graphing
A local calculator application with basic arithmetic and function graphing.

Features:
- Basic arithmetic: add, subtract, multiply, divide
- Function graphing with f(x)= format
- Supports: polynomials, trigonometric functions (sin, cos, tan), sqrt

Usage:
    python main.py

Requirements:
    - Python 3.7+
    - tkinter (usually included with Python)
    - matplotlib (pip install matplotlib)
"""

import sys
import os

# Ensure the package can find its modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from frontend.gui import CalculatorApp
import tkinter as tk


def main():
    """Launch the calculator application."""
    print("Starting Python Calculator with Graphing...")
    print("=" * 50)
    print("Features:")
    print("  - Basic Calculator: +, -, *, /")
    print("  - Function Grapher: supports f(x)= format")
    print("    Examples: x^2, sin(x), 2x+1, cos(x)")
    print("=" * 50)

    root = tk.Tk()
    root.minsize(800, 500)

    app = CalculatorApp(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
