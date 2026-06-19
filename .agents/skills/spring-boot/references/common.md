# Common

Use this reference for project setup and shared Spring Boot conventions.

## Defaults

- Maven
- Spring Boot 4.1.0
- a Java version supported by the target Spring Boot release
- Java 25 only when the project explicitly targets the latest JDK
- no database by default
- PostgreSQL and Redis as the only optional infra
- Podman Compose, not Docker Compose

## Setup Flow

1. Confirm project name, package name, Java version, and required modules.
2. Ask the user for the project name before generating the project.
3. Generate the project from Spring Initializr with only the selected dependencies.
4. Generate only the config files required by the selected modules.
5. Add Podman Compose only when PostgreSQL or Redis is needed locally.
6. Run tests before adding feature code.

## Dependency Selection

- Usually keep: `web`, `validation`, `lombok`, `configuration-processor`.
- Add `data-jpa` and `postgresql` only when persistence is required.
- Add `data-redis` only when caching, session, queue-like, or key-value use cases exist.
- Add `springdoc-openapi` only when the API should expose Swagger UI.
- Add `testcontainers` only when the project actually runs integration tests against real services.

## Starter Template

```sh
curl https://start.spring.io/starter.zip \
  -d artifactId=<project-name> \
  -d bootVersion=4.1.0 \
  -d dependencies=web,validation,lombok,configuration-processor \
  -d javaVersion=<java-version> \
  -d packageName=com.example.app \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

Replace `<project-name>` with the user input.

Replace `<java-version>` with the chosen version.

## Config Checklist

- Generate a minimal `application.yml` or `application.properties`.
- Add PostgreSQL settings only when `data-jpa,postgresql` is selected.
- Add Redis settings only when `data-redis` is selected.
- Generate `compose.yaml` only when local PostgreSQL or Redis is needed.
- Use `podman compose up -d` and `podman compose down`.
- Do not add placeholders for unused services.

## Naming Rules

| Type | Suffix |
| --- | --- |
| Controller | `Controller` |
| Service interface | `Service` |
| Service implementation | `ServiceImpl` |
| Entity | `Entity` |
| Repository | `Repository` |
| Configuration | `Configuration` |
| Request DTO | `RequestBody` |
| Response DTO | `ResponseBody` |

## Package Rules

- Avoid deep package nesting unless the domain size really needs it.
- Start simple with top-level packages such as `controller/`, `service/`, `repository/`, `entity/`, `config/`, and `dto/`.
- If the domain grows, split by domain under the layer package rather than adding many nested levels.

```text
service/
  BookService.java
  BookServiceImpl.java
```

```text
service/
  book/
    BookService.java
    BookServiceImpl.java
  school/
    SchoolService.java
    SchoolServiceImpl.java
```

## Service Structure

- Define a service interface by default.
- Add a matching `ServiceImpl` implementation by default.
- Keep this pattern even when there is only one implementation, because multiple implementations are expected.