from pathlib import Path

prompts_path = Path(__file__).parent

USER = (prompts_path / "user.txt").read_text()
SYSTEM = (prompts_path / "system.txt").read_text()
