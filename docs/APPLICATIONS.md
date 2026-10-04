# Application infrastructure

Anacrusis keeps Discover and its Flatpak backend, makes the full upstream Flathub
catalog available, and provides both Toolbx and Distrobox. This layer installs no
additional Flatpak applications and creates no containers automatically.

The shared configuration is `recipes/modules/applications.yml`. It installs the
Fedora `distrobox` and `toolbox` packages, copies the system configuration, and
enables the Flathub setup timer. The image build checks that Podman, Flatpak,
Discover, and Discover's Flatpak backend remain installed, and validates the
systemd units.

## Flathub configuration

The upstream descriptor is stored at
`files/system/usr/share/flatpak/remotes.d/flathub.flatpakrepo`. It was retrieved
from <https://dl.flathub.org/repo/flathub.flatpakrepo>; its SHA-256 is
`3371dd250e61d9e1633630073fefda153cd4426f72f4afa0c3373ae2e8fea03a`.
It includes Flathub's public signing key and has neither a filter nor a subset.
Review descriptor and signing-key changes before refreshing this copy.

Flatpak's [native defaults](https://docs.flatpak.org/en/latest/flatpak-command-reference.html#flatpakrepo)
create the system remote on fresh installations. Native defaults alone skip an
existing remote, so a one-time migration also handles an inherited filtered
Flathub installation:

1. Add `flathub` from the local descriptor if needed.
2. Enable it and GPG verification, clear its filter and subset, set the upstream URL, and expose its applications
   and runtime dependencies to Discover.
3. Write `/var/lib/anacrusis/flathub-configured-v1` only after both commands
   succeed.

The timer starts setup 30 seconds after boot. A failed setup retries every three
minutes, with each attempt limited to two minutes. Once the marker exists,
future boots skip setup. Users can subsequently disable Flathub or customize its
filter without Anacrusis repeatedly undoing their choice. The migration changes
system Flathub configuration; per-user remotes, other system remotes, and
installed applications are preserved. Existing remote trust is retained; new
remotes import the key from the descriptor. GPG verification stays enabled.

Flathub state and the migration marker live in persistent `/var`; rolling back
the operating-system image does not roll back that state.

This deliberately avoids BlueBuild's current `default-flatpaks` setup service,
which can remove Fedora remotes and their applications when a Fedora repository
is not also configured. See the [upstream implementation](https://github.com/blue-build/modules/blob/main/modules/default-flatpaks/v2/post-boot/system-flatpak-setup).

## Validation

The Linux CI smoke check uses real Flatpak in a disposable system installation.
It exercises fresh setup, migration from a filtered/disabled remote, retained
Fedora remote configuration, signature verification settings, and repeated
setup. It does not download or install applications. Run it on Linux with
Flatpak installed:

```sh
sudo python3 tests/check_flathub.py
```

Boot each architecture and complete these checks before declaring this layer
ready:

- Verify setup succeeds with `systemctl status anacrusis-flathub-setup.service`
  and inspect its journal. Confirm the marker appears only on success.
- Boot offline and verify local configuration works. Simulate a failed setup
  attempt and verify it retries successfully once the cause is resolved.
- Inspect `flatpak remotes --system --show-details`; confirm full Flathub is
  enabled. Open Discover and install, run, update, and remove a chosen app.
- Repeat from a Fedora installation with filtered Flathub and existing apps.
  Verify its apps and other remotes survive the migration.
- Disable Flathub after successful setup, reboot, and verify it stays disabled.
- Run `toolbox create` and `toolbox enter` as an ordinary user; separately create
  and enter a Distrobox using an image that supports the native architecture.
- Verify existing Toolbx containers survive an image update and rollback.

Build-time package checks and the isolated CI smoke check do not establish
desktop integration, container usability, or systemd retry behavior on a booted
Anacrusis system.
