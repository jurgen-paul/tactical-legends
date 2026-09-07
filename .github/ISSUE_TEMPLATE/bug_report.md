name: Bug Report
description: Report a bug or issue you've encountered
title: "[BUG] "
labels: ["bug", "needs-triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug! Please fill in the details below to help us investigate.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Brief description of the bug
      placeholder: "What happened?"
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this bug?
      placeholder: |
        1. Start game with difficulty set to "Normal"
        2. Create a squad with 2 warriors
        3. Move first unit to tile (5, 3)
        4. Bug occurs when...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen instead?
      placeholder: "The unit should move to the selected tile"
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened?
      placeholder: "The unit moves to a different tile or the game crashes"
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating System
      options:
        - Windows 10
        - Windows 11
        - macOS 10.14
        - macOS 11+
        - Ubuntu 18.04
        - Ubuntu 20.04
        - Ubuntu 22.04
        - Fedora
        - Arch Linux
        - Other
    validations:
      required: true

  - type: input
    id: os-version
    attributes:
      label: OS Version
      description: Specific version if "Other" selected
      placeholder: "e.g., CentOS 7"

  - type: input
    id: game-version
    attributes:
      label: Game Version
      description: What version are you running?
      placeholder: "v1.0.0 or 'latest develop branch'"
    validations:
      required: true

  - type: textarea
    id: system-info
    attributes:
      label: System Information
      description: Additional hardware/software details
      placeholder: |
        CPU: Intel i7-9700K
        RAM: 16GB
        GPU: NVIDIA RTX 2080
        Compiler: GCC 9.3

  - type: textarea
    id: logs
    attributes:
      label: Error Logs
      description: Any error messages or console output
      placeholder: "Paste error logs or console output here"
      render: shell

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots/Video
      description: Visual evidence of the bug (optional)
      placeholder: "You can drag and drop images or paste image URLs"

  - type: textarea
    id: workaround
    attributes:
      label: Workaround (if known)
      description: Any temporary workaround you've found
      placeholder: "e.g., Restarting the game fixes it temporarily"

  - type: checkboxes
    id: checklist
    attributes:
      label: Verification Checklist
      options:
        - label: I have searched existing issues and this is not a duplicate
          required: true
        - label: I am using the latest version of the game
          required: true
        - label: I can reliably reproduce this bug
          required: true
        - label: I have provided all necessary information
          required: true
