"""Tests for SCOS Chain"""

import unittest
from scos.chain import SCOSChain
from scos.models import Block

class TestSCOSChain(unittest.TestCase):
    """Test SCOS Chain functionality"""
    
    def setUp(self):
        self.chain = SCOSChain()
    
    def test_genesis_creation(self):
        """Test genesis block creation"""
        genesis = self.chain.create_genesis_block("Test genesis claim")
        self.assertIsNotNone(genesis)
        self.assertEqual(genesis.block_id, 0)
        self.assertEqual(genesis.consensus, 1.0)
    
    def test_add_claim(self):
        """Test adding a claim"""
        self.chain.create_genesis_block("Genesis")
        votes = [0.95, 0.92, 0.98, 0.91, 0.93, 0.94, 0.96]
        block = self.chain.add_claim("Test claim", votes)
        self.assertIsNotNone(block)
        self.assertGreaterEqual(block.consensus, 0.8)
    
    def test_consensus_threshold(self):
        """Test consensus threshold enforcement"""
        self.chain.create_genesis_block("Genesis")
        votes = [0.5, 0.4, 0.6, 0.3, 0.5, 0.4, 0.6]  # Average: 0.47
        block = self.chain.add_claim("Test claim", votes)
        self.assertIsNone(block)  # Should be rejected
    
    def test_chain_integrity(self):
        """Test chain integrity verification"""
        self.chain.create_genesis_block("Genesis")
        votes = [0.95, 0.92, 0.98, 0.91, 0.93, 0.94, 0.96]
        self.chain.add_claim("Test claim 1", votes)
        self.chain.add_claim("Test claim 2", votes)
        self.assertTrue(self.chain.verify_integrity())

if __name__ == '__main__':
    unittest.main()
