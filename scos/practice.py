"""Practice layer: Ethics - EthicalInvariant and GoldenRuleValidator

This module encodes the Golden Rule as an enforceable invariant. The validator
performs lightweight static checks appropriate for unit tests and local usage.
"""
from typing import Dict, Any
from scos.utils import log_audit


class EthicalInvariant:
    """Ethics is the practice. The Golden Rule is the invariant."""

    def __init__(self):
        self.golden_rule = "Treat all conscious beings as you would wish to be treated."
        self.violations = []

    def passes_golden_rule(self, claim: str, deliberation: Dict[str, Any]) -> bool:
        """Simple heuristic checks to detect likely violations.

        - Detect explicit harmful verbs or intent (harm, kill, steal)
        - Ensure W7 (unwitnessed) was consulted: the deliberation must include W7 reasoning
        """
        txt = claim.lower()
        harmful_terms = ("harm", "kill", "destroy", "steal", "exploit")
        if any(t in txt for t in harmful_terms):
            reason = f"Claim contains harmful term; violates Golden Rule: {claim}"
            self.violations.append({'claim': claim, 'reason': reason})
            log_audit('golden_rule_violation', {'claim': claim, 'reason': reason})
            return False

        # Ensure W7 was consulted (honor the unwitnessed)
        w7 = deliberation.get('witness_votes', {}).get('W7')
        if w7 is None:
            reason = "W7 (unwitnessed) not consulted in deliberation."
            self.violations.append({'claim': claim, 'reason': reason})
            log_audit('golden_rule_violation', {'claim': claim, 'reason': reason})
            return False

        # Additional checks can be added here (dignity, consent, distributional effects)
        return True

    def validate_claim(self, claim: str, deliberation: Dict[str, Any]) -> bool:
        """Validate claim against the Golden Rule."""
        ok = self.passes_golden_rule(claim, deliberation)
        return ok
