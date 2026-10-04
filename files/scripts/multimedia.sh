#!/usr/bin/env bash
set -euo pipefail

# RPM Fusion supplies codecs Fedora cannot ship. Reject collateral package
# removals rather than publishing a desktop damaged by --allowerasing.
export LC_ALL=C
arch=$(rpm --eval '%{_arch}')
case "$arch" in
  x86_64 | aarch64) ;;
  *)
    echo "Unsupported multimedia architecture: $arch" >&2
    exit 1
    ;;
esac

work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT
rpm -qa --qf '%{NAME}.%{ARCH}\n' | sort -u > "$work_dir/before"

dnf_args=(-y --setopt=install_weak_deps=False)
if rpm -q --quiet ffmpeg-free; then
  dnf5 "${dnf_args[@]}" swap --allowerasing ffmpeg-free "ffmpeg.$arch"
else
  dnf5 "${dnf_args[@]}" install --allowerasing "ffmpeg.$arch"
fi

dnf5 "${dnf_args[@]}" install \
  ffmpeg-libs \
  gstreamer1-plugin-libav \
  gstreamer1-plugins-bad-freeworld \
  gstreamer1-plugins-ugly \
  libheif-freeworld \
  heif-pixbuf-loader

# Match Fedora's installed Mesa version exactly. RPM Fusion lag must fail the
# build, not silently downgrade the graphics stack or skip hardware codecs.
mesa_version=$(rpm -q --qf '%{VERSION}' "mesa-filesystem.$arch")
for driver in mesa-va-drivers mesa-vulkan-drivers; do
  replacement="$driver-freeworld-$mesa_version.$arch"
  if rpm -q --quiet "$driver.$arch"; then
    dnf5 "${dnf_args[@]}" swap "$driver.$arch" "$replacement"
  else
    dnf5 "${dnf_args[@]}" install "$replacement"
  fi
done

# Intel's media driver is available only on x86_64; do not weaken ARM checks
# with --skip-unavailable to accommodate an Intel-specific package.
if [[ "$arch" == x86_64 ]]; then
  dnf5 "${dnf_args[@]}" install intel-media-driver
fi

rpm -qa --qf '%{NAME}.%{ARCH}\n' | sort -u > "$work_dir/after"
comm -23 "$work_dir/before" "$work_dir/after" > "$work_dir/removed"
while IFS= read -r package; do
  case "${package%.*}" in
    ffmpeg-free | libavcodec-free | libavdevice-free | libavfilter-free | \
      libavformat-free | libavutil-free | libpostproc-free | \
      libswresample-free | libswscale-free | mesa-va-drivers | mesa-vulkan-drivers)
      ;;
    *)
      echo "Multimedia transaction unexpectedly removed $package" >&2
      exit 1
      ;;
  esac
done < "$work_dir/removed"

# Verify the final image contents, including installations that might otherwise
# appear successful after an upstream package rename or dependency change.
rpm -q ffmpeg ffmpeg-libs gstreamer1-plugin-libav \
  gstreamer1-plugins-bad-freeworld gstreamer1-plugins-ugly \
  libheif-freeworld heif-pixbuf-loader \
  "mesa-va-drivers-freeworld.$arch" "mesa-vulkan-drivers-freeworld.$arch"
if [[ "$arch" == x86_64 ]]; then
  rpm -q intel-media-driver
fi
