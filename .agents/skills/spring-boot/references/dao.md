# DAO

Use this reference for entities, repositories, mappers, and persistence details.

## Repository Rules

- Use Spring Data JPA repositories.
- Prefer derived queries first.
- Use JPQL or another explicit query mechanism when a derived query is no longer clear.
- Do not put business rules in repositories.

## Entity Rules

- Model persisted domain state in entities.
- Keep entity fields aligned with storage concerns.
- Avoid turning DTO-only data into entity fields.
- Add validation only for domain or persistence invariants that belong on the entity.
- Use bidirectional relationships only when the domain and query pattern justify them.

## Mapping

- Use MapStruct for DTO <-> Entity mapping when the project standard includes MapStruct.
- Map entities to the request and response DTOs defined by the controller layer.
- Support single object mapping and list mapping.
- Add explicit mapper methods for create request DTO -> entity.
- Add explicit mapper methods for update request DTO -> existing entity.
- Add explicit mapper methods for entity -> response DTO.
- Add explicit mapper methods for `List<Entity>` -> `List<ResponseDto>` when an endpoint returns collections.
- Do not hand-write repetitive mapping code unless the project already has a clear reason to avoid MapStruct.