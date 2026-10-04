# Build and Release notes — Android App Bundle (.aab)

This document contains general guidance for building an Android App Bundle and preparing a Play Store release.

Unity
- File > Build Settings > Android > Switch Platform to Android
- Player Settings: set Package Name (com.example.tacticallegends), Version, and Version Code
- Build > Build (select "Build App Bundle")

Gradle (non-Unity Android projects)
- ./gradlew bundleRelease
- Output: app/build/outputs/bundle/release/app-release.aab

Signing and Play App Signing
- Generate a signing key (keystore) and sign your AAB or let Play manage the keys.

Verify with bundletool
1. Build an APK from the AAB (universal) for local testing:

```bash
# build universal apks
bundletool build-apks --bundle=app-release.aab --output=app.apks --mode=universal
bundletool install-apks --apks=app.apks
```

Internal testing
- Upload the signed AAB to Play Console internal testing track first
- Use internal testers to validate installation and basic runtime behavior

Common checks
- Target SDK >= current Play requirement
- No excessive runtime permissions requested
- Privacy policy URL is reachable and accurate
- Asset images meet Play Store dimensions and format

