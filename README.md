# Python Calculator with Graphing

A local Python calculator application featuring basic arithmetic with PEMDAS support and multi-function graphing capabilities.

## Features

### Calculator
- **Basic Operations**: Addition, subtraction, multiplication, division
- **PEMDAS Support**: Full expression evaluation with proper order of operations
- **Parentheses**: Nested expressions like `((2+3)*4)^2`
- **Exponents**: Use `^` for powers (e.g., `2^3` = 8)
- **Constants**: `pi` and `e` built-in
- **Functions**: `sqrt()` for square roots
- **Expression Input**: Type full expressions directly or use the button pad

### Grapher
- **Multiple Functions**: Plot several functions on the same graph
- **Color-Coded**: Each function gets a unique color (10 colors available)
- **Edit In-Place**: Click a function to modify it without removing
- **Adjustable Range**: Change x-axis range and replot all functions
- **Function Management**: Add, remove, or clear all functions
- **Export**: Save graphs as PNG, JPEG, PDF, or SVG

### Supported Math Functions
| Function | Example | Description |
|----------|---------|-------------|
| Basic ops | `2+3*4` | Add, subtract, multiply, divide |
| Exponents | `x^2`, `2^3` | Powers |
| Parentheses | `(2+3)*4` | Grouping |
| Sine | `sin(x)` | Trigonometric sine |
| Cosine | `cos(x)` | Trigonometric cosine |
| Tangent | `tan(x)` | Trigonometric tangent |
| Square root | `sqrt(x)` | Square root |
| Constants | `pi`, `e` | Mathematical constants |

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install matplotlib directly:

```bash
pip install matplotlib
```

## Usage

### Running the Application

```bash
python3 main.py
```

### Calculator Panel

1. **Type expressions** directly in the input field, or use the buttons
2. Press **Enter** or click **=** to evaluate
3. Results appear in the display below the input

**Example expressions:**
```
2+3*4         → 14    (multiplication first)
(2+3)*4       → 20    (parentheses first)
2^3+1         → 9     (exponent first)
sqrt(16)+2    → 6     (function evaluation)
((2+3)*2)^2   → 100   (nested parentheses)
```

### Grapher Panel

1. **Add a function**: Type an expression (e.g., `x^2`) and click **Add** or press Enter
2. **Add more functions**: Repeat to plot multiple functions on the same graph
3. **Edit a function**: Click it in the list, modify, and click **Update**
4. **Remove a function**: Select it and click **Remove**
5. **Change range**: Modify x min/max values and click **Replot**
6. **Save graph**: Click **Save PNG** to export

**Example functions to try:**
```
x^2           → Parabola
sin(x)        → Sine wave
2x+1          → Linear function
x^3-2x        → Cubic function
cos(x)+x      → Combined function
sqrt(x)       → Square root curve
```

## Project Structure

```
calculator/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── backend/
│   ├── __init__.py
│   ├── calculator.py   # PEMDAS expression evaluator
│   └── grapher.py      # Function parser & plot data generator
└── frontend/
    ├── __init__.py
    └── gui.py          # Tkinter GUI with matplotlib integration
```

## Architecture

### Backend

**calculator.py**
- `Calculator` class with basic arithmetic methods
- `evaluate_expression()` for full PEMDAS expression parsing
- Input validation and error handling

**grapher.py**
- `Grapher` class for function parsing
- Converts `f(x)=` format to evaluatable expressions
- Generates (x, y) coordinate data for plotting

### Frontend

**gui.py**
- `CalculatorApp` class - main application window
- Two-panel layout: Calculator (left) and Grapher (right)
- Matplotlib integration for graph rendering
- Function list management with edit-in-place support

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Evaluate expression / Add function |
| Backspace | Delete last character |

## Export Formats

When saving graphs, the following formats are supported:
- **PNG** - Best for web and presentations (default)
- **JPEG** - Compressed image format
- **PDF** - Vector format for documents
- **SVG** - Scalable vector graphics

## Examples

### PEMDAS Demonstration
```
Input: 2+3*4-10/2
Steps: 2 + 12 - 5 = 9
       (multiplication and division first, left to right)
       (then addition and subtraction, left to right)
```

### Comparing Functions
Plot these together to see intersections:
1. `x` (linear)
2. `x^2` (quadratic)
3. `sqrt(x)` (square root)

## Troubleshooting

### "No module named 'matplotlib'"
```bash
pip install matplotlib
```

### "No module named 'tkinter'"
- **macOS**: `brew install python-tk`
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **Windows**: Reinstall Python with tkinter option checked

### Graph not displaying
Ensure matplotlib backend is compatible with tkinter:
```python
import matplotlib
matplotlib.use('TkAgg')
```

## License

MIT License - Feel free to use and modify.

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.
