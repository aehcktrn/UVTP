# UVTP Proof of Concept (Python)

## Restoring Trust in Human Communication in the Age of AI

**Author:** Adrien Eberhaerd (Prom')  
**Date:** May 2026  
**Status:** Version 1.0 - Draft

This directory contains a functional simulation of the **Universal Voice Trust Protocol**. The goal of this PoC is to demonstrate how a cryptographic side-channel can certify an identity during a voice call, regardless of the audio quality or potential voice cloning.

## Prerequisites
The PoC requires **Python 3.7+** and the **PyNaCl** library (a Python binding for `libsodium`).

```bash
pip install pynacl
```

### Running the Demo
Simply execute the script to simulate a complete verification workflow (from key generation to trust-badge display):

```bash
python poc_demo.py
```

## What this PoC demonstrates
### 1. Hardware-Bound Identity
The script generates an Ed25519 key pair. In a production environment, the private key would be generated inside the smartphone's Secure Enclave or TEE, making it impossible to extract even if the device is compromised.

### 2. Side-Channel Proof Generation
When an outgoing call is initiated, the script creates a JSON-LD payload containing:

The caller's identifier (DID).

A salted hash of the recipient's number (for privacy).

A Nonce and a Timestamp (to prevent replay attacks).

### 3. Cryptographic Attestation
The payload is signed using the private key. This signature is the "Proof of Life" of the device. Even if an attacker clones your voice perfectly, they cannot produce this signature without your physical hardware.

### 4. Verification & Freshness
The "Callee" (receiver) verifies:

Integrity: Has the data been tampered with?

Authenticity: Does the signature match the caller's public key?

Freshness: Is the proof recent (less than 10 seconds)? If a proof is reused 5 minutes later, it is rejected.

## ⚠️ Limitations
This is a simulated workflow. In a real-world scenario, the Call-Proof would be transmitted via a decentralized relay network (UVTP-Provider).

The "Discovery" phase (finding the caller's public key) is simplified here for demonstration purposes.

© 2026 UVTP Project. Licensed under Apache 2.0.