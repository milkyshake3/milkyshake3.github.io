# Noel Mendoza // Portfolio & Security Lab

> **1st-Year BCA Student // Software Engineering with a Security Focus**  
> *"grow wings and fly • zero tracking • self-contained"*

Live site: [https://noelbuilds.dev](https://noelbuilds.dev)

[ADD SCREENSHOT]

---

## Overview

A single-file portfolio built with vanilla web technologies, zero external frameworks, zero third-party tracking, and no runtime media assets (animation frames are embedded directly as data).

The interface combines aerospace telemetry, architectural grid blueprints, and retro CRT styling with a 24-frame dot-matrix eagle flapping loop and an offline Web Audio ambient synthesizer.

---

## Key Features

- **Living Canvas Background Engine**:
  - Cobalt sky gradient with drifting pixelated clouds and coordinate grid lines.
  - 24-frame dot-matrix eagle flapping at 12 FPS on an architectural CAD pitch grid. Animation frame data derived from a video by Milk & Peppers, used with permission.
  - Motion comfort modes: `CALM` (default) and `STATIC` (reduced-motion accessibility).

- **Interactive CLI Terminal Drawer (`[ >_ CLI ]`)**:
  - Slide-down CRT terminal overlay with scanlines and command history.
  - Keybindings: Press **``` ` ```** (backtick) / **`~`** or **`ESC`** to toggle.
  - Recon commands: `whoami`, `skills`, `projects`, `contact`, `pgp`, `sound [on|off]`, `motion [calm|static]`, `clear`, `exit`.

- **Opt-in Native Web Audio Synthesizer**:
  - Offline synthesis using browser `AudioContext` and oscillators — zero audio files, zero network bandwidth.
  - Celestial chord progression (**F#m $\rightarrow$ A $\rightarrow$ D $\rightarrow$ E**) with warm low-pass filters, subtle detuning, a sub drone, and filtered noise air.
  - Off by default; enabled via top navigation `[ SOUND: ON / OFF ]` or through the CLI.

- **Tactile HUD Toast & One-Click Contact**:
  - One-click `[ copy email ]` button with clipboard write and instant luminous HUD toast notification.
  - Prefilled `mailto:` action button for outreach.

- **OPSEC PGP Key & Cryptographic Fingerprint**:
  - Collapsible drawer revealing verified PGP fingerprint (`ede9 a793 9d24 fe6b cd66 f31d 89b2 16a3 16a5 613e`) and armored public key block.

- **Cyber Scroll Progress Bar & Favicon**:
  - Cyan-to-green gradient bar fixed under top navigation tracking reading depth.
  - Inline SVG dot-matrix wing favicon and OpenGraph/Twitter card metadata.

---

## How It Works

### Render Loop
The background animation runs on an HTML5 Canvas 2D render loop driven by `requestAnimationFrame`. Each frame calculates elapsed time deltas to update procedural cloud positions and advance the 12 FPS eagle flapping loop (`Math.floor(now / frameDuration) % BIRD_FRAMES.length`). Coordinates are anchored to a central flight reticle that tracks dynamic bounding keyframes, rendering dot-matrix particles, accent sensor bloom, and the vertical serif motto alongside CAD-style measurement lines.

### Motion Modes
The engine provides two distinct motion modes:
- `CALM` (default): Grounded camera coordinates with slow, tranquil breathing and drifting clouds to prevent vestibular discomfort.
- `STATIC`: Freezes the canvas into a fixed snapshot (frame 0) with stationary clouds and reticle.

Users can toggle modes via the `[ MOTION: CALM / STATIC ]` button in the navigation bar or using the terminal command `motion [calm|static]`. The selected preference is saved to `localStorage` with an in-memory fallback if storage access is restricted.

### Web Audio Graph
Ambient sound is generated in real time without external audio files. When enabled, a native `AudioContext` creates dual oscillator voices (sine and triangle waves) routed through low-pass biquad filters, an envelope gain node, a sub-bass oscillator, and a pink noise generator simulating high-altitude atmosphere. Voices cycle across an ambient chord progression (**F#m $\rightarrow$ A $\rightarrow$ D $\rightarrow$ E**). The audio engine is silent by default and complies with browser autoplay policies.

### Reduced-Motion Handling
The site checks system accessibility preferences using `window.matchMedia('(prefers-reduced-motion: reduce)')`. If the operating system or browser requests reduced motion and no manual preference has been stored, the engine automatically defaults to `STATIC` mode, halting animation loops and disabling rapid visual transitions.

---

## Limitations

- **Single-File Payload**: Embedding all styles, script logic, and 24 frames of coordinate datasets inside `index.html` increases the initial HTML file size (~295 KB).
- **Audio Autoplay Restrictions**: Modern browsers prevent audio playback prior to explicit user gesture interaction; sound must be activated manually.
- **Canvas Hardware Acceleration**: Render performance for multi-pass coordinate grids and procedural film grain depends on client-side 2D canvas acceleration.

---

## Tech Stack & Capabilities

| Domain | Technologies & Skills |
| :--- | :--- |
| **Used / Foundations** | **Python** (Sentinel-Trader), **C** coursework (pointers, memory, low-level I/O), **C++**, **Java**, **Linux CLI**, **Git**, technical writing |
| **Research / Practice** | **OPSEC** & privacy research, **OSINT** surface mapping, **Wireshark** & packet analysis, **MITRE ATT&CK** mapping |
| **Learning Next** | **Rust**, security labs, and **OWASP Top 10** fundamentals |
| **Frontend Engineering** | Native HTML5 Canvas 2D, Web Audio API, Vanilla JavaScript (ES6+), Modern CSS3 Grid/Flexbox |

---

## Local Setup & Preview

Because this portfolio is 100% self-contained in a single file, you can preview it immediately:

### Option 1: Direct File Open
Open `index.html` directly in any modern web browser (Chrome, Edge, Firefox, Safari).

### Option 2: Local PowerShell Server
Run the included preview server script:
```powershell
powershell -ExecutionPolicy Bypass -File server.ps1
```
Then navigate to `http://localhost:8080/` in your browser.

---

## Repository Structure

```text
├── index.html          # Entire self-contained portfolio & living canvas engine
├── server.ps1          # Lightweight local HTTP preview server
├── README.md           # Project documentation & tech breakdown
├── .gitignore          # Git exclusions for OS & temporary files
└── dev/                # Development tools & helper scripts
```

---

## Credits

- [Animation and motto based on a video by Milk & Peppers](https://www.milkandpeppers.co.uk/), used with permission.

---

## Contact

- **Email**: [contact@noelbuilds.dev](mailto:contact@noelbuilds.dev)
- **GitHub**: [@milkyshake3](https://github.com/milkyshake3)
- **LinkedIn**: [Noel Mendoza](https://www.linkedin.com/in/noel-mendoza-411618434/)
- **PGP Fingerprint**: `ede9 a793 9d24 fe6b cd66 f31d 89b2 16a3 16a5 613e`
