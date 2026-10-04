# Anacrusis roadmap

Anacrusis is an independent atomic KDE desktop based on Fedora Kinoite. Preserve
Fedora's desktop workflow and expose upstream functionality. Default what improves
the platform broadly; offer personal workflow changes through optional recipes.

## Baseline: build, publish, boot

The Fedora 44 recipe builds directly from
`quay.io/fedora-ostree-desktops/kinoite:44`, targets amd64 and arm64, and includes
only signing. CI has built and published both architectures and verified the
image signature. The public image index has been inspected independently.

Milestone zero is complete only after these remaining checks:

- Boot each architecture in a disposable VM and reach a working Plasma session.
- Test acquisition of signing trust and a signed installation or rebase.
- Verify an image update is staged, boots successfully, and retains user data.
- Exercise rollback to the previous deployment after a failed update.
- Record image digests, VM setup, commands, and results for reproducibility.

Passing a container build establishes the pipeline; it does not establish that
the resulting operating system boots or that recovery works.

## Identity

The proposed shared configuration is `recipes/modules/identity.yml`. It is not
yet imported into the active recipe. It uses BlueBuild's `os-release` module to
set the displayed name to Anacrusis, identify the release as Anacrusis 44, and
point project links at this repository.

Preserve Fedora's `ID`, `ID_LIKE`, `VERSION_ID`, and `VARIANT_ID` for upstream
tool compatibility. Keep Plasma's layout, theme, shortcuts, and applications
unchanged in this milestone. Cosmetic assets can follow separately.

Once approved, import the configuration before signing:

```yaml
modules:
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
