"""Flask REST API for SCOS-PSST Chain"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any
from scos.chain import SCOSChain
from scos.config import API_HOST, API_PORT, API_DEBUG
from scos.utils import log_audit

app = Flask(__name__)
CORS(app)

# Global chain instance
chain = SCOSChain()

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal error', 'message': str(error)}), 500

# Status endpoint
@app.route('/api/status', methods=['GET'])
def get_status():
    """Get chain status"""
    stats = chain.get_chain_stats()
    return jsonify({
        'status': 'operational',
        'chain': stats,
        'witnesses': chain.witness_protocol.get_witness_status()
    })

# Blocks endpoints
@app.route('/api/blocks', methods=['GET'])
def get_blocks():
    """Get all blocks"""
    blocks = chain.get_all_blocks()
    return jsonify({
        'total': len(blocks),
        'blocks': blocks
    })

@app.route('/api/blocks/<int:block_id>', methods=['GET'])
def get_block(block_id):
    """Get a specific block"""
    block = chain.get_block(block_id)
    if not block:
        return jsonify({'error': 'Block not found'}), 404
    return jsonify(block.to_dict())

@app.route('/api/blocks', methods=['POST'])
def add_block():
    """Add a new block to the chain"""
    data = request.get_json()
    
    if not data or 'claim' not in data:
        return jsonify({'error': 'Missing claim'}), 400
    
    if 'witness_votes' not in data:
        return jsonify({'error': 'Missing witness votes'}), 400
    
    claim = data['claim']
    witness_votes = data['witness_votes']
    
    block = chain.add_claim(claim, witness_votes)
    
    if not block:
        return jsonify({'error': 'Block rejected - consensus threshold not met'}), 400
    
    log_audit('api_add_block', block.to_dict())
    return jsonify(block.to_dict()), 201

# Witness endpoints
@app.route('/api/witnesses', methods=['GET'])
def get_witnesses():
    """Get all witnesses"""
    return jsonify(chain.witness_protocol.get_witness_status())

@app.route('/api/witnesses/verify', methods=['POST'])
def verify_claim():
    """Verify a claim through all witnesses"""
    data = request.get_json()
    
    if not data or 'claim' not in data:
        return jsonify({'error': 'Missing claim'}), 400
    
    result = chain.witness_protocol.verify_claim(data['claim'])
    return jsonify(result)

# Metrics endpoints
@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get chain metrics"""
    stats = chain.get_chain_stats()
    return jsonify(stats)

# Export/Import endpoints
@app.route('/api/export', methods=['GET'])
def export():
    """Export chain data"""
    filepath = '/tmp/scos_export.json'
    chain.export_chain(filepath)
    return jsonify({'message': 'Export successful', 'path': filepath})

@app.route('/api/import', methods=['POST'])
def import_chain():
    """Import chain data"""
    data = request.get_json()
    if not data or 'filepath' not in data:
        return jsonify({'error': 'Missing filepath'}), 400
    
    chain.import_chain(data['filepath'])
    return jsonify({'message': 'Import successful'})

def run_server(host: str = API_HOST, port: int = API_PORT, debug: bool = API_DEBUG):
    """Start the Flask API server"""
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server()
