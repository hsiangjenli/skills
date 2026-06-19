# Controller

Use this reference for controllers, request and response DTOs, and API validation.

## Workflow

1. Define the shared request and response envelope first.
2. Define the shared error envelope alongside the response envelope.
3. Define request and response DTOs per endpoint or use case.
4. Delegate business logic to services.
5. Let the service layer produce the response body.
6. Return `ResponseEntity<Response<TBody>>` for success and let `@RestControllerAdvice` build `ResponseEntity<ErrorResponse<TBody>>` for failure.

## Envelope

| Part | Rule |
| --- | --- |
| Request | Define a shared `Request<TBody>` first |
| Response | Define a shared `Response<TBody>` first |
| Error response | Define a shared `ErrorResponse<TBody>` with the same envelope shape |
| Header | Keep a fixed header format |
| Body | Put the actual request or response DTO in `body` |

Use a fixed header structure for all APIs so routing and cross-cutting fields stay consistent.

| Header field | Purpose |
| --- | --- |
| `apiCode` | API code used by BL routing to route to the target endpoint |
| `sourceChannel` | Request source |
| `txnSequence` | Transaction id shared across the whole transaction flow |
| `returnCode` | Response result code |
| `returnMessage` | Response result message |

| Header rule | Meaning |
| --- | --- |
| Request to response | Response header should inherit from request header |
| Cross-API flow | Reuse the same `txnSequence` when one transaction calls multiple APIs |
| Request status fields | `returnCode` and `returnMessage` stay empty on request |
| Response status | `returnCode` and `returnMessage` are filled on response |
| Contract changes | Keep envelope changes centralized in shared request and response types |

```java
public record Header(
	String apiCode,
	String sourceChannel,
	String txnSequence,
	String returnCode,
	String returnMessage
) {}

public record Request<TBody>(
	Header header,
	TBody body
) {}

public record Response<TBody>(
	Header header,
	TBody body
) {}

public record ErrorResponse<TBody>(
	Header header,
	TBody body
) {}

@PostMapping("/createUser")
public ResponseEntity<Response<CreateUserResponseBody>> createUser(
	@RequestBody Request<CreateUserRequestBody> request
) {
	CreateUserResponseBody responseBody = userService.createUser(request.body());
	Header responseHeader = new Header(
		request.header().apiCode(),
		request.header().sourceChannel(),
		request.header().txnSequence(),
		"SUCCESS",
		"User created successfully"
	);
	Response<CreateUserResponseBody> response = new Response<>(responseHeader, responseBody);
	return ResponseEntity.ok(response);
}
```

## Error Envelope

- Populate the header with the same routing and transaction fields as the request when they are available.
- Use `returnCode` and `returnMessage` to describe the error at the protocol level.
- Keep the `body` field in the error response even when it is empty.
- Let controllers stay focused on success flow; the advice layer should translate failures.

## DTO Guidance

- Prefer `record` for DTOs.
- Prefer separate request and response DTOs per endpoint or use case.
- Put endpoint-specific DTO fields in `body`, not in the shared header.
- Let services produce response bodies; controllers should wrap them in the shared response envelope.
- Avoid passing entities directly across controller boundaries.
- Keep error responses on the same envelope shape; use an empty body when no error detail is returned.

## Validation Guidance

- Put bean validation annotations on request models when the contract requires them.
