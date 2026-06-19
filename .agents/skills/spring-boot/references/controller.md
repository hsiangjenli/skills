# Controller

Use this reference for controllers, request and response DTOs, and API validation.

## Workflow

1. Define the shared request and response envelope first.
2. Define request and response DTOs per endpoint or use case.
3. Delegate business logic to services.
4. Let the service layer produce the response body.
5. Return `ResponseEntity<Response<TBody>>`.

## Envelope

| Part | Rule |
| --- | --- |
| Request | Define a shared `Request<TBody>` first |
| Response | Define a shared `Response<TBody>` first |
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

## DTO Guidance

- Prefer `record` for DTOs.
- Prefer separate request and response DTOs per endpoint or use case.
- Put endpoint-specific DTO fields in `body`, not in the shared header.
- Let services produce response bodies; controllers should wrap them in the shared response envelope.
- Avoid passing entities directly across controller boundaries.

## Validation Guidance

- Put bean validation annotations on request models when the contract requires them.