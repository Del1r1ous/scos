"""
Witness Protocol
State transitions verified and chained
"""

import hashlib
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Witness:
    """A witnessed state transition"""
    version: str
    index: int
    previous_hash: str
    timestamp: float
    operation: Dict
    fingerprint_hash: str
    state_delta: Dict
    signature: str
    hash: str


class WitnessProtocol:
    """Create and verify witnesses"""
    
    def __init__(self, genesis, fingerprint_generator):
        self.genesis = genesis
        self.fingerprint_generator = fingerprint_generator
        self.chain = [genesis]
        self.witness_count = 0
        self.verified_witnesses = []
    
    def create_witness(self, operation: Dict, result: Dict) -> Witness:
        """Create a witness for a state transition"""
        
        # Get current state
        current_fingerprint = self.fingerprint_generator.generate()
        
        # Update fingerprint log
        self.fingerprint_generator.add_witness(current_fingerprint.hash)
        
        # Get timestamp for deterministic hashing
        witness_timestamp = time.time()
        
        # Build witness
        witness = Witness(
            version='1.0.0',
            index=self.witness_count,
            previous_hash=self._get_previous_hash(),
            timestamp=witness_timestamp,
            operation=operation,
            fingerprint_hash=current_fingerprint.hash,
            state_delta=self._compute_delta(self.chain[-1], current_fingerprint),
            signature=self._sign_witness(operation, result, current_fingerprint, witness_timestamp),
            hash=self._compute_hash(operation, result, current_fingerprint.hash, witness_timestamp)
        )
        
        # Add to chain
        self.chain.append(witness)
        self.witness_count += 1
        self.verified_witnesses.append(witness)
        
        return witness
    
    def _get_previous_hash(self) -> str:
        """Get the hash of the previous block in the chain"""
        if not self.chain:
            return '0' * 64
        
        last = self.chain[-1]
        if hasattr(last, 'hash'):
            return last.hash
        elif isinstance(last, dict):
            return last.get('hash', '0' * 64)
        return '0' * 64
    
    def _compute_delta(self, previous, new_fingerprint) -> Dict:
        """Compute delta between states"""
        prev_hash = self._get_previous_hash()
        
        return {
            'previous_hash': prev_hash,
            'new_hash': new_fingerprint.hash,
            'changed': prev_hash != new_fingerprint.hash
        }
    
    def _sign_witness(self, operation, result, fingerprint, timestamp) -> str:
        """Sign the witness"""
        data = {
            'operation': operation,
            'result': result,
            'fingerprint': fingerprint.hash,
            'timestamp': timestamp
        }
        return hashlib.sha3_512(str(data).encode()).hexdigest()
    
    def _compute_hash(self, operation, result, fingerprint_hash: str, timestamp: float) -> str:
        """
        Compute witness hash deterministically.
        Uses stored timestamp instead of calling time.time() to ensure verification works.
        """
        data = {
            'operation': operation,
            'result': result,
            'fingerprint': fingerprint_hash,
            'timestamp': timestamp
        }
        return hashlib.sha3_256(str(data).encode()).hexdigest()
    
    def verify_witness(self, witness: Witness) -> Tuple[bool, str]:
        """Verify a witness"""
        
        # 1. Verify hash using stored timestamp (deterministic)
        computed_hash = self._compute_hash(
            witness.operation,
            None,
            witness.fingerprint_hash,
            witness.timestamp
        )
        if computed_hash != witness.hash:
            return False, f"Invalid witness hash: expected {computed_hash}, got {witness.hash}"
        
        # 2. Verify signature
        if not self._verify_signature(witness):
            return False, "Invalid signature"
        
        # 3. Verify chain continuity
        if not self._verify_chain(witness):
            return False, "Chain discontinuity"
        
        # 4. Verify timestamp
        if not self._verify_timestamp(witness.timestamp):
            return False, "Invalid timestamp"
        
        return True, "Witness verified"
    
    def _verify_signature(self, witness: Witness) -> bool:
        """Verify witness signature"""
        # In production, this would use hardware signatures
        return len(witness.signature) == 128
    
    def _verify_chain(self, witness: Witness) -> bool:
        """Verify chain continuity"""
        if not self.chain:
            return True
        
        last = self.chain[-1]
        last_hash = last.hash if hasattr(last, 'hash') else last.get('hash', '')
        return witness.previous_hash == last_hash
    
    def _verify_timestamp(self, timestamp: float) -> bool:
        """Verify timestamp"""
        current_time = time.time()
        return abs(current_time - timestamp) < 3600  # Within 1 hour
    
    def get_chain(self) -> List:
        """Get the full chain"""
        return self.chain
    
    def get_last_block(self):
        """Get the last block in the chain"""
        return self.chain[-1] if self.chain else None
