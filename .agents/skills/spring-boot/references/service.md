# Service

Use this reference for use-case logic, orchestration, and transaction boundaries.

## Rules

- Keep one service method aligned to one use case where practical.
- Keep controllers thin and move business logic into services.
- Define a `*Service` interface and a matching `*ServiceImpl` by default.
- Place transaction boundaries in services.
- Annotate write or mixed use cases with `@Transactional`.
- Use `@Transactional(readOnly = true)` for read-only use cases when the project already follows that pattern.
- Keep transaction scope small and aligned to a use case.
- Keep repository access focused on persistence concerns and map data at the service boundary when needed.
- Return the response body DTO, domain result, or command result expected by the controller contract; avoid leaking repository-specific shapes upward.
- Use dedicated mapper classes or methods when the same conversion is repeated across multiple service methods.
- Avoid embedding repository queries or persistence branching inside controllers.
