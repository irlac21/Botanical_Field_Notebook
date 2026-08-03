import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

APP = PROJECT_DIR / "app.py"


subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APP)
    ]
)