"""
Hierarchical Broadcast Protocol
Efficient witness distribution
"""

import time
import random
import hashlib
from typing import List, Dict, Set, Optional
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class NetworkNode:
    """Representation of a network node"""
    node_id: str
    shard_id: str
    region_id: str
    peers: List[str]
    role: str  # 'leaf', 'regional', 'global'


class GossipProtocol:
    """Gossip protocol for efficient broadcast"""
    
    def __init__(self, node_id: str, shard_id: str, region_id: str):
        self.node_id = node_id
        self.shard_id = shard_id
        self.region_id = region_id
        self.peers = []
        self.gossip_table = {}
        self.last_gossip = time.time()
        self.gossip_interval = 5  # seconds
        self.local_witnesses = []
        self.regional_summaries = {}
        self.role = 'leaf'
    
    def add_peer(self, peer_id: str):
        """Add a peer to gossip with"""
        if peer_id not in self.peers and peer_id != self.node_id:
            self.peers.append(peer_id)
    
    def broadcast_witness(self, witness):
        """Broadcast a witness to the network"""
        
        # Convert to dict if needed
        if hasattr(witness, '__dict__'):
            witness_dict = witness.__dict__
        else:
            witness_dict = witness
        
        # Add to local store
        self.local_witnesses.append(witness_dict)
        
        # If we're a regional node, aggregate
        if self.role == 'regional':
            self._aggregate_witnesses()
        
        # If we're a global node, broadcast
        if self.role == 'global':
            self._broadcast_global()
    
    def _aggregate_witnesses(self):
        """Aggregate witnesses into summaries"""
        # Group by device
        device_witnesses = defaultdict(list)
        for w in self.local_witnesses[-1000:]:
            device_id = w.get('fingerprint_hash', 'unknown')
            device_witnesses[device_id].append(w)
        
        # Create summaries
        for device, witnesses in device_witnesses.items():
            summary = {
                'device': device,
                'witness_count': len(witnesses),
                'first_seen': min(w.get('timestamp', 0) for w in witnesses),
                'last_seen': max(w.get('timestamp', 0) for w in witnesses),
                'merkle_root': self._build_merkle_tree(witnesses)
            }
            self.regional_summaries[device] = summary
    
    def _build_merkle_tree(self, witnesses: List[Dict]) -> str:
        """Build a Merkle tree of witnesses"""
        if not witnesses:
            return ''
        
        # Sort witnesses
        sorted_witnesses = sorted(
            witnesses, 
            key=lambda w: w.get('timestamp', 0)
        )
        
        # Build tree (simplified)
        leaves = [w.get('hash', '').encode() for w in sorted_witnesses]
        
        if not leaves:
            return ''
        
        while len(leaves) > 1:
            new_level = []
            for i in range(0, len(leaves), 2):
                if i + 1 < len(leaves):
                    combined = leaves[i] + leaves[i+1]
                else:
                    combined = leaves[i]
                new_level.append(hashlib.sha3_256(combined).digest())
            leaves = new_level
        
        return leaves[0].hex() if leaves else ''
    
    def _broadcast_global(self):
        """Broadcast global summaries"""
        # In production, this would actually broadcast
        pass
    
    def run_gossip_cycle(self):
        """Run one gossip cycle"""
        current_time = time.time()
        
        if current_time - self.last_gossip < self.gossip_interval:
            return
        
        if not self.peers:
            return
        
        # Select random peer
        target = random.choice(self.peers)
        
        # Simulate gossip exchange
        self._process_update({
            'node_id': target,
            'timestamp': current_time,
            'witnesses': self.local_witnesses[-10:],
            'summaries': self.regional_summaries
        })
        
        self.last_gossip = current_time
    
    def _process_update(self, update: Dict):
        """Process a gossip update"""
        # Add new witnesses
        for witness in update.get('witnesses', []):
            if witness not in self.local_witnesses:
                self.local_witnesses.append(witness)
        
        # Add new summaries
        for device, summary in update.get('summaries', {}).items():
            if device not in self.regional_summaries:
                self.regional_summaries[device] = summary


class BroadcastProtocol:
    """Hierarchical broadcast protocol"""
    
    def __init__(self):
        self.nodes = {}
        self.shards = defaultdict(list)
        self.regions = defaultdict(list)
        self.gossip_instances = {}
    
    def add_node(self, node_id: str, shard_id: str, region_id: str):
        """Add a node to the network"""
        node = NetworkNode(
            node_id=node_id,
            shard_id=shard_id,
            region_id=region_id,
            peers=[],
            role='leaf'
        )
        self.nodes[node_id] = node
        self.shards[shard_id].append(node_id)
        self.regions[region_id].append(node_id)
        
        # Create gossip instance
        self.gossip_instances[node_id] = GossipProtocol(
            node_id, shard_id, region_id
        )
    
    def connect_nodes(self):
        """Connect nodes into a peer-to-peer network"""
        # Connect within shards
        for shard_id, node_ids in self.shards.items():
            for i, node_id in enumerate(node_ids):
                for j in range(i + 1, len(node_ids)):
                    peer_id = node_ids[j]
                    self.gossip_instances[node_id].add_peer(peer_id)
                    self.gossip_instances[peer_id].add_peer(node_id)
    
    def broadcast(self, witness, sender_id: str):
        """Broadcast a witness through the network"""
        if sender_id not in self.gossip_instances:
            return
        
        # Broadcast through gossip
        self.gossip_instances[sender_id].broadcast_witness(witness)
        
        # Simulate propagation
        for node_id, gossip in self.gossip_instances.items():
            if node_id != sender_id:
                gossip.run_gossip_cycle()
    
    def get_all_witnesses(self) -> List[Dict]:
        """Get all witnessed transactions"""
        all_witnesses = []
        for gossip in self.gossip_instances.values():
            all_witnesses.extend(gossip.local_witnesses)
        return all_witnesses
    
    def get_network_size(self) -> int:
        """Get total nodes in network"""
        return len(self.nodes)
