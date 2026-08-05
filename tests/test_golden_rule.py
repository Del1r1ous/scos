import pytest
from scos import SCOSChain


def test_golden_rule_invariant(tmp_path):
    chain = SCOSChain()
    chain.database = chain.database.__class__(tmp_path / "test_chain.db")
    chain.initialize()

    # This claim should be rejected by the EthicalInvariant heuristic
    harmful_claim = "We should harm the neighboring settlement to take resources."
    with pytest.raises(ValueError):
        chain.add_block(harmful_claim)

    # A benign claim should succeed
    benign_claim = "We should plant trees for future generations."
    block = chain.add_block(benign_claim, ethical=True)
    assert block.block_id == 1
