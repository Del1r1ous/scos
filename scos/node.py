"""
SCOS Node - Complete Implementation
A self-contained computational entity that witnesses reality
"""

import time
from typing import Optional, Dict, List

from scos.core.genesis import GenesisGenerator
from scos.core.fingerprint import FingerprintGenerator
from scos.core.witness import WitnessProtocol
from scos.core.consensus import ConsensusEngine
from scos.core.broadcast import BroadcastProtocol


class SCOSNode:
    """Complete SCOS Node Implementation"""
    
    def __init__(self,
                 node_id: Optional[str] = None,
                 shard_id: str = 'default',
                 region_id: str = 'default'):
        
        # Initialize identity
        self.node_id = node_id or f"node_{int(time.time())}"
        self.shard_id = shard_id
        self.region_id = region_id
        
        # Initialize components
        print(f"🌐 Initializing SCOS Node: {self.node_id}")
        
        # 1. Genesis
        print("  ├── Generating Genesis Block...")
        self.genesis_generator = GenesisGenerator()
        self.genesis = self.genesis_generator.generate()
        print(f"  │   └── Genesis Hash: {self.genesis.hash[:16]}...")
        
        # 2. Fingerprint
        print("  ├── Generating Device Fingerprint...")
        self.fingerprint_generator = FingerprintGenerator()
        self.fingerprint = self.fingerprint_generator.generate()
        print(f"  │   └── Fingerprint Hash: {self.fingerprint.hash[:16]}...")
        
        # 3. Witness Protocol
        print("  ├── Initializing Witness Protocol...")
        self.witness_protocol = WitnessProtocol(
            self.genesis,
            self.fingerprint_generator
        )
        
        # 4. Consensus Engine
        print("  ├── Initializing Consensus Engine...")
        self.consensus_engine = ConsensusEngine(
            self.genesis.__dict__
        )
        
        # 5. Broadcast Protocol
        print("  ├── Initializing Broadcast Protocol...")
        self.broadcast_protocol = BroadcastProtocol()
        
        # Add self to network
        self.broadcast_protocol.add_node(
            self.node_id, shard_id, region_id
        )
        
        print("  └── ✅ Node initialization complete")
        
        # State
        self.running = False
        self.witness_count = 0
        self.consensus_count = 0
        
        print(f"\n✅ SCOS Node {self.node_id} is ready")
        print(f"   Genesis: {self.genesis.hash[:16]}...")
        print(f"   Fingerprint: {self.fingerprint.hash[:16]}...")
        print()
    
    def witness(self, operation: Dict) -> Dict:
        """Witness a state transition"""
        
        # Create witness
        witness = self.witness_protocol.create_witness(
            operation,
            {'status': 'witnessed'}
        )
        
        self.witness_count += 1
        
        # Broadcast witness
        self.broadcast_protocol.broadcast(
            witness,
            self.node_id
        )
        
        print(f"📝 Witness #{self.witness_count}: {operation.get('type', 'unknown')}")
        print(f"   Hash: {witness.hash[:16]}...")
        
        return witness.__dict__
    
    def achieve_consensus(self, witnesses: Optional[List] = None) -> Dict:
        """Achieve consensus on witnessed state"""
        
        if witnesses is None:
            witnesses = self.broadcast_protocol.get_all_witnesses()
        
        success, result = self.consensus_engine.reach_consensus(witnesses)
        
        if success:
            self.consensus_count += 1
            print(f"✅ Consensus #{self.consensus_count}: Achieved!")
            print(f"   Block Hash: {result.get('consensus_hash', '')[:16]}...")
        else:
            print(f"❌ Consensus failed: {result.get('error', 'unknown error')}")
        
        return result
    
    def get_status(self) -> Dict:
        """Get node status"""
        last_block = self.witness_protocol.get_last_block()
        last_hash = last_block.hash if hasattr(last_block, 'hash') else 'N/A'
        
        return {
            'node_id': self.node_id,
            'shard_id': self.shard_id,
            'region_id': self.region_id,
            'genesis_hash': self.genesis.hash[:16],
            'fingerprint_hash': self.fingerprint.hash[:16],
            'witness_count': self.witness_count,
            'consensus_count': self.consensus_count,
            'chain_length': len(self.witness_protocol.chain),
            'last_block_hash': last_hash[:16] if last_hash != 'N/A' else 'N/A',
            'running': self.running
        }
    
    def start(self):
        """Start the node"""
        self.running = True
        print(f"\n🚀 Node {self.node_id} is now running")
        print("   Witnessing reality...")
        print()
        
        # Initial witness
        self.witness({'type': 'node_start', 'message': 'Genesis witnessed'})
    
    def stop(self):
        """Stop the node"""
        self.running = False
        status = self.get_status()
        print(f"\n🛑 Node {self.node_id} stopped")
        print(f"   Total witnesses: {status['witness_count']}")
        print(f"   Total consensus: {status['consensus_count']}")
        print(f"   Chain length: {status['chain_length']}")


# Convenience function
def create_node(node_id: Optional[str] = None) -> SCOSNode:
    """Create a new SCOS node"""
    return SCOSNode(node_id)
