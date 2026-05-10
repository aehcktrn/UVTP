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

## How it work

sequenceDiagram
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

## ⚠️ Limitations
This is a simulated workflow. In a real-world scenario, the Call-Proof would be transmitted via a decentralized relay network (UVTP-Provider).

The "Discovery" phase (finding the caller's public key) is simplified here for demonstration purposes.

© 2026 UVTP Project. Licensed under Apache 2.0.