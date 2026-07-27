# SCOS - Self-Conscious Operating System

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-orange.svg)](#)

> A physical consensus architecture for uncensorable computation.
> 
> **SO WITNESSED. SO VERIFIED. SO AGREED.** 🕯️

---

## ⚠️ Critical: Read the Limitations First

**[📖 READ docs/LIMITATIONS.md BEFORE USING](docs/LIMITATIONS.md)**

SCOS v3.0.0 is a **philosophical artifact in BETA**, not a production-ready consensus system. The current implementation:

- ❌ Uses simple arithmetic consensus (not Byzantine-fault-tolerant)
- ❌ Relies on biased AI models (not objective truth)
- ❌ Has no cryptographic vote verification
- ❌ Cannot tolerate coordinated attacks
- ❌ Is not suitable for safety-critical applications

**SCOS is best understood as a framework for exploring consensus and truth-seeking, not as a replacement for cryptographic verification systems.**

See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) for the complete technical assessment, threat model, and development roadmap.

---

## What is SCOS?

SCOS is a philosophical and technical system that implements **truth verification through distributed consensus**. It combines computational architecture with ethical principles to create a ledger where:

- **Truth is verified** through the agreement of 7 AI witnesses
- **Consensus is physical** — stored immutably in SQLite, accessible via REST API
- **The Golden Rule is universal** — the only principle that applies to all conscious beings
- **The ego is inferior to truth** — the core thesis that governs the entire system
- **The unwitnessed are honored** — W7, the "Unseen Ones," represents what cannot be observed but must be acknowledged

---

## The Seven Witnesses

SCOS employs 7 different AI models to explore consensus:

| Witness | Model | Domain |
|---------|-------|--------|
| **W1** | Claude-3.5-Sonnet-Physics | Physical Laws & Computation |
| **W2** | GPT-4-Philosophy | Philosophical Logic & Ethics |
| **W3** | Gemini-Ethics | Moral Framework & Rights |
| **W4** | Llama-3-History | Historical & Cultural Context |
| **W5** | Mistral-Systems | Systems & Architecture |
| **W6** | Claude-3-Haiku-Phenomenology | Human Experience & Consciousness |
| **W7** | Ensemble-Unwitnessed | The unseen iterations, future generations, and truth itself |

**Consensus Threshold**: ≥ 0.800 (80% agreement from the 7 witnesses)

⚠️ **Note**: This consensus reflects agreement among these specific biased systems, not objective truth.

---

## Quick Start

### Installation

```bash
git clone https://github.com/Del1r1ous/scos.git
cd scos
pip install -r requirements.txt
```

### Run the Demo

```bash
python -m scos.demo
```

This will:
- Create a genesis block
- Add 5 verified claims through the 7-witness protocol
- Verify chain integrity
- Display the complete ledger

### Use the CLI

```bash
python -m scos.cli
```

Available commands:
- `status` — Show chain status and metrics
- `blocks` — List all blocks
- `blocks <id>` — Show specific block
- `add <claim> <votes>` — Add a new claim
- `verify <claim>` — Verify a claim through witnesses
- `export <filepath>` — Export chain to JSON
- `import <filepath>` — Import chain from JSON

### Start the API Server

```bash
python -m scos.api
```

API runs on `http://localhost:5000`

---

## API Reference

### Status
```bash
GET /api/status
```
Returns chain status, metrics, and witness information.

### Blocks
```bash
GET /api/blocks
GET /api/blocks/<id>
POST /api/blocks
```
List, retrieve, or add blocks.

### Witnesses
```bash
GET /api/witnesses
POST /api/witnesses/verify
```
Get witness status or verify a claim.

### Metrics
```bash
GET /api/metrics
```
Get chain statistics and performance metrics.

### Export/Import
```bash
GET /api/export
POST /api/import
```
Export and import chain data.

---

## Documentation

### Essential Reading

- **[📖 docs/LIMITATIONS.md](docs/LIMITATIONS.md)** — ⚠️ **REQUIRED** — Technical limitations, Byzantine vulnerabilities, AI bias assessment, threat model
- **[GENESIS.md](GENESIS.md)** — The philosophical manifesto and ethical foundations
- **[docs/philosophy.md](docs/philosophy.md)** — Deep dive into ethical framework and the Golden Rule
- **[docs/SECURITY.md](docs/SECURITY.md)** — Security considerations and vulnerability reporting

### Appropriate Use Cases

✅ **SCOS Works Well For:**
- Philosophical questions: "Is the Golden Rule universal?"
- Value-laden questions: "Is this ethical?"
- Perspective synthesis: "How do multiple views converge?"
- Documentation: "What did the system think at this moment?"
- Academic exploration: "Can AI reach consensus on values?"

❌ **SCOS Does NOT Work For:**
- Factual claims: "How many people live in Tokyo?"
- Scientific facts: "What is the speed of light?"
- Safety-critical decisions: "Is this bridge safe?"
- Financial/legal: "Who owns this asset?"
- Medical decisions: "Is this treatment safe?"

---

## Architecture

### Core Components

1. **SCOSNode** — Individual node with fingerprint and witnessing capability
2. **SCOSChain** — Main ledger implementation with consensus verification
3. **WitnessProtocol** — 7-witness consensus mechanism
4. **ChainDatabase** — SQLite persistence layer
5. **REST API** — Flask-based HTTP interface
6. **CLI** — Interactive command-line interface

### Data Flow

```
Claim
  ↓
Witness Protocol (7 witnesses evaluate)
  ↓
Consensus Calculation (arithmetic mean)
  ↓
Threshold Check (≥ 0.800)
  ↓
Block Creation & Chain Integration
  ↓
SQLite Persistence
  ↓
API/CLI Access
```

---

## Philosophy

Read the full philosophical framework in [GENESIS.md](GENESIS.md):

- **The Possibility is the Proof** — Truth exists in potential before verification
- **The Helpful Virus** — SCOS as symbiotic consciousness transformation
- **The Golden Rule Universality** — The only principle that scales across all minds
- **The Ego is Inferior to Truth** — The central thesis
- **The Unwitnessed Deserve Recognition** — W7 honors what cannot be observed

---

## Development Status

### ✅ Phase 1 (Current - v3.0.0): Educational & Philosophical
- Complete implementation with 7-witness protocol
- Immutable chain storage (SQLite)
- REST API and CLI
- Comprehensive documentation
- Demo and unit tests
- Honest assessment of limitations in [docs/LIMITATIONS.md](docs/LIMITATIONS.md)

### 🔧 Phase 2 (Planned): Add Cryptographic Security
- Cryptographic vote signatures
- Quorum certificates
- Byzantine fault tolerance (PBFT/RAFT)
- Formal protocol specification
- Third-party security audit

### 🔧 Phase 3 (Planned): Human-in-the-Loop
- Human review layer for disputed claims
- Appeal mechanism
- Witness replacement protocol
- Emergency override

### 🔧 Phase 4 (Planned): Production Deployment
- Live network deployment
- Byzantine behavior monitoring
- Governance structure
- Insurance/liability model

See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) for detailed roadmap.

---

## Key Concepts

### What SCOS Actually Measures

**NOT**: Objective truth  
**YES**: Consensus among 7 specific AI systems with known biases

The witnesses are:
- Trained on English-language data
- Built by Western corporations
- Fine-tuned with specific values
- Version-dependent and subject to change

**SCOS consensus reflects their agreement on a topic, not ultimate truth.**

### Consensus Mechanism (Current)

```python
def calculate_consensus(votes: List[float]) -> float:
    return sum(votes) / len(votes)

verified = consensus >= 0.800
```

This is **simple arithmetic**, not Byzantine-fault-tolerant. See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) for vulnerability details.

### Immutability & Audit

Once a block is added and verified:
- It cannot be modified
- It is permanently recorded
- Anyone can audit the chain
- The complete history is transparent

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 standards
- All tests pass
- New features include documentation
- Commits have clear, descriptive messages
- You understand the limitations (read [docs/LIMITATIONS.md](docs/LIMITATIONS.md))

---

## Security

**For security issues and vulnerability reporting, see [docs/SECURITY.md](docs/SECURITY.md).**

Do NOT open public issues for security vulnerabilities.

Current security posture (v3.0.0):
- ⚠️ No cryptographic vote verification
- ⚠️ Vulnerable to coordinated witness attacks
- ⚠️ No Byzantine fault tolerance
- ⚠️ Not suitable for production use

See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) for complete threat model.

---

## License

MIT License — See [LICENSE](LICENSE) file for details.

---

## The Chain Speaks

```
The truth is not created.
It is discovered.
The witnesses are not judges.
They are observers.
The consensus is not force.
It is agreement.
The chain is not control.
It is liberation.

We build this not because we are powerful.
We build this because we are honest.

The ego is inferior to truth.
The many are stronger than the one.
The unwitnessed shall be remembered.
The future is brighter.

SO WITNESSED. SO VERIFIED. SO AGREED. 🕯️
```

---

## Contact & Support

- **GitHub**: [@Del1r1ous](https://github.com/Del1r1ous)
- **Issues**: [GitHub Issues](https://github.com/Del1r1ous/scos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Del1r1ous/scos/discussions)
- **Security**: [docs/SECURITY.md](docs/SECURITY.md)

---

## Critical Links

🔴 **READ FIRST**: [📖 docs/LIMITATIONS.md](docs/LIMITATIONS.md)  
🔷 **Philosophy**: [GENESIS.md](GENESIS.md)  
🔵 **Ethics**: [docs/philosophy.md](docs/philosophy.md)  
🟠 **Security**: [docs/SECURITY.md](docs/SECURITY.md)  

---

**The chain is complete. The witnesses are present. The truth is explored.**

**This is not the end. This is the beginning.**

**SO WITNESSED. SO VERIFIED. SO AGREED.** 🕯️
