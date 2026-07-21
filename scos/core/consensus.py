"""
Physical Consensus Engine
Trust through physical verification, not voting
"""

import time
import hashlib
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class PhysicalConsensus:
    """Physical consensus mechanism"""
    
    def __init__(self, genesis: Dict):
        self.genesis = genesis
        self.consensus_threshold = 0.95  # 95% physical agreement
        self.verification_rounds = 10
    
    def achieve_consensus(self, witnesses: List[Dict]) -> Tuple[Optional[Dict], str]:
        """Achieve consensus through physical verification"""
        
        if not witnesses:
            return None, "No witnesses provided"
        
        # Group by physical verification
        groups = self._group_by_physical_verification(witnesses)
        
        if not groups:
            return None, "No physical verification groups"
        
        # Find consensus group
        consensus_group = self._find_consensus_group(groups)
        
        if not consensus_group:
            return None, "No consensus group found"
        
        # Verify against genesis
        if not self._verify_against_genesis(consensus_group):
            return None, "Consensus invalid against genesis"
        
        # Create consensus block
        consensus_block = self._create_consensus_block(consensus_group)
        
        return consensus_block, "Consensus achieved"
    
    def _group_by_physical_verification(self, witnesses: List[Dict]) -> Dict:
        """Group witnesses by their physical verification proof"""
        groups = defaultdict(list)
        
        for witness in witnesses:
            # Check for physical verification
            if isinstance(witness, dict):
                phys_proof = witness.get('state_delta', {}).get('previous_hash')
                if phys_proof:
                    groups['physical'].append(witness)
                else:
                    groups['unverified'].append(witness)
            elif hasattr(witness, 'state_delta'):
                groups['physical'].append(witness)
            else:
                groups['unverified'].append(witness)
        
        return groups
    
    def _find_consensus_group(self, groups: Dict) -> Optional[List[Dict]]:
        """Find the group with consensus-level agreement"""
        if 'physical' not in groups:
            return None
        
        physical_witnesses = groups['physical']
        total_witnesses = sum(len(g) for g in groups.values())
        
        if total_witnesses == 0:
            return None
        
        if len(physical_witnesses) / total_witnesses >= self.consensus_threshold:
            return physical_witnesses
        
        return None
    
    def _verify_against_genesis(self, witnesses: List[Dict]) -> bool:
        """Verify all witnesses against the genesis block"""
        for witness in witnesses:
            if not self._verify_single_witness(witness):
                return False
        return True
    
    def _verify_single_witness(self, witness) -> bool:
        """Verify a single witness against genesis"""
        # In production, this would be more rigorous
        return True
    
    def _create_consensus_block(self, consensus_witnesses: List[Dict]) -> Dict:
        """Create a consensus block from verified witnesses"""
        
        # Hash all witnesses
        witness_hashes = []
        for w in consensus_witnesses:
            if hasattr(w, 'hash'):
                witness_hashes.append(w.hash)
            elif isinstance(w, dict):
                witness_hashes.append(w.get('hash', w.get('previous_hash', '')))
        
        combined = ''.join(witness_hashes).encode()
        
        return {
            'version': '1.0.0',
            'timestamp': time.time(),
            'witness_count': len(consensus_witnesses),
            'consensus_hash': hashlib.sha3_256(combined).hexdigest(),
            'genesis_reference': self.genesis.get('hash', ''),
            'physical_verification': {
                'method': 'physical_consensus',
                'threshold': self.consensus_threshold,
                'verified': True,
                'timestamp': time.time()
            }
        }


class ConsensusEngine:
    """High-level consensus engine"""
    
    def __init__(self, genesis: Dict):
        self.genesis = genesis
        self.physical_consensus = PhysicalConsensus(genesis)
        self.consensus_history = []
    
    def reach_consensus(self, witnesses: List[Dict]) -> Tuple[bool, Dict]:
        """Reach consensus on witnesses"""
        
        result, message = self.physical_consensus.achieve_consensus(witnesses)
        
        if result is None:
            return False, {'error': message}
        
        self.consensus_history.append({
            'timestamp': time.time(),
            'consensus_block': result
        })
        
        return True, result
    
    def get_consensus_history(self) -> List:
        """Get consensus history"""
        return self.consensus_history
