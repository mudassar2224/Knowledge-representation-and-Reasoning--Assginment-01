# AIML loader for greetings, help, and farewells.

import os
import re

import aiml


_kernel = None


def load_aiml():
    """Bootstrap the AIML kernel with family.aiml."""
    global _kernel

    aiml_path = os.path.join(os.path.dirname(__file__), "family.aiml")

    _kernel = aiml.Kernel()
    _kernel.setTextEncoding(None)
    _kernel.learn(aiml_path)
    print("[AIML] Bot loaded successfully.")
    return _kernel


def get_kernel():
    global _kernel
    if _kernel is None:
        load_aiml()
    return _kernel


def _aiml_text(user_input):
    text = user_input.strip().upper()
    text = re.sub(r"[^A-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_aiml_response(user_input):
    """Return an AIML response string, or an empty string when nothing matched."""
    response = get_kernel().respond(_aiml_text(user_input))
    return response.strip() if response else ""
