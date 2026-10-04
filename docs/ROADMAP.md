# Anacrusis roadmap

Anacrusis is an independent atomic KDE desktop based on Fedora Kinoite. Preserve
Fedora's desktop workflow and expose upstream functionality. Default what improves
the platform broadly; offer personal workflow changes through optional recipes.

## Baseline: build, publish, boot

The initial Fedora 44 recipe built directly from
`quay.io/fedora-ostree-desktops/kinoite:44`, targeted amd64 and arm64, and included
only signing. CI built and published both architectures and verified the image
signature. The public image index was inspected independently. New layers still
need their own image builds and runtime validation.

Milestone zero is complete only after these remaining checks:

- Boot each architecture in a disposable VM and reach a working Plasma session.
- Test acquisition of signing trust and a signed installation or rebase.
- Verify an image update is staged, boots successfully, and retains user data.
- Exercise rollback to the previous deployment after a failed update.
- Record image digests, VM setup, commands, and results for reproducibility.

Passing a container build establishes the pipeline; it does not establish that
the resulting operating system boots or that recovery works.

## Identity

The shared configuration is `recipes/modules/identity.yml`, now enabled in the
recipe. It uses BlueBuild's `os-release` module to
set the displayed name to Anacrusis, identify the release as Anacrusis 44, and
point project links at this repository.

Preserve Fedora's `ID`, `ID_LIKE`, `VERSION_ID`, and `VARIANT_ID` for upstream
tool compatibility. Keep Plasma's layout, theme, shortcuts, and applications
unchanged in this milestone. Cosmetic assets can follow separately.

The identity configuration runs after package changes and before signing:

```yaml
modules:
  - from-file: modules/multimedia.yml
  - from-file: modules/applications.yml
  - from-file: modules/identity.yml
  - type: signing
```

Validate and build both architectures, then inspect `/etc/os-release` and
the displayed identity in a VM. Identity changes must preserve the already
working publication and signing path.

## Platform layers

Add one layer per reviewed change, using shared configuration under
`recipes/modules/`:

1. RPM Fusion Free and Nonfree multimedia support, including codecs and
   appropriate Mesa replacements. Verify package availability and conflicts on
   both architectures before enabling replacements.
2. Full Flathub configuration while retaining Discover.
3. Distrobox while retaining Toolbx.
4. Homebrew integration.
5. An Anacrusis `ujust` framework with a small initial recipe set.
6. bootc update staging without automatic reboot, with competing update
   mechanisms handled explicitly. Test this policy in VMs before recommending it.
7. Light desktop branding that preserves the Fedora/KDE workflow.

The first multimedia implementation is now enabled through
`recipes/modules/multimedia.yml`; see [its package policy and validation
requirements](MULTIMEDIA.md). The identity and multimedia changes have not yet
completed a full image build. The next application infrastructure checkpoint is
prepared separately through `recipes/modules/applications.yml`: full Flathub,
Distrobox, and retained Toolbx and Discover. See [its configuration and runtime
checks](APPLICATIONS.md). Merge this checkpoint after the multimedia checkpoint
passes its image builds.

Each layer must build on both architectures and receive runtime checks relevant
to its behavior. Do not describe a planned capability as already available.

## Releases and variants

Use explicit Fedora release tags. A future `45-testing` channel follows a
working 44 baseline; promotion and major upgrades must be deliberate. Do not
silently redirect installed users to a newer Fedora release.

NVIDIA Open and T2 hardware variants can follow the shared base. Require a
hardware-specific need, upstream package support, and a realistic testing path
before adding a variant or promising architecture coverage.

MouseTiler, a left-side Plasma panel, and other personal desktop preferences
belong in optional `ujust` recipes. Prefer KDE's supported configuration
interfaces and keep user changes reversible.

## Agreed baseline decisions

These decisions carry forward the project brainstorming. Revisit them explicitly
when evidence warrants a change.

| Area | Decision |
| --- | --- |
| Desktop and kernel | Stock Fedora KDE experience and stock Fedora kernel |
| Application store | Keep Discover; full upstream Flathub; no additional default Flatpaks for now |
| Multimedia | RPM Fusion Free, selective Nonfree packages, full FFmpeg/GStreamer/HEIF support, Mesa VA-API and Vulkan replacements |
| CLI and development | Toolbx, Distrobox, Homebrew, and an Anacrusis `ujust` toolbox |
| Gaming | Optional user-selected setup |
| Hardware variants | Separate x86_64 NVIDIA Open and T2 images; stock kernel except where T2 requires otherwise |
| Personal preferences | Optional recipes for MouseTiler, panel placement, and application bundles |

## Optional toolbox candidates

Design the `ujust` framework before adding a large recipe collection. Start with
status and diagnostics, then introduce helpers with explicit prompts, documented
effects, and a recovery path where they modify system configuration:

- System, GPU, and hardware diagnostics; explicit firmware checks and updates.
- Optional CLI/developer/AI tools and Flatpak application bundles.
- KDE layout and MouseTiler helpers using supported KDE interfaces.
- SSH hardening that verifies working key access before disabling password login.
- TPM/LUKS enrollment that verifies hardware, Secure Boot state, the target
  device, and a usable recovery key before enrollment. Review PCR policy rather
  than copying one fixed policy from a personal setup guide.
- Hardware-specific suspend tuning, and firmware extraction for a future T2
  variant.

Investigate Fedora's existing firewall behavior for KDE Connect and mDNS before
adding rules. Research snapshots for user data separately from image rollback;
do not layer a traditional root Snapper workflow onto bootc. Evaluate SMB/CIFS
documentation and multimedia thumbnail integration against the actual KDE base
before installing additional services or packages.

Personal DNS providers, private-network agents, large personal font collections,
and blanket service disabling stay outside the default image. The personal setup
guides are sources of candidate recipes, not specifications to apply wholesale.
