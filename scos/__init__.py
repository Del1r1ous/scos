"""SCOS package - exports for SCOS 4.0

This __init__ is intended for the scos-4.0 branch and exposes the corrected
architecture's primary classes.
"""

from .ground import GenesisWitness
from .process import WitnessProtocol
from .practice import EthicalInvariant
from .tool import SCOSChain

__all__ = [
    'GenesisWitness',
    'WitnessProtocol',
    'EthicalInvariant',
    'SCOSChain'
]
