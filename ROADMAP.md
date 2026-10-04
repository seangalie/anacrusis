# Anacrusis Roadmap

**Status:** Working roadmap  
**Date:** 2026-10-03

This roadmap implements the decisions in `PROJECT_SPEC.md`. The specification is authoritative when this roadmap and the spec conflict.

## Phase 0 — Build Pipeline Baseline

Goal: prove that Anacrusis can build and publish a minimal Fedora Kinoite-derived image before adding product features.

### Deliverables

- [ ] BlueBuild repository scaffold
- [ ] Fedora Kinoite 44 base
- [ ] `linux/amd64`
- [ ] `linux/arm64`
- [ ] Cosign signing
- [ ] explicit Fedora release tag (`:44`)
- [ ] successful GitHub Actions build
- [ ] successful image publication
- [ ] basic boot/rebase validation

### Do not add yet

- RPM Fusion
- Homebrew
- custom Flatpaks
- Distrobox changes
- `ujust`
- branding beyond metadata required for the build
- NVIDIA
- T2

## Phase 1 — Anacrusis Identity

Goal: make the image clearly Anacrusis without changing Plasma workflow.

### Deliverables

- [ ] project description and README
- [ ] `/etc/os-release` identity
- [ ] `ID=anacrusis`
- [ ] `ID_LIKE=fedora`
- [ ] release-aware `PRETTY_NAME`
- [ ] appropriate boot/About System identity
- [ ] initial project documentation
- [ ] Fedora/Kinoite relationship and independence statement

### Deferred

- logo polish
- final wallpaper
- installer artwork
- heavy branding

## Phase 2 — Multimedia and RPM Fusion

Goal: solve common Fedora multimedia and codec setup while retaining Fedora's overall system architecture.

### Deliverables

- [ ] RPM Fusion Free
- [ ] RPM Fusion Nonfree
- [ ] full FFmpeg stack
- [ ] extended GStreamer codecs
- [ ] `libheif-freeworld`
- [ ] HEIF desktop integration
- [ ] `ffmpegthumbnailer`
- [ ] `mesa-va-drivers-freeworld`
- [ ] `mesa-vulkan-drivers-freeworld`
- [ ] x86_64 build validation
- [ ] aarch64 build validation

### Validation

- [ ] video decode functionality
- [ ] HEIF/HEIC thumbnails/previews
- [ ] hardware video acceleration where supported
- [ ] CI failure is visible if RPM Fusion/Fedora package versions temporarily diverge

## Phase 3 — Application Infrastructure

Goal: provide a clean GUI software path without imposing application choices.

### Deliverables

- [ ] full upstream Flathub remote
- [ ] KDE Discover retained
- [ ] Flatpak CLI retained
- [ ] Fedora-filtered Flathub behavior removed/replaced where necessary
- [ ] no large default Flatpak bundle
- [ ] document Discover/Flatpak as GUI application path

## Phase 4 — Mutable User-Space Tooling

Goal: provide flexible CLI and development environments without encouraging host layering.

### Deliverables

- [ ] Toolbx retained
- [ ] Distrobox included
- [ ] Homebrew included
- [ ] Homebrew shell integration
- [ ] Homebrew update behavior documented
- [ ] software-management hierarchy documented

## Phase 5 — ujust Foundation

Goal: establish Anacrusis's optional configuration and orchestration layer.

### Initial recipes

- [ ] `system-status`
- [ ] `update`
- [ ] `rollback`
- [ ] `pin-deployment`
- [ ] `firmware-check`
- [ ] `firmware-update`
- [ ] `hardware-info`
- [ ] `gpu-diagnostics`

### Guardrails

- [ ] thin wrappers around upstream mechanisms
- [ ] commands remain visible and understandable
- [ ] no hidden automatic user-environment mutation
- [ ] safe failure on unsupported hardware

## Phase 6 — Update Policy

Goal: make bootc the authoritative OS update mechanism.

### Deliverables

- [ ] `bootc` host update path
- [ ] automatic update checking
- [ ] automatic download/staging
- [ ] no automatic reboot
- [ ] remove/disable competing rpm-ostree GUI host-update path
- [ ] Discover continues to manage Flatpaks
- [ ] Homebrew remains independently managed
- [ ] Toolbx/Distrobox remain user-controlled
- [ ] rollback documentation

## Phase 7 — Optional System and Networking Recipes

Goal: convert useful recurring setup tasks into safe opt-in helpers.

### High-priority system candidates

- [ ] `setup-luks-tpm`
- [ ] `setup-ssh-server`
- [ ] `configure-s2idle`
- [ ] `install-cli-tools`
- [ ] `install-developer-tools`

### Mesh networking

- [ ] `mesh-network` interactive selector
- [ ] `install-tailscale`
- [ ] `install-netbird`
- [ ] `install-nebula`
- [ ] `install-zerotier`

Networking recipes should install only the selected provider and leave authentication, enrollment, management URLs, and network IDs to the upstream client.

### Networking acceptance requirements

- [ ] signed package repository or Fedora package used where practical
- [ ] no remote `curl | sudo bash` installer in normal recipe flow
- [ ] no credential or enrollment-secret storage by Anacrusis
- [ ] service enablement handled where required
- [ ] clear next-step command shown to the user
- [ ] removal/cleanup path documented
- [ ] x86_64 and aarch64 support validated where upstream supports both

### Safety requirements

- [ ] no hardcoded LUKS device
- [ ] recovery key required/verified before TPM enrollment
- [ ] SSH public key verified before password auth is disabled
- [ ] clear confirmation before consequential changes

## Phase 8 — Optional Desktop Themes and Profiles

Goal: support expressive and productivity-focused Plasma customization without changing the default Anacrusis desktop.

### Theme/profile framework

- [ ] define a theme/profile recipe convention
- [ ] keep theme changes user-scoped where practical
- [ ] define a restore/default mechanism
- [ ] prefer supported KDE configuration interfaces over brittle direct file editing
- [ ] document asset licensing requirements

### Initial candidates

- [ ] `theme-retro`
  - retro-inspired color scheme
  - left-side Plasma panel
  - coordinated wallpaper and desktop settings
- [ ] MouseTiler integration where appropriate
- [ ] optional productivity-oriented profile
- [ ] restore/default Plasma layout helper if safe and maintainable

Theme recipes may combine panel layout, colors, wallpaper, window-management helpers, and related Plasma settings into a coherent optional profile.

These remain opt-in even if they are actively used and tested by the maintainer. No optional theme becomes the Anacrusis default merely because it is project-maintained.

## Phase 9 — NVIDIA Open Variant

Goal: provide a dedicated modern NVIDIA image without polluting the standard image.

### Target

- x86_64 first

### Deliverables

- [ ] separate image definition
- [ ] Fedora stock kernel
- [ ] NVIDIA open kernel modules
- [ ] NVIDIA user-space stack
- [ ] Secure Boot workflow
- [ ] update/rollback validation
- [ ] documented supported GPU generations

### Future

- [ ] evaluate aarch64 NVIDIA support

## Phase 10 — Apple T2 Variant

Goal: support Intel Macs with Apple T2 hardware through a dedicated image.

### Deliverables

- [ ] separate x86_64 image
- [ ] T2 Linux Fedora kernel integration
- [ ] T2 support packages
- [ ] audio support
- [ ] fan support
- [ ] required kernel arguments
- [ ] `t2-firmware` helper
- [ ] `t2-status` diagnostics
- [ ] clear non-redistributable firmware policy

## Phase 11 — Fedora Next-Release Testing

Goal: make Anacrusis usable during Fedora Beta so users and contributors can test before GA.

### Policy

When Fedora Beta Atomic/Kinoite images become available:

- [ ] create next-release testing build
- [ ] publish explicit `:<release>-testing` tag
- [ ] validate standard x86_64
- [ ] validate standard aarch64
- [ ] build NVIDIA if dependencies are ready
- [ ] build T2 if dependencies are ready
- [ ] accept and triage testing feedback

Fedora GA does not automatically promote the testing image.

## Phase 12 — Stable Release Promotion

A testing release may become stable when:

### Build

- [ ] x86_64 standard builds
- [ ] aarch64 standard builds
- [ ] images are signed
- [ ] intended registry tags are correct

### Upgrade and recovery

- [ ] update from previous Anacrusis build succeeds
- [ ] explicit major-version switch succeeds
- [ ] rollback succeeds
- [ ] staged update behavior works without forced reboot

### Desktop

- [ ] Plasma session works
- [ ] Discover works
- [ ] Flathub works
- [ ] no unintended desktop-layout changes

### Multimedia

- [ ] FFmpeg stack works
- [ ] HEIF works
- [ ] Mesa freeworld packages resolve on both Tier 1 architectures

### Tooling

- [ ] Toolbx works
- [ ] Distrobox works
- [ ] Homebrew works
- [ ] core `ujust` recipes work

### Variants

Variant-specific failures should be documented clearly. A specialized T2 delay should not necessarily block the standard image.

## Phase 13 — Installation and Onboarding

Goal: make Anacrusis approachable without masking its Fedora/bootc foundations.

Research and decide:

- [ ] supported rebase path from Fedora Kinoite
- [ ] bootc-native installation instructions
- [ ] downloadable ISO strategy
- [ ] first-boot experience
- [ ] Secure Boot documentation
- [ ] recovery documentation
- [ ] migration back to Fedora Kinoite

## Phase 14 — Visual Identity

Goal: give Anacrusis a recognizable identity without turning it into a themed Plasma distribution.

Potential scope:

- [ ] logo
- [ ] restrained color system
- [ ] wallpaper
- [ ] project website assets
- [ ] boot/installer artwork where appropriate

Do not change stock Plasma workflow solely for branding.

## Backlog / Research

- [ ] user-data snapshot strategy
- [ ] Btrfs `/home` snapshot helpers
- [ ] SMB/CIFS documentation or helper
- [ ] rechunking / Chunkah
- [ ] ARM64 NVIDIA
- [ ] optional Flatpak application bundles
- [ ] additional optional theme profiles
- [ ] future creative-workstation profile
- [ ] future gaming helper/profile
- [ ] final trademark/domain diligence
