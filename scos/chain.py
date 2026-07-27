"""SCOS-PSST Chain - The main ledger implementation"""

from typing import List, Dict, Any, Optional
from scos.models import Block, ChainDatabase
from scos.witnesses import WitnessProtocol
from scos.utils import (
    compute_hash, timestamp_now, calculate_consensus,
    calculate_inversion_score, verify_chain_integrity, log_audit
)
from scos.config import (
    CONSENSUS_THRESHOLD, MINIMUM_WITNESSES, MAXIMUM_WITNESSES
)

class SCOSChain:
    """The SCOS-PSST Consensus Chain"""
    
    def __init__(self, chain_id: str = "SCOS-PSST-V3.0"):
        self.chain_id = chain_id
        self.db = ChainDatabase()
        self.witness_protocol = WitnessProtocol()
        self.blocks: List[Block] = []
        self.consensus_threshold = CONSENSUS_THRESHOLD
        self.created_at = timestamp_now()
        self._load_blocks()
    
    def _load_blocks(self):
        """Load blocks from database"""
        self.blocks = self.db.get_all_blocks()
    
    def create_genesis_block(self, claim: str) -> Block:
        """Create the genesis (first) block"""
        genesis_block = Block(
            block_id=0,
            claim=claim,
            witnesses=[1.0] * 7,  # All witnesses agree on genesis
            previous_hash=None,
            data={
                'type': 'genesis',
                'chain_id': self.chain_id,
                'timestamp': timestamp_now()
            }
        )
        
        self.blocks.append(genesis_block)
        self.db.add_block(genesis_block)
        log_audit('create_genesis_block', genesis_block.to_dict())
        
        return genesis_block
    
    def add_claim(self, claim: str, witness_votes: List[float]) -> Optional[Block]:
        """Add a new claim to the chain with witness verification"""
        if len(self.blocks) == 0:
            return self.create_genesis_block(claim)
        
        if len(witness_votes) < MINIMUM_WITNESSES:
            log_audit('add_claim_failed', {
                'claim': claim,
                'reason': f'Insufficient witnesses: {len(witness_votes)} < {MINIMUM_WITNESSES}'
            })
            return None
        
        consensus = calculate_consensus(witness_votes)
        
        if consensus < self.consensus_threshold:
            log_audit('add_claim_failed', {
                'claim': claim,
                'consensus': consensus,
                'threshold': self.consensus_threshold
            })
            return None
        
        # Create new block
        new_block = Block(
            block_id=len(self.blocks),
            claim=claim,
            witnesses=witness_votes,
            previous_hash=self.blocks[-1].hash,
            data={
                'inversion_score': calculate_inversion_score({'consensus': consensus})
            }
        )
        
        self.blocks.append(new_block)
        self.db.add_block(new_block)
        log_audit('add_claim_success', new_block.to_dict())
        
        return new_block
    
    def verify_integrity(self) -> bool:
        """Verify the integrity of the entire chain"""
        return verify_chain_integrity(self.blocks)
    
    def get_block(self, block_id: int) -> Optional[Block]:
        """Retrieve a block by ID"""
        if 0 <= block_id < len(self.blocks):
            return self.blocks[block_id]
        return None
    
    def get_all_blocks(self) -> List[Dict[str, Any]]:
        """Get all blocks as dictionaries"""
        return [block.to_dict() for block in self.blocks]
    
    def get_chain_stats(self) -> Dict[str, Any]:
        """Get statistics about the chain"""
        total_consensus = sum([b.consensus for b in self.blocks])
        avg_consensus = total_consensus / len(self.blocks) if self.blocks else 0.0
        
        return {
            'chain_id': self.chain_id,
            'total_blocks': len(self.blocks),
            'average_consensus': avg_consensus,
            'chain_verified': self.verify_integrity(),
            'created_at': self.created_at,
            'witness_count': len(self.witness_protocol.witnesses),
            'consensus_threshold': self.consensus_threshold
        }
    
    def export_chain(self, filepath: str):
        """Export chain data to JSON file"""
        import json
        data = {
            'chain_id': self.chain_id,
            'created_at': self.created_at,
            'blocks': self.get_all_blocks(),
            'stats': self.get_chain_stats()
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        log_audit('export_chain', {'filepath': filepath})
    
    def import_chain(self, filepath: str):
        """Import chain data from JSON file"""
        import json
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Load blocks
        for block_data in data['blocks']:
            block = Block(
                block_id=block_data['block_id'],
                claim=block_data['claim'],
                witnesses=block_data['witnesses'],
                previous_hash=block_data['previous_hash'],
                data=block_data.get('data', {})
            )
            self.db.add_block(block)
        
        self._load_blocks()
        log_audit('import_chain', {'filepath': filepath})
    
    def __repr__(self):
        return f"SCOSChain(id={self.chain_id}, blocks={len(self.blocks)}, verified={self.verify_integrity()})"
