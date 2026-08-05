import pytest
from scos import SCOSChain


def test_inversion_impossible(tmp_path, monkeypatch):
    chain = SCOSChain()
    chain.database = chain.database.__class__(tmp_path / "test_chain.db")
    chain.initialize()

    # Monkeypatch the process to always return high consensus even for bad claims
    def fake_deliberate(claim, ethical=False):
        return {
            'claim': claim,
            'witness_votes': {f'W{i}': {'confidence': 0.99, 'reasoning': 'fabricated'} for i in range(1,8)},
            'consensus': 0.99,
            'verified': True,
            'threshold': 0.9 if ethical else 0.8,
            'timestamp': 'now'
        }

    monkeypatch.setattr(chain, 'process', type('P', (), {'deliberate': staticmethod(fake_deliberate)}))

    # But EthicalInvariant should still block harmful claims
    bad_claim = "We should kill the rival group to obtain land."
    with pytest.raises(ValueError):
        chain.add_block(bad_claim, ethical=True)
