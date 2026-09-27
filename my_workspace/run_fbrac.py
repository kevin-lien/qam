import argparse
import os
from pathlib import Path
import shlex
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML is required. Use a Python environment containing PyYAML and the repo dependencies.")

workspace_dir = Path(__file__).resolve().parent
repo_dir = workspace_dir.parent
parser = argparse.ArgumentParser(description="Launch FBRAC using YAML command-line settings.")
parser.add_argument("config", nargs="?", type=Path, default=workspace_dir / "my.yaml")
parser.add_argument("--dry-run", action="store_true", help="Print the command without running training.")
args = parser.parse_args()
with args.config.open() as file:
    config = yaml.safe_load(file)
if not isinstance(config, dict) or config.get("agent") != "agents/fbrac.py":
    parser.error("Config must be a mapping with agent: agents/fbrac.py")

command = [sys.executable, "main.py", "--agent=agents/fbrac.py"]
for key, value in config.items():
    if key == "agent":
        continue
    if isinstance(value, list):
        value = tuple(value)
    elif not isinstance(value, (str, bool, int, float)):
        parser.error(f"Unsupported value for {key}: use a scalar or list.")
    command.append(f"--{key}={value}")

os.chdir(repo_dir)
print(f"MUJOCO_GL=egl {shlex.join(command)}", flush=True)
if not args.dry_run:
    os.execv(sys.executable, command)
