"""Exercise transaction safeguards without pretending to resolve real RPMs."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]

# Simulate only the command boundary. Actual package solving belongs to the
# two-architecture image build; these tests target architecture selection,
# failure propagation, and protection against collateral removals.
FAKE_TOOL = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import re
import sys

state_path = Path(os.environ["RPM_TEST_STATE"])
state = json.loads(state_path.read_text())
arch = os.environ["RPM_TEST_ARCH"]
args = sys.argv[1:]
tool = Path(sys.argv[0]).name

def matches(spec):
    return [key for key in state if key == spec or key.startswith(spec + ".")]

if tool == "rpm":
    if "--eval" in args:
        print(arch)
    elif "-qa" in args:
        print("\n".join(state))
    else:
        specs = []
        skip = False
        for arg in args:
            if skip:
                skip = False
            elif arg == "--qf":
                skip = True
            elif not arg.startswith("-"):
                specs.append(arg)
        for spec in specs:
            keys = matches(spec)
            if not keys:
                sys.exit(1)
            if "--qf" in args:
                print(state[keys[0]], end="")
            elif "--quiet" not in args:
                print(spec)
elif tool == "dnf5":
    with open(os.environ["RPM_TEST_LOG"], "a") as log:
        log.write(json.dumps(args) + "\n")
    if os.environ.get("RPM_TEST_FAIL") == "1":
        print("Simulated unsatisfiable dependencies", file=sys.stderr)
        sys.exit(42)
    command = next(arg for arg in args if arg in ("swap", "install"))
    specs = [arg for arg in args[args.index(command) + 1:] if not arg.startswith("-")]
    if command == "swap":
        old = specs.pop(0)
        for key in matches(old):
            del state[key]
    for spec in specs:
        name = re.sub(r"-[0-9].*$", "", spec)
        if not name.endswith((".x86_64", ".aarch64")):
            name += "." + arch
        if spec != os.environ.get("RPM_TEST_OMIT"):
            state[name] = "26.2.3"
    if any(spec.startswith("ffmpeg.") for spec in specs):
        state.pop("libavcodec-free." + arch, None)
        state["ffmpeg-libs." + arch] = "8.1.3"
        removed = os.environ.get("RPM_TEST_DROP")
        if removed:
            state.pop(removed, None)
    state_path.write_text(json.dumps(state))
'''


class MultimediaTests(unittest.TestCase):
    def run_script(self, arch="x86_64", *, absent=False, **options):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            state = {
                f"mesa-filesystem.{arch}": "26.2.3",
                f"plasma-workspace.{arch}": "6.6.0",
                "plasma-workspace.i686": "6.6.0",
            }
            if not absent:
                for name in (
                    "ffmpeg-free",
                    "libavcodec-free",
                    "mesa-va-drivers",
                    "mesa-vulkan-drivers",
                ):
                    state[f"{name}.{arch}"] = "26.2.3"
            state_path = temp / "state.json"
            state_path.write_text(json.dumps(state))
            for tool in ("rpm", "dnf5"):
                path = temp / tool
                path.write_text(FAKE_TOOL)
                path.chmod(0o755)
            log = temp / "dnf.log"
            env = {
                **os.environ,
                "PATH": str(temp) + os.pathsep + os.environ["PATH"],
                "RPM_TEST_ARCH": arch,
                "RPM_TEST_STATE": str(state_path),
                "RPM_TEST_LOG": str(log),
                **options,
            }
            result = subprocess.run(
                ["bash", str(ROOT / "files/scripts/multimedia.sh")],
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            commands = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            return result, commands

    def test_both_architectures_and_matching_mesa(self):
        for arch in ("x86_64", "aarch64"):
            with self.subTest(arch=arch):
                result, commands = self.run_script(arch)
                self.assertEqual(result.returncode, 0, result.stderr)
                installed = [argument for command in commands for argument in command]
                self.assertEqual("intel-media-driver" in installed, arch == "x86_64")
                self.assertIn(f"mesa-va-drivers-freeworld-26.2.3.{arch}", installed)
                self.assertIn(f"mesa-vulkan-drivers-freeworld-26.2.3.{arch}", installed)

    def test_base_without_existing_codec_packages(self):
        result, _ = self.run_script("aarch64", absent=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_collateral_removal_fails_even_when_other_arch_remains(self):
        result, _ = self.run_script(RPM_TEST_DROP="plasma-workspace.i686")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unexpectedly removed plasma-workspace.i686", result.stderr)

    def test_solver_failure_stops_immediately(self):
        result, commands = self.run_script(RPM_TEST_FAIL="1")
        self.assertEqual(result.returncode, 42)
        self.assertEqual(len(commands), 1)

    def test_successful_command_with_missing_required_package_fails(self):
        result, _ = self.run_script(RPM_TEST_OMIT="libheif-freeworld")
        self.assertNotEqual(result.returncode, 0)

    def test_unknown_architecture_fails_before_mutation(self):
        result, commands = self.run_script("riscv64")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(commands, [])


if __name__ == "__main__":
    unittest.main()
