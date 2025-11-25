import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared import setup_logging

setup_logging()
