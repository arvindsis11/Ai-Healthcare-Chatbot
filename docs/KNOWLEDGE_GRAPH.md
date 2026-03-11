# Healthcare Knowledge Graph Design

## Entities

- `Symptom`
- `Condition`
- `Medication`
- `Specialist`

## Relationships

- `Symptom` -> `Condition` (`indicates`)
- `Condition` -> `Medication` (`treated_by`)
- `Condition` -> `Specialist` (`managed_by`)

## Example Subgraph

```text
fever -> viral infection
viral infection -> antipyretics
viral infection -> general physician
```

## Integration Plan

1. Build graph index from curated medical datasets.
2. Add graph traversal retrieval before LLM generation.
3. Inject graph-derived evidence as citations.
4. Track provenance and confidence score per edge.
