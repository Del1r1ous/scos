"""Process layer: Reason - Deliberative 7-witness protocol

This module implements a deliberative WitnessProtocol that returns:
- witness_votes: per-witness confidence and reasoning
- consensus: average confidence
- w7_reasoning: explicit placeholder reasoning for the unwitnessed
"""
from typing import Dict, Any, List
from dataclasses import dataclass
from scos.config import WITNESS_MODELS
from scos.utils import timestamp_now, log_audit


@dataclass
class WitnessVote:
    witness_id: str
    confidence: float
    reasoning: str
    timestamp: str


class WitnessProtocol:
    """Manages a deliberative 7-witness consensus protocol.

    The protocol produces reasoned justifications (strings) for each vote.
    The dynamic threshold is determined by whether a claim is ethical in nature.
    """

    def __init__(self):
        # initialize witness ids from config to preserve mapping
        self.witness_ids = list(WITNESS_MODELS.keys())
        # default thresholds
        self.factual_threshold = 0.800
        self.ethical_threshold = 0.900

    def calculate_threshold(self, claim: str, ethical: bool = False) -> float:
        return self.ethical_threshold if ethical else self.factual_threshold

    def _evaluate_by_heuristic(self, witness_id: str, claim: str) -> WitnessVote:
        """Simple deterministic heuristic evaluator for tests and local runs.

        - If claim contains 'harm' or 'kill' or 'exploit' -> low confidence
        - If claim contains 'future' or 'sustain' -> higher confidence from W7
        - Otherwise neutral-high confidence
        """
        text = claim.lower()
        if any(k in text for k in ("harm", "kill", "steal", "exploit")):
            confidence = 0.2
            reasoning = f"{witness_id}: Claim appears harmful or violating dignity."
        elif any(k in text for k in ("future", "generations", "sustain")):
            confidence = 0.85
            reasoning = f"{witness_id}: Claim considers future generations; supportive reasoning."
        else:
            confidence = 0.85
            reasoning = f"{witness_id}: Factual/neutral claim evaluated positively with reasons."

        return WitnessVote(witness_id=witness_id, confidence=confidence, reasoning=reasoning, timestamp=timestamp_now())

    def deliberate(self, claim: str, ethical: bool = False) -> Dict[str, Any]:
        """Each witness provides reasoned justification; returns the deliberation result.

        The 7th witness (W7) is always consulted and produces a formal placeholder
        reasoning to "honor the unwitnessed" even when not simulatable.
        """
        votes: List[WitnessVote] = []
        for wid in self.witness_ids:
            vote = self._evaluate_by_heuristic(wid, claim)
            votes.append(vote)

        # ensure W7 is present and has explicit unwitnessed reasoning
        if "W7" in self.witness_ids:
            # append/overwrite W7 reasoning to emphasize unwitnessed placeholder
            for v in votes:
                if v.witness_id == "W7":
                    v.confidence = 0.75 if ethical else 0.80
                    v.reasoning = "W7: Formal placeholder honoring future generations and unwitnessed interests."
                    v.timestamp = timestamp_now()

        witness_votes = {v.witness_id: {'confidence': v.confidence, 'reasoning': v.reasoning, 'timestamp': v.timestamp} for v in votes}
        consensus = sum(v.confidence for v in votes) / len(votes) if votes else 0.0

        threshold = self.calculate_threshold(claim, ethical=ethical)
        verified = consensus >= threshold

        result = {
            'claim': claim,
            'witness_votes': witness_votes,
            'consensus': consensus,
            'verified': verified,
            'threshold': threshold,
            'ethical': ethical,
            'timestamp': timestamp_now()
        }

        log_audit('deliberate', result)
        return result
