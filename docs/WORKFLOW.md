# Development Workflow & Version Control

Guidelines for collaborative development, version control, and code review processes for Tactical Legends.

## Table of Contents

1. [Git Workflow](#git-workflow)
2. [Branch Strategy](#branch-strategy)
3. [Commit Conventions](#commit-conventions)
4. [Pull Request Process](#pull-request-process)
5. [Code Review Guidelines](#code-review-guidelines)
6. [Release Management](#release-management)
7. [Versioning](#versioning)

---

## Git Workflow

### Workflow Overview

Tactical Legends uses a **modified Git Flow** workflow with feature branches and staged releases:

```
main (releases only)
  ↑
  ├← develop (integration branch)
  │   ↑
  │   ├← feature/xxx (features)
  │   ├← bugfix/xxx (bug fixes)
  │   ├← docs/xxx (documentation)
  │   └← refactor/xxx (refactoring)
  │
  ├← release/v1.x.x (release preparation)
  │   ↑
  │   └← hotfix/xxx (urgent fixes)
```

### Initial Setup

```bash
# Clone repository
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends

# Add upstream remote
git remote add upstream https://github.com/jurgen-paul/tactical-legends.git
git remote add origin https://github.com/YOUR_USERNAME/tactical-legends.git

# Verify remotes
git remote -v
# origin    https://github.com/YOUR_USERNAME/tactical-legends.git (fetch)
# origin    https://github.com/YOUR_USERNAME/tactical-legends.git (push)
# upstream  https://github.com/jurgen-paul/tactical-legends.git (fetch)
# upstream  https://github.com/jurgen-paul/tactical-legends.git (push)
```

---

## Branch Strategy

### Main Branches

#### `main`
- **Purpose**: Production-ready code only
- **Protection**: Requires PR review + passing tests
- **Merge Source**: `release/` branches only
- **Tag**: Version tags (v1.0.0, v1.1.0)

```bash
# Merge release into main
git checkout main
git merge --no-ff release/v1.1.0
git tag -a v1.1.0 -m "Release version 1.1.0"
git push upstream main --tags
```

#### `develop`
- **Purpose**: Integration branch for features
- **Status**: Should always be stable and deployable
- **Merge Source**: Feature/bugfix/docs branches
- **Frequency**: New features merged regularly

```bash
# Update develop from upstream
git checkout develop
git pull upstream develop
```

### Feature Branches

#### Naming Convention
```
feature/FEATURE-NAME
bugfix/BUG-NAME
docs/DOC-NAME
refactor/REFACTOR-NAME
chore/CHORE-NAME
```

#### Creating a Feature Branch

```bash
# Update local develop
git checkout develop
git pull upstream develop

# Create feature branch
git checkout -b feature/add-ai-aggression-setting

# Make changes
git add .
git commit -m "Add AI aggression difficulty setting"

# Keep updated with upstream
git fetch upstream
git rebase upstream/develop
```

#### Finishing a Feature Branch

```bash
# Final cleanup
git rebase -i upstream/develop  # Interactive rebase for clean history

# Push to your fork
git push origin feature/add-ai-aggression-setting

# Create Pull Request on GitHub
# (Merge target: develop branch)
```

### Release Branches

Used for release preparation (version bumps, release notes):

```bash
# Create release branch from develop
git checkout -b release/v1.1.0 develop

# Update version numbers
# Update CHANGELOG.md
# Final testing

git commit -m "Bump version to 1.1.0"

# Merge to main
git checkout main
git merge --no-ff release/v1.1.0
git tag -a v1.1.0 -m "Release 1.1.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.1.0

# Cleanup
git branch -d release/v1.1.0
```

### Hotfix Branches

For urgent fixes to production:

```bash
# Create from main
git checkout -b hotfix/critical-ai-crash main

# Make fix
git commit -m "Fix critical AI crash on unit death"

# Merge to main
git checkout main
git merge --no-ff hotfix/critical-ai-crash
git tag -a v1.1.1 -m "Hotfix 1.1.1"

# Merge back to develop
git checkout develop
git merge --no-ff hotfix/critical-ai-crash

# Cleanup
git branch -d hotfix/critical-ai-crash
```

---

## Commit Conventions

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Code style (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without feature change
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Build, CI/CD, dependencies

### Scope

Scope of the change:
- `ai` - AI system changes
- `battle` - Battle/combat system
- `ui` - User interface
- `campaign` - Campaign/story system
- `audio` - Audio system
- `build` - Build system
- `docs` - Documentation
- `tests` - Test changes

### Subject

- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period at end
- Max 50 characters

### Body

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Separate from subject with blank line

### Footer

- Reference issues: `Fixes #123`
- Reference PRs: `Related to #456`
- Breaking changes: `BREAKING CHANGE: ...`

### Examples

```bash
# Feature
feat(ai): add difficulty-based decision randomness

Implement difficulty scaling that adjusts how randomly AI units make decisions.
On Easy mode, AI has 80% randomness in non-critical decisions.
On Hard mode, AI uses 20% randomness for more predictable (exploitable) play.

Closes #45

# Bug fix
fix(battle): resolve turn order reset after unit defeat

Previously, when a unit was defeated mid-turn, the turn order would reset
causing all remaining units to skip their turns. Now turn order continues
properly by tracking turn indices rather than unit references.

Fixes #123

# Documentation
docs(gameplay): update combat system documentation

Add detailed explanation of action point system and how abilities cost AP.
Include examples of valid and invalid action sequences.

# Refactoring
refactor(pathfinding): extract heuristic calculation to separate function

Extract Manhattan distance heuristic into its own method for better
code organization and testability.

# Performance
perf(rendering): optimize sprite batching for large maps

Batch sprites by texture before rendering to reduce draw calls from 500
to 50 on large maps, improving frame rate by 40%.
```

### Commit Best Practices

```bash
# Make logical, atomic commits
git add src/ai/behavior_tree.cpp
git commit -m "feat(ai): implement behavior tree selector node"

# Keep commits small and focused
# ✓ Good: One feature per commit
# ✗ Bad: Multiple unrelated changes in one commit

# Use interactive rebase to clean up before PR
git rebase -i upstream/develop

# Don't rewrite public history
# ✓ Good: Rebase before first push
# ✗ Bad: Rebase after push (unless force-push agreed upon)
```

---

## Pull Request Process

### Before Creating a PR

1. **Create feature branch** from `develop`
2. **Make focused changes** related to one feature/fix
3. **Write clear commit messages** following conventions
4. **Test locally** - run tests and verify functionality
5. **Keep updated** with `develop` branch:
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```
6. **Clean up history** with interactive rebase if needed
7. **Verify no conflicts** before pushing

### Creating a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open PR on GitHub** with:
   - Clear title following convention
   - Detailed description
   - Reference related issues
   - Screenshot/video for UI changes

3. **PR Template** (in `.github/pull_request_template.md`):
   ```markdown
   ## Description
   Brief description of changes

   ## Related Issues
   Fixes #123
   Related to #456

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   How was this tested?
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Manual testing

   ## Screenshots
   (if applicable)

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Comments added for complex logic
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] No new warnings generated
   - [ ] Changes tested locally
   ```

### PR Naming Convention

```
[TYPE] Brief description

# Examples:
[FEATURE] Add AI aggression difficulty setting
[BUGFIX] Fix turn order reset on unit defeat
[DOCS] Update combat system documentation
[REFACTOR] Extract pathfinding heuristic function
```

---

## Code Review Guidelines

### For Authors

**Before requesting review:**
- Self-review your own changes first
- Ensure tests pass: `ctest --output-on-failure`
- Check code style with linter
- Verify no merge conflicts
- Keep PR focused (one feature per PR)

**Responding to feedback:**
- Thank reviewers for feedback
- Ask questions if feedback is unclear
- Don't argue - discuss respectfully
- Make requested changes promptly
- Push updates - don't force-push (keep history)

### For Reviewers

**What to check:**
1. **Functionality**: Does code do what it claims?
2. **Design**: Does it follow architecture patterns?
3. **Tests**: Are there adequate tests? Do they pass?
4. **Style**: Does it follow code guidelines?
5. **Performance**: Any obvious inefficiencies?
6. **Security**: Any potential vulnerabilities?
7. **Documentation**: Are changes documented?

**Review comments:**
- Use "Request Changes" for blocking issues
- Use "Comment" for suggestions/questions
- Be constructive and helpful
- Acknowledge good work

**Approval criteria:**
- ✅ At least 2 approvals from maintainers
- ✅ All checks passing (CI/CD, tests)
- ✅ No merge conflicts
- ✅ Documentation updated
- ✅ Code follows style guidelines

### Review Checklist

```markdown
### Code Quality
- [ ] Code is clear and readable
- [ ] No unnecessary complexity
- [ ] Follows project conventions
- [ ] DRY principle (Don't Repeat Yourself)

### Testing
- [ ] Tests are comprehensive
- [ ] Edge cases covered
- [ ] Tests are readable and maintainable
- [ ] No test skips/ignores without reason

### Documentation
- [ ] Code comments explain "why"
- [ ] Public APIs documented
- [ ] README updated if needed
- [ ] CHANGELOG updated

### Performance
- [ ] No obvious inefficiencies
- [ ] Appropriate algorithms used
- [ ] No unnecessary allocations
- [ ] Caching used appropriately

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] No SQL injection risks
- [ ] Proper error handling
```

---

## Release Management

### Release Checklist

```markdown
## Pre-Release (1 week before)
- [ ] Create release branch: `release/vX.Y.Z`
- [ ] Update version in CMakeLists.txt
- [ ] Update CHANGELOG.md with all changes
- [ ] Update README.md if needed
- [ ] Run full test suite
- [ ] Test on all platforms
- [ ] Security audit if applicable

## Testing Phase
- [ ] Build on Linux
- [ ] Build on macOS
- [ ] Build on Windows
- [ ] Run all unit tests
- [ ] Run integration tests
- [ ] Manual gameplay testing
- [ ] Performance profiling

## Release Day
- [ ] Merge release branch to main
- [ ] Create version tag: `v1.2.0`
- [ ] Merge back to develop
- [ ] Create GitHub Release
- [ ] Update website documentation
- [ ] Announce release in discussions

## Post-Release
- [ ] Monitor for critical issues
- [ ] Prepare hotfix branch if needed
- [ ] Start next development cycle
- [ ] Update roadmap/milestones
```

### Version Bumping

```bash
# Release preparation
git checkout -b release/v1.2.0 develop

# Update version in CMakeLists.txt
# version(PROJECT_NAME 1 2 0)

# Update CHANGELOG.md
# Update docs if needed

git add CMakeLists.txt CHANGELOG.md
git commit -m "chore(release): bump version to 1.2.0"

# Merge to main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release 1.2.0"
git push upstream main --tags

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0
git push upstream develop
```

---

## Versioning

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Examples

```
v0.1.0 - Initial development
v0.5.0 - Major features added
v1.0.0 - First stable release
v1.1.0 - New features (backward compatible)
v1.1.1 - Bug fixes
v2.0.0 - Breaking changes, new API
```

### Pre-Release Versions

```
v1.1.0-alpha.1   # Alpha release
v1.1.0-beta.1    # Beta release
v1.1.0-rc.1      # Release candidate
```

### Version Consistency

All version references must match:
- `CMakeLists.txt`: `project(tactical_legends VERSION 1.1.0)`
- `docs/OVERVIEW.md`: Update version section
- `CHANGELOG.md`: Add release notes
- GitHub Releases: Tag and notes
- Website: Update version info

---

## Development Tips

### Keep Your Fork Updated

```bash
# Add upstream as remote (one time)
git remote add upstream https://github.com/jurgen-paul/tactical-legends.git

# Update regularly
git fetch upstream
git rebase upstream/develop

# Or pull with rebase
git pull --rebase upstream develop
```

### Squash Commits Before Merge

```bash
# Rebase and squash (interactive mode)
git rebase -i upstream/develop

# Mark commits to squash
# pick aaa1111 First commit
# squash bbb2222 Second commit  <- squash this
# squash ccc3333 Third commit   <- squash this

# Result: one clean commit
```

### View Commit History

```bash
# View recent commits
git log --oneline -10

# View with graph
git log --graph --oneline --all

# View specific author
git log --author="jurgen-paul" --oneline
```

### Resolve Merge Conflicts

```bash
# View conflicts
git status

# Edit conflicted files, then
git add <resolved-file>
git commit -m "chore: resolve merge conflicts with develop"
```

---

## Continuous Integration

### GitHub Actions

Workflows run automatically on:
- **Push to branches**: Tests on every push
- **Pull requests**: Tests before merge
- **Releases**: Build and test artifacts

Workflow file: `.github/workflows/ci.yml`

```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build
        run: |
          mkdir build && cd build
          cmake -S.. -B.
          cmake --build .
      - name: Tests
        run: ctest --output-on-failure
```

---

## Community Guidelines

- **Be respectful** in all interactions
- **Assume good intent** when reviewing
- **Ask questions** rather than make demands
- **Give credit** to contributors
- **Share knowledge** generously
- **Report security issues** privately first
- **Follow Code of Conduct** in all communications

See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) for full guidelines.

---

**Last Updated**: September 2024
**Version**: 1.0.0
