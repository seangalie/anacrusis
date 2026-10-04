# Working on anacrusis

Instructions for AI coding agents. `CLAUDE.md` imports this file, so shared
instructions belong here, not there.

## Project overview

anacrusis is an independent atomic KDE desktop: a bootable OCI image built on
Fedora Kinoite (`quay.io/fedora-ostree-desktops/kinoite`) with
[BlueBuild](https://blue-build.org). Installation, boot, update, and rollback
validation are still pending; see the README and `docs/ROADMAP.md`. There is no
application code: the repository is a BlueBuild recipe plus the files, scripts,
and modules it pulls into the image. Images are published to
`ghcr.io/seangalie/anacrusis` for `linux/amd64` and `linux/arm64`, and signed
with cosign.

## Commands

CI builds the image with `blue-build/github-action` (`.github/workflows/build.yml`).
Locally, with the [BlueBuild CLI](https://blue-build.org/how-to/local/) and
Docker or Podman:

```sh
# Validate the recipe against the BlueBuild schemas:
bluebuild validate recipes/recipe.yml
# Render the Containerfile without building (output is git-ignored):
bluebuild generate -o Containerfile recipes/recipe.yml
# Build the image locally:
bluebuild build recipes/recipe.yml
# Lint build scripts (CI runs this over every tracked *.sh / *.bash):
git ls-files -z -- '*.sh' '*.bash' | xargs -0 -r shellcheck
```

A full image build is slow, so validate the recipe and shellcheck scripts
before relying on CI to catch mistakes.

## Repository layout

- `recipes/recipe.yml` -- the image definition: base image, Fedora version,
  platforms, and the ordered list of modules. Its first line points
  yaml-language-server at the recipe schema.
- `recipes/modules/` -- shared module configuration imported with `from-file`.
  Files here are inactive until a recipe references them.
- `files/system/` -- files to copy into the image, laid out as they appear
  from `/` (`files/system/etc/...` becomes `/etc/...`). This only happens once
  the recipe includes a `files` module with `source: system` and
  `destination: /`.
- `files/scripts/` -- shell scripts run during the build by a `script` module
  in the recipe. Each must start with `set -euo pipefail` (or the equivalent
  `set -oue pipefail`) so a failing command fails the build.
- `modules/` -- custom BlueBuild modules local to this repository.
- `cosign.pub` -- the public half of the image signing key. Users verify
  images with it; do not change it unless the key is being rotated.
- `.github/workflows/` -- the image build, plus the lint workflows.

## Conventions

- **Fedora version:** `image-version` in the recipe is pinned to a Fedora
  release (currently 44) and mirrored in `alt-tags`. Users stay on it until a
  deliberate major upgrade, so never bump it as a side effect of other work.
- **Image contents:** anything under `files/system/` ships to every user.
  Keep stray files (`.DS_Store`, editor backups, notes) out of it.
- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org):
  `feat: add flatpak defaults`, `fix(scripts): handle missing repo file`.
- **Formatting** follows `.editorconfig`: UTF-8, LF line endings, and a final
  newline; 2-space indents for YAML, JSON, TOML, and shell. The Lint workflow
  enforces it with editorconfig-checker and runs shellcheck over every `*.sh`
  and `*.bash` file.
- **GitHub Actions:** pin every third-party action to a full commit SHA with its
  version in a trailing comment (`uses: owner/action@<sha> # vX.Y.Z`), and grant
  each workflow only the `permissions:` it needs. actionlint and zizmor check
  every change under `.github/workflows/`. Never let a build of `main` be
  cancelled mid-run: it could publish an image without signing it.

## Boundaries

- Never commit secrets. In particular `cosign.key` / `cosign.private` must never
  be committed; the private key lives only in the `SIGNING_SECRET` repository
  secret.
- Leave the text of `LICENSE` unmodified.
- Do not make a change pass by weakening the checks: no blanket shellcheck
  disables, removed lint steps, or skipped signing. Fix the cause, or stop and
  report what is failing.
- Ask before changing the base image, the Fedora version, the target platforms,
  the image name, the signing setup, or anything else that changes what existing
  users get on their next update.
