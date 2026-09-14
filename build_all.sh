#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
WEB_DIR="$ROOT/webconfig"
DISK_DIR="$ROOT/disk"
BUILD_DIR="$ROOT/build"
CONFIG_HTM="$WEB_DIR/config.htm"
DISK_IMG="$DISK_DIR/disk.img"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[+]${NC} $*"; }
warn() { echo -e "${YELLOW}[!]${NC} $*"; }
die()  { echo -e "${RED}[x]${NC} $*"; exit 1; }

# ── Version input ────────────────────────────────────────────────────────────
VERSION_FILE="$ROOT/VERSION"
[ -f "$VERSION_FILE" ] || die "VERSION file not found at $VERSION_FILE"

DEFAULT_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')
[ -z "$DEFAULT_VERSION" ] && die "VERSION file is empty"

read -rp "$(echo -e "${YELLOW}[?]${NC} Version [${DEFAULT_VERSION}]: ")" VERSION
VERSION="${VERSION:-$DEFAULT_VERSION}"

# Write back to VERSION file if changed
if [ "$VERSION" != "$DEFAULT_VERSION" ]; then
    echo "$VERSION" > "$VERSION_FILE"
    log "Updated VERSION file to $VERSION"
fi
log "Version: $VERSION"

# Parse version: "0.79" -> MAJOR=0, MINOR=79
VER_MAJOR="${VERSION%%.*}"
VER_MINOR="${VERSION#*.}"
[[ "$VER_MAJOR" =~ ^[0-9]+$ ]] && [[ "$VER_MINOR" =~ ^[0-9]+$ ]] \
    || die "Invalid version format '$VERSION' (expected: MAJOR.MINOR, e.g. 0.79)"

# ── Step 1: Generate config.htm ──────────────────────────────────────────────
log "Step 1/3: Generating config.htm ..."
cd "$WEB_DIR"
python3 -B render.py || die "render.py failed"

UNPACKED_SIZE=$(wc -c < "$CONFIG_HTM")
log "  config.htm generated ($UNPACKED_SIZE bytes)"

# ── Step 2: Pack into disk image ─────────────────────────────────────────────
log "Step 2/3: Packing into disk image ..."
cd "$DISK_DIR"
sudo ./create.sh || die "create.sh failed"
sha256sum "$CONFIG_HTM" | awk '{print $1}' > "$DISK_DIR/.config_htm_hash"
log "  disk.img updated"

# ── Step 3: Build firmware ───────────────────────────────────────────────────
log "Step 3/3: Building firmware ..."
cd "$ROOT"
cmake -S . -B "$BUILD_DIR" -DVERSION_MAJOR="$VER_MAJOR" -DVERSION_MINOR="$VER_MINOR" || die "cmake configure failed"

cmake --build "$BUILD_DIR" || die "cmake build failed"

# ── Summary ──────────────────────────────────────────────────────────────────
UF2=$(ls -1t "$BUILD_DIR"/*.uf2 2>/dev/null | head -1)
if [ -n "$UF2" ]; then
    UF2_SIZE=$(wc -c < "$UF2")
    echo ""
    log "========== Build Complete =========="
    log "  version    : $VERSION"
    log "  config.htm : $UNPACKED_SIZE bytes"
    log "  disk.img   : $(wc -c < "$DISK_IMG") bytes"
    log "  firmware   : $UF2_SIZE bytes → $(basename "$UF2")"
fi
