name: Feature Request
description: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: ["enhancement", "needs-triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thank you for suggesting a feature! Please describe your idea in detail below.

  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: What feature would you like to see?
      placeholder: "Describe the feature you'd like to have..."
    validations:
      required: true

  - type: textarea
    id: motivation
    attributes:
      label: Motivation & Use Case
      description: Why do you need this feature? What problem does it solve?
      placeholder: |
        This would be useful because...
        Players want to...
        It would improve...
    validations:
      required: true

  - type: textarea
    id: proposal
    attributes:
      label: Proposed Solution
      description: How do you think this should work?
      placeholder: |
        The feature could work like this:
        1. User does X
        2. System responds with Y
        3. Result is Z
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Any alternative approaches you've considered?
      placeholder: "Other ways to solve this problem..."

  - type: dropdown
    id: category
    attributes:
      label: Feature Category
      options:
        - Gameplay
        - UI/UX
        - Performance
        - Audio
        - Graphics
        - AI
        - Campaign/Story
        - Multiplayer
        - Accessibility
        - Developer Tools
        - Other
    validations:
      required: true

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low (nice to have)
        - Medium (would improve experience)
        - High (important for the game)
        - Critical (blocks other features)
    validations:
      required: true

  - type: textarea
    id: examples
    attributes:
      label: Examples or References
      description: Any games or features that do something similar?
      placeholder: |
        Similar to feature X in game Y...
        Like how [other game] does this...

  - type: textarea
    id: implementation
    attributes:
      label: Implementation Notes
      description: Technical thoughts on implementation (optional)
      placeholder: "This could be implemented using... This would require changes to..."

  - type: checkboxes
    id: checklist
    attributes:
      label: Verification Checklist
      options:
        - label: I have searched existing issues and this is not a duplicate
          required: true
        - label: This feature aligns with the game's design
          required: true
        - label: I have provided sufficient detail
          required: true
