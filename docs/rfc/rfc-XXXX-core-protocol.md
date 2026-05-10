**Network Working Group**                                     **Adrien Eberhaerd (Prom')**
**Internet-Draft**                                            **Open-Source Project**
**Intended status: Standards Track**                          **May 2026**
**Expires: November 2026**

# RFC XXXX: Universal Voice Trust Protocol (UVTP)

## Abstract
This document specifies the **Universal Voice Trust Protocol (UVTP)**, an application-layer protocol designed to cryptographically attest to the identity of participants in a real-time voice communication session. UVTP leverages an out-of-band (OOB) data channel and asymmetric cryptography to mitigate identity theft and "vishing" attacks enabled by generative AI voice synthesis (Audio Deepfakes).

## Status of this Memo
This Internet-Draft is submitted in full conformance with the provisions of BCP 78 and BCP 79. This is a working document intended for community review and standardization.

---

## 1. Introduction
Traditional voice communication channels lack native identity authentication. Current telecommunications standards (e.g., STIR/SHAKEN) authenticate the originating telephone number but do not verify the biological or cryptographic identity of the speaker. With the advent of near-perfect voice cloning, audio becomes a fallible biometric.

UVTP introduces a **side-channel verification layer** that binds a telephonic session to a cryptographic proof generated within a terminal's hardware-protected environment.

### 1.1 Terminology
*   **Caller**: The entity initiating the voice session.
*   **Callee**: The entity receiving the voice session.
*   **UVTP-Provider**: A decentralized discovery service facilitating the transit of call proofs.
*   **Trust-Badge**: A hardware-secured UI element indicating a verified identity.

---

## 2. Protocol Architecture
UVTP assumes the existence of **Decentralized Identifiers (DIDs)**. Private keys MUST be stored within a terminal’s **Trusted Execution Environment (TEE)** or **Secure Element (SE)** and MUST NOT be exportable.

### 2.1 Verification Workflow
1.  **Generation**: Upon call initiation, the Caller’s terminal generates a signed `Call-Proof`.
2.  **Publication**: The `Call-Proof` is transmitted to a UVTP-Provider with a limited Time-to-Live (TTL).
3.  **Discovery**: Upon receiving the signaling (GSM/VoIP), the Callee’s terminal queries the UVTP network using the Caller’s identifier.
4.  **Attestation**: If the signature is verified against the Caller’s registered public key, the terminal displays the Trust-Badge.

---

## 3. Technical Specifications

### 3.1 Call-Proof Data Format (JSON-LD)
Payloads MUST be kept minimal to ensure a total latency overhead of <200ms.

```json
{
  "@context": "[https://w3id.org/uvtp/v1](https://w3id.org/uvtp/v1)",
  "type": "CallProof",
  "issuer": "did:uvtp:tel:+33612345678",
  "target": "hash(tel:+33687654321)",
  "iat": 1715241600,
  "nonce": "a7b2c9d1e3f4...",
  "signature": {
    "type": "Ed25519Signature2020",
    "proofValue": "z58D6DbW7..."
  }
}

```

### 3.2 Cryptographic Suite
Signature Algorithm: **Ed25519 (RFC 8032)** for high-speed verification and small signature size.

Hashing: **SHA-256** for salt-hashed target identifiers.

Transport: **TLS 1.3 over QUIC (HTTP/3)** to minimize handshake latency.

## 4. Security Considerations
### 4.1 Anti-Replay Mechanism
Every **Call-Proof** MUST include an **iat** (Issued At) timestamp. Terminals SHOULD reject any proof older than 10 seconds. Nonces MUST be cached for the duration of the TTL to prevent replay attacks within the valid window.

### 4.2 Metadata Privacy
To prevent mass surveillance, the Callee's identifier MUST be hashed or queried using **Private Information Retrieval (PIR)** techniques. The UVTP-Provider SHOULD NOT be able to map a specific Caller to a specific Callee in cleartext.

### 4.3 Out-of-Band Resilience
UVTP is designed to be independent of the audio codec. Even if the voice channel is compromised or simulated, the integrity of the data channel remains intact, provided the Caller's physical device is not compromised.

## 5. Implementation Guidelines
### 5.1 Operating System Integration
OS vendors (e.g., Android, iOS) SHOULD expose a standardized API to allow the native dialer to interact with the UVTP stack.

### 5.2 Trust-Badge Integrity
The Trust-Badge MUST be rendered in a protected UI overlay to prevent "UI Redressing" attacks by malicious third-party applications.

## 6. IANA Considerations
This document currently makes no requests of IANA.

## 7. References
**RFC 8032**: Edwards-Curve Digital Signature Algorithm (EdDSA).

**W3C DID Core**: Decentralized Identifiers (DIDs) v1.0.

**RFC 7515**: JSON Web Signature (JWS).