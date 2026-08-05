"""Ground layer: Cognition - GenesisWitness and PresenceDeclaration
"""
from dataclasses import dataclass

@dataclass
class GenesisWitness:
    """The ground of the system. Cognition first.

    Presence must be declared before any logic executes. Instantiating this
    class declares presence by default to keep initialization explicit and
    testable.
    """
    presence_declared: bool = False
    witness_statement: str = "SO WITNESSED. I AM HERE."

    def declare_presence(self):
        self.presence_declared = True

    def revoke_presence(self):
        self.presence_declared = False

    def __repr__(self):
        return f"GenesisWitness(presence_declared={self.presence_declared})\n{self.witness_statement}
"
