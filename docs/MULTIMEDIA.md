# Multimedia layer

`recipes/modules/multimedia.yml` enables RPM Fusion Free and Nonfree through
BlueBuild's [DNF module](https://blue-build.org/reference/modules/dnf/), then runs
`files/scripts/multimedia.sh`. The script executes at image build time, not on
the installed user's machine.

## Package policy

- Replace Fedora's restricted FFmpeg CLI and conflicting libraries with RPM
  Fusion's `ffmpeg` and `ffmpeg-libs`.
- Install Fedora's `gstreamer1-plugin-libav` together with RPM Fusion's
  `gstreamer1-plugins-bad-freeworld` and `gstreamer1-plugins-ugly`.
- Add `libheif-freeworld` and Fedora's `heif-pixbuf-loader` for HEIF support.
- Replace the native architecture's Mesa VA-API and Vulkan driver packages with
  their freeworld equivalents for hardware video codecs.
- Install `intel-media-driver` on x86_64 only. ARM builds use the shared Mesa
  packages and must not silently skip missing packages.

Package names were checked against Fedora and RPM Fusion's Fedora 44 metadata
for x86_64 and aarch64. Fedora's current FFmpeg GStreamer plugin is
[`gstreamer1-plugin-libav`](https://packages.fedoraproject.org/pkgs/gstreamer1-plugin-libav/gstreamer1-plugin-libav/),
rather than the historical `gstreamer1-libav` name. RPM Fusion's Fedora 44 Mesa
packages provide VA-API and Vulkan drivers; the old `mesa-vdpau-drivers-freeworld`
package is absent from these repositories.

References: [RPM Fusion package repositories](https://download1.rpmfusion.org/free/fedora/),
[Mesa freeworld source](https://github.com/rpmfusion/mesa-freeworld), and
[RPM Fusion multimedia guidance](https://rpmfusion.org/Howto/Multimedia).

## Build safeguards

Mesa freeworld packages depend on the matching Fedora `mesa-filesystem` version.
The script requests that exact version from the enabled stable repositories. If
RPM Fusion lags Fedora, the build fails and the previously published image stays
available. Do not fix a mismatch by enabling testing repositories, downgrading
the graphics stack, or skipping packages.

FFmpeg conflicts require an
[`--allowerasing` transaction](https://dnf5.readthedocs.io/en/latest/commands/swap.8.html).
The script records installed package names and architectures before changes and
rejects removals outside the explicitly replaced FFmpeg and Mesa packages. This
protects the existing desktop and applications even if the solver finds an
unexpected way to satisfy a dependency conflict. Required codec packages are
queried again at the end, so a missing installation also fails the build.

Weak dependencies are disabled for these transactions to avoid pulling optional
applications into the platform layer. RPM signature checking stays enabled. No
package-solving errors are ignored.

## Validation checkpoint

The local regression suite tests architecture selection, exact Mesa version
requests, unsupported architectures, solver failure propagation, missing required
packages, and rejection of collateral removals including multilib packages. It
uses simulated `rpm` and `dnf5` commands and does not validate actual dependencies.

Before describing multimedia support as verified:

1. Build the composed recipe successfully for both architectures in CI and
   verify the resulting signed image index.
2. Confirm Plasma, Discover, Firefox, and Toolbx remain installed and usable.
3. Play known H.264, H.265, and AAC samples through both FFmpeg and GStreamer.
4. Open a HEIF image in relevant desktop applications.
5. Test VA-API and Vulkan video support on applicable AMD/Intel hardware; a VM
   without GPU passthrough does not establish hardware codec support.

Record tested image digests, hardware, and media results. The initial signed
Kinoite baseline build alone is not evidence that this layer works.
