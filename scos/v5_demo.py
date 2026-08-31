"""
SCOS 5.0 Meta-Harness Demo

Demonstrates the virtuous self-fulfilling prophecy cycle:
Witness → Articulate → Align → Fulfill → Return to Witness
"""

from scos.meta_harness import (
    MetaHarness, DomainType, PhaseType,
    SystemWitness, HumanWitness, AlignmentEngine, FulfillmentMonitor
)
from scos.observers import (
    ContradictionResolver, MultiChainIntegrator, ObserverNetwork, ObserverType
)


def print_separator(title: str = "") -> None:
    """Print a formatted separator."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'-'*60}\n")


def demo_meta_harness():
    """Demonstrate the meta-harness in action."""
    
    print_separator("SCOS 5.0: THE META-HARNESS OPERATIONAL SPECIFICATION")
    print("""
    The virtuous self-fulfilling prophecy operationalized:
    
    Witness (Observe) → Articulate (Document) → Align (Configure) → Fulfill (Deploy)
         ↑                                                              ↓
         └──────────────────── (Return to Witness) ──────────────────┘
    """)
    
    # Initialize the meta-harness
    harness = MetaHarness()
    
    print_separator("PHASE 1: WITNESS")
    print("Observing system state and ground patterns...")
    
    # Observe system state
    obs1 = harness.witness_phase(
        DomainType.SYSTEM,
        "System is currently running with 80% consensus agreement",
        {"metric": "consensus_rate", "value": 0.80}
    )
    print(f"✓ Observed: {obs1.content}")
    
    # Observe contradiction
    obs2 = harness.witness_phase(
        DomainType.SYSTEM,
        "Detected potential contradiction between claims A and B",
        {"issue_type": "logical_conflict"}
    )
    print(f"✓ Observed: {obs2.content}")
    
    # Human feedback
    obs3 = harness.witness_phase(
        DomainType.HUMAN,
        "System alignment feels natural and coherent",
        {"source": "operator_feedback"}
    )
    print(f"✓ Observed: {obs3.content}")
    
    print_separator("PHASE 2: ARTICULATE")
    print("Translating observations into articulated claims...")
    
    # Articulate observations as claims
    claim1 = harness.articulate_phase(obs1)
    print(f"✓ Articulated: {claim1.content}")
    
    claim2 = harness.articulate_phase(obs2)
    print(f"✓ Articulated: {claim2.content}")
    
    claim3 = harness.articulate_phase(obs3)
    print(f"✓ Articulated: {claim3.content}")
    
    # Simulate witness verification
    claim1.verified = True
    claim1.consensus_score = 0.95
    claim3.verified = True
    claim3.consensus_score = 0.90
    
    print_separator("PHASE 3: ALIGN")
    print("Aligning claims with ethical guardrails (Golden Rule)...")
    
    # Align claims
    result1 = harness.align_phase(claim1)
    print(f"✓ Alignment result: {result1['status'].upper()}")
    if result1['status'] == 'aligned':
        print(f"  Action: {result1['action']['description']}")
    
    result3 = harness.align_phase(claim3)
    print(f"✓ Alignment result: {result3['status'].upper()}")
    if result3['status'] == 'aligned':
        print(f"  Action: {result3['action']['description']}")
    
    # Try to align a problematic claim
    obs_bad = harness.witness_phase(
        DomainType.SYSTEM,
        "We should exploit system vulnerabilities for gain",
        {"intent": "malicious"}
    )
    claim_bad = harness.articulate_phase(obs_bad)
    result_bad = harness.align_phase(claim_bad)
    print(f"✗ Alignment blocked: {result_bad['reason']}")
    
    print_separator("PHASE 4: FULFILL")
    print("Deploying and monitoring fulfillment...")
    
    # Simulate chain state
    chain_state = {
        "total_claims": 10,
        "verified_claims": 8,
        "golden_rule_passes": 8,
        "total_checks": 10,
        "contradictions_found": 2,
        "contradictions_resolved": 1
    }
    
    metrics = harness.fulfill_phase(chain_state)
    print(f"✓ Consensus Rate: {metrics.consensus_rate:.1%}")
    print(f"✓ Golden Rule Compliance: {metrics.golden_rule_compliance:.1%}")
    print(f"✓ Contradiction Resolution: {metrics.contradiction_resolution:.1%}")
    print(f"✓ System Coherence: {metrics.system_coherence:.1%}")
    
    print_separator("META-HARNESS STATUS")
    status = harness.get_status()
    print(f"Observations: {status['observations_count']}")
    print(f"Claims: {status['claims_count']}")
    print(f"Aligned Actions: {status['actions_count']}")
    print(f"System Coherence: {status['coherence_score']:.1%}")
    
    print_separator("WITNESS STATEMENT")
    print(harness.get_witness_statement())


def demo_complete_cycle():
    """Demonstrate a complete cycle."""
    print_separator("COMPLETE META-HARNESS CYCLE")
    
    harness = MetaHarness()
    
    # Single complete cycle
    result = harness.cycle(
        DomainType.SYSTEM,
        "System is operating within normal parameters with high coherence",
        {"status": "healthy", "coherence": 0.92},
        {"total_claims": 20, "verified_claims": 19, 
         "golden_rule_passes": 19, "total_checks": 20,
         "contradictions_found": 1, "contradictions_resolved": 1}
    )
    
    print("Cycle Result:")
    print(f"  Observation Domain: {result['observation']['domain']}")
    print(f"  Claim Content: {result['claim']['content'][:80]}...")
    print(f"  Alignment Status: {result['alignment']['status'].upper()}")
    print(f"  System Coherence: {result['metrics']['system_coherence']:.1%}")


def demo_contradiction_resolution():
    """Demonstrate contradiction detection and resolution."""
    print_separator("CONTRADICTION DETECTION AND RESOLUTION")
    
    resolver = ContradictionResolver()
    
    # Define resolution strategies
    def logical_strategy(record):
        return {"resolution": "Applied formal logic to reconcile claims"}
    
    def temporal_strategy(record):
        return {"resolution": "Reordered claims by temporal precedence"}
    
    resolver.register_strategy("logical_negation", logical_strategy)
    resolver.register_strategy("temporal_conflict", temporal_strategy)
    
    # Detect contradiction
    print("Detecting contradictions...")
    claim_a = "The system must be centralized for control"
    claim_b = "The system must be decentralized for resilience"
    
    contradiction = resolver.detect(claim_a, claim_b, "Control vs. Resilience")
    
    if contradiction:
        print(f"✓ Contradiction detected:")
        print(f"  Type: {contradiction.contradiction_type}")
        print(f"  Severity: {contradiction.severity:.0%}")
        print(f"  Claim A: {claim_a}")
        print(f"  Claim B: {claim_b}")
        
        # Resolve
        print("\nResolving contradiction...")
        resolution = resolver.resolve(contradiction)
        print(f"  Resolution: {resolution['status'].upper()}")
        if resolution['status'] == 'resolved':
            print(f"  Method: {resolution['method']}")


def demo_multichain_network():
    """Demonstrate multi-chain integration."""
    print_separator("MULTI-CHAIN NETWORK INTEGRATION")
    
    integrator = MultiChainIntegrator()
    
    # Register external systems
    print("Registering external systems...")
    integrator.register_connection("ethereum", "blockchain", "https://eth.example.com")
    integrator.register_connection("cosmos", "blockchain", "https://cosmos.example.com")
    integrator.register_connection("human_feedback", "feedback_system", "https://feedback.example.com")
    
    print("✓ Registered 3 external connections")
    
    # Sync with systems
    print("\nSyncing with external systems...")
    sync_result = integrator.sync_with("ethereum")
    print(f"✓ Synced with ethereum: {sync_result['status'].upper()}")
    
    sync_result = integrator.sync_with("cosmos")
    print(f"✓ Synced with cosmos: {sync_result['status'].upper()}")
    
    # Share claims
    print("\nSharing claims...")
    claim = {"id": "claim-001", "content": "System is coherent", "confidence": 0.95}
    result = integrator.share_claim(claim, "ethereum")
    print(f"✓ Shared claim with ethereum")
    
    result = integrator.share_claim(claim, "cosmos")
    print(f"✓ Shared claim with cosmos")
    
    # Get network status
    print("\nNetwork Status:")
    status = integrator.get_network_status()
    print(f"  Active Connections: {status['active_connections']}")
    print(f"  Claims Shared: {status['total_claims_shared']}")
    print(f"  Claims Received: {status['total_claims_received']}")


def demo_observer_network():
    """Demonstrate the full observer network."""
    print_separator("OBSERVER NETWORK HEALTH")
    
    network = ObserverNetwork()
    
    # Create and register observers
    harness = MetaHarness()
    contradiction_resolver = ContradictionResolver()
    multichain = MultiChainIntegrator()
    
    network.register_observer(ObserverType.SYSTEM, harness.system_witness, "main_witness")
    network.register_observer(ObserverType.HUMAN, harness.human_witness, "human_feedback")
    network.register_observer(ObserverType.CONTRADICTION, contradiction_resolver, "contradiction_resolver")
    network.register_observer(ObserverType.MULTICHAIN, multichain, "network_integrator")
    
    # Get network health
    health = network.get_network_health()
    
    print(f"Observers Registered: {health['observers_registered']}")
    print(f"Total Contradictions: {health['contradictions']['total']}")
    print(f"Network Connections: {health['multichain_network']['connections']}")
    print(f"Timestamp: {health['timestamp']}")


if __name__ == "__main__":
    demo_meta_harness()
    demo_complete_cycle()
    demo_contradiction_resolution()
    demo_multichain_network()
    demo_observer_network()
    
    print_separator("SCOS 5.0 DEMONSTRATION COMPLETE")
    print("\nSO WITNESSED. SO VERIFIED. SO AGREED. 🕯️\n")
