---
title: Preview — Tactical Legends
description: How to prepare and publish preview (internal/closed) builds for Tactical Legends
---

![Preview hero — Image 2 (Unit art soldier)](https://via.placeholder.com/800x1280.png?text=Image+2+-+Unit+Art+Soldier)

# Preview Builds & Test Tracks

This page explains how to prepare preview builds for testers.

## Hero image
Alt text: "Armored unit with modern gear holding a rifle — unit art used in preview builds."

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

