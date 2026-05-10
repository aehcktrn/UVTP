# Contributing to UVTP

First of all, thank you for considering contributing to the Universal Voice Trust Protocol! We are building a global standard to restore trust in human communication, and your help is vital.

## Our Philosophy
UVTP is built on **Zero-Trust** and **Hardware-Bound Security**. All contributions must prioritize:
1.  **Security**: No shortcuts. Private keys must remain in protected enclaves.
2.  **Privacy**: Minimize metadata exposure.
3.  **Performance**: Authentication must happen in real-time (<200ms).

## How to Contribute

### 1. Discussing Changes
Before starting work on a major feature, please open an **Issue** or join our **Discord** to discuss the architectural implications. This prevents wasted effort on features that might conflict with the RFC core.

### 2. Coding Standards
*   **Core Library**: Must be written in C or Rust for portability and TEE compatibility.
*   **PoC / Tools**: Python 3.7+ using `PyNaCl`.
*   **Documentation**: All public-facing documentation and comments must be in **English**.

### 3. Pull Request Process
1.  Fork the repository and create your branch from `main`.
2.  Ensure your code adheres to the existing style.
3.  Include a clear description of the problem solved or the feature added.
4.  Update the relevant documentation or RFC section if necessary.
5.  All commits must be signed (`git commit -S`) to ensure origin authenticity.

## Development Certificate of Origin (DCO)
By contributing to this project, you agree that your contributions are licensed under the **Apache License 2.0**.

---
*Questions? Contact the maintainer*

© 2026 UVTP Project. Licensed under Apache 2.0.