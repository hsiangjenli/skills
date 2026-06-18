---
name: spring-boot
description: Build or extend Spring Boot applications with a phase-aware workflow. Use when the task involves project setup, testing, controller-service-repository structure, DTO and entity design, persistence, or routine Spring Boot development decisions.
---

# Spring Boot Development

Use this skill for routine Spring Boot work. Read only the matching file in `references/`.

## Use This Skill When

| Situation | Use this skill |
| --- | --- |
| Project setup | Create or align a Spring Boot project |
| Application changes | Add or change controller, service, DTO, entity, or repository code |
| Testing | Decide test scope for a Spring Boot change |

## Workflow

1. Identify the phase: setup, web, persistence, or testing.
2. Read the matching reference file only.
3. Reuse project conventions.
4. Make the smallest coherent change.
5. Run the narrowest validation.

## Reference Map

| Topic | Reference |
| --- | --- |
| Project setup and shared conventions | `references/common.md` |
| Controller, request, response, and API validation | `references/controller.md` |
| Use-case logic and transaction boundaries | `references/service.md` |
| Entity, repository, mapper, and persistence | `references/dao.md` |
| Test scope and validation checks | `references/unit-test.md` |

## Rules

| Rule | Meaning |
| --- | --- |
| Separate layers | Keep controller, service, and persistence concerns separate |
| Add only what is needed | Do not add DTOs, entities, mappers, or repositories unless the use case needs them |
| Test with the change | Treat tests as part of the change |
| Check version-sensitive behavior | Check Spring docs when behavior is version-sensitive |

## Quick Decisions

| Decision | Default |
| --- | --- |
| When to use a DTO | When the API contract differs from the persistence model or needs request validation |
| When to use an entity | Only for persisted domain state |
| When to add mapping | When both DTOs and entities exist |
| When to split services | When they have multiple reasons to change |
