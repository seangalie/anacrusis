"""Linux smoke check using real Flatpak in a disposable system installation."""

import configparser
import os
from pathlib import Path
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SYSTEM = ROOT / "files/system"
DESCRIPTOR = SYSTEM / "usr/share/flatpak/remotes.d/flathub.flatpakrepo"
SERVICE = SYSTEM / "usr/lib/systemd/system/anacrusis-flathub-setup.service"


def check():
    with tempfile.TemporaryDirectory(prefix="anacrusis-flatpak-") as directory:
        temp = Path(directory)
        installation = temp / "installation"
        env = {
            **os.environ,
            "FLATPAK_SYSTEM_DIR": str(installation),
            "FLATPAK_CONFIG_DIR": str(temp / "config"),
            "FLATPAK_DATA_DIR": str(temp / "data"),
        }
        for name in ("config", "data"):
            (temp / name).mkdir()

        def run(*arguments):
            return subprocess.run(arguments, env=env, check=True, text=True, timeout=120)

        def setup():
            # Exercise the actual service's Flatpak commands, replacing only
            # the immutable descriptor path with its source in this checkout.
            for line in SERVICE.read_text().splitlines():
                if line.startswith("ExecStart=/usr/bin/flatpak "):
                    arguments = shlex.split(line.removeprefix("ExecStart="))
                    arguments = [
                        str(DESCRIPTOR) if arg == "/usr/share/flatpak/remotes.d/flathub.flatpakrepo" else arg
                        for arg in arguments
                    ]
                    run(*arguments)

        def configuration():
            config = configparser.ConfigParser(interpolation=None)
            config.read(installation / "repo/config")
            return config

        setup()
        remote = 'remote "flathub"'
        fresh = configuration()[remote]
        assert fresh["url"] == "https://dl.flathub.org/repo/"
        assert fresh.getboolean("gpg-verify")
        assert not fresh.get("xa.filter")

        # Reproduce the filtered/disabled remote inherited from Fedora, with
        # another system remote whose configuration must remain untouched.
        filter_file = temp / "fedora-flathub.filter"
        filter_file.write_text("deny *\nallow app/org.mozilla.firefox/*\n")
        run("flatpak", "remote-modify", "--system", f"--filter={filter_file}", "--disable", "--no-gpg-verify", "--subset=verified", "flathub")
        run("flatpak", "remote-add", "--system", "fedora", "oci+https://registry.fedoraproject.org")
        fedora_before = dict(configuration()['remote "fedora"'])

        setup()
        config = configuration()
        upgraded = config[remote]
        assert upgraded["url"] == "https://dl.flathub.org/repo/"
        assert upgraded.getboolean("gpg-verify")
        assert not upgraded.get("xa.filter")
        assert not upgraded.get("xa.subset")
        assert not upgraded.getboolean("xa.disable", fallback=False)
        assert not upgraded.getboolean("xa.noenumerate", fallback=False)
        assert not upgraded.getboolean("xa.nodeps", fallback=False)
        assert dict(config['remote "fedora"']) == fedora_before

        # A repeated migration must remain harmless to the configured remotes.
        before = {section: dict(config[section]) for section in config.sections()}
        setup()
        after = configuration()
        assert {section: dict(after[section]) for section in after.sections()} == before
        print("Flathub fresh setup, filter migration, signature verification, and repeat setup passed")


if __name__ == "__main__":
    check()
