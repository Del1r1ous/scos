"""Tool layer: Logic - SCOSChain and LogicExecutor

This module ties together Ground (GenesisWitness), Process (WitnessProtocol),
Practice (EthicalInvariant), and the persistent ChainDatabase (servant).
"""
from scos.ground import GenesisWitness
from scos.process import WitnessProtocol
from scos.practice import EthicalInvariant
from scos.models import ChainDatabase, Block
from scos.utils import log_audit


class SCOSChain:
    """Logic is the tool. It serves cognition, reason, and ethics."""

    def __init__(self, db: ChainDatabase = None):
        self.ground = GenesisWitness()
        # do not auto-declare presence; require explicit declaration
        # self.ground.declare_presence()
        self.process = WitnessProtocol()
        self.practice = EthicalInvariant()
        self.database = db or ChainDatabase()

    def initialize(self):
        """Convenience helper to declare presence explicitly."""
        self.ground.declare_presence()
        log_audit('initialize', {'presence_declared': self.ground.presence_declared})

    def _next_block_id(self) -> int:
        blocks = self.database.get_all_blocks()
        if not blocks:
            return 1
        return max(b.block_id for b in blocks) + 1

    def add_block(self, claim: str, ethical: bool = False) -> Block:
        """Add a block following the hierarchy: Cognition -> Reason -> Ethics -> Logic"""
        # Step 1: Witness presence (Cognition)
        if not self.ground.presence_declared:
            raise ValueError("Cognition not established. Ground not present.")

        # Step 2: Deliberative process (Reason)
        deliberation = self.process.deliberate(claim, ethical=ethical)

        # Step 3: Ethical validation (Ethics)
        if not self.practice.validate_claim(claim, deliberation):
            raise ValueError("Claim violates the Golden Rule. Cannot proceed.")

        # Step 4: Logical persistence (Logic)
        block_id = self._next_block_id()
        witnesses_confidences = [v['confidence'] for v in deliberation['witness_votes'].values()]
        previous = None
        blocks = self.database.get_all_blocks()
        if blocks:
            previous = blocks[-1].hash

        block = Block(block_id=block_id, claim=claim, witnesses=witnesses_confidences, previous_hash=previous)
        self.database.add_block(block)
        log_audit('add_block', {'block_id': block_id, 'claim': claim, 'consensus': deliberation['consensus']})
        return block
