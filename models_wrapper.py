import importlib
import sys

class CodeSnippet:
    pass

def import_models():
    try:
        models_module = importlib.import_module("models")
        if hasattr(models_module, 'CodeSnippet'):
            global CodeSnippet
            CodeSnippet = models_module.CodeSnippet
    except Exception as e:
        print(f"Error importing models: {e}")
        print("Using fallback CodeSnippet class.")

import_models()
