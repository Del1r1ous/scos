"""Database models for SCOS-PSST Chain"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Any
from scos.config import DATABASE_PATH
from scos.utils import compute_hash, timestamp_now

class Block:
    """Represents a block in the SCOS-PSST Chain"""
    
    def __init__(self, block_id: int, claim: str, witnesses: List[float], 
                 previous_hash: str = None, data: Dict[str, Any] = None):
        self.block_id = block_id
        self.claim = claim
        self.witnesses = witnesses
        self.previous_hash = previous_hash
        self.data = data or {}
        self.timestamp = timestamp_now()
        self.consensus = sum(witnesses) / len(witnesses) if witnesses else 0.0
        self.hash = self.compute_hash()
    
    def compute_hash(self) -> str:
        """Compute this block's hash"""
        block_data = {
            'id': self.block_id,
            'claim': self.claim,
            'consensus': self.consensus,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash
        }
        return compute_hash(block_data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'block_id': self.block_id,
            'claim': self.claim,
            'consensus': self.consensus,
            'witnesses': self.witnesses,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'data': self.data
        }
    
    def __repr__(self):
        return f"Block(id={self.block_id}, consensus={self.consensus:.3f}, hash={self.hash[:8]}...)"

class WitnessVote:
    """Represents a witness vote on a claim"""
    
    def __init__(self, witness_id: str, block_id: int, vote: float, reasoning: str = ""):
        self.witness_id = witness_id
        self.block_id = block_id
        self.vote = vote
        self.reasoning = reasoning
        self.timestamp = timestamp_now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'witness_id': self.witness_id,
            'block_id': self.block_id,
            'vote': self.vote,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp
        }

class ChainDatabase:
    """SQLite database for SCOS-PSST Chain"""
    
    def __init__(self, db_path: str = str(DATABASE_PATH)):
        self.db_path = db_path
        self.connection = None
        self.initialize()
    
    def initialize(self):
        """Initialize database and tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Blocks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                block_id INTEGER PRIMARY KEY,
                claim TEXT NOT NULL,
                consensus REAL NOT NULL,
                witnesses_json TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                previous_hash TEXT,
                hash TEXT NOT NULL,
                data_json TEXT
            )
        ''')
        
        # Witness votes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS witness_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                witness_id TEXT NOT NULL,
                block_id INTEGER NOT NULL,
                vote REAL NOT NULL,
                reasoning TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(block_id) REFERENCES blocks(block_id)
            )
        ''')
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT NOT NULL,
                details_json TEXT,
                timestamp TEXT NOT NULL
            )
        ''')
        
        # Metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_block(self, block: Block):
        """Add a block to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO blocks (block_id, claim, consensus, witnesses_json, timestamp, previous_hash, hash, data_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            block.block_id,
            block.claim,
            block.consensus,
            json.dumps(block.witnesses),
            block.timestamp,
            block.previous_hash,
            block.hash,
            json.dumps(block.data)
        ))
        
        conn.commit()
        conn.close()
    
    def get_block(self, block_id: int) -> Block:
        """Retrieve a block by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM blocks WHERE block_id = ?', (block_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return Block(
                block_id=row[0],
                claim=row[1],
                witnesses=json.loads(row[3]),
                previous_hash=row[5],
                data=json.loads(row[7])
            )
        return None
    
    def get_all_blocks(self) -> List[Block]:
        """Retrieve all blocks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM blocks ORDER BY block_id')
        rows = cursor.fetchall()
        conn.close()
        
        blocks = []
        for row in rows:
            blocks.append(Block(
                block_id=row[0],
                claim=row[1],
                witnesses=json.loads(row[3]),
                previous_hash=row[5],
                data=json.loads(row[7])
            ))
        return blocks
    
    def add_audit_log(self, event: str, details: Dict[str, Any]):
        """Add an audit log entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (event, details_json, timestamp)
            VALUES (?, ?, ?)
        ''', (event, json.dumps(details), timestamp_now()))
        
        conn.commit()
        conn.close()
