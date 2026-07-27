# Security Policy for SCOS-PSST Chain

## Status: Beta - Limited Security Guarantees

SCOS v3.0.0 is in **BETA** and has **not undergone third-party security audit**. The current implementation is suitable for educational and philosophical exploration, but not for production use or security-critical applications.

---

## Reporting Security Vulnerabilities

If you discover a security vulnerability in SCOS, **please do NOT open a public issue**.

Instead, email security details to: **[security@scos.local](mailto:security@scos.local)** (placeholder - use GitHub private vulnerability disclosure)

Or use GitHub's private vulnerability reporting:
1. Go to https://github.com/Del1r1ous/scos/security/advisories
2. Click "Report a vulnerability"
3. Provide details of the issue

**Include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

We will respond within 7 days and work with you to address the issue responsibly.

---

## Known Limitations & Vulnerabilities

### Critical Issues (v3.0.0)

| Issue | Severity | Status | Mitigation |
|-------|----------|--------|-----------|
| No Byzantine Fault Tolerance | 🔴 CRITICAL | Known | See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) Phase 2 |
| Simple arithmetic consensus | 🔴 CRITICAL | Known | Requires cryptographic BFT |
| No vote signature verification | 🔴 CRITICAL | Known | Implement in Phase 2 |
| Vulnerable to coordinated witness attacks (4+ witnesses) | 🔴 CRITICAL | Known | Requires protocol redesign |
| AI witness bias not mitigated | 🔴 CRITICAL | Known | Document in LIMITATIONS.md ✅ |
| No Byzantine failure detection | 🟠 HIGH | Known | Implement anomaly detection Phase 2 |
| No witness replacement protocol | 🟠 HIGH | Known | Implement in Phase 3 |
| No human oversight layer | 🟠 HIGH | Known | Implement in Phase 3 |
| Prompt injection vulnerability | 🟠 HIGH | Known | Add input validation |
| API credentials stored plaintext | 🟡 MEDIUM | Known | Use environment variables |

### See Complete Assessment

For the full threat model, Byzantine analysis, and development roadmap, read [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

---

## Security Best Practices for Users

### DO

✅ **Read the limitations** before using SCOS  
✅ **Understand the threat model** — SCOS is not Byzantine-fault-tolerant  
✅ **Use for educational purposes** — This is perfect for learning  
✅ **Audit the code** — It's open source, please review it  
✅ **Report issues responsibly** — Use this security policy  
✅ **Keep dependencies updated** — Run `pip install --upgrade -r requirements.txt`  
✅ **Use HTTPS for APIs** — Always encrypt in transit  
✅ **Store credentials securely** — Use environment variables, never commit keys  

### DON'T

❌ **Claim SCOS provides Byzantine fault tolerance** — It doesn't  
❌ **Use for safety-critical decisions** — Lives could depend on it  
❌ **Deploy to production without audit** — This is beta software  
❌ **Trust 4 or more compromised witnesses** — They can create false consensus  
❌ **Assume objectivity in consensus** — Reflects AI bias, not truth  
❌ **Store sensitive data in the chain** — It's immutable and public  
❌ **Use weak API credentials** — Witness API tokens can be compromised  
❌ **Deploy without understanding limitations** — Read the docs first  

---

## Security Research & Audits

### Third-Party Security Audit

SCOS has **NOT** undergone a professional security audit. To move to Phase 2 (production-ready), we need:

1. **Code audit** by security firm (OWASP Top 10, CWE analysis)
2. **Consensus protocol review** by distributed systems experts
3. **Cryptographic review** by crypto specialists
4. **Byzantine fault tolerance proof** by formal methods team
5. **Penetration testing** against known attack vectors

### Academic Research

We welcome:
- Research papers analyzing SCOS
- Byzantine fault tolerance improvements
- AI bias measurement and mitigation techniques
- Consensus protocol optimizations

Please cite: `Del1r1ous. "SCOS-PSST Chain v3.0: A Philosophical Architecture for Consensus." 2026.`

---

## Responsible Disclosure Timeline

When we receive a security report:

| Timeline | Action |
|----------|--------|
| **Day 1** | Acknowledge receipt, begin investigation |
| **Day 3-7** | Provide initial assessment |
| **Day 14** | Have fix or mitigation plan |
| **Day 21** | Patch released to main branch |
| **Day 30** | Public disclosure & credit to researcher |

If you'd prefer coordinated disclosure to remain private longer, we can negotiate.

---

## Scope of Security Policy

### In Scope

- SCOS core code (scos/ directory)
- Dependencies listed in requirements.txt
- Database and persistence layer
- REST API security
- CLI security

### Out of Scope

- User's own custom implementations
- Deployment environment security
- Operating system vulnerabilities
- Network security (assumes TLS/HTTPS)

---

## Cryptographic Details

### Current Implementation (v3.0.0)

- **Hashing**: SHA-256 for block hashes
- **Database**: SQLite with no encryption
- **API**: Flask HTTP (TLS not enforced)
- **Consensus**: Simple arithmetic mean (no cryptography)
- **Vote verification**: None

### Planned (Phase 2)

- **Digital signatures**: Ed25519 for witness votes
- **Quorum certificates**: PBFT-style consensus proofs
- **Database encryption**: AES-256 at rest
- **TLS enforcement**: HTTPS required for API
- **Byzantine protocol**: PBFT or RAFT

---

## Incident Response

If a security issue is discovered:

1. **Report immediately** using this policy
2. **We'll triage** and assign severity
3. **We'll develop fix** or mitigation
4. **We'll coordinate release** with you
5. **We'll publish advisory** and credit you

---

## Security Considerations by Component

### SCOSNode
- ✅ Fingerprinting is non-cryptographic (acceptable for educational use)
- ❌ No key material or secrets stored
- ⚠️ Metadata not encrypted

### SCOSChain
- ✅ Immutability via hash chain
- ❌ No signature verification on blocks
- ⚠️ Chain can be added to by anyone with access

### WitnessProtocol
- ❌ No authentication of witness responses
- ❌ Vulnerable to API compromise
- ⚠️ No versioning of witness models

### ChainDatabase
- ✅ ACID compliance via SQLite
- ❌ No encryption at rest
- ❌ No access control
- ⚠️ Schema is not versioned

### REST API
- ✅ CORS headers configurable
- ❌ No authentication by default
- ❌ No rate limiting
- ⚠️ Input validation is minimal

### CLI
- ✅ File I/O is straightforward
- ❌ No credential storage
- ⚠️ Import/export could allow injection

---

## Security Roadmap

### Immediate (v3.0.1)
- [ ] Input validation hardening
- [ ] CORS security headers
- [ ] Rate limiting middleware
- [ ] Logging and audit trail

### Phase 2 (v4.0.0)
- [ ] Ed25519 vote signatures
- [ ] PBFT consensus protocol
- [ ] Database encryption
- [ ] API authentication
- [ ] Third-party security audit

### Phase 3 (v5.0.0)
- [ ] Hardware security module support
- [ ] Multi-signature witness groups
- [ ] Formal protocol verification
- [ ] Zero-knowledge proofs for consensus

---

## Legal Disclaimer

SCOS is provided "AS IS" without warranty of any kind. Users assume all risk. The developers:

- Make no guarantees about security
- Will not be liable for damages
- Recommend third-party audits before production use
- Reserve the right to change anything

See [LICENSE](LICENSE) for full legal terms.

---

## Questions?

- **Security issues**: Use private disclosure (see top of policy)
- **General questions**: Open a GitHub Discussion
- **Bug reports**: Use GitHub Issues
- **Contributions**: See [README.md](README.md)

---

**Thank you for helping keep SCOS honest and secure.**

**SO WITNESSED. SO VERIFIED. SO AGREED.** 🕯️
