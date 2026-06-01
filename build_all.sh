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

# ── Step 1: Generate config.htm ──────────────────────────────────────────────
log "Step 1/3: Generating config.htm ..."
cd "$WEB_DIR"
python3 -B render.py || die "render.py failed"

UNPACKED_SIZE=$(wc -c < "$CONFIG_HTM")
log "  config.htm generated ($UNPACKED_SIZE bytes)"

# ── Step 2: Pack into disk image ─────────────────────────────────────────────
log "Step 2/3: Packing into disk image ..."

NEED_PACK=1
if [ -f "$DISK_IMG" ] && [ -f "$DISK_DIR/.config_htm_hash" ]; then
    OLD_HASH=$(cat "$DISK_DIR/.config_htm_hash")
    NEW_HASH=$(sha256sum "$CONFIG_HTM" | awk '{print $1}')
    if [ "$OLD_HASH" = "$NEW_HASH" ]; then
        warn "  config.htm unchanged, skipping disk image rebuild"
        NEED_PACK=0
    fi
fi

if [ "$NEED_PACK" -eq 1 ]; then
    cd "$DISK_DIR"
    sudo ./create.sh || die "create.sh failed"
    sha256sum "$CONFIG_HTM" | awk '{print $1}' > "$DISK_DIR/.config_htm_hash"
    log "  disk.img updated"
fi

# ── Step 3: Build firmware ───────────────────────────────────────────────────
log "Step 3/3: Building firmware ..."
cd "$ROOT"

NEED_RECONFIGURE=0
if [ ! -f "$BUILD_DIR/CMakeCache.txt" ]; then
    NEED_RECONFIGURE=1
elif [ "$ROOT/CMakeLists.txt" -nt "$BUILD_DIR/CMakeCache.txt" ]; then
    warn "  CMakeLists.txt changed, reconfiguring ..."
    NEED_RECONFIGURE=1
fi

if [ "$NEED_RECONFIGURE" -eq 1 ]; then
    cmake -S . -B "$BUILD_DIR" || die "cmake configure failed"
fi

cmake --build "$BUILD_DIR" || die "cmake build failed"

# ── Summary ──────────────────────────────────────────────────────────────────
UF2=$(ls -1t "$BUILD_DIR"/*.uf2 2>/dev/null | head -1)
if [ -n "$UF2" ]; then
    UF2_SIZE=$(wc -c < "$UF2")
    echo ""
    log "========== Build Complete =========="
    log "  config.htm : $UNPACKED_SIZE bytes"
    log "  disk.img   : $(wc -c < "$DISK_IMG") bytes"
    log "  firmware   : $UF2_SIZE bytes → $(basename "$UF2")"
fi
