import json
import time
import secrets
import hashlib
import nacl.encoding
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

def generate_target_hash(phone_number):
    """
    Simulates hashing the callee's phone number to ensure metadata privacy.
    In a real-world scenario, a salted hash or PIR should be used.
    """
    return hashlib.sha256(phone_number.encode()).hexdigest()

def create_call_proof(caller_did, target_phone, signing_key):
    """
    Generates a signed UVTP payload.
    Compliant with UVTP RFC Section 3.1.
    """
    # 1. Prepare data components
    target_hash = generate_target_hash(target_phone)
    iat = int(time.time())  # Issued At (Unix timestamp)
    nonce = secrets.token_hex(16)  # High-entropy nonce to prevent replay
    
    # 2. Build the JSON-LD structure
    payload = {
        "@context": "https://w3id.org/uvtp/v1",
        "type": "CallProof",
        "issuer": caller_did,
        "target": f"hash({target_hash})",
        "iat": iat,
        "nonce": nonce
    }
    
    # 3. Deterministic serialization (sorted keys) for signature consistency
    payload_json = json.dumps(payload, sort_keys=True)
    
    # 4. Sign with Private Key (Ed25519)
    # In production, this operation happens inside the Secure Enclave / TEE
    signed_packet = signing_key.sign(payload_json.encode())
    
    # Append the signature block to the final dictionary
    payload["signature"] = {
        "type": "Ed25519Signature2020",
        "proofValue": signed_packet.signature.hex()
    }
    
    return payload, payload_json

def verify_call_proof(proof_packet, public_key_hex):
    """
    Validates the integrity, authenticity, and freshness of a UVTP proof.
    """
    # Extract the signature
    sig_hex = proof_packet["signature"]["proofValue"]
    
    # Reconstruct the original message by removing the signature block
    original_data = proof_packet.copy()
    del original_data["signature"]
    
    # Ensure same serialization as the signer
    message_to_verify = json.dumps(original_data, sort_keys=True).encode()
    
    # Load the public key
    verify_key = VerifyKey(public_key_hex, encoder=nacl.encoding.HexEncoder)
    
    try:
        # Cryptographic verification
        verify_key.verify(message_to_verify, bytes.fromhex(sig_hex))
        
        # Freshness Check: Verify 'iat' is within the 10-second window
        current_time = int(time.time())
        if current_time - original_data["iat"] > 10:
            return False, "ERROR: Proof expired (Potential Replay Attack)"
            
        return True, "SUCCESS: Identity cryptographically certified"
    
    except BadSignatureError:
        return False, "ERROR: Invalid signature (Potential Deepfake/Spoofing)"

# --- SIMULATION WORKFLOW ---
if __name__ == "__main__":
    print("--- Initializing Hardware-Bound Keys (Simulated TEE) ---")
    # Generate a signing key (Private) and its corresponding verify key (Public)
    sk = SigningKey.generate()
    vk = sk.verify_key
    public_key_hex = vk.encode(encoder=nacl.encoding.HexEncoder)
    
    print(f"Caller Identifier (Public Key): {public_key_hex.decode()}\n")

    # STEP 1: Caller generates the proof at the start of the call
    caller_id = "did:uvtp:tel:+33612345678"
    target_phone = "+33687654321"
    print(f"Initiating call to {target_phone}...")
    
    proof, _ = create_call_proof(caller_id, target_phone, sk)
    print("Generated UVTP Call-Proof:")
    print(json.dumps(proof, indent=2))
    print("\n" + "-"*60 + "\n")

    # STEP 2: Callee receives the call and verifies the proof via side-channel
    print("Incoming call signal received... Querying UVTP Proof...")
    
    # Simulation: Callee retrieves the proof and the Caller's public key
    is_valid, message = verify_call_proof(proof, public_key_hex)
    
    if is_valid:
        print(f"✅ {message}")
        print("Action: Displaying 'TRUST-BADGE' on incoming call UI.")
    else:
        print(f"❌ {message}")
        print("Action: Warning user of UNVERIFIED/SUSPECTED identity.")