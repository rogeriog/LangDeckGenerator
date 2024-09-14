import os
import uuid
from pathlib import Path


def Config():
    """
    This function retrieves the PIXABAY_KEY from environment variables.
    """
    PIXABAY_KEY = os.environ.get("PIXABAY_KEY")
