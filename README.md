# Anacrusis

[![Image build](https://github.com/seangalie/anacrusis/actions/workflows/build.yml/badge.svg)](https://github.com/seangalie/anacrusis/actions/workflows/build.yml)
[![Lint](https://github.com/seangalie/anacrusis/actions/workflows/lint.yml/badge.svg)](https://github.com/seangalie/anacrusis/actions/workflows/lint.yml)

An independent atomic KDE desktop based on Fedora Kinoite, built with
[BlueBuild](https://blue-build.org).

Anacrusis keeps Fedora's Plasma experience familiar and adds platform capabilities
in small, verifiable stages. Personal desktop preferences belong in optional
recipes rather than the default image.

## Current status

Anacrusis is in early development. The initial Fedora Kinoite 44 image has built
and published successfully for both `linux/amd64` and `linux/arm64`, with Cosign
signature verification passing in CI. Boot, installation, rollback, and update
testing are still outstanding; this is not yet a release recommended for everyday
use.

The active recipe currently contains only the Fedora Kinoite base and BlueBuild's
signing module. RPM Fusion, additional Flathub configuration, Distrobox, Homebrew,
`ujust`, branding, and Anacrusis update policy are planned work. See the
[roadmap and validation gates](docs/ROADMAP.md).

## Images and release policy

| Image | Architectures | Purpose |
| --- | --- | --- |
| `ghcr.io/seangalie/anacrusis:44` | amd64, arm64 | Fedora 44 development baseline |

Track an explicit Fedora release tag. Updates to `44` stay on Fedora 44; a major
upgrade will require choosing a new release tag. Do not track `latest`: any tag
left over from the Workshop demo is not the Anacrusis release channel.

The base image is `quay.io/fedora-ostree-desktops/kinoite:44`. This direct Fedora
desktop OCI dependency is an architectural choice we will revisit if Fedora
establishes a different supported desktop source.

## Verification and development testing

From a checkout of this repository, with
[Cosign installed](https://docs.sigstore.dev/cosign/system_config/installation/),
verify the published image against the project's public key:

```sh
cosign verify --key cosign.pub ghcr.io/seangalie/anacrusis:44
```

Inspect the image index without downloading the desktop image:

```sh
docker buildx imagetools inspect ghcr.io/seangalie/anacrusis:44
```

The index should contain both `linux/amd64` and `linux/arm64`. BuildKit also adds
attestation entries reported as `unknown/unknown`; those are not bootable images.

Installation instructions will follow disposable VM testing of the initial
rebase, signing trust, boot, update, and rollback paths. The project intends to
use bootc for image management; the baseline build alone does not validate that
workflow. No Anacrusis installation ISO is published yet.

## Contributing

Keep changes small enough that each image build tests one new layer. With the
[BlueBuild CLI](https://blue-build.org/how-to/local/) and a working Linux container
builder, run these from the repository root:

```sh
bluebuild validate recipes/recipe.yml
bluebuild generate -o Containerfile recipes/recipe.yml
bluebuild build recipes/recipe.yml
```

CI also runs ShellCheck, EditorConfig checks, actionlint, and zizmor. Third-party
actions are pinned to commit SHAs and updated through Dependabot.

Shared module configuration belongs under `recipes/modules/`, imported with
BlueBuild's [`from-file`](https://blue-build.org/how-to/multiple-files/) syntax.
The top-level `modules/` directory is reserved for custom module implementations.
System files go under `files/system/`; build scripts go under `files/scripts/`.
Neither directory changes the image until a recipe references it.

See [AGENTS.md](AGENTS.md) for repository conventions and
[GitHub Issues](https://github.com/seangalie/anacrusis/issues) to report problems.
