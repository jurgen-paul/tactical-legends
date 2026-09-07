# Installation & Setup Guide

Complete instructions for building and running Tactical Legends on your system.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Linux Installation](#linux-installation)
3. [macOS Installation](#macos-installation)
4. [Windows Installation](#windows-installation)
5. [Troubleshooting](#troubleshooting)
6. [Development Setup](#development-setup)

---

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10, macOS 10.14, Ubuntu 18.04 LTS |
| **CPU** | Intel i5 / AMD Ryzen 5 or equivalent |
| **RAM** | 4 GB |
| **GPU** | Intel HD Graphics / NVIDIA GTX 960 / AMD R7 260X |
| **Storage** | 2 GB free space |
| **Display** | 1920×1080 or higher |

### Recommended Specifications

| Component | Recommendation |
|-----------|----------------|
| **OS** | Windows 11, macOS 12+, Ubuntu 20.04 LTS |
| **CPU** | Intel i7 / AMD Ryzen 7 or equivalent |
| **RAM** | 8 GB |
| **GPU** | NVIDIA RTX 2060 / AMD RX 5700 XT or better |
| **Storage** | 2 GB SSD space |
| **Display** | 2560×1440 or higher, 144Hz+ |

### Build Requirements

To compile from source, you need:

- **CMake**: 3.16 or higher
- **C++ Compiler**: C++17 compatible
  - GCC 9.0+
  - Clang 10+
  - MSVC 2019 or newer
- **SDL2 Development Libraries**
- **Git**: For cloning the repository

---

## Linux Installation

### Ubuntu / Debian

#### Step 1: Install Dependencies

```bash
sudo apt update
sudo apt install -y \
  cmake \
  g++ \
  git \
  libsdl2-dev \
  libsdl2-image-dev \
  libsdl2-mixer-dev \
  libsdl2-ttf-dev
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends
```

#### Step 3: Create Build Directory

```bash
mkdir build
cd build
```

#### Step 4: Configure Build

```bash
# Standard Release build
cmake -S.. -B. -DCMAKE_BUILD_TYPE=Release

# Alternative: Debug build (for development)
cmake -S.. -B. -DCMAKE_BUILD_TYPE=Debug
```

#### Step 5: Compile

```bash
# Single-threaded build
cmake --build .

# Multi-threaded build (faster)
cmake --build . -j$(nproc)
```

#### Step 6: Run Game

```bash
./tactical_legends
```

### Fedora / RHEL / CentOS

```bash
# Install dependencies
sudo dnf install -y \
  cmake \
  gcc-c++ \
  git \
  SDL2-devel \
  SDL2_image-devel \
  SDL2_mixer-devel \
  SDL2_ttf-devel

# Clone and build
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends
mkdir build && cd build
cmake -S.. -B. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)

# Run
./tactical_legends
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S cmake gcc git sdl2 sdl2_image sdl2_mixer sdl2_ttf

# Clone and build
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends
mkdir build && cd build
cmake -S.. -B. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)

# Run
./tactical_legends
```

---

## macOS Installation

### Prerequisites

- **macOS 10.14** or later
- **Xcode Command Line Tools**
- **Homebrew** (recommended package manager)

### Step 1: Install Xcode Tools

```bash
xcode-select --install
```

### Step 2: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 3: Install Dependencies

```bash
brew update
brew install cmake sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

### Step 4: Clone Repository

```bash
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends
```

### Step 5: Build Project

```bash
mkdir build
cd build
cmake -S.. -B. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(sysctl -n hw.ncpu)
```

### Step 6: Run Game

```bash
./tactical_legends
```

### (Optional) Create App Bundle

```bash
# Create macOS application bundle
mkdir -p Tactical\ Legends.app/Contents/MacOS
mkdir -p Tactical\ Legends.app/Contents/Resources

cp tactical_legends Tactical\ Legends.app/Contents/MacOS/
cp ../assets/* Tactical\ Legends.app/Contents/Resources/

# Run as application
open Tactical\ Legends.app
```

---

## Windows Installation

### Prerequisites

- **Windows 10** or later
- **Visual Studio 2019** or newer (Community Edition is free)
- **CMake 3.16+**

### Using Visual Studio

#### Step 1: Install Visual Studio

Download from https://visualstudio.microsoft.com/

Components to install:
- Desktop development with C++
- CMake tools for Windows

#### Step 2: Install CMake

Download from https://cmake.org/download/

Or use Chocolatey:
```powershell
choco install cmake
```

#### Step 3: Install SDL2 Libraries

Option A: Using vcpkg (Microsoft's package manager)

```powershell
# Clone vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg

# Bootstrap vcpkg
.\bootstrap-vcpkg.bat

# Install SDL2 libraries
.\vcpkg install sdl2:x64-windows sdl2-image:x64-windows sdl2-mixer:x64-windows sdl2-ttf:x64-windows

# Note the integration command that appears
```

Option B: Manual installation

Download SDL2 development libraries from:
- https://www.libsdl.org/
- https://www.libsdl.org/projects/

#### Step 4: Clone Repository

```powershell
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends
```

#### Step 5: Generate Visual Studio Project

```powershell
# Using vcpkg
cmake -S. -B build -G "Visual Studio 16 2019" `
  -DCMAKE_TOOLCHAIN_FILE=C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake

# Without vcpkg (manual SDL2 paths)
cmake -S. -B build -G "Visual Studio 16 2019"
```

#### Step 6: Open and Build

```powershell
# Open in Visual Studio
start build\tactical_legends.sln

# Or build from command line
cmake --build build --config Release
```

#### Step 7: Run

```powershell
.\build\Release\tactical_legends.exe
```

### Using Command Prompt (Advanced)

```batch
REM Clone repository
git clone https://github.com/jurgen-paul/tactical-legends.git
cd tactical-legends

REM Create build directory
mkdir build
cd build

REM Configure
cmake -S.. -B. -G "Visual Studio 16 2019"

REM Build
cmake --build . --config Release

REM Run
.\Release\tactical_legends.exe
```

---

## Troubleshooting

### Common Issues

#### CMake Not Found

**Error**: `cmake: command not found`

**Solution**:
- Linux: `sudo apt install cmake`
- macOS: `brew install cmake`
- Windows: Download from https://cmake.org/download/

#### Missing SDL2 Libraries

**Error**: `SDL2 not found` or `Could not find SDL2`

**Solution**:
```bash
# Linux (Ubuntu)
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev

# macOS
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

# Windows
# Use vcpkg as shown in Windows installation section
```

#### C++ Compiler Issues

**Error**: `g++: command not found` or `cl.exe not found`

**Solution**:
```bash
# Linux
sudo apt install build-essential

# macOS
xcode-select --install

# Windows
# Install Visual Studio with C++ tools
```

#### Game Won't Start / Window Issues

**Error**: Window doesn't appear or crashes immediately

**Solutions**:
1. Verify SDL2 libraries are properly installed
2. Check graphics drivers are up to date
3. Try windowed mode (check settings.json)
4. Run in debug mode for detailed output:
   ```bash
   ./tactical_legends --debug
   ```

#### Build Fails with Permission Error

**Error**: `Permission denied` when running `cmake --build`

**Solution**:
```bash
# Linux/macOS
sudo chmod +x ./build/tactical_legends

# Or rebuild
cd build
rm -rf *
cmake ..
cmake --build .
```

#### Port Already in Use

**Error**: `Port 5000 already in use` or similar

**Solution**:
```bash
# Find process using port
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in config
```

---

## Development Setup

### Building for Development

```bash
# Create debug build
mkdir build-debug
cd build-debug
cmake -S.. -B. -DCMAKE_BUILD_TYPE=Debug
cmake --build .

# Run with debug symbols
gdb ./tactical_legends
```

### Running Tests

```bash
cd build
ctest --output-on-failure

# Run specific test
ctest -R test_ai_system -V

# Generate coverage report
cmake --build . --target coverage
open coverage/index.html
```

### Code Formatting

```bash
# Install clang-format
sudo apt install clang-format  # Linux
brew install clang-format      # macOS

# Format all code
find src -name "*.cpp" -o -name "*.h" | xargs clang-format -i

# Or use pre-commit hook
cp scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### Debugging

#### Linux / macOS with GDB

```bash
# Build with debug symbols
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build .

# Run under debugger
gdb ./tactical_legends

# Common GDB commands
(gdb) run
(gdb) break main
(gdb) continue
(gdb) print variable_name
(gdb) step
(gdb) next
```

#### Visual Studio Debugger

1. Open `build/tactical_legends.sln` in Visual Studio
2. Set breakpoints by clicking line numbers
3. Press **F5** to run with debugger
4. Use Debug menu for stepping, inspection

#### LLDB (macOS)

```bash
lldb ./tactical_legends
(lldb) run
(lldb) breakpoint set --name main
(lldb) continue
```

### Profiling Performance

```bash
# Linux: Using perf
perf record ./tactical_legends
perf report

# macOS: Using Instruments
instruments -t "System Trace" ./tactical_legends

# Valgrind (memory profiling)
valgrind --leak-check=full ./tactical_legends
```

---

## Environment Variables

Optional configuration via environment variables:

```bash
# Set log level
export TACTICAL_LOG_LEVEL=DEBUG

# Disable audio
export TACTICAL_NO_AUDIO=1

# Force windowed mode
export TACTICAL_WINDOWED=1

# Set resolution
export TACTICAL_WIDTH=1280
export TACTICAL_HEIGHT=720

# Enable verbose output
export TACTICAL_VERBOSE=1
```

---

## Next Steps

After installation:

1. **Run the game**: `./tactical_legends`
2. **Read gameplay guide**: See [GAMEPLAY.md](GAMEPLAY.md)
3. **Explore architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Contribute**: See [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review [FAQ on GitHub](https://github.com/jurgen-paul/tactical-legends/discussions)
3. Search [existing issues](https://github.com/jurgen-paul/tactical-legends/issues)
4. Open a [new issue](https://github.com/jurgen-paul/tactical-legends/issues/new) with:
   - Your OS and version
   - Installation steps you followed
   - Complete error message
   - Relevant logs

---

**Last Updated**: September 2024
**Version**: 1.0.0
