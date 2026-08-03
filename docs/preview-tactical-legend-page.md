---
title: Preview — Tactical Legends
description: How to prepare and publish preview (internal/closed) builds for Tactical Legends
---

![Preview hero — Image 2 (Unit art soldier)](../store-assets/ss2.md)

# Preview Builds & Test Tracks

This page explains how to prepare preview builds for testers.

## Hero image
Alt text: "Armored unit with modern gear holding a rifle — unit art used in preview builds."

## Annotated screenshots for preview & QA

### Squad Bay (annotated)
![Annotated — Squad Bay](../store-assets/annotated/annotated-ss5.svg)

**Transcript (OCR):**

TACTICAL LEGENDS
RISE OF OISTARIAN

Left navigation:
- COMMAND
- SQUAD (highlighted)
- CODEX

Main header:
SQUAD BAY

Card (example):
RIFLEMAN
Trooper-9BF9
Frontline Trooper - 0 kills - 0 ops
HP 10 | AP 2 | MOV 4 | RNG 4
DMG 3-5 • Suppressing Fire
Weapon: TL-Standard Rifle

---

### Cinematic quote (annotated)
![Annotated — Cinematic quote](../store-assets/annotated/annotated-ss6.svg)

**Transcript (OCR):**

"LEGENDS ARE
WRITTEN IN THE SAND —
AND BURIED IN IT.

- SELA REYN - HALCYON-03 - FINAL TRANSMISSION"

Chapter selector: CH-03 // THE VAULT OF EDEN

---

### Chapter title — Storm Descent (annotated)
![Annotated — Storm Descent](../store-assets/annotated/annotated-ss7.svg)

**Transcript (OCR):**

STORM
DESCENT

— THE SKY BLEEDS
SAND —

Chapter selector: CH-02 // STORM DESCENT

---

## New image captions (Images 8–11)

Image 8 — Futuristic Rooftop Operative

Short alt text: "Futuristic soldier with glowing visor fires a rifle over a neon city with VTOL craft overhead."

Caption: "A heavily armored operative with a glowing orange visor fires a high-tech rifle from a rooftop command post as VTOL craft circle above a futuristic skyline. Monitors and supporting soldiers in the foreground emphasize a coordinated, high-stakes operation."

Image 9 — Portrait Trooper

Short alt text: "Front-facing soldier portrait wearing tactical vest with flags and headset."

Caption: "Portrait of a frontline trooper in a tactical vest and helmet, displaying national patches. Portrait-style lighting and neutral background suitable for character bios."

Image 10 — Unit Art: Masked Trooper

Short alt text: "Masked and armored trooper standing full-body with rifle — unit art."

Caption: "Full-body unit artwork showing a masked trooper in olive gear with weapon and modular pouches — useful as a roster unit card or art asset."

Image 11 — Vault of Eden Hero Art

Short alt text: "Cloaked figure in the Vault of Eden — mysterious hero art."

Caption: "A mysterious cloaked figure standing before an ancient obelisk in a vault, glowing eyes and a teal aura — strong hero artwork for production listings."

## Steps to prepare preview build
1. Update manifest/package name for the preview flavour (if using productFlavors)
2. Increment versionCode and versionName
3. Produce signed AAB and upload to internal testing track
4. Share internal test link with QA

## Screenshots and marketing
- Use store-assets/screenshots/ for preview screenshots
- Use store-assets/feature_graphic.png for temporary feature graphic

## Quick test commands
```bash
# Build (Gradle)
./gradlew bundleRelease
# Install universal apks for local QA
bundletool build-apks --bundle=app-release.aab --output=app.apks --mode=universal
bundletool install-apks --apks=app.apks
```

