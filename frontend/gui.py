"""
Calculator GUI Module
Tkinter-based user interface with calculator and graphing panels.
Supports full expression input with PEMDAS evaluation.
Supports multiple functions on the same graph.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.calculator import Calculator
from backend.grapher import Grapher


class CalculatorApp:
    """Main calculator application with arithmetic and graphing capabilities."""

    # Colors for multiple function plots
    PLOT_COLORS = ['#2196F3', '#F44336', '#4CAF50', '#FF9800', '#9C27B0',
                   '#00BCD4', '#E91E63', '#8BC34A', '#FF5722', '#673AB7']

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Calculator with Graphing")
        self.root.resizable(True, True)

        # Initialize backends
        self.calculator = Calculator()
        self.grapher = Grapher()

        # Calculator state - now supports expression mode
        self.expression = ""
        self.last_result = ""
        self.just_evaluated = False

        # Graphing state - support multiple functions
        self.plotted_functions = []  # List of (func_string, x_vals, y_vals, color)
        self.editing_index = None  # Track which function is being edited

        # Create main container with two panels
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # Create panels
        self._create_calculator_panel()
        self._create_graph_panel()

        # Bind keyboard events
        self.root.bind('<Key>', self._on_key_press)

    def _create_calculator_panel(self):
        """Create the calculator panel with display and buttons."""
        calc_frame = ttk.LabelFrame(self.main_frame, text="Calculator (PEMDAS)", padding="10")
        calc_frame.grid(row=0, column=0, sticky="n", padx=(0, 10))

        # Expression display (editable)
        self.display_var = tk.StringVar(value="")
        self.display_entry = ttk.Entry(
            calc_frame,
            textvariable=self.display_var,
            font=("Arial", 20),
            justify="right",
            width=20
        )
        self.display_entry.grid(row=0, column=0, columnspan=5, pady=(0, 5), sticky="ew")
        self.display_entry.bind("<Return>", lambda e: self._evaluate())

        # Result display (readonly)
        self.result_var = tk.StringVar(value="0")
        result_display = ttk.Entry(
            calc_frame,
            textvariable=self.result_var,
            font=("Arial", 16),
            justify="right",
            width=20,
            state="readonly"
        )
        result_display.grid(row=1, column=0, columnspan=5, pady=(0, 10), sticky="ew")

        # Button layout - expanded with parentheses and exponent
        buttons = [
            ('(', 2, 0), (')', 2, 1), ('^', 2, 2), ('C', 2, 3), ('⌫', 2, 4),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3), ('sqrt', 3, 4),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3), ('pi', 4, 4),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3), ('e', 5, 4),
            ('0', 6, 0), ('.', 6, 1), ('±', 6, 2), ('+', 6, 3), ('=', 6, 4),
        ]

        # Create buttons
        for (text, row, col) in buttons:
            # Make = button stand out
            if text == '=':
                btn = ttk.Button(
                    calc_frame,
                    text=text,
                    width=5,
                    command=lambda t=text: self._on_button_click(t),
                    style='Accent.TButton'
                )
            else:
                btn = ttk.Button(
                    calc_frame,
                    text=text,
                    width=5,
                    command=lambda t=text: self._on_button_click(t)
                )
            btn.grid(row=row, column=col, padx=2, pady=2)

        # Instructions label
        instructions = ttk.Label(
            calc_frame,
            text="Type expressions like: 2+3*4, (2+3)^2, sqrt(16)",
            font=("Arial", 9),
            foreground="gray"
        )
        instructions.grid(row=7, column=0, columnspan=5, pady=(10, 0))

    def _create_graph_panel(self):
        """Create the graphing panel with input and matplotlib display."""
        graph_frame = ttk.LabelFrame(self.main_frame, text="Function Grapher (Multi-Function)", padding="10")
        graph_frame.grid(row=0, column=1, sticky="nsew")
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(2, weight=1)

        # Input frame
        input_frame = ttk.Frame(graph_frame)
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="f(x) =").grid(row=0, column=0, padx=(0, 5))

        self.function_var = tk.StringVar(value="x^2")
        self.function_entry = ttk.Entry(
            input_frame,
            textvariable=self.function_var,
            font=("Arial", 12),
            width=30
        )
        self.function_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        self.function_entry.bind("<Return>", lambda e: self._add_or_update_function())

        self.add_btn = ttk.Button(input_frame, text="Add", command=self._add_or_update_function)
        self.add_btn.grid(row=0, column=2, padx=(0, 5))

        clear_all_btn = ttk.Button(input_frame, text="Clear All", command=self._clear_graph)
        clear_all_btn.grid(row=0, column=3, padx=(0, 5))

        save_btn = ttk.Button(input_frame, text="Save PNG", command=self._save_graph)
        save_btn.grid(row=0, column=4)

        # Range and function list frame
        controls_frame = ttk.Frame(graph_frame)
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        controls_frame.columnconfigure(1, weight=1)

        # Range inputs
        range_frame = ttk.Frame(controls_frame)
        range_frame.grid(row=0, column=0, sticky="w")

        ttk.Label(range_frame, text="x range:").grid(row=0, column=0, padx=(0, 5))

        self.x_min_var = tk.StringVar(value="-10")
        x_min_entry = ttk.Entry(range_frame, textvariable=self.x_min_var, width=6)
        x_min_entry.grid(row=0, column=1, padx=(0, 5))

        ttk.Label(range_frame, text="to").grid(row=0, column=2, padx=5)

        self.x_max_var = tk.StringVar(value="10")
        x_max_entry = ttk.Entry(range_frame, textvariable=self.x_max_var, width=6)
        x_max_entry.grid(row=0, column=3, padx=(0, 10))

        # Replot button (for when range changes)
        replot_btn = ttk.Button(range_frame, text="Replot", command=self._replot_all)
        replot_btn.grid(row=0, column=4)

        # Function list frame
        list_frame = ttk.LabelFrame(graph_frame, text="Plotted Functions", padding="5")
        list_frame.grid(row=1, column=0, sticky="e", pady=(0, 5))

        # Listbox for functions
        self.func_listbox = tk.Listbox(
            list_frame,
            height=4,
            width=30,
            font=("Arial", 10),
            selectmode=tk.SINGLE
        )
        self.func_listbox.grid(row=0, column=0, sticky="ew")
        self.func_listbox.bind('<<ListboxSelect>>', self._on_function_select)

        # Button frame for list actions
        list_btn_frame = ttk.Frame(list_frame)
        list_btn_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        list_btn_frame.columnconfigure(0, weight=1)
        list_btn_frame.columnconfigure(1, weight=1)

        # Remove selected button
        remove_btn = ttk.Button(list_btn_frame, text="Remove", command=self._remove_selected_function)
        remove_btn.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        # Cancel edit button
        self.cancel_btn = ttk.Button(list_btn_frame, text="Cancel Edit", command=self._cancel_edit, state="disabled")
        self.cancel_btn.grid(row=0, column=1, sticky="ew", padx=(2, 0))

        # Matplotlib figure
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self._setup_graph()

        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")

        # Example functions label
        examples = ttk.Label(
            graph_frame,
            text="Examples: x^2, sin(x), 2x+1, cos(x)+x, sqrt(x), x^3-2x",
            font=("Arial", 9),
            foreground="gray"
        )
        examples.grid(row=3, column=0, sticky="w", pady=(5, 0))

    def _setup_graph(self):
        """Set up the graph with grid and labels."""
        self.ax.clear()
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)

    def _get_next_color(self):
        """Get the next color for plotting."""
        color_index = len(self.plotted_functions) % len(self.PLOT_COLORS)
        return self.PLOT_COLORS[color_index]

    def _on_key_press(self, event):
        """Handle keyboard input when display is focused."""
        # Only process if display entry is focused
        if self.root.focus_get() != self.display_entry:
            return

    def _on_button_click(self, button: str):
        """Handle calculator button clicks."""
        # Get current expression
        self.expression = self.display_var.get()

        # If just evaluated and starting fresh with a number/function
        if self.just_evaluated and button not in ['+', '-', '*', '/', '^', '=', 'C', '⌫']:
            self.expression = ""
            self.just_evaluated = False

        if button.isdigit() or button == '.':
            self._append_to_expression(button)
        elif button in ['+', '-', '*', '/', '^']:
            self._append_to_expression(button)
            self.just_evaluated = False
        elif button in ['(', ')']:
            self._append_to_expression(button)
        elif button == 'sqrt':
            self._append_to_expression('sqrt(')
        elif button == 'pi':
            self._append_to_expression('pi')
        elif button == 'e':
            self._append_to_expression('e')
        elif button == '=':
            self._evaluate()
        elif button == 'C':
            self._clear_all()
        elif button == '⌫':
            self._backspace()
        elif button == '±':
            self._toggle_sign()

    def _append_to_expression(self, text: str):
        """Append text to the current expression."""
        self.expression = self.display_var.get() + text
        self.display_var.set(self.expression)
        self.just_evaluated = False

    def _evaluate(self):
        """Evaluate the current expression using PEMDAS."""
        expression = self.display_var.get().strip()

        if not expression:
            return

        try:
            result = self.calculator.evaluate_expression(expression)

            # Format result (remove unnecessary decimals)
            if result == int(result):
                result_str = str(int(result))
            else:
                result_str = f"{result:.10g}"

            self.result_var.set(f"= {result_str}")
            self.last_result = result_str
            self.just_evaluated = True

        except ValueError as e:
            self.result_var.set(f"Error: {str(e)}")
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

    def _clear_all(self):
        """Clear all calculator state."""
        self.expression = ""
        self.display_var.set("")
        self.result_var.set("0")
        self.just_evaluated = False

    def _backspace(self):
        """Remove the last character."""
        current = self.display_var.get()
        if current:
            self.display_var.set(current[:-1])
        self.just_evaluated = False

    def _toggle_sign(self):
        """Wrap expression in negation or toggle."""
        current = self.display_var.get()
        if current:
            if current.startswith('-(') and current.endswith(')'):
                # Remove negation
                self.display_var.set(current[2:-1])
            elif current.startswith('-'):
                # Remove leading minus
                self.display_var.set(current[1:])
            else:
                # Add negation
                self.display_var.set(f"-({current})")

    def _on_function_select(self, event):
        """Handle function selection in the listbox for editing."""
        selection = self.func_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if 0 <= index < len(self.plotted_functions):
            # Load the selected function into the entry for editing
            func_string, _, _, _ = self.plotted_functions[index]
            self.function_var.set(func_string)
            self.editing_index = index

            # Update UI to show edit mode
            self.add_btn.config(text="Update")
            self.cancel_btn.config(state="normal")

    def _cancel_edit(self):
        """Cancel editing and reset to add mode."""
        self.editing_index = None
        self.function_var.set("")
        self.func_listbox.selection_clear(0, tk.END)

        # Reset UI to add mode
        self.add_btn.config(text="Add")
        self.cancel_btn.config(state="disabled")

    def _add_or_update_function(self):
        """Add a new function or update an existing one."""
        func_string = self.function_var.get().strip()
        if not func_string:
            messagebox.showwarning("Warning", "Please enter a function to plot.")
            return

        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())

            if x_min >= x_max:
                messagebox.showwarning("Warning", "x min must be less than x max.")
                return

            # Check if we're editing an existing function
            if self.editing_index is not None:
                # Update existing function
                _, _, _, color = self.plotted_functions[self.editing_index]

                x_vals, y_vals = self.grapher.generate_plot_data(
                    func_string, x_min, x_max, 500
                )

                # Update the function in place (keep the same color)
                self.plotted_functions[self.editing_index] = (func_string, x_vals, y_vals, color)

                # Reset edit mode
                self._cancel_edit()

            else:
                # Adding new function - check for duplicates
                for existing_func, _, _, _ in self.plotted_functions:
                    if existing_func == func_string:
                        messagebox.showinfo("Info", f"Function '{func_string}' is already plotted.")
                        return

                x_vals, y_vals = self.grapher.generate_plot_data(
                    func_string, x_min, x_max, 500
                )

                color = self._get_next_color()

                # Store the function data
                self.plotted_functions.append((func_string, x_vals, y_vals, color))

                # Clear input for next function
                self.function_var.set("")

            # Update the listbox and redraw
            self._update_function_list()
            self._redraw_graph()

        except ValueError as e:
            messagebox.showerror("Error", f"Could not plot function: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def _add_function(self):
        """Legacy method - redirects to _add_or_update_function."""
        self._add_or_update_function()

    def _remove_selected_function(self):
        """Remove the selected function from the graph."""
        selection = self.func_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a function to remove.")
            return

        index = selection[0]
        if 0 <= index < len(self.plotted_functions):
            self.plotted_functions.pop(index)

            # Reset edit mode if we were editing this or any function
            self._cancel_edit()

            self._update_function_list()
            self._redraw_graph()

    def _update_function_list(self):
        """Update the listbox with current functions."""
        self.func_listbox.delete(0, tk.END)
        for func_string, _, _, color in self.plotted_functions:
            # Add color indicator
            self.func_listbox.insert(tk.END, f"f(x) = {func_string}")

        # Color the listbox items
        for i, (_, _, _, color) in enumerate(self.plotted_functions):
            self.func_listbox.itemconfig(i, fg=color)

    def _redraw_graph(self):
        """Redraw all functions on the graph."""
        self._setup_graph()

        if not self.plotted_functions:
            self.canvas.draw()
            return

        all_y_vals = []

        for func_string, x_vals, y_vals, color in self.plotted_functions:
            self.ax.plot(x_vals, y_vals, color=color, linewidth=2, label=f"f(x) = {func_string}")
            all_y_vals.extend(y_vals)

        # Set x limits
        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())
            self.ax.set_xlim(x_min, x_max)
        except ValueError:
            pass

        # Auto-scale y-axis with some padding
        if all_y_vals:
            y_min, y_max = min(all_y_vals), max(all_y_vals)
            y_padding = (y_max - y_min) * 0.1 if y_max != y_min else 1
            self.ax.set_ylim(y_min - y_padding, y_max + y_padding)

        self.ax.legend(loc='upper right')
        self.canvas.draw()

    def _replot_all(self):
        """Replot all functions with new range."""
        if not self.plotted_functions:
            return

        try:
            x_min = float(self.x_min_var.get())
            x_max = float(self.x_max_var.get())

            if x_min >= x_max:
                messagebox.showwarning("Warning", "x min must be less than x max.")
                return

            # Regenerate data for all functions with new range
            new_plotted = []
            for func_string, _, _, color in self.plotted_functions:
                x_vals, y_vals = self.grapher.generate_plot_data(
                    func_string, x_min, x_max, 500
                )
                new_plotted.append((func_string, x_vals, y_vals, color))

            self.plotted_functions = new_plotted
            self._redraw_graph()

        except ValueError as e:
            messagebox.showerror("Error", f"Could not replot: {e}")

    def _clear_graph(self):
        """Clear all functions from the graph."""
        self.plotted_functions = []
        self._cancel_edit()  # Reset edit mode
        self._update_function_list()
        self._setup_graph()
        self.canvas.draw()

    def _save_graph(self):
        """Save the current graph as a PNG file."""
        if not self.plotted_functions:
            messagebox.showinfo("Info", "No functions to save. Add some functions first.")
            return

        # Open save dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            ],
            title="Save Graph As"
        )

        if file_path:
            try:
                # Save the figure with high resolution
                self.figure.savefig(file_path, dpi=150, bbox_inches='tight',
                                   facecolor='white', edgecolor='none')
                messagebox.showinfo("Success", f"Graph saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save graph: {e}")


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
