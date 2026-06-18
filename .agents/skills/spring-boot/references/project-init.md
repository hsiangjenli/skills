# Project Initialization

Use this reference when creating a new Spring Boot project. Keep the base project small and choose dependencies from actual needs.

## Defaults

- Prefer Maven.
- Prefer Spring Boot 4.1.0.
- Prefer Java 25.
- Do not add a database by default.
- Only keep PostgreSQL and Redis as optional infra.
- Use Podman Compose, not Docker Compose.

## Dependency Selection

Start with a small core, then add only the needed modules.

- Usually keep: `web`, `validation`, `lombok`, `configuration-processor`.
- Add `data-jpa` and `postgresql` only when persistence is required.
- Add `data-redis` only when caching, session, queue-like, or key-value use cases exist.
- Add `springdoc-openapi` only when the API should expose Swagger UI.
- Add `testcontainers` only when the project actually runs integration tests against real services.

## Bootstrap Flow

1. Confirm project name, package name, Java version, and required modules.
2. Ask the user for the project name before generating the project.
3. Generate the project from Spring Initializr with only the selected dependencies.
4. Add infra config only for the services the project really uses.
5. Add Podman Compose only when PostgreSQL or Redis is needed locally.
6. Run tests before adding feature code.

## Starter Template

Adjust the dependency list before running:

```sh
curl https://start.spring.io/starter.zip \
  -d artifactId=<project-name> \
  -d bootVersion=4.1.0 \
  -d dependencies=web,validation,lombok,configuration-processor \
  -d javaVersion=25 \
  -d packageName=com.example.app \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

Replace `<project-name>` with the name provided by the user.

If the project needs persistence, extend `dependencies` with `data-jpa,postgresql`.

If the project needs Redis, extend `dependencies` with `data-redis`.

## Configurations

Generate configuration files from the selected modules instead of writing every service config by default.

- Always generate a minimal `application.yml` or `application.properties`.
- Add PostgreSQL settings only when `data-jpa,postgresql` is selected.
- Add Redis settings only when `data-redis` is selected.
- Generate `compose.yaml` only when local PostgreSQL or Redis is needed.
- Use Podman Compose commands in examples and workflow text.

Keep generated config small. Do not add placeholders for services the project does not use.

## Local Infra

- If PostgreSQL is needed, add datasource and JPA settings.
- If Redis is needed, add Redis connection settings.
- Do not add MongoDB or other databases in this default path.
- Add Podman Compose only for the selected services.

Example local infra choices:

- PostgreSQL only
- Redis only
- PostgreSQL + Redis

Use `podman compose up -d` and `podman compose down` for local service lifecycle.

## Package Shape

If the repo has no convention, start with:

```text
com.example.app
  controller
  service
  repository
  dto
  mapper
  config
```

## Validation

After setup:

- run the default test task first,
- start local infra only if the project uses it,
- then run the application.