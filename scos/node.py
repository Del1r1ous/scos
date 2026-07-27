"""SCOS Node implementation - The basic unit of the system"""

import os
import platform
from typing import Dict, Any, List
from uuid import uuid4
from scos.utils import compute_fingerprint, compute_hash, timestamp_now, log_audit

class SCOSNode:
    """A node in the SCOS network"""
    
    def __init__(self, node_id: str = None):
        self.node_id = node_id or str(uuid4())
        self.fingerprint = self._compute_fingerprint()
        self.created_at = timestamp_now()
        self.witnessed_claims = []
        self.consensus_votes = {}
        self.metadata = {}
    
    def _compute_fingerprint(self) -> str:
        """Compute hardware fingerprint for this node"""
        hardware_data = {
            'cpu': platform.processor(),
            'system': platform.system(),
            'machine': platform.machine(),
            'node_name': platform.node(),
        }
        return compute_fingerprint(hardware_data)
    
    def witness_claim(self, claim: str, confidence: float = 0.5) -> Dict[str, Any]:
        """Witness and verify a claim"""
        witness_entry = {
            'claim': claim,
            'confidence': confidence,
            'timestamp': timestamp_now(),
            'node_id': self.node_id,
            'fingerprint': self.fingerprint
        }
        
        self.witnessed_claims.append(witness_entry)
        log_audit('witness_claim', witness_entry)
        
        return witness_entry
    
    def vote_on_consensus(self, claim_id: str, vote: float) -> bool:
        """Vote on a consensus claim"""
        if 0.0 <= vote <= 1.0:
            self.consensus_votes[claim_id] = vote
            log_audit('vote_on_consensus', {
                'claim_id': claim_id,
                'vote': vote,
                'node_id': self.node_id
            })
            return True
        return False
    
    def get_node_info(self) -> Dict[str, Any]:
        """Get node information"""
        return {
            'node_id': self.node_id,
            'fingerprint': self.fingerprint,
            'created_at': self.created_at,
            'witnessed_claims': len(self.witnessed_claims),
            'consensus_votes': len(self.consensus_votes),
            'metadata': self.metadata
        }
    
    def __repr__(self):
        return f"SCOSNode(id={self.node_id[:8]}..., fingerprint={self.fingerprint[:8]}...)"
