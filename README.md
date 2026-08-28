# Movio - Fast Desktop Switching

Movio is an open-source hardware KVM switch that lets you seamlessly control two computers with a single keyboard and mouse. Simply drag your mouse cursor to the edge of the screen to switch between computers — the keyboard follows automatically, making it feel like you're using one single machine.

Based on the [DeskHop](https://github.com/hrvach/deskhop) project, Movio brings significant improvements including a redesigned web configuration interface with Chinese/English i18n, enhanced firmware stability, optimized mouse switching logic, and a comprehensive build system.

![Movio case and board](img/case_and_board_s.png)

## Features

- **No delay** when switching between computers
- Simply **drag the mouse pointer** between monitors — no buttons needed
- **No software** to install on either computer
- **Full galvanic isolation** (2kV) between outputs
- Works with **Linux, macOS, Windows, and Android**
- Up to **6 extended screens** per computer
- Affordable components (<15€ total)
- 3D printable snap-fit case
- **Chinese/English** bilingual web configuration interface
- Completely **[free and open source](https://certification.oshwa.org/de000149.html)**

[User Manual (中文)](misc/Movio_Product_Introduction.md) | [Comparison with DeskHop](misc/Movio_vs_DeskHop.md)

![Open Source Hardware Logo](img/oshw.svg)

------

## How it works

The device acts as an intermediary between your keyboard/mouse and the computers, establishing and maintaining USB connections with both computers simultaneously. It forwards your mouse and keystrokes to the selected output based on your cursor position or keyboard shortcuts.

## Mouse

The mouse HID report descriptor uses absolute coordinates while internally accumulating relative movements. When the cursor reaches the screen edge in the direction of the other computer, the Y coordinate is preserved and the X axis is flipped — the cursor seamlessly appears at the same height on the other monitor.

![Movio Mouse Demo](img/deskhop-demo.gif)

<p align="center">Dragging the mouse from Mac to Linux automatically switches outputs.</p>

## Keyboard

The keyboard automatically follows the mouse — when you switch outputs by dragging the mouse, keyboard input is forwarded to the same computer. You can also switch independently using `Left Ctrl + Caps Lock`.

Keyboard LED states (e.g. Caps Lock) are remembered per computer and restored on switch. LEDs can also serve as output indicators showing which computer is currently active.

![Movio Typing Demo](img/demo-typing.gif)

------

## What's new in Movio (vs DeskHop)

Movio is a fork of [DeskHop](https://github.com/hrvach/deskhop) with the following improvements:

### Web Configuration UI

- **Chinese/English bilingual support** — full i18n with language toggle (defaults to Chinese)
- **Redesigned visual theme** — new orange color scheme (#ff6600), custom SVG icons, page favicon
- **Interaction feedback** — buttons show "✓ Executed" confirmation, Save button shows "Done" in green
- **Custom range sliders** — cross-browser consistent styling, fixes Chromium Linux rendering bug
- **Bootloader button fix** — fixes the original issue where bootloader mode couldn't be triggered from the web UI

### Firmware Stability

- **Off-by-one fixes** — 4 boundary check corrections preventing potential array out-of-bounds
- **CRC32 type fix** — checksum value corrected from `uint8_t` to `uint32_t` (was silently truncated)
- **NKRO fallback** — keyboards that advertise NKRO but send boot-format reports now work correctly
- **System report length check** — prevents out-of-bounds read on system control reports

### Mouse Behavior

- **Smoother virtual desktop switching** — local switches (virtual desktop) use zero threshold for seamless transitions; cross-computer jumps retain the threshold to prevent accidental switches
- **Composite keyboard fix** — QMK keyboards with mouse interfaces no longer cause cursor jumping
- **macOS drag fix** — dragging windows across virtual desktops no longer leaves mouse buttons "stuck"

### LED Management

- **Dual-state tracking** — separated desired/actual LED states for reliable synchronization
- **LED sync task** — 30Hz periodic check ensures keyboard LEDs match the expected state

### Build System

- **One-click build script** (`build_all.sh`) — automates web page packaging, disk image creation, and firmware compilation
- **Version input** — interactive version prompt with memory, passed to CMake
- **Improved .gitignore** — covers IDE files, OS artifacts, build objects, Python cache

### Other

- **PIO USB stability** — timing and initialization fixes for more reliable USB communication
- **USB descriptor fix** — corrected CDC interface numbering in debug mode
- **Packet validation** — firmware upgrade messages now pass validation whitelist
- **Code quality** — removed unused declarations, fixed macro precedence, improved constants

See [Movio_vs_DeskHop.md](misc/Movio_vs_DeskHop.md) for the full detailed comparison.

------

## Getting Started

### Installation

1. Connect your **mouse** to the USB port with the mouse icon
2. Connect your **keyboard** to the USB port with the keyboard icon
3. Connect both computers via **Type-C cables**
4. The LED will flash when peripherals are detected
5. Power on both computers — mouse cursor can now cross between screens

> **Note**: Both computers must be connected and providing USB power. Most modern desktops and laptops provide USB power even when shut down.

### Initial Firmware Flash (New Builds)

1. Download `movio.uf2` from [Releases](https://github.com/likeaturtle/Movio/releases)
2. Connect Type-C to the **A port** computer
3. Copy `movio.uf2` to the "MOVIO" USB drive that appears
4. Repeat for the **B port**

------

## Keyboard Shortcuts

### Configuration

| Action | Shortcut |
|--------|----------|
| Enter config mode | `Left Ctrl` + `Right Shift` + `C` + `O` |
| Reset flash config | `Right Shift` + `F12` + `D` |
| Save screen height offset | `Right Shift` + `F12` + `Y` |

### Usage

| Action | Shortcut | Description |
|--------|----------|-------------|
| Switch output | `Left Ctrl` + `Caps Lock` | Switch keyboard/mouse to other computer |
| Gaming mode | `Left Ctrl` + `Right Shift` + `G` | Lock to screen, standard relative mouse |
| Enable screensaver | `Left Ctrl` + `Right Shift` + `S` | Prevent computer sleep |
| Disable screensaver | `Left Ctrl` + `Right Shift` + `X` | Turn off screensaver |
| Slow mouse mode | `Right Ctrl` + `Right Alt` | Toggle slower mouse for precision |
| Lock to current screen | `Right Ctrl` + `K` | Prevent accidental switching |
| Lock both screens | `Right Ctrl` + `L` | Lock both computers (set OS in config first) |

------

## Web Configuration

Movio provides a local WebHID-based configuration page for adjusting device settings.

### How to enter config mode

1. Press `Left Ctrl` + `Right Shift` + `C` + `O` — the device reboots and mounts a USB drive named **"MOVIO"**
2. Open `config.htm` from the drive using **Chrome or Chromium** (Firefox does not support WebHID)
3. Click **Connect** and allow the device to pair
4. Adjust settings — changes take effect immediately
5. Click **Save** to persist to flash, then **Exit** to leave config mode

![Web Config](img/config-page-big.png)

### Configuration Options

**Per Output (A/B):**

| Option | Description |
|--------|-------------|
| Screen Count | Number of monitors on this computer (1-3) |
| Speed X / Speed Y | Mouse movement speed on each axis (1-100) |
| Border Top / Bottom | Screen height offset (0-32767) for alignment |
| Operating System | Linux / macOS / Windows / Android / Other |
| Screen Position | Left or Right in the layout |
| Cursor Park Position | Where cursor goes on switch: Top / Bottom / Previous |

**Screensaver:**

| Option | Description |
|--------|-------------|
| Mode | Disabled / Pong (bouncing) / Jitter (1px movement) |
| Only If Inactive | Only activate when user is idle |
| Idle Time | Inactivity period before activation (microseconds) |
| Max Time | Maximum screensaver runtime (microseconds) |

**Common:**

| Option | Description |
|--------|-------------|
| Force Mouse Boot Mode | Simple mouse init for compatibility |
| Force KBD Boot Protocol | Boot protocol keyboard init for compatibility |
| KBD LED as Indicator | Use Caps Lock LED as output indicator |
| Enforce Ports | Force specific USB port usage |
| Jump Threshold | Extra movement distance before cross-computer switch (0-3000) |

### Linux udev rule

If Chromium on Linux doesn't see the device, create:

```
/etc/udev/rules.d/99-movio.rules
```

```
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1209", ATTRS{idProduct}=="c000", GROUP="plugdev", MODE="0660"
```

Make sure your user is in the `plugdev` group.

------

## Upgrading Firmware

**Option 1 — Config Mode (Recommended)**

Press `Left Ctrl` + `Right Shift` + `C` + `O` to enter config mode. Copy the `movio.uf2` file to the "MOVIO" USB drive. Both boards will be upgraded automatically (LED blinks during the process).

**Option 2 — ROM Bootloader**

Hold the on-board button while connecting each Pico via USB. Copy the `.uf2` file to the "RPI-RP2" drive that appears.

**Option 3 — CDC Flash (Debug builds only)**

If built with `DH_DEBUG_CDC_FLASH=ON`:
```shell
echo -n 'flash' > /dev/tty.usbmodem11104
```

------

## Advanced Features

### Screen Height Calibration

When screens differ in size or resolution, calibrate the switch height:

1. Park the mouse on the **larger** screen at the height of the smaller screen
2. Press `Right Shift` + `F12` + `Y`
3. LED and Caps Lock flash to confirm
4. Repeat for the bottom border if needed
5. Calibration is saved to flash permanently

![Border height difference](img/border_top_s.png)

### Multiple Screens

For multi-monitor setups, set the **Operating System** and **Screen Count** for each output in the web config. Main screens should be in the middle, secondary screens on the edges.

### Gaming Mode

Press `Left Ctrl` + `Right Shift` + `G` to toggle gaming mode — locks to current screen and switches mouse to standard relative mode. Useful for games, virtual machines, and unsupported operating systems.

### Mouse Slowdown

Press `Right Ctrl` + `Right Alt` to toggle slow-mouse mode for precision work (e.g., dragging a video slider to an exact position).

------

## Hardware

The circuit is based on two Raspberry Pi Pico boards (4.10€ each), connected via UART and separated by a TI ISO7721DR digital isolator (~1.5€). USB host/device support is implemented using [Pico-PIO-USB](https://github.com/sekigon-gonnoc/Pico-PIO-USB).

### Bill of Materials (PCB v1.1)

| Component | Part | Qty | Price / € |
|-----------|------|-----|-----------|
| U1, U2 | Raspberry Pi Pico | 2 | 8.20 |
| J1, J4 | USB-A PCB connector | 2 | 0.40 |
| U4 | TI ISO7721DR | 1 | 1.40 |
| C1, C2 | 0805 SMD 100nF | 2 | 0.18 |
| R1-R4 | 0805 SMD 27Ω | 4 | 0.12 |
| U3, U5 | TPD4E1U06DBVR (ESD) | 2 | 0.62 |
| C3, C4 | 4.7µF SMD 0805 | 2 | 0.14 |
| J2, J3 | Headers 2.54 1x3 | 2 | 0.16 |
| | | **Total** | **11.22** |

Additional: [PCB Gerber files](pcb/) (1.6mm thickness) | [3D printable case](case/) (~33g filament)

### PCB

![PCB Image](img/plocica2.png)

Single-side routing, 90Ω differential impedance target, 1.6mm thickness. v1.1 adds ESD protection, VBUS capacitors, and USB 27Ω resistors.

### Case

![Movio with 3D Printed Case](img/deskhop-case.gif)

Snap-fit design, no screws. Uses ~33g of filament, takes a couple of hours to print.

------

## How to Build

### Prerequisites (Debian/Ubuntu)

```shell
apt update
apt install build-essential cmake gcc-arm-none-eabi libnewlib-arm-none-eabi python3
```

### Build

```shell
cmake -S . -B build
cmake --build build
```

### One-click build (recommended)

The `build_all.sh` script automates the entire process (web page → disk image → firmware):

```shell
./build_all.sh
```

It will prompt for a version number (e.g., `0.79`), then generate `config.htm`, pack the disk image, and compile the firmware with the specified version.

### Docker (reproducible builds)

```shell
docker-compose -f misc/docker.yml run --rm build_container
```

### Rebuild web UI

```shell
cd webconfig && python3 render.py  # requires jinja2
```

------

## Security and Safety

Movio is designed with security as a fundamental principle:

- **No data transfer** between computers — no copy-paste, file sharing, or information leakage
- **No input history** retained on the device
- **No device-initiated keystrokes** — only user input is forwarded
- **Physical isolation** — 2kV galvanic isolation between outputs via digital isolator
- **ESD/surge protection** — TVS protection on USB ports (PCB v1.1)
- **No wireless** — no Bluetooth, WiFi, or network connectivity
- **No trusted computers** — connected computers are never treated as trusted
- **Auto-exit** — config mode automatically disables after inactivity timeout
- **Fixed-length packets** — cross-device communication uses fixed-size packets with a short whitelist of config options
- **No exposed endpoints** — keyboard/mouse custom endpoints are not exposed to computers
- **Local-only config** — web config page runs entirely locally, no external resources loaded
- **Full source audit** — complete open source with no binary blobs

------

## FAQ

**Q: Can I use just two Picos without a PCB or isolator?**
A: Yes, though an isolator is recommended for proper electrical isolation.

**Q: Will different monitor resolutions cause problems?**
A: No. Mouse movement uses abstract coordinate space; each computer maps it to its physical screen.

**Q: Does the keyboard follow the mouse when switching?**
A: Yes. Switching via mouse automatically switches the keyboard, and vice versa.

**Q: Does it work with Logitech Unifying receivers?**
A: Yes. Combo receivers are well supported in recent firmware.

**Q: Does it work with wireless keyboards/mice with separate receivers?**
A: Yes. Wireless devices with independent receivers work fine.

**Q: Can I use Firefox for the config page?**
A: No. The config page uses WebHID, which Firefox does not support. Use Chrome or Chromium.

**Q: Why is the config page compressed/weird-looking?**
A: This is intentional — the page self-decompresses due to limited device storage. The full source code is in this repository.

**Q: Why not an online config page?**
A: Loading external JavaScript that interacts with input devices is a security risk. The config page is entirely local.

**Q: Do both computers need to be powered on?**
A: Yes. Each board is powered by its connected computer. Most modern computers provide USB power even when shut down. If using only one computer, a USB hub can connect both keyboard and mouse to a single port.

**Q: Build or compilation issues?**
A: Check the [Troubleshooting Wiki](https://github.com/hrvach/deskhop/wiki/Troubleshooting).

------

## Software Alternatives

1. [Barrier](https://github.com/debauchee/barrier) — Free, Open Source
1. [Input Leap](https://github.com/input-leap/input-leap) — Free, Open Source
1. [Synergy](https://symless.com/synergy) — Commercial
1. [Mouse Without Borders](https://www.microsoft.com/en-us/garage/wall-of-fame/mouse-without-borders/) — Free, Windows only
1. [Universal Control](https://support.apple.com/en-my/HT212757) — Free, Apple only

------

## Known Limitations

- Windows 10 KB5003637 broke HID absolute coordinates — limited to 1 screen on Windows
- Advanced keyboard features (knobs, extra buttons, sliders) may not work
- Both computers must provide USB power for the device to operate
- macOS multi-screen has an experimental workaround in recent firmware

------

## License

Movio is free and open source hardware. See [OSHWA certification](https://certification.oshwa.org/de000149.html).

## Disclaimer

Building and using this project is at your own risk. Please take necessary safety precautions. The author is not liable for any injuries, damages, or other consequences.

------

**Upstream**: [hrvach/deskhop](https://github.com/hrvach/deskhop) | **Fork**: [likeaturtle/Movio](https://github.com/likeaturtle/Movio)
