# Anacrusis Project Specification

**Status:** Draft / working specification  
**Date:** 2026-10-03  
**Project:** Anacrusis  
**Repository:** `seangalie/anacrusis`

## 1. Project Summary

Anacrusis is an independent atomic KDE Linux desktop based on Fedora Kinoite.

The project goal is to preserve the familiarity and upstream character of Fedora Kinoite while incorporating a small number of practical improvements that experienced Fedora users commonly apply after installation. Anacrusis should improve capability and reduce repetitive setup work without becoming a heavily opinionated desktop distribution.

Anacrusis is not Fedora Kinoite and should be clearly branded and documented as an independent downstream project based on Fedora Kinoite.

## 2. Project Identity

The name **Anacrusis** comes from the musical term for pickup notes: notes that occur before the first full measure and lead into the next phrase.

The name reflects several ideas behind the project:

- giving good hardware another useful life;
- taking a strong upstream base and carrying it into a new movement;
- creating momentum toward what comes next without discarding what came before;
- maintaining an art- and music-adjacent identity without tying the project to a specific hardware category.

### Technical descriptor

> **Anacrusis — an independent atomic KDE desktop based on Fedora Kinoite.**

The project should not use Fedora, Kinoite, KDE, Atomic, Immutable, Blue, or similar upstream terms as part of the primary product name.

## 3. Core Principles

### 3.1 Fedora first

Anacrusis should inherit Fedora Kinoite defaults unless there is a concrete reason to change them.

Changes should solve broadly applicable problems or remove common post-install friction. Personal workflow preferences should not become system defaults.

### 3.2 Capability over replacement

Where possible, Anacrusis should add useful capability rather than replace upstream components.

Examples:

- Keep KDE Discover rather than replacing it with Bazaar.
- Keep Fedora KDE Plasma defaults rather than imposing a custom desktop layout.
- Add Distrobox while retaining Toolbx.
- Add Homebrew as a complementary user-space package manager rather than replacing Fedora tooling.

### 3.3 Keep the immutable host deliberate

The image should contain software that belongs to the operating system:

- hardware enablement;
- drivers;
- codecs and multimedia integration;
- system services;
- core host utilities needed by the platform;
- software required to support Anacrusis features.

General user applications, development stacks, and personal workflow tools should normally live outside the immutable image.

### 3.4 User software belongs in the appropriate layer

Preferred software-management hierarchy:

1. **OS image / RPM** — hardware, system services, codecs, host integration.
2. **Flatpak / Flathub** — graphical desktop applications.
3. **Homebrew** — user-level CLI applications and developer utilities.
4. **Toolbx** — Fedora-native mutable development environments.
5. **Distrobox** — alternate Linux userlands and mutable development environments.
6. **ujust** — configuration, orchestration, optional workflows, recovery, and setup helpers.

### 3.5 Optional workflows should remain optional

Anacrusis should support opinionated workflows through `ujust` recipes rather than imposing them as defaults.

Examples include:

- MouseTiler;
- a left-side Plasma panel;
- developer CLI bundles;
- gaming setup;
- TPM-based LUKS unlock;
- SSH server setup;
- laptop power-management tweaks.

### 3.6 Multi-architecture is a first-class requirement

The standard Anacrusis image should support both:

- `x86_64` / `linux/amd64`
- `aarch64` / `linux/arm64`

A feature should not be added to the standard image without considering both architectures.

Hardware-specific variants may intentionally support only one architecture.

## 4. Baseline Product Matrix

| Area | Decision |
| --- | --- |
| Base | Fedora Kinoite |
| Architectures | x86_64 + aarch64 |
| Kernel | Fedora stock |
| Desktop | Fedora KDE Plasma defaults |
| Discover | Keep |
| Bazaar | Reject |
| RPM Fusion Free | Enable |
| RPM Fusion Nonfree | Enable, selective use |
| Full FFmpeg | RPM Fusion |
| Extended GStreamer codecs | RPM Fusion |
| HEIF codecs | RPM Fusion |
| Mesa VA-API freeworld | Include |
| Mesa Vulkan freeworld | Include |
| Flatpak | Keep |
| Flathub | Full upstream remote |
| Default extra Flatpaks | None or minimal |
| Toolbx | Include |
| Distrobox | Include |
| Homebrew | Include |
| `ujust` | Include |
| NVIDIA Open | Separate x86_64 variant |
| Apple T2 | Separate x86_64 variant |
| Custom kernel | T2 variant only |
| Gaming stack | User-selectable, not baked in |

## 5. Base Image Strategy

The project should begin from Fedora's Kinoite OCI image rather than a Universal Blue product image.

Initial baseline:

```yaml
base-image: quay.io/fedora-ostree-desktops/kinoite
image-version: 44

platforms:
  - linux/amd64
  - linux/arm64
```

The rationale is to keep Anacrusis close to Fedora Kinoite and selectively add desired functionality instead of inheriting and then removing broader Universal Blue product decisions.

If Fedora later changes the preferred official desktop bootc/OCI source, Anacrusis should follow Fedora rather than preserve an obsolete base for compatibility.

## 6. Desktop Policy

The default Anacrusis desktop should remain visually and behaviorally close to Fedora Kinoite.

### Keep

- Fedora/KDE Plasma defaults
- stock Plasma panel behavior
- stock KDE applications unless specifically justified
- KDE Discover
- upstream KDE configuration interfaces

### Light Anacrusis identity is acceptable

Appropriate identity changes include:

- Anacrusis distribution name;
- Anacrusis logo;
- `/etc/os-release`;
- boot and installer identification;
- About System identity;
- restrained Anacrusis wallpaper or lock-screen artwork.

### Do not impose by default

- custom panel placement;
- tiling scripts;
- custom keyboard layouts;
- custom workspace behavior;
- heavy Plasma theming;
- replacement launchers or app stores.

These belong in optional recipes or future purpose-built derivatives.

## 7. Multimedia and RPM Fusion

RPM Fusion is part of the standard Anacrusis design because it fills common multimedia and hardware-acceleration gaps while remaining familiar to experienced Fedora users.

### Repositories

Enable:

- RPM Fusion Free
- RPM Fusion Nonfree

Nonfree packages should be consumed selectively.

### Standard multimedia target

Expected standard-image components include:

- full RPM Fusion `ffmpeg`;
- `ffmpeg-libs`;
- extended GStreamer plugins;
- `libheif-freeworld`;
- HEIF desktop integration;
- `ffmpegthumbnailer`;
- `mesa-va-drivers-freeworld`;
- `mesa-vulkan-drivers-freeworld`.

The project should prefer coherent package replacement over fragile partial codec combinations when practical.

CI should fail rather than silently fall back to reduced Fedora codec functionality when RPM Fusion temporarily lags an upstream package transition.

## 8. Flatpak and Flathub

Flatpak remains the primary GUI application model.

Anacrusis should configure the normal unrestricted upstream Flathub remote directly.

### Policy

- Keep KDE Discover.
- Keep the Flatpak CLI.
- Do not replace Discover with Bazaar.
- Do not ship a large curated Flatpak application bundle by default.
- Let users select applications through Discover or `flatpak`.
- Optional application bundles may later be implemented through `ujust`.

Potential future optional bundles:

- creative applications;
- developer applications;
- gaming applications;
- communications/office applications.

## 9. Toolbx and Distrobox

Both should ship.

### Toolbx

Primary role:

- Fedora-native development and troubleshooting;
- mutable Fedora development environments;
- close alignment with upstream Fedora workflows.

### Distrobox

Primary role:

- alternate Linux userlands;
- Ubuntu, Debian, Arch, openSUSE, and similar environments;
- mutable development workloads that do not belong on the host.

The existence of these tools should reduce pressure to layer project-specific development packages into the host image.

## 10. Homebrew

Homebrew should be included as the preferred home for user-level CLI utilities.

Anacrusis should use the established Universal Blue/BlueBuild Homebrew integration where practical rather than inventing a separate installation layout.

Homebrew should not define Anacrusis defaults. It provides a supported user-space software channel.

Typical optional CLI categories include:

- shell productivity;
- Git and repository tools;
- system monitoring;
- development utilities;
- AI/ML CLI tools.

These should normally be installed by users or optional `ujust` bundles, not preinstalled in the image.

## 11. ujust

`ujust` is a core Anacrusis capability, but should remain a thin orchestration layer rather than an Anacrusis-only replacement for upstream tools.

A user should still be able to see and use the underlying Fedora, KDE, bootc, Flatpak, Homebrew, Toolbx, and Distrobox mechanisms directly.

### Initial recipe families

#### System

- `firmware-check`
- `firmware-update`
- `setup-luks-tpm`
- `setup-ssh-server`
- `configure-s2idle`

#### Hardware

- `hardware-info`
- `gpu-diagnostics`
- T2-specific helpers

#### Software

- `install-cli-tools`
- `install-developer-tools`
- optional Flatpak bundles later

#### Networking

- `mesh-network`
- `install-tailscale`
- `install-netbird`
- `install-nebula`
- `install-zerotier`

Mesh networking recipes should install and prepare the selected client but should not enroll the machine into a user's private network automatically. Authentication, enrollment keys, management URLs, and network IDs remain under the control of the upstream client and the user.

#### Desktop and themes

- `install-mousetiler`
- `theme-retro`
- additional optional theme/profile recipes
- possible future productivity profile

Theme recipes may combine Plasma panel placement, color schemes, wallpaper, window-management helpers, and related user-facing configuration into a coherent optional profile. They must not change the default Anacrusis desktop experience.

#### Recovery

- `system-status`
- `update`
- `rollback`
- `pin-deployment`

Names are provisional. Recipes should be small, explicit, inspectable, and reversible where practical.

## 12. Updates

`bootc` should be the authoritative operating-system update path.

### Default update behavior

| Behavior | Default |
| --- | --- |
| Check for OS updates | Automatic |
| Download/stage OS update | Automatic |
| Automatic reboot | No |
| Manual update | Yes |
| Rollback | Yes |
| Automatic major Fedora release upgrade | No |

Anacrusis should not allow Fedora's rpm-ostree GUI updater and a bootc updater to compete for ownership of the host update path.

### Discover

Discover should manage applications, not the host operating-system image.

The rpm-ostree Discover backend should be removed or disabled if it conflicts with the bootc update design.

### Other package domains

- Flatpaks: managed by Discover / Flatpak.
- Homebrew: managed by Brew and its own timers.
- Toolbx: user controlled.
- Distrobox: user controlled.

Anacrusis should not automatically mutate user development containers.

### No forced reboot

The system may check, download, and stage an update automatically, but should wait for the user's normal reboot.

## 13. Rollback and Recovery

Rollback is a normal feature of the platform, not an emergency-only feature.

Anacrusis documentation and `ujust` should make it easy to:

- inspect the current deployment;
- identify the previous deployment;
- roll back;
- pin a known-good deployment before risky changes;
- distinguish OS rollback from user-data backup.

A future user-data snapshot strategy may complement bootc rollback, but root-filesystem Snapper behavior should not be copied from mutable Fedora without separate evaluation.

## 14. Release Lifecycle

Anacrusis follows Fedora's lifecycle rather than inventing an independent LTS policy.

### Supported states

At any given time, the project may maintain:

- the current stable Fedora-based Anacrusis release;
- the previous still-supported Fedora-based release;
- a public testing release based on the next Fedora Beta.

### Testing start

The public next-release testing branch begins when Fedora publishes the first Beta Atomic/Kinoite images.

Pre-Beta CI experimentation may occur internally, but Beta is the public starting line.

### GA promotion

Fedora GA does not automatically promote the Anacrusis testing image to stable.

Promotion occurs only after Anacrusis validation succeeds.

### End of life

When the corresponding Fedora release reaches end of life:

- new Anacrusis builds for that release stop;
- the final signed image may remain available;
- the release is marked unsupported;
- Anacrusis does not claim security support beyond Fedora's lifecycle.

## 15. Versioning and Registry Tags

Anacrusis follows Fedora release numbering.

Examples:

- Anacrusis 44
- Anacrusis 45
- Anacrusis 46

Do not introduce a separate arbitrary semantic release number for the distribution.

### Installed systems should track explicit release tags

Preferred:

```text
ghcr.io/seangalie/anacrusis:44
ghcr.io/seangalie/anacrusis:45
```

Avoid installed systems tracking moving major-release tags such as `latest` or a generic `stable`.

A Fedora major-version upgrade should require explicit user action.

### Testing tags

Examples:

```text
ghcr.io/seangalie/anacrusis:45-testing
```

Hardware variants should use separate image names rather than overloading tags where practical.

## 16. Image Family

### Standard

**Anacrusis**

Architectures:

- x86_64
- aarch64

Kernel:

- Fedora stock

This is the canonical product and highest-priority image.

### NVIDIA Open

**Anacrusis NVIDIA**

Initial architecture:

- x86_64

Kernel:

- Fedora stock

Driver strategy:

- NVIDIA open kernel modules
- appropriate NVIDIA user-space components
- Secure Boot integration

ARM64 NVIDIA support may be explored later but should remain experimental until the full dependency chain is proven.

### Apple T2

**Anacrusis T2**

Architecture:

- x86_64

Kernel:

- T2 Linux Fedora-patched kernel

Additional requirements may include:

- T2 support packages;
- audio integration;
- fan support;
- firmware extraction helpers;
- T2-specific kernel arguments.

Apple firmware that cannot legally be redistributed must not be embedded in the image. Anacrusis should instead provide a helper to guide firmware extraction from a user's own macOS installation.

## 17. Hardware Support Policy

Support tiers describe what the project tests and promises, not the relative importance of an architecture.

Initial target:

| Image | Architecture | Initial status |
| --- | --- | --- |
| Standard | x86_64 | Tier 1 |
| Standard | aarch64 | Tier 1 |
| NVIDIA Open | x86_64 | Tier 1 |
| T2 | x86_64 | Tier 2 / specialized |
| NVIDIA Open | aarch64 | Experimental / future |

Hardware-specific variants should not pollute the standard image.

## 18. Optional System Helpers Derived from Prior Setup Guides

The following recurring setup tasks are candidates for `ujust`, documentation, or future modules.

### Strong candidates

- firmware checking/updating;
- TPM2/LUKS enrollment with recovery-key guardrails;
- hardware and GPU diagnostics;
- T2 firmware helper;
- SSH server setup and hardening;
- laptop `s2idle` configuration;
- optional CLI tool bootstrap;
- optional mesh-network client installation.

### Mesh networking

Anacrusis should support common mesh/VPN clients as optional host-integrated recipes rather than preinstalling any one provider.

Initial candidates:

- Tailscale
- NetBird
- Nebula
- ZeroTier

The project should support the category rather than prefer the maintainer's personal provider.

Mesh-network recipes should:

- detect an existing installation before changing anything;
- prefer signed package repositories or Fedora packages over remote `curl | sudo bash` installers;
- install only the selected provider;
- enable required system services where appropriate;
- never capture or persist authentication secrets, enrollment keys, private management URLs, or network IDs;
- leave account authentication and network enrollment to the upstream client;
- provide the upstream command needed to continue;
- document whether a reboot is required;
- provide or document a clean removal path, including third-party repository cleanup;
- support x86_64 and aarch64 where the upstream provider supports both.

### Document first, automate later

- SMB/CIFS mounting;
- advanced firewall configuration;
- user-data snapshot strategy;
- custom GRUB appearance.

### Keep out of Anacrusis defaults

- hardcoded DNS-over-TLS provider choices;
- private NetBird infrastructure;
- large personal font bundles;
- personal application selections;
- boot-service disabling that may be hardware/network dependent.

## 19. Optional Theme Profiles

Anacrusis may provide optional desktop theme/profile recipes as a way to support expressive Plasma customization without changing the base desktop.

The base Anacrusis session should continue to track Fedora Kinoite/KDE Plasma defaults.

Theme recipes may combine:

- Plasma panel placement and sizing;
- KDE color schemes;
- wallpapers;
- icon or cursor selections where licensing and packaging are appropriate;
- window-management helpers such as MouseTiler;
- workspace or launcher configuration;
- other reversible user-level Plasma settings.

Example:

```text
ujust theme-retro
```

A `theme-retro` profile might combine a retro-inspired color palette with a left-side panel and other coordinated Plasma settings.

Theme/profile rules:

- themes are opt-in only;
- theme recipes must not be required for normal Anacrusis operation;
- recipes should modify user configuration rather than system-wide defaults whenever practical;
- changes should be reversible, ideally with a documented restore/default recipe;
- theme assets must have compatible redistribution licenses;
- theme recipes should avoid brittle direct editing of large Plasma configuration files when supported KDE configuration interfaces exist;
- a theme should represent a coherent profile rather than a collection of arbitrary tweaks;
- no theme becomes the default merely because it is maintained or preferred by the project maintainer.

This model allows Anacrusis to participate in the broader interest in highly customized Linux desktop aesthetics without turning Anacrusis itself into a themed distribution.

## 20. Security and Safety Guardrails for Recipes

Recipes that make consequential system changes should:

- inspect the current state first;
- clearly describe the change;
- avoid hardcoded device names;
- create or verify recovery paths where appropriate;
- require confirmation before destructive or security-sensitive changes;
- fail safely when prerequisites are missing;
- avoid downloading and executing unpinned third-party scripts without explicit justification.

Examples:

- TPM/LUKS setup must verify a recovery key before enrollment.
- SSH hardening should verify that a usable authorized public key exists before disabling password authentication.
- T2 firmware helpers should make clear that firmware comes from the user's own system and is not supplied by Anacrusis.

## 21. Initial Repository Architecture

The repository should favor composable shared modules over one monolithic recipe.

Conceptual structure:

```text
anacrusis/
├── recipes/
│   ├── anacrusis.yml
│   ├── modules/
│   │   ├── identity.yml
│   │   ├── multimedia.yml
│   │   ├── flatpak.yml
│   │   ├── containers.yml
│   │   ├── brew.yml
│   │   ├── ujust.yml
│   │   └── updates.yml
│   └── variants/
│       ├── nvidia.yml
│       └── t2.yml
├── files/
│   └── system/
├── just/
├── docs/
├── .github/
└── README.md
```

The exact structure may change as BlueBuild implementation details are validated.

## 22. Contributor and Agent Guardrails

These rules are intended for human contributors and coding agents.

1. Do not add a new default application or system customization solely because it is useful to one workflow.
2. Prefer upstream Fedora/KDE behavior unless the specification explicitly changes it.
3. Prefer optional `ujust` recipes for workflow preferences.
4. Consider x86_64 and aarch64 before adding anything to the standard image.
5. Keep hardware-specific dependencies inside hardware-specific variants.
6. Do not replace KDE Discover.
7. Do not introduce a custom kernel into the standard image.
8. Do not add a gaming stack to the standard image.
9. Do not automatically update Toolbx or Distrobox containers.
10. Keep host-package additions deliberate and small.
11. Optional networking integrations should support multiple providers rather than making one provider part of the Anacrusis identity.
12. Optional desktop theming belongs in recipes/profiles, not in the default Plasma configuration.
13. Prefer small pull requests that implement one architectural decision at a time.
14. Any proposal that materially changes these principles should update this specification before or alongside the implementation.

## 23. Explicit Non-Goals

Anacrusis is not intended to be:

- Bazzite without gaming;
- Aurora with features removed;
- a custom Plasma theme distribution;
- a gaming-first distribution;
- a developer-stack distribution;
- an old-hardware-only distribution;
- an LTS Fedora derivative;
- a replacement for Fedora Kinoite;
- a platform that hides Fedora/KDE/bootc mechanics behind proprietary abstractions.

## 24. Open Research Items

The following remain intentionally unresolved:

- exact implementation of RPM Fusion repository and package replacement in BlueBuild;
- exact `ujust` packaging strategy and dependency chain;
- whether to use Universal Blue's existing `ublue-os-just` package unchanged or eventually reduce dependencies;
- exact bootc staging timer implementation;
- rechunking / Chunkah optimization after the initial image works;
- Secure Boot workflow for NVIDIA;
- ARM64 NVIDIA feasibility;
- full T2 image build mechanism;
- user-data snapshot strategy;
- installation/ISO strategy;
- first-boot/onboarding experience;
- final visual identity, logo, and wallpaper;
- trademark/domain diligence for Anacrusis before broader public promotion.

## 25. Initial Acceptance Criteria

The first Anacrusis baseline is successful when:

- Fedora Kinoite builds through BlueBuild;
- x86_64 image publishes successfully;
- aarch64 image publishes successfully;
- both are represented under the intended release tag;
- Cosign signing works;
- the image can boot on a test system or VM;
- the image identifies itself as Anacrusis only after the identity milestone is intentionally added;
- no example BlueBuild packages, application removals, or demo Flatpaks remain unintentionally.

This baseline should remain intentionally boring. Features are added only after the build pipeline itself is proven.
