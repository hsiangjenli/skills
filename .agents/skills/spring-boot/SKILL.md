---
name: spring-boot
description: Build or extend Spring Boot applications with a phase-aware workflow. Use when the task involves project setup, testing, controller-service-repository structure, DTO and entity design, persistence, or routine Spring Boot development decisions.
---

# Spring Boot Development

Use this skill for routine Spring Boot work. Read only the matching file in `references/`.

## Use This Skill When

- setting up a Spring Boot project
- adding or changing controller, service, DTO, entity, or repository code
- deciding test scope for a Spring Boot change

## Workflow

1. Identify the phase: setup, web, persistence, or testing.
2. Read the matching reference file only.
3. Reuse project conventions.
4. Make the smallest coherent change.
5. Run the narrowest validation.

## Reference Map

- For creating or aligning a new project, read `references/project-init.md`.
- For controller, service, DTO, and validation work, read `references/web-layer.md`.
- For entity, repository, and transactional persistence work, read `references/persistence.md`.
- For test scope, slice selection, and test data setup, read `references/testing.md`.

## Rules

- Keep controller, service, and persistence concerns separate.
- Do not add DTOs, entities, mappers, or repositories unless the use case needs them.
- Treat tests as part of the change.
- Check Spring docs when behavior is version-sensitive.

## Quick Decisions

- Use a DTO when the API contract differs from the persistence model or needs request validation.
- Use an entity only for persisted domain state.
- Add mapping code only when both DTOs and entities exist.
- Split services only when they have multiple reasons to change.
