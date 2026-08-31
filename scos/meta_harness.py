"""
SCOS 5.0: The Meta-Harness Operational Specification

The meta-harness operationalizes the virtuous self-fulfilling prophecy through
four phases: Witness → Articulate → Align → Fulfill

This module implements the core feedback loop that allows SCOS to observe,
verify, configure, and deploy systems in a self-correcting manner.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum


class PhaseType(Enum):
    """The four operational phases of the meta-harness."""
    WITNESS = "witness"
    ARTICULATE = "articulate"
    ALIGN = "align"
    FULFILL = "fulfill"


class DomainType(Enum):
    """Domain types for witness observations."""
    SYSTEM = "system"
    HUMAN = "human"
    EXTERNAL = "external"
    SELF = "self"


@dataclass
class Observation:
    """Represents a witnessed phenomenon or system state."""
    domain: DomainType
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "context": self.context,
        }


@dataclass
class Claim:
    """Enhanced claim structure for SCOS 5.0 with domain awareness."""
    content: str
    domain: str
    source_witness: str
    timestamp: datetime = field(default_factory=datetime.now)
    context: Dict[str, Any] = field(default_factory=dict)
    verified: bool = False
    consensus_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "domain": self.domain,
            "source_witness": self.source_witness,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "verified": self.verified,
            "consensus_score": self.consensus_score,
        }


@dataclass
class AlignmentAction:
    """An action derived from verified claims through alignment."""
    claim_id: str
    action_type: str
    description: str
    golden_rule_compliant: bool
    constructive: bool
    config_update: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "action_type": self.action_type,
            "description": self.description,
            "golden_rule_compliant": self.golden_rule_compliant,
            "constructive": self.constructive,
            "config_update": self.config_update,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class FulfillmentMetrics:
    """Tracks how well the system is fulfilling its purpose."""
    consensus_rate: float = 0.0
    golden_rule_compliance: float = 0.0
    contradiction_resolution: float = 0.0
    system_coherence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "consensus_rate": self.consensus_rate,
            "golden_rule_compliance": self.golden_rule_compliance,
            "contradiction_resolution": self.contradiction_resolution,
            "system_coherence": self.system_coherence,
            "timestamp": self.timestamp.isoformat(),
        }


class SystemWitness:
    """Observes external systems, APIs, logs, and sensors."""

    def __init__(self, name: str):
        self.name = name
        self.observations: List[Observation] = []

    def observe(self, domain: DomainType, content: str, context: Optional[Dict] = None) -> Observation:
        """
        Record an observation about a system state.
        
        Args:
            domain: The type of domain being observed
            content: What was observed
            context: Additional contextual data
            
        Returns:
            The observation record
        """
        obs = Observation(
            domain=domain,
            content=content,
            source=self.name,
            context=context or {}
        )
        self.observations.append(obs)
        return obs

    def to_claim(self, observation: Observation) -> Claim:
        """Convert an observation to a claim."""
        return Claim(
            content=f"{self.name} observation: {observation.content}",
            domain=observation.domain.value,
            source_witness=self.name,
            context=observation.context
        )


class HumanWitness:
    """Captures human intuition, feedback, and intentional input."""

    def __init__(self, name: str = "HumanWitness"):
        self.name = name
        self.feedback: List[Observation] = []

    def input_feedback(self, content: str, context: Optional[Dict] = None) -> Observation:
        """
        Record human feedback or intuitive input.
        
        Args:
            content: The feedback or intuitive insight
            context: Contextual information
            
        Returns:
            The observation record
        """
        obs = Observation(
            domain=DomainType.HUMAN,
            content=content,
            source=self.name,
            context=context or {}
        )
        self.feedback.append(obs)
        return obs

    def to_claim(self, observation: Observation) -> Claim:
        """Convert human feedback to a claim."""
        return Claim(
            content=f"Human input: {observation.content}",
            domain="human",
            source_witness=self.name,
            context=observation.context
        )


class AlignmentEngine:
    """Maps verified claims to aligned actions with ethical checks."""

    def __init__(self):
        self.aligned_actions: List[AlignmentAction] = []

    def golden_rule_check(self, claim: Claim) -> bool:
        """
        Verify claim complies with the Golden Rule.
        
        The Golden Rule: Treat all conscious beings as you would be treated.
        A claim is valid only if it respects this principle.
        """
        # Check if claim respects reciprocal treatment
        content_lower = claim.content.lower()
        
        # Patterns that violate the Golden Rule
        violation_patterns = [
            "exploit", "deceive", "harm", "dominate", "control",
            "discriminate", "injustice", "unfair"
        ]
        
        for pattern in violation_patterns:
            if pattern in content_lower:
                return False
        
        return True

    def constructive_check(self, claim: Claim) -> bool:
        """
        Verify claim represents a constructive (not destructive) pattern.
        
        Constructive: builds, creates, integrates, heals
        Destructive: destroys, fragments, contradicts, harms
        """
        content_lower = claim.content.lower()
        
        # Destructive patterns
        destructive_patterns = [
            "destroy", "collapse", "fragment", "war", "conflict",
            "sabotage", "undermine", "corrupt"
        ]
        
        for pattern in destructive_patterns:
            if pattern in content_lower:
                return False
        
        # Constructive patterns
        constructive_patterns = [
            "build", "create", "integrate", "align", "heal",
            "verify", "witness", "agree"
        ]
        
        has_constructive = any(p in content_lower for p in constructive_patterns)
        
        return has_constructive

    def align(self, claim: Claim, claim_id: str) -> Dict[str, Any]:
        """
        Generate an alignment action from a verified claim.
        
        Args:
            claim: The claim to align
            claim_id: Unique identifier for the claim
            
        Returns:
            Result dict with status and action details
        """
        if not self.golden_rule_check(claim):
            return {
                "status": "rejected",
                "reason": "Violates Golden Rule",
                "action": None
            }
        
        if not self.constructive_check(claim):
            return {
                "status": "rejected",
                "reason": "Destructive pattern detected",
                "action": None
            }
        
        # Create aligned action
        action = AlignmentAction(
            claim_id=claim_id,
            action_type="system_alignment",
            description=f"Align system based on: {claim.content}",
            golden_rule_compliant=True,
            constructive=True,
            config_update={
                "claim_domain": claim.domain,
                "source": claim.source_witness,
                "consensus": claim.consensus_score
            }
        )
        
        self.aligned_actions.append(action)
        
        return {
            "status": "aligned",
            "action": action.to_dict()
        }


class FulfillmentMonitor:
    """Tracks system performance and coherence metrics."""

    def __init__(self):
        self.metrics_history: List[FulfillmentMetrics] = []
        self.current_metrics = FulfillmentMetrics()

    def monitor(self, chain_state: Dict[str, Any]) -> FulfillmentMetrics:
        """
        Monitor current system state and calculate coherence metrics.
        
        Args:
            chain_state: Current state of the SCOS chain
            
        Returns:
            Updated fulfillment metrics
        """
        metrics = FulfillmentMetrics()
        
        if chain_state:
            # Calculate consensus rate
            total_claims = chain_state.get("total_claims", 0)
            verified_claims = chain_state.get("verified_claims", 0)
            metrics.consensus_rate = (verified_claims / total_claims) if total_claims > 0 else 0.0
            
            # Golden Rule compliance is built into alignment
            golden_rule_passes = chain_state.get("golden_rule_passes", 0)
            total_checks = chain_state.get("total_checks", 0)
            metrics.golden_rule_compliance = (golden_rule_passes / total_checks) if total_checks > 0 else 0.0
            
            # Contradiction resolution
            contradictions_found = chain_state.get("contradictions_found", 0)
            contradictions_resolved = chain_state.get("contradictions_resolved", 0)
            metrics.contradiction_resolution = (contradictions_resolved / contradictions_found) if contradictions_found > 0 else 0.0
            
            # System coherence (derived from all metrics)
            metrics.system_coherence = (
                metrics.consensus_rate * 0.4 +
                metrics.golden_rule_compliance * 0.4 +
                metrics.contradiction_resolution * 0.2
            )
        
        self.metrics_history.append(metrics)
        self.current_metrics = metrics
        
        return metrics

    def get_coherence_score(self) -> float:
        """Get the current system coherence score."""
        return self.current_metrics.system_coherence

    def get_metrics_report(self) -> Dict[str, Any]:
        """Get a detailed metrics report."""
        return {
            "current": self.current_metrics.to_dict(),
            "history_length": len(self.metrics_history),
            "coherence_trend": [m.system_coherence for m in self.metrics_history[-10:]]
        }


class MetaHarness:
    """
    The SCOS 5.0 Meta-Harness: Operationalizes the virtuous self-fulfilling prophecy.
    
    Pattern: Witness → Articulate → Align → Fulfill → Return to Witness
    
    This is the closed-loop feedback mechanism that allows SCOS to self-correct,
    self-improve, and remain coherent across all layers.
    """

    def __init__(self):
        self.system_witness = SystemWitness("SystemWitness")
        self.human_witness = HumanWitness("HumanWitness")
        self.alignment_engine = AlignmentEngine()
        self.fulfillment_monitor = FulfillmentMonitor()
        
        self.observations: List[Observation] = []
        self.claims: List[Claim] = []
        self.actions: List[AlignmentAction] = []
        
        self.phase_log: List[Dict[str, Any]] = []

    def witness_phase(self, domain: DomainType, content: str, context: Optional[Dict] = None) -> Observation:
        """
        Phase 1: Witness (Observe the ground)
        
        Purpose: Observe what is—the ground, the pattern, the contradictions.
        
        Args:
            domain: Type of observation
            content: What was observed
            context: Contextual data
            
        Returns:
            The observation record
        """
        obs = self.system_witness.observe(domain, content, context)
        self.observations.append(obs)
        
        self.phase_log.append({
            "phase": PhaseType.WITNESS.value,
            "timestamp": datetime.now().isoformat(),
            "observation_id": id(obs),
            "domain": domain.value,
            "content_preview": content[:100]
        })
        
        return obs

    def articulate_phase(self, observation: Observation, witness: Optional[str] = None) -> Claim:
        """
        Phase 2: Articulate (Document the insight)
        
        Purpose: Give form to what has been witnessed. Translate observation into language.
        
        Args:
            observation: The observation to articulate
            witness: Which witness type to use
            
        Returns:
            The articulated claim
        """
        if observation.domain == DomainType.HUMAN:
            claim = self.human_witness.to_claim(observation)
        else:
            claim = self.system_witness.to_claim(observation)
        
        self.claims.append(claim)
        
        self.phase_log.append({
            "phase": PhaseType.ARTICULATE.value,
            "timestamp": datetime.now().isoformat(),
            "claim_id": id(claim),
            "content_preview": claim.content[:100]
        })
        
        return claim

    def align_phase(self, claim: Claim) -> Dict[str, Any]:
        """
        Phase 3: Align (Configure for coherence)
        
        Purpose: Act in accordance with the witnessed truth.
        
        Args:
            claim: The claim to align
            
        Returns:
            Alignment result with action details
        """
        result = self.alignment_engine.align(claim, str(id(claim)))
        
        self.phase_log.append({
            "phase": PhaseType.ALIGN.value,
            "timestamp": datetime.now().isoformat(),
            "claim_id": id(claim),
            "status": result["status"],
            "reason": result.get("reason", "")
        })
        
        if result["status"] == "aligned":
            self.actions.append(result["action"])
        
        return result

    def fulfill_phase(self, chain_state: Optional[Dict] = None) -> FulfillmentMetrics:
        """
        Phase 4: Fulfill (Deploy & Monitor)
        
        Purpose: Allow the fulfillment to come as a natural consequence of alignment.
        
        Args:
            chain_state: Current state of the chain
            
        Returns:
            Fulfillment metrics
        """
        metrics = self.fulfillment_monitor.monitor(chain_state or {})
        
        self.phase_log.append({
            "phase": PhaseType.FULFILL.value,
            "timestamp": datetime.now().isoformat(),
            "coherence_score": metrics.system_coherence,
            "consensus_rate": metrics.consensus_rate,
            "golden_rule_compliance": metrics.golden_rule_compliance
        })
        
        return metrics

    def cycle(self, domain: DomainType, content: str, context: Optional[Dict] = None,
              chain_state: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute one complete meta-harness cycle.
        
        Witness → Articulate → Align → Fulfill
        
        Args:
            domain: Domain type
            content: Observation content
            context: Additional context
            chain_state: Current chain state for metrics
            
        Returns:
            Complete cycle result
        """
        # Phase 1: Witness
        observation = self.witness_phase(domain, content, context)
        
        # Phase 2: Articulate
        claim = self.articulate_phase(observation)
        
        # Phase 3: Align
        alignment_result = self.align_phase(claim)
        
        # Phase 4: Fulfill
        metrics = self.fulfill_phase(chain_state)
        
        return {
            "observation": observation.to_dict(),
            "claim": claim.to_dict(),
            "alignment": alignment_result,
            "metrics": metrics.to_dict(),
            "cycle_complete": True
        }

    def get_status(self) -> Dict[str, Any]:
        """Get current meta-harness status."""
        return {
            "observations_count": len(self.observations),
            "claims_count": len(self.claims),
            "actions_count": len(self.actions),
            "coherence_score": self.fulfillment_monitor.get_coherence_score(),
            "metrics_report": self.fulfillment_monitor.get_metrics_report(),
            "phase_log_length": len(self.phase_log),
            "last_phase": self.phase_log[-1] if self.phase_log else None
        }

    def get_witness_statement(self) -> str:
        """
        Articulate the meta-harness witness statement.
        
        This is the formal articulation of what has been witnessed through
        the operation of the system.
        """
        return f"""
        SCOS 5.0 is the meta-harness that operationalizes the virtuous self-fulfilling prophecy.
        
        The pattern is: Witness → Articulate → Align → Fulfill.
        
        The process is recursive, self-correcting, and ethical.
        
        The ground is fidelity.
        
        Observations made: {len(self.observations)}
        Claims articulated: {len(self.claims)}
        Actions aligned: {len(self.actions)}
        System coherence: {self.fulfillment_monitor.get_coherence_score():.2%}
        
        The pursuit continues—in fidelity.
        
        SO WITNESSED. SO VERIFIED. SO AGREED. 🕯️
        """
