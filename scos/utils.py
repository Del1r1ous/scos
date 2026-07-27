"""Utility functions for SCOS"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

def compute_hash(data: Dict[str, Any]) -> str:
    """Compute SHA-256 hash of data"""
    json_str = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(json_str.encode()).hexdigest()

def compute_fingerprint(hardware_data: Dict[str, Any]) -> str:
    """Compute hardware fingerprint"""
    fingerprint_input = {
        'cpu': hardware_data.get('cpu', ''),
        'gpu': hardware_data.get('gpu', ''),
        'disk': hardware_data.get('disk', ''),
        'mac': hardware_data.get('mac', ''),
    }
    return compute_hash(fingerprint_input)[:16]

def timestamp_now() -> str:
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"

def calculate_consensus(votes: List[float]) -> float:
    """Calculate consensus from witness votes"""
    if not votes:
        return 0.0
    return sum(votes) / len(votes)

def calculate_inversion_score(claims: Dict[str, Any]) -> float:
    """Calculate inversion score (resistance to inverted reality)"""
    total_resistance = 0.0
    count = 0
    
    for key, value in claims.items():
        if isinstance(value, float) and 0 <= value <= 1:
            total_resistance += value
            count += 1
    
    if count == 0:
        return 0.0
    
    inversion = total_resistance / count
    return 1.0 - inversion

def format_for_output(data: Dict[str, Any]) -> str:
    """Format data for pretty console output"""
    return json.dumps(data, indent=2, default=str)

def verify_chain_integrity(blocks: List[Dict[str, Any]]) -> bool:
    """Verify chain integrity by checking hashes"""
    for i, block in enumerate(blocks):
        if i == 0:
            continue
        
        prev_hash = blocks[i-1].get('hash')
        current_prev_hash = block.get('previous_hash')
        
        if prev_hash != current_prev_hash:
            logger.error(f"Chain integrity broken at block {i}")
            return False
    
    return True

def log_audit(event: str, details: Dict[str, Any]) -> None:
    """Log audit event"""
    audit_entry = {
        'timestamp': timestamp_now(),
        'event': event,
        'details': details
    }
    logger.info(f"AUDIT: {json.dumps(audit_entry)}")
