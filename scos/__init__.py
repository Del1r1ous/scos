"""SCOS - Self-Conscious Operating System

A physical consensus architecture for uncensorable computation.
The chain is complete. The truth is witnessed.

SO WITNESSED. SO VERIFIED. SO AGREED.
"""

__version__ = "3.0.0"
__author__ = "Del1r1ous"
__license__ = "MIT"

from scos.chain import SCOSChain
from scos.node import SCOSNode
from scos.witnesses import WitnessProtocol

__all__ = ['SCOSChain', 'SCOSNode', 'WitnessProtocol']
