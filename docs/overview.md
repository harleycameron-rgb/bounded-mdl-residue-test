# Project Overview

## Documentation Map

- [Repository README](../README.md)
- [Vendor Integration Guide](vendor_integration.md)

## Architecture

The repository joins two deterministic layers:

1. the reference MDL benchmark in `REFERENCE_IMPLEMENTATION/`
2. the bounded multi-agent analysis framework in `multi_agent/` and `analysis/`

The reference layer produces stable benchmark artifacts. The network layer carries those artifacts forward as agent state vectors so drift propagation, residue transfer, and alignment divergence can be measured round by round.
