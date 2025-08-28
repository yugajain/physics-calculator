

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import re

class PhysicsCalculatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Physics Calculator with Powers")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')

        # Physics constants
        self.constants = {
            'h': 6.63e-34,       # Planck constant (J·s)
            'ℏ': 1.054571817e-34,      # Reduced Planck constant (J·s)
            'c': 300000000,            # Speed of light (m/s)
            'e': 1.602176634e-19,      # Elementary charge (C)
            'mₑ': 9.1e-31,    # Electron mass (kg)
            'mₚ': 1.67e-27,   # Proton mass (kg)
            'mₙ': 1.675e-27,    # Neutron mass (kg)
            'u': 1.66e-27,    # Atomic mass unit (kg)
            'α': 0.007297352566,       # Fine structure constant
            'ε₀': 8.854187817e-12,     # Permittivity of free space (F/m)
            'μ₀': 1.25663706e-6,       # Permeability of free space (H/m)
            'G': 6.67430e-11,          # Gravitational constant (m³/(kg·s²))
            'kB': 1.380649e-23,        # Boltzmann constant (J/K)
            'NA': 6.02214076e23,       # Avogadro constant (mol⁻¹)
            'R∞': 1.097e7,             # Rydberg constant (m⁻¹)
            'π': math.pi,              # Pi
            'euler': math.e            # Euler's number
        }

        # Unit conversions
        self.units = {
            'eV': 1.602176634e-19,     # Electron volt to Joules
            'keV': 1.602176634e-16,    # Kilo eV to Joules
            'MeV': 1.602176634e-13,    # Mega eV to Joules
            'nm': 1e-9,                # Nanometer to meters
            'pm': 1e-12,               # Picometer to meters
            'fm': 1e-15,               # Femtometer to meters
            'Å': 1e-10,                # Angstrom to meters
            'MHz': 1e6,                # Megahertz to Hertz
            'GHz': 1e9,                # Gigahertz to Hertz
            'THz': 1e12                # Terahertz to Hertz
        }

        self.current_input = ""
        self.scientific_mode = True
        self.history = []

        self.setup_gui()

    def setup_gui(self):
        # Create main frames
        top_frame = tk.Frame(self.root, bg='#2b2b2b')
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        middle_frame = tk.Frame(self.root, bg='#2b2b2b')
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Title
        title_label = tk.Label(top_frame, text="Physics Calculator for modern physics by yuga jain", 
                              font=('Arial', 18, 'bold'), bg='#2b2b2b', fg='#00ff88')
        title_label.pack()

        subtitle_label = tk.Label(top_frame, text="Numbers with many zeros auto-format as powers of 10", 
                                 font=('Arial', 11), bg='#2b2b2b', fg='#cccccc')
        subtitle_label.pack()

        # Display frame
        display_frame = tk.Frame(middle_frame, bg='#1a1a1a', relief=tk.SUNKEN, bd=2)
        display_frame.pack(fill=tk.X, pady=5)

        # Main display
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Label(display_frame, textvariable=self.display_var, 
                               font=('Courier New', 24, 'bold'), bg='#000000', fg='#00ff88',
                               height=2, anchor='e', relief=tk.SUNKEN, bd=1)
        self.display.pack(fill=tk.X, padx=5, pady=5)

        # Input display (shows what user is typing)
        self.input_var = tk.StringVar(value="")
        self.input_display = tk.Label(display_frame, textvariable=self.input_var,
                                     font=('Courier New', 12), bg='#1a1a1a', fg='#888888',
                                     height=1, anchor='e')
        self.input_display.pack(fill=tk.X, padx=5)

        # Controls frame
        controls_frame = tk.Frame(display_frame, bg='#1a1a1a')
        controls_frame.pack(fill=tk.X, padx=5, pady=2)

        # Control buttons
        tk.Button(controls_frame, text="Scientific Notation", command=self.toggle_mode,
                 bg='#666666', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(controls_frame, text="Clear History", command=self.clear_history,
                 bg='#666666', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(controls_frame, text="Copy Result", command=self.copy_result,
                 bg='#666666', fg='white', font=('Arial', 9)).pack(side=tk.LEFT, padx=2)

        # Main content frame
        content_frame = tk.Frame(middle_frame, bg='#2b2b2b')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left side - Constants
        constants_frame = tk.LabelFrame(content_frame, text="Physics Constants (Click to Insert)", 
                                      bg='#3a3a3a', fg='#ff35a7', font=('Arial', 11, 'bold'))
        constants_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.create_constants_buttons(constants_frame)

        # Center - Calculator
        calc_frame = tk.Frame(content_frame, bg='#2b2b2b')
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.create_calculator_buttons(calc_frame)

        # Right side - History and Units
        right_frame = tk.Frame(content_frame, bg='#2b2b2b')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        # History
        history_frame = tk.LabelFrame(right_frame, text="Calculation History", 
                                    bg='#3a3a3a', fg='#35a7ff', font=('Arial', 11, 'bold'))
        history_frame.pack(fill=tk.BOTH, expand=True, pady=(0,5))

        self.history_text = scrolledtext.ScrolledText(history_frame, width=30, height=15,
                                                     bg='#1a1a1a', fg='#cccccc',
                                                     font=('Courier New', 9))
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Units
        units_frame = tk.LabelFrame(right_frame, text="Unit Conversions", 
                                  bg='#3a3a3a', fg='#35ffa7', font=('Arial', 11, 'bold'))
        units_frame.pack(fill=tk.X)

        self.create_units_buttons(units_frame)

    def create_constants_buttons(self, parent):
        # Create scrollable frame for constants
        canvas = tk.Canvas(parent, bg='#3a3a3a', width=200)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#3a3a3a')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Constants buttons with descriptions
        constant_descriptions = {
            'h': 'Planck constant',
            'ℏ': 'Reduced Planck',
            'c': 'Speed of light',
            'e': 'Elementary charge',
            'mₑ': 'Electron mass',
            'mₚ': 'Proton mass',
            'mₙ': 'Neutron mass',
            'u': 'Atomic mass unit',
            'α': 'Fine structure',
            'ε₀': 'Permittivity',
            'μ₀': 'Permeability',
            'G': 'Gravitational',
            'kB': 'Boltzmann',
            'NA': 'Avogadro',
            'R∞': 'Rydberg',
            'π': 'Pi',
            'euler': 'Euler\'s number'
        }

        row = 0
        for symbol, value in self.constants.items():
            scientific_val = self.format_scientific(value)
            desc = constant_descriptions.get(symbol, symbol)

            # Create button frame
            btn_frame = tk.Frame(scrollable_frame, bg='#3a3a3a')
            btn_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=1)
            scrollable_frame.grid_columnconfigure(0, weight=1)

            btn = tk.Button(btn_frame, text=symbol, 
                           command=lambda s=symbol: self.add_constant(s),
                           bg='#ff35a7', fg='white', font=('Arial', 12, 'bold'),
                           width=4)
            btn.pack(side=tk.LEFT, padx=(0,5))

            desc_label = tk.Label(btn_frame, text=f"{desc}\n{scientific_val}",
                                 bg='#3a3a3a', fg='#cccccc', font=('Arial', 8),
                                 justify=tk.LEFT)
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            row += 1

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_calculator_buttons(self, parent):
        # Calculator buttons frame
        calc_buttons_frame = tk.Frame(parent, bg='#2b2b2b')
        calc_buttons_frame.pack(expand=True)

        # Power functions section
        power_frame = tk.LabelFrame(calc_buttons_frame, text="Power & Scientific Functions",
                                  bg='#3a3a3a', fg='#a735ff', font=('Arial', 11, 'bold'))
        power_frame.pack(fill=tk.X, pady=5)

        power_buttons_data = [
            ('x²', 'Square', lambda: self.add_power_function('**2')),
            ('x³', 'Cube', lambda: self.add_power_function('**3')),
            ('x^y', 'Power', lambda: self.add_to_input('^')),
            ('√x', 'Square root', lambda: self.add_function('sqrt(')),
            ('∛x', 'Cube root', lambda: self.add_function('cbrt(')),
            ('10^x', '10 to power x', lambda: self.add_function('10**')),
            ('e^x', 'e to power x', lambda: self.add_function('euler**')),
            ('ln(x)', 'Natural log', lambda: self.add_function('ln(')),
            ('log(x)', 'Base-10 log', lambda: self.add_function('log10(')),
            ('sin(x)', 'Sine', lambda: self.add_function('sin(')),
            ('cos(x)', 'Cosine', lambda: self.add_function('cos(')),
            ('tan(x)', 'Tangent', lambda: self.add_function('tan('))
        ]

        for i, (text, tooltip, command) in enumerate(power_buttons_data):
            btn = tk.Button(power_frame, text=text, command=command,
                           bg='#a735ff', fg='white', font=('Arial', 10, 'bold'),
                           width=7, height=2)
            btn.grid(row=i//6, column=i%6, padx=2, pady=2)
            self.create_tooltip(btn, tooltip)

        # Standard calculator buttons
        std_frame = tk.Frame(calc_buttons_frame, bg='#2b2b2b')
        std_frame.pack(pady=20)

        # Button layout
        buttons = [
            ['C', 'CE', '←', '/', '(', ')'],
            ['7', '8', '9', '*', 'π', 'e'],
            ['4', '5', '6', '-', 'x²', '√'],
            ['1', '2', '3', '+', '^', 'ln'],
            ['±', '0', '.', '=', 'EXP', 'ANS']
        ]

        for row, button_row in enumerate(buttons):
            for col, button_text in enumerate(button_row):
                if button_text == '=':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=self.calculate,
                                   bg='#ff6b35', fg='white', font=('Arial', 16, 'bold'),
                                   width=5, height=2)
                elif button_text in ['C', 'CE', '←']:
                    cmd = lambda t=button_text: self.clear_function(t)
                    btn = tk.Button(std_frame, text=button_text,
                                   command=cmd,
                                   bg='#ff6b35', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text in ['+', '-', '*', '/', '(', ')']:
                    cmd = lambda t=button_text: self.add_to_input(t)
                    btn = tk.Button(std_frame, text=button_text,
                                   command=cmd,
                                   bg='#35a7ff', fg='white', font=('Arial', 16, 'bold'),
                                   width=5, height=2)
                elif button_text == '±':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=self.toggle_sign,
                                   bg='#35a7ff', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text == 'π':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_constant('π'),
                                   bg='#ff35a7', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text == 'e':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_constant('euler'),
                                   bg='#ff35a7', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text == 'x²':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_power_function('**2'),
                                   bg='#a735ff', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text == '√':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_function('sqrt('),
                                   bg='#a735ff', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text == '^':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_to_input('^'),
                                   bg='#a735ff', fg='white', font=('Arial', 16, 'bold'),
                                   width=5, height=2)
                elif button_text == 'ln':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_function('ln('),
                                   bg='#a735ff', fg='white', font=('Arial', 12, 'bold'),
                                   width=5, height=2)
                elif button_text == 'EXP':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=lambda: self.add_to_input('e'),
                                   bg='#666666', fg='white', font=('Arial', 10, 'bold'),
                                   width=5, height=2)
                elif button_text == 'ANS':
                    btn = tk.Button(std_frame, text=button_text,
                                   command=self.add_last_result,
                                   bg='#666666', fg='white', font=('Arial', 10, 'bold'),
                                   width=5, height=2)
                else:
                    cmd = lambda t=button_text: self.add_to_input(t)
                    btn = tk.Button(std_frame, text=button_text,
                                   command=cmd,
                                   bg='#4a4a4a', fg='white', font=('Arial', 16, 'bold'),
                                   width=5, height=2)

                btn.grid(row=row, column=col, padx=2, pady=2)

    def create_units_buttons(self, parent):
        # Unit descriptions
        unit_descriptions = {
            'eV': 'Electron volt',
            'keV': 'Kilo eV', 
            'MeV': 'Mega eV',
            'nm': 'Nanometer',
            'pm': 'Picometer',
            'fm': 'Femtometer',
            'Å': 'Angstrom',
            'MHz': 'Megahertz',
            'GHz': 'Gigahertz',
            'THz': 'Terahertz'
        }

        row = 0
        for symbol, value in self.units.items():
            scientific_val = self.format_scientific(value)
            desc = unit_descriptions.get(symbol, symbol)

            btn_frame = tk.Frame(parent, bg='#3a3a3a')
            btn_frame.grid(row=row, column=0, sticky='ew', padx=2, pady=1)
            parent.grid_columnconfigure(0, weight=1)

            btn = tk.Button(btn_frame, text=symbol, 
                           command=lambda s=symbol: self.add_unit(s),
                           bg='#35ffa7', fg='black', font=('Arial', 10, 'bold'),
                           width=6)
            btn.pack(side=tk.LEFT, padx=(0,5))

            desc_label = tk.Label(btn_frame, text=f"{desc}\n{scientific_val}",
                                 bg='#3a3a3a', fg='#cccccc', font=('Arial', 8),
                                 justify=tk.LEFT)
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

            row += 1

    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background='#ffffe0', 
                           relief='solid', borderwidth=1, font=('Arial', 9))
            label.pack()
            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def format_scientific(self, number):
        """Convert number to scientific notation format with × symbol"""
        if number == 0:
            return "0"

        if not self.scientific_mode:
            return str(number)

        abs_num = abs(number)
        if abs_num >= 1000000 or (abs_num <= 0.000001 and abs_num != 0):
            exp = int(math.floor(math.log10(abs_num)))
            mantissa = number / (10 ** exp)

            if abs(mantissa - round(mantissa, 3)) < 1e-10:
                mantissa = round(mantissa, 3)
            else:
                mantissa = round(mantissa, 6)

            return f"{mantissa}×10^{exp}"
        else:
            if abs(number - round(number)) < 1e-10:
                return str(int(round(number)))
            else:
                return f"{number:.8g}"

    def add_to_input(self, value):
        if self.current_input == "0" and value.isdigit():
            self.current_input = value
        elif self.current_input == "" and value.isdigit():
            self.current_input = value
        else:
            self.current_input += str(value)
        self.update_display()

    def add_constant(self, symbol):
        value = self.constants[symbol]
        if self.current_input == "0" or self.current_input == "":
            self.current_input = str(value)
        else:
            # If last character is a number or ), add multiplication
            if self.current_input[-1].isdigit() or self.current_input[-1] == ')':
                self.current_input += '*' + str(value)
            else:
                self.current_input += str(value)
        self.update_display()

    def add_unit(self, symbol):
        value = self.units[symbol]
        if self.current_input == "0" or self.current_input == "":
            self.current_input = str(value)
        else:
            # If last character is a number or ), add multiplication
            if self.current_input[-1].isdigit() or self.current_input[-1] == ')':
                self.current_input += '*' + str(value)
            else:
                self.current_input += str(value)
        self.update_display()

    def add_function(self, func):
        if self.current_input == "0" or self.current_input == "":
            self.current_input = func
        else:
            # If last character is a number or ), add multiplication before function
            if self.current_input[-1].isdigit() or self.current_input[-1] == ')':
                self.current_input += '*' + func
            else:
                self.current_input += func
        self.update_display()

    def add_power_function(self, power):
        if self.current_input and (self.current_input[-1].isdigit() or self.current_input[-1] == ')'):
            self.current_input += power
        else:
            self.current_input += '(' + self.current_input + ')' + power
        self.update_display()

    def add_last_result(self):
        if hasattr(self, 'last_result'):
            self.add_to_input(str(self.last_result))

    def clear_function(self, clear_type):
        if clear_type == 'C':
            self.current_input = ""
        elif clear_type == 'CE':
            self.current_input = ""
        elif clear_type == '←':
            if len(self.current_input) > 0:
                self.current_input = self.current_input[:-1]
        self.update_display()

    def toggle_sign(self):
        try:
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
        except:
            pass

    def update_display(self):
        # Show current input in the input display
        self.input_var.set(self.current_input if self.current_input else "0")

        # Try to evaluate and show formatted result in main display
        try:
            if self.current_input and self.current_input.replace('.','').replace('-','').replace('e','').replace('+','').isdigit():
                # If it's just a number, format it
                val = float(self.current_input)
                formatted = self.format_scientific(val)
                self.display_var.set(formatted)
            else:
                # Show the input as-is
                self.display_var.set(self.current_input if self.current_input else "0")
        except:
            self.display_var.set(self.current_input if self.current_input else "0")

    def calculate(self):
        try:
            if not self.current_input:
                return

            # Prepare expression for evaluation
            expression = self.current_input.replace('^', '**')

            # Handle scientific notation input
            expression = re.sub(r'(\d+\.?\d*)\s*×\s*10\*\*([+-]?\d+)', r'(\1 * 10**\2)', expression)

            # Create safe evaluation environment
            safe_dict = {
                '__builtins__': {},
                'sqrt': math.sqrt,
                'cbrt': lambda x: x**(1/3),
                'log10': math.log10,
                'ln': math.log,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'exp': math.exp,
                'abs': abs,
                'pow': pow
            }

            # Add constants and units
            safe_dict.update(self.constants)
            safe_dict.update(self.units)

            # Evaluate
            result = eval(expression, safe_dict)
            self.last_result = result

            # Format result
            formatted_result = self.format_scientific(result)

            # Update display
            self.display_var.set(formatted_result)

            # Add to history
            history_entry = f"{self.current_input} = {formatted_result}\n"
            self.history.append(history_entry)
            self.history_text.insert(tk.END, history_entry)
            self.history_text.see(tk.END)

            # Set current input to result for chaining
            self.current_input = str(result)
            self.input_var.set(self.current_input)

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.display_var.set(error_msg)
            messagebox.showerror("Calculation Error", error_msg)

    def toggle_mode(self):
        self.scientific_mode = not self.scientific_mode
        mode_text = "ON" if self.scientific_mode else "OFF"
        messagebox.showinfo("Scientific Notation", f"Scientific notation mode: {mode_text}")
        self.update_display()

    def clear_history(self):
        self.history.clear()
        self.history_text.delete(1.0, tk.END)
        messagebox.showinfo("History", "Calculation history cleared!")

    def copy_result(self):
        result = self.display_var.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        messagebox.showinfo("Copied", f"Result copied to clipboard: {result}")

    def run(self):
        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()

        # Show initial help
        help_text = """🧮 PHYSICS CALCULATOR READY!

Features:
• Click physics constants (h, c, e, etc.) to insert values
• Power functions: x², x³, x^y, √x, 10^x, etc.
• Numbers with many zeros auto-format as scientific notation
• Example: 1500000 → 1.5×10^6
• Calculation history saved on the right
• Copy results to clipboard

Try: h*c, me*c^2, sqrt(kB*300), 10^8"""

        self.history_text.insert(tk.END, help_text + "\n\n")

        self.root.mainloop()

    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        if key.isdigit() or key in '+-*/.()':
            self.add_to_input(key)
        elif key == '\r' or key == '\n':  # Enter key
            self.calculate()
        elif key == '\x08':  # Backspace
            self.clear_function('←')
        elif key == '\x1b':  # Escape
            self.clear_function('C')


def main():
    """Main function to run the calculator"""
    try:
        calc = PhysicsCalculatorGUI()
        calc.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Make sure you have tkinter installed and a display available.")


if __name__ == "__main__":
    main()
