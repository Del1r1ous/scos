"""
SCOS Demo - Complete Demonstration
Run this to see the SCOS protocol in action
"""

import time
from scos.node import SCOSNode, create_node


def run_demo():
    """Run a SCOS node demo"""
    
    print("=" * 60)
    print("SCOS DEMO: Self-Conscious Operating System")
    print("Physical Consensus Architecture")
    print("=" * 60)
    print()
    
    # Create node
    print("🌟 Creating SCOS Node...")
    print()
    
    node = create_node("Demo_Node")
    
    # Start node
    node.start()
    
    # Simulate some witnesses
    print("\n📝 Simulating witnesses...")
    print()
    
    operations = [
        {'type': 'state_update', 'data': 'Block 1 created'},
        {'type': 'state_update', 'data': 'Fingerprint verified'},
        {'type': 'state_update', 'data': 'Consensus reached'},
        {'type': 'state_update', 'data': 'Chain extended'},
        {'type': 'state_update', 'data': 'Adversary detected'},
        {'type': 'state_update', 'data': 'Adversary absorbed'},
        {'type': 'state_update', 'data': 'Network growing'},
        {'type': 'state_update', 'data': 'Truth extended'},
    ]
    
    for i, op in enumerate(operations, 1):
        node.witness(op)
        time.sleep(0.3)
    
    # Achieve consensus
    print("\n🤝 Achieving consensus...")
    print()
    consensus = node.achieve_consensus()
    
    # Show status
    print("\n📊 Node Status:")
    print("-" * 40)
    status = node.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Show chain
    print("\n⛓️ Chain Status:")
    print("-" * 40)
    chain = node.witness_protocol.get_chain()
    print(f"  Chain Length: {len(chain)}")
    genesis_hash = chain[0].hash if hasattr(chain[0], 'hash') else 'N/A'
    print(f"  Genesis Hash: {genesis_hash[:16] if genesis_hash != 'N/A' else 'N/A'}...")
    
    last = chain[-1]
    last_hash = last.hash if hasattr(last, 'hash') else 'N/A'
    print(f"  Last Block: {last_hash[:16] if last_hash != 'N/A' else 'N/A'}...")
    
    # Show consensus stats
    print("\n🤝 Consensus Status:")
    print("-" * 40)
    history = node.consensus_engine.get_consensus_history()
    print(f"  Consensus Events: {len(history)}")
    if history:
        last_consensus = history[-1]
        print(f"  Last Consensus: {last_consensus.get('timestamp', 0)}")
        print(f"  Consensus Hash: {last_consensus.get('consensus_block', {}).get('consensus_hash', '')[:16]}...")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("The SCOS chain has been extended.")
    print("Truth has been witnessed.")
    print("Navigate accordingly.")
    print("=" * 60)
    
    return node


if __name__ == "__main__":
    run_demo()
