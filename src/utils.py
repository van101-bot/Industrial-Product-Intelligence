import ast

def parse_dict(value):
    """Safely parse dict-like strings into Python dicts."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return ast.literal_eval(value)
        except Exception:
            return {}
    return {}

def build_search_text(*args):
    """Concatenate multiple fields into a single search string."""
    parts = [str(arg).strip() for arg in args if arg not in (None, "", "nan")]
    return " ".join(parts)
