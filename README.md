# UVTP - Universal Voice Trust Protocol

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Status-Draft-orange.svg)]()

**UVTP** is an open-source, application-layer protocol designed to restore trust in voice communications. It provides a cryptographic defense against AI-generated voice cloning (Audio Deepfakes) using an out-of-band (OOB) verification channel.

## The Problem
With the rise of generative AI, voice has become a fallible biometric. Attackers can now clone a person's voice with just a few seconds of audio, rendering traditional "vishing" (voice phishing) defenses and simple voice recognition obsolete.

## The Solution
UVTP decouples **voice transmission** from **identity certification**. 
Instead of trusting the audio stream, UVTP generates a hardware-backed cryptographic proof on the caller's device and verifies it on the callee's device via a secure data side-channel.

## Key Features
*   **Zero-Trust Architecture**: Never trust the audio; always verify the key.
*   **Hardware-Bound Security**: Private keys are stored in the device's Secure Enclave/TEE.
*   **Privacy by Design**: Uses Decentralized Identifiers (DIDs) and hashed metadata to protect user privacy.
*   **Agnostic**: Works across GSM, VoIP, and any messaging app.

## Project Structure
*   `docs/rfc/`: Technical specifications and protocol drafts.
*   `core/`: Reference implementation of the cryptographic engine.
*   `poc/`: Python-based Proof of Concept for quick testing.

## Getting Involved
We are looking for contributors in the following areas:
*   Cryptography (Ed25519, Zero-Knowledge Proofs)
*   Mobile Development (Android StrongBox / iOS Secure Enclave)
*   Network Architecture (High-availability relays)

# Contributing
This project is in its early stages. We welcome security researchers, cryptographers, and mobile OS architects.
Please read our CONTRIBUTING.md and SECURITY.md before submitting Pull Requests.

# License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

Created with love and maintained by Adrien Eberhaerd (Prom').

© 2026 UVTP Project. Licensed under Apache 2.0.
