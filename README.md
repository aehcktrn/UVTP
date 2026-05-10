# UVTP - Universal Voice Trust Protocol

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status](https://img.shields.io/badge/Status-Draft-orange.svg)]()

**UVTP** is an open-source, application-layer protocol designed to restore trust in voice communications. It provides a cryptographic defense against AI-generated voice cloning (Audio Deepfakes) using an out-of-band (OOB) verification channel.

## The Problem
With the rise of generative AI, voice has become a fallible biometric. Attackers can now clone a person's voice with just a few seconds of audio, rendering traditional "vishing" (voice phishing) defenses and simple voice recognition obsolete.

## The Solution
UVTP decouples **voice transmission** from **identity certification**. 
Instead of trusting the audio stream, UVTP generates a hardware-backed cryptographic proof on the caller's device and verifies it on the callee's device via a secure data side-channel.

## How it work

sequence_diagram
    participant Caller as 📱 Caller (Alice)
    participant Relay as 🌐 UVTP Relay
    participant Callee as 📱 Callee (Bob)
    participant PSTN as 📞 Telecom Network (Voice)

    Note over Caller: 1. Start Call & Generate Proof
    Caller->>Relay: POST /proof (Signed JSON + Target Hash)
    
    Note over Caller, PSTN: 2. Voice path established
    Caller->>PSTN: Initiate Voice Call
    PSTN->>Callee: Incoming Call...

    Note over Callee: 3. Fetch & Verify
    Callee->>Relay: GET /proof (for incoming caller DID)
    Relay-->>Callee: Returns Signed Call-Proof
    
    Note over Callee: 4. Cryptographic Validation
    Callee->>Callee: Check Signature, IAT & Nonce
    
    Note over Callee: 5. Trust UI
    Callee-->>Callee: Display ✅ TRUST-BADGE

### The UVTP Handshake:

**Generation**: The caller’s device signs a Call-Proof using an Ed25519 key secured in the Secure Enclave.

**Signaling**: The proof is sent to a decentralized UVTP Relay before the call signal reaches the target.

**Validation**: Upon receiving the call, the callee's device fetches the proof via its data connection (independent of the voice channel).

**Certification**: The identity is verified locally on the device. If the math checks out, the user sees a Trust-Badge on the dialer UI.

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
