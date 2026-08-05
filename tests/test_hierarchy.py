import pytest
from scos import SCOSChain


def test_hierarchy_enforced(tmp_path):
    # Use a fresh DB in tmp_path to avoid touching repo data
    db_path = tmp_path / "test_chain.db"
    chain = SCOSChain()
    chain.database = chain.database.__class__(db_path)

    # Initially presence not declared: adding a block must fail
    with pytest.raises(ValueError):
        chain.add_block("A factual claim about physics.")

    # Declare presence and try again
    chain.initialize()
    block = chain.add_block("A factual claim about physics.")
    assert block.block_id == 1
    assert len(chain.database.get_all_blocks()) == 1
