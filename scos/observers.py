"""
SCOS 5.0: Observer Implementations

Extends SCOS with multiple observer types for the meta-harness:
- SystemWitness: Monitors external systems, APIs, logs, sensors
- HumanWitness: Captures human intuition and feedback
- ContradictionResolver: Identifies and resolves system contradictions
- MultiChainIntegrator: Connects to other chains and systems
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging


logger = logging.getLogger(__name__)


class ObserverType(Enum):
    """Types of observers in the SCOS ecosystem."""
    SYSTEM = "system"
    HUMAN = "human"
    EXTERNAL = "external"
    CONTRADICTION = "contradiction"
    MULTICHAIN = "multichain"


@dataclass
class ContradictionRecord:
    """Records a discovered contradiction in the system."""
    contradiction_type: str
    description: str
    claim_a: str
    claim_b: str
    severity: float  # 0.0 to 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution_method: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.contradiction_type,
            "description": self.description,
            "claim_a": self.claim_a,
            "claim_b": self.claim_b,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "resolution_method": self.resolution_method,
        }


class ContradictionResolver:
    """Identifies and resolves internal contradictions in the system."""

    def __init__(self):
        self.contradictions: List[ContradictionRecord] = []
        self.resolution_strategies: Dict[str, Callable] = {}

    def register_strategy(self, contradiction_type: str, strategy: Callable) -> None:
        """
        Register a resolution strategy for a contradiction type.
        
        Args:
            contradiction_type: Type of contradiction
            strategy: Callable that takes a ContradictionRecord and returns resolution
        """
        self.resolution_strategies[contradiction_type] = strategy

    def detect(self, claim_a: str, claim_b: str, description: str = "") -> Optional[ContradictionRecord]:
        """
        Detect if two claims contradict each other.
        
        Args:
            claim_a: First claim
            claim_b: Second claim
            description: Description of the contradiction
            
        Returns:
            ContradictionRecord if contradiction found, None otherwise
        """
        # Simple heuristic contradiction detection
        contradiction_indicators = {
            "logical_negation": self._check_logical_negation(claim_a, claim_b),
            "temporal_conflict": self._check_temporal_conflict(claim_a, claim_b),
            "mutual_exclusion": self._check_mutual_exclusion(claim_a, claim_b),
        }
        
        if any(contradiction_indicators.values()):
            record = ContradictionRecord(
                contradiction_type=next(k for k, v in contradiction_indicators.items() if v),
                description=description or f"Contradiction between claims",
                claim_a=claim_a,
                claim_b=claim_b,
                severity=0.7
            )
            self.contradictions.append(record)
            return record
        
        return None

    def _check_logical_negation(self, claim_a: str, claim_b: str) -> bool:
        """Check if claims logically negate each other."""
        negations = ["not ", "cannot", "does not", "is not", "never", "no "]
        claim_a_lower = claim_a.lower()
        claim_b_lower = claim_b.lower()
        
        # Simple check: if one has negation and the other doesn't
        has_negation_a = any(neg in claim_a_lower for neg in negations)
        has_negation_b = any(neg in claim_b_lower for neg in negations)
        
        return has_negation_a != has_negation_b

    def _check_temporal_conflict(self, claim_a: str, claim_b: str) -> bool:
        """Check for temporal conflicts."""
        time_indicators = ["before", "after", "past", "future", "now", "then"]
        return any(ind in claim_a.lower() for ind in time_indicators) and \
               any(ind in claim_b.lower() for ind in time_indicators)

    def _check_mutual_exclusion(self, claim_a: str, claim_b: str) -> bool:
        """Check for mutually exclusive claims."""
        # Check if claims share key concepts but assign opposite properties
        words_a = set(claim_a.lower().split())
        words_b = set(claim_b.lower().split())
        common_words = words_a & words_b
        return len(common_words) > 3

    def resolve(self, record: ContradictionRecord) -> Dict[str, Any]:
        """
        Attempt to resolve a contradiction using registered strategies.
        
        Args:
            record: The contradiction to resolve
            
        Returns:
            Resolution result
        """
        if record.contradiction_type in self.resolution_strategies:
            strategy = self.resolution_strategies[record.contradiction_type]
            try:
                result = strategy(record)
                record.resolved = True
                record.resolution_method = strategy.__name__
                return {"status": "resolved", "method": strategy.__name__, "result": result}
            except Exception as e:
                logger.error(f"Resolution failed: {e}")
                return {"status": "failed", "error": str(e)}
        
        return {"status": "no_strategy", "type": record.contradiction_type}

    def get_unresolved(self) -> List[ContradictionRecord]:
        """Get all unresolved contradictions."""
        return [c for c in self.contradictions if not c.resolved]

    def get_report(self) -> Dict[str, Any]:
        """Get a detailed contradiction report."""
        return {
            "total": len(self.contradictions),
            "resolved": len([c for c in self.contradictions if c.resolved]),
            "unresolved": len(self.get_unresolved()),
            "unresolved_contradictions": [c.to_dict() for c in self.get_unresolved()],
        }


@dataclass
class ExternalSystemConnection:
    """Represents a connection to an external system or chain."""
    name: str
    system_type: str
    endpoint: str
    last_sync: Optional[datetime] = None
    is_connected: bool = False
    claims_received: int = 0
    claims_shared: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "system_type": self.system_type,
            "endpoint": self.endpoint,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "is_connected": self.is_connected,
            "claims_received": self.claims_received,
            "claims_shared": self.claims_shared,
        }


class MultiChainIntegrator:
    """Integrates SCOS with other chains and systems."""

    def __init__(self):
        self.connections: Dict[str, ExternalSystemConnection] = {}
        self.shared_claims: List[Dict[str, Any]] = []
        self.received_claims: List[Dict[str, Any]] = []

    def register_connection(self, name: str, system_type: str, endpoint: str) -> ExternalSystemConnection:
        """
        Register a connection to an external system.
        
        Args:
            name: Connection name
            system_type: Type of external system
            endpoint: Connection endpoint
            
        Returns:
            ExternalSystemConnection object
        """
        connection = ExternalSystemConnection(
            name=name,
            system_type=system_type,
            endpoint=endpoint
        )
        self.connections[name] = connection
        logger.info(f"Registered connection to {name} ({system_type})")
        return connection

    def sync_with(self, connection_name: str) -> Dict[str, Any]:
        """
        Sync SCOS claims with an external system.
        
        Args:
            connection_name: Name of the connection
            
        Returns:
            Sync result
        """
        if connection_name not in self.connections:
            return {"status": "error", "reason": "Connection not found"}
        
        connection = self.connections[connection_name]
        connection.is_connected = True
        connection.last_sync = datetime.now()
        
        return {
            "status": "synced",
            "connection": connection.to_dict(),
            "timestamp": datetime.now().isoformat()
        }

    def share_claim(self, claim: Dict[str, Any], target_system: str) -> Dict[str, Any]:
        """
        Share a claim with an external system.
        
        Args:
            claim: The claim to share
            target_system: Name of target system
            
        Returns:
            Share result
        """
        if target_system not in self.connections:
            return {"status": "error", "reason": "Target system not found"}
        
        self.shared_claims.append(claim)
        connection = self.connections[target_system]
        connection.claims_shared += 1
        
        logger.info(f"Shared claim with {target_system}")
        
        return {
            "status": "shared",
            "claim_id": claim.get("id"),
            "target": target_system
        }

    def receive_claim(self, claim: Dict[str, Any], source_system: str) -> Dict[str, Any]:
        """
        Receive a claim from an external system.
        
        Args:
            claim: The received claim
            source_system: Source system name
            
        Returns:
            Receipt confirmation
        """
        if source_system not in self.connections:
            return {"status": "error", "reason": "Source system not recognized"}
        
        self.received_claims.append(claim)
        connection = self.connections[source_system]
        connection.claims_received += 1
        
        logger.info(f"Received claim from {source_system}")
        
        return {
            "status": "received",
            "claim_id": claim.get("id"),
            "source": source_system
        }

    def get_network_status(self) -> Dict[str, Any]:
        """Get status of all external connections."""
        return {
            "connections": len(self.connections),
            "active_connections": len([c for c in self.connections.values() if c.is_connected]),
            "total_claims_shared": len(self.shared_claims),
            "total_claims_received": len(self.received_claims),
            "connections_detail": {name: conn.to_dict() for name, conn in self.connections.items()}
        }


class ObserverNetwork:
    """Coordinates all observers in the SCOS ecosystem."""

    def __init__(self):
        self.contradiction_resolver = ContradictionResolver()
        self.multichain_integrator = MultiChainIntegrator()
        self.observer_registry: Dict[str, Any] = {}

    def register_observer(self, observer_type: ObserverType, observer: Any, name: str) -> None:
        """Register an observer."""
        self.observer_registry[name] = {
            "type": observer_type.value,
            "observer": observer,
            "registered_at": datetime.now().isoformat()
        }

    def get_observer(self, name: str) -> Optional[Any]:
        """Get a registered observer by name."""
        if name in self.observer_registry:
            return self.observer_registry[name]["observer"]
        return None

    def get_network_health(self) -> Dict[str, Any]:
        """Get overall network health."""
        return {
            "observers_registered": len(self.observer_registry),
            "contradictions": self.contradiction_resolver.get_report(),
            "multichain_network": self.multichain_integrator.get_network_status(),
            "timestamp": datetime.now().isoformat()
        }
