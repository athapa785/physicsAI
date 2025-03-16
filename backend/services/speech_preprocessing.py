"""
Speech preprocessing utilities for converting text and mathematical expressions to speech-friendly format.
"""

import re

def preprocess_latex_for_speech(text: str) -> str:
    """Convert LaTeX math expressions to spoken form."""
    # Remove LaTeX text formatting commands that should be ignored
    text_commands_to_remove = [
        r'\\mathbf{([^}]+)}',
        r'\\mathrm{([^}]+)}',
        r'\\mathit{([^}]+)}',
        r'\\mathsf{([^}]+)}',
        r'\\mathtt{([^}]+)}',
        r'\\text{([^}]+)}',
        r'\\textbf{([^}]+)}',
        r'\\textit{([^}]+)}',
        r'\\emph{([^}]+)}',
        r'\\mbox{([^}]+)}',
        r'\\displaystyle',
        r'\\scriptstyle',
        r'\\scriptscriptstyle',
        r'\\textstyle',
    ]
    
    # Replace formatting commands with their content
    for pattern in text_commands_to_remove:
        if pattern.endswith('}'):
            text = re.sub(pattern, r'\1', text)
        else:
            text = re.sub(pattern, '', text)
    
    # Handle common LaTeX commands
    latex_replacements = {
        r'\\frac{([^}]+)}{([^}]+)}': lambda m: f"{m.group(1)} over {m.group(2)}",
        r'\\dfrac{([^}]+)}{([^}]+)}': lambda m: f"{m.group(1)} over {m.group(2)}",
        r'\\sqrt{([^}]+)}': lambda m: f"square root of {m.group(1)}",
        r'\\sqrt\[([^]]+)\]{([^}]+)}': lambda m: f"{m.group(1)} root of {m.group(2)}",
        r'\\int_{([^}]+)}^{([^}]+)}': lambda m: f"integral from {m.group(1)} to {m.group(2)} of",
        r'\\sum_{([^}]+)}^{([^}]+)}': lambda m: f"sum from {m.group(1)} to {m.group(2)} of",
        r'\\prod_{([^}]+)}^{([^}]+)}': lambda m: f"product from {m.group(1)} to {m.group(2)} of",
        r'\\lim_{([^}]+)}': lambda m: f"limit as {m.group(1)}",
        r'\\vec{([^}]+)}': lambda m: f"vector {m.group(1)}",
        r'\\hat{([^}]+)}': lambda m: f"unit vector {m.group(1)}",
        r'\\partial': 'partial derivative',
        r'\\Delta': 'change in',
        r'\\alpha': 'alpha',
        r'\\beta': 'beta',
        r'\\gamma': 'gamma',
        r'\\theta': 'theta',
        r'\\lambda': 'lambda',
        r'\\mu': 'mu',
        r'\\pi': 'pi',
        r'\\rho': 'rho',
        r'\\sigma': 'sigma',
        r'\\tau': 'tau',
        r'\\phi': 'phi',
        r'\\omega': 'omega',
        r'\\infty': 'infinity',
        r'\\approx': 'approximately equals',
        r'\\neq': 'not equal to',
        r'\\geq': 'greater than or equal to',
        r'\\leq': 'less than or equal to',
        r'\\cdot': 'times',
        r'\\times': 'times',
        r'\\div': 'divided by',
        r'_0': ' initial',
        r'_f': ' final',
        r'_{init}': ' initial',
        r'_{final}': ' final',
        r'\\left': '',
        r'\\right': '',
    }
    
    # Apply LaTeX replacements
    for pattern, replacement in latex_replacements.items():
        if callable(replacement):
            text = re.sub(pattern, replacement, text)
        else:
            text = re.sub(pattern, replacement, text)
    
    # Handle superscripts in LaTeX
    text = re.sub(r'\^{([^}]+)}', lambda m: f" to the power of {m.group(1)}", text)
    text = re.sub(r'\^(\d)', lambda m: f" to the power of {m.group(1)}", text)
    
    return text

def preprocess_math_for_speech(text: str) -> str:
    """Preprocess mathematical expressions for better speech synthesis."""
    # First handle any LaTeX in the text
    text = preprocess_latex_for_speech(text)
    
    # Replace common math symbols
    replacements = {
        '+': ' plus ',
        '×': ' cross ',
        '*': ' times ',
        '/': ' divided by ',
        '=': ' equals ',
        '^2': ' squared ',
        '^3': ' cubed ',
        '^': ' to the power of ',
        '√': ' square root of ',
        'π': ' pi ',
        '∞': ' infinity ',
        '≈': ' approximately equals ',
        '≠': ' not equal to ',
        '≤': ' less than or equal to ',
        '≥': ' greater than or equal to ',
        '<': ' less than ',
        '>': ' greater than ',
        'Δ': ' delta ',
        'α': ' alpha ',
        'β': ' beta ',
        'γ': ' gamma ',
        'θ': ' theta ',
        'λ': ' lambda ',
        'ρ': ' rho ',
        'σ': ' sigma ',
        'φ': ' phi ',
        'ω': ' omega ',
        '→': ' vector ',
        '⇒': ' implies ',
        '∈': ' is an element of ',
        '∉': ' is not an element of ',
        '∫': ' integral of ',
        '∂': ' partial derivative of ',
        '∑': ' sum of ',
        '∏': ' product of ',
    }
    
    # Handle common physics variables and units
    physics_replacements = {
        'v0': 'v initial',
        'v1': 'v final',
        't0': 't initial',
        't1': 't final',
        'dx': 'change in x',
        'dy': 'change in y',
        'dz': 'change in z',
        'dt': 'change in time',
        'dv': 'change in velocity',
        'da': 'change in acceleration',
        'dE': 'change in energy',
        'dP': 'change in momentum',
        'dθ': 'change in theta',
        'dφ': 'change in phi',
        'm/s': 'meters per second',
        'm/s²': 'meters per second squared',
        'km/h': 'kilometers per hour',
        'N/m': 'newtons per meter',
        'N⋅m': 'newton meters',
        'kg/m³': 'kilograms per cubic meter',
        'J/K': 'joules per kelvin',
        'W/m²': 'watts per square meter',
        'rad/s': 'radians per second',
        'Hz': 'hertz',
        'kHz': 'kilohertz',
        'MHz': 'megahertz',
    }
    
    # Replace superscript numbers with 'to the power of'
    text = re.sub(r'⁰', ' to the power of 0', text)
    text = re.sub(r'¹', ' to the power of 1', text)
    text = re.sub(r'²', ' squared ', text)
    text = re.sub(r'³', ' cubed ', text)
    text = re.sub(r'⁴', ' to the power of 4', text)
    text = re.sub(r'⁵', ' to the power of 5', text)
    text = re.sub(r'⁶', ' to the power of 6', text)
    text = re.sub(r'⁷', ' to the power of 7', text)
    text = re.sub(r'⁸', ' to the power of 8', text)
    text = re.sub(r'⁹', ' to the power of 9', text)
    
    # Handle fractions
    text = re.sub(r'\d+/\d+', lambda m: m.group().replace('/', ' divided by '), text)
    
    # Handle scientific notation
    text = re.sub(r'(\d+)e([+-]?\d+)', lambda m: f"{m.group(1)} times ten to the power of {m.group(2)}", text)
    
    # Replace physics variables and units
    for symbol, replacement in physics_replacements.items():
        text = text.replace(symbol, replacement)
    
    # Replace math symbols
    for symbol, replacement in replacements.items():
        text = text.replace(symbol, replacement)
    
    # Handle function notation and parentheses
    text = re.sub(r'([A-Za-z])\(([^)]+)\)', lambda m: f"{m.group(1)} of {m.group(2).replace(',', ' and')}", text)
    text = re.sub(r'\(([^)]+)\)', lambda m: f" of {m.group(1)} ", text)
    
    # Add pauses around equations for better clarity
    text = re.sub(r'\$(.*?)\$', r', \1, ', text)
    text = re.sub(r'\\\((.*?)\\\)', r', \1, ', text)
    text = re.sub(r'\\\[(.*?)\\\]', r', \1, ', text)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
