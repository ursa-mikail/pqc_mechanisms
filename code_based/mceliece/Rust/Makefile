# McEliece Cryptosystem Project Makefile

# Variables
CARGO = cargo
RUSTC = rustc
PROJECT_NAME = mce
TARGET_DIR = target
RELEASE_DIR = $(TARGET_DIR)/release
DEBUG_DIR = $(TARGET_DIR)/debug
BIN_NAME = $(PROJECT_NAME)

# Default target
.DEFAULT_GOAL := help

.PHONY: all build release debug clean test run help fmt lint install uninstall

## Build targets

# Build everything (debug + release)
all: debug release

# Build in debug mode (default)
debug:
	@echo "Building in debug mode..."
	$(CARGO) build
	@echo "Debug build complete: $(DEBUG_DIR)/$(BIN_NAME)"

# Build in release mode
release:
	@echo "Building in release mode..."
	$(CARGO) build --release
	@echo "Release build complete: $(RELEASE_DIR)/$(BIN_NAME)"

# Run the application
run:
	$(CARGO) run

# Run in release mode
run-release:
	$(CARGO) run --release

## Development targets

# Run tests
test:
	$(CARGO) test

# Format code
fmt:
	$(CARGO) fmt

# Check code quality
lint:
	$(CARGO) clippy

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	$(CARGO) clean
	@echo "Clean complete"

# Install the binary to Cargo's bin directory
install: release
	$(CARGO) install --path .

# Uninstall the binary
uninstall:
	$(CARGO) uninstall $(PROJECT_NAME)

## Utility targets

# Show project information
info:
	@echo "=== Project Information ==="
	@echo "Project: $(PROJECT_NAME)"
	@echo "Rust version: $(shell $(RUSTC) --version | cut -d' ' -f2)"
	@echo "Target directory: $(TARGET_DIR)"
	@echo "Debug binary: $(DEBUG_DIR)/$(BIN_NAME)"
	@echo "Release binary: $(RELEASE_DIR)/$(BIN_NAME)"
	@echo "Dependencies:"
	@$(CARGO) tree

# Check for vulnerabilities
audit:
	$(CARGO) audit

# Generate documentation
doc:
	$(CARGO) doc --open

# Build for production (includes optimization and stripping)
production: release
	@echo "Stripping debug symbols for production..."
	strip $(RELEASE_DIR)/$(BIN_NAME)
	@echo "Production build ready: $(RELEASE_DIR)/$(BIN_NAME)"
	@ls -lh $(RELEASE_DIR)/$(BIN_NAME)

# Size analysis
size:
	@echo "=== Binary Sizes ==="
	@echo "Debug:"
	@ls -lh $(DEBUG_DIR)/$(BIN_NAME) | awk '{print $$5}'
	@echo "Release:"
	@ls -lh $(RELEASE_DIR)/$(BIN_NAME) | awk '{print $$5}'

# Show help
help:
	@echo "McEliece Cryptosystem Project Makefile"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "  Build:"
	@echo "    all        - Build everything (debug + release)"
	@echo "    build      - Build in debug mode (alias for debug)"
	@echo "    debug      - Build in debug mode"
	@echo "    release    - Build in release mode"
	@echo "    production - Build optimized release binary (stripped)"
	@echo ""
	@echo "  Execution:"
	@echo "    run        - Run in debug mode"
	@echo "    run-release - Run in release mode"
	@echo ""
	@echo "  Development:"
	@echo "    test       - Run tests"
	@echo "    fmt        - Format code"
	@echo "    lint       - Run clippy linter"
	@echo "    doc        - Generate and open documentation"
	@echo ""
	@echo "  Maintenance:"
	@echo "    clean      - Remove build artifacts"
	@echo "    install    - Install binary to cargo bin"
	@echo "    uninstall  - Uninstall binary"
	@echo "    audit      - Check for security vulnerabilities"
	@echo ""
	@echo "  Information:"
	@echo "    info       - Show project information"
	@echo "    size       - Show binary sizes"
	@echo "    help       - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run        # Build and run in debug mode"
	@echo "  make release    # Build optimized version"
	@echo "  make clean test # Clean then run tests"

# Alias for debug build
build: debug