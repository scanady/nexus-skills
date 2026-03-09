---
applyTo: "**/*.java"
---
# Java Coding Standards

## Naming Conventions
- Use `PascalCase` for classes, interfaces, enums, and records
- Use `camelCase` for methods, variables, and parameters
- Use `UPPER_SNAKE_CASE` for constants (`static final`)
- Prefix interfaces with behavior names, not `I`: `Serializable`, `Comparable` — not `ISerializable`
- Name boolean methods with `is`, `has`, `can`, `should`: `isValid()`, `hasPermission()`
- Name factory methods with `of`, `from`, `create`: `Duration.ofMinutes(5)`
- Use plural names for collections: `List<User> users`, not `List<User> userList`

## Code Style
- Prefer `var` for local variables when the type is obvious from the right-hand side
- Prefer records over classes for immutable data carriers
- Prefer `sealed` interfaces/classes when the set of subtypes is known and fixed
- Use `Optional` for return types that may be absent — never for fields or parameters
- Prefer `Stream` operations over manual loops for collection transformations
- Use `switch` expressions (with `->`) instead of `switch` statements where possible
- Prefer text blocks (`"""`) for multi-line strings
- Limit line length to 120 characters

## Immutability
- Make fields `final` by default — only remove `final` when mutation is required
- Return unmodifiable collections from public methods: `List.copyOf()`, `Collections.unmodifiableList()`
- Use `List.of()`, `Set.of()`, `Map.of()` for small immutable collections
- Prefer records or `@Value` objects for DTOs and value types

## Error Handling
- Never catch `Exception` or `Throwable` broadly — catch specific exception types
- Never swallow exceptions with empty catch blocks
- Use custom exception classes for domain-specific errors, extending `RuntimeException`
- Include contextual information in exception messages: entity IDs, operation names, input values
- Use `try-with-resources` for all `AutoCloseable` resources
- Prefer unchecked exceptions over checked exceptions for business logic errors
- Log exceptions at the boundary where they are handled, not where they are rethrown

```java
// Correct: specific exception with context
throw new OrderNotFoundException("Order not found: orderId=" + orderId);

// Incorrect: generic exception, no context
throw new RuntimeException("not found");
```

## Null Safety
- Never return `null` from a method — use `Optional`, an empty collection, or a default value
- Annotate parameters and return types with `@Nullable` / `@NonNull` when using nullability annotations
- Use `Objects.requireNonNull()` for validating constructor and method parameters at entry points
- Prefer `Optional.map()` / `Optional.orElseThrow()` chains over `if (x != null)` nesting

```java
// Correct: Optional chain
String displayName = userRepository.findById(id)
    .map(User::getDisplayName)
    .orElseThrow(() -> new UserNotFoundException("User not found: id=" + id));

// Incorrect: null check nesting
User user = userRepository.findById(id).orElse(null);
if (user != null) {
    return user.getDisplayName();
}
throw new RuntimeException("not found");
```

## Collections and Streams
- Prefer `List.of()` / `Set.of()` / `Map.of()` over `Arrays.asList()` or `new ArrayList<>()`
- Use `Collectors.toList()` or `.toList()` (Java 16+) at the end of stream pipelines
- Avoid multi-line lambdas in streams — extract to a named method
- Prefer `map` + `filter` over `forEach` with conditionals
- Use `flatMap` to flatten nested collections

## Method Design
- Keep methods under 30 lines — extract helper methods for complex logic
- Limit parameters to 3 — use a parameter object or builder for more
- Return early to reduce nesting: guard clauses at the top of methods
- Make methods `static` when they do not access instance state
- Use method references (`User::getName`) over lambdas (`u -> u.getName()`) when readable

## Class Design
- One top-level public class per file
- Order members: static fields, instance fields, constructors, public methods, private methods
- Prefer composition over inheritance — use interfaces and delegation
- Keep classes focused on a single responsibility
- Mark classes `final` if they are not designed for extension
- Use the builder pattern for objects with more than 3 constructor parameters

## Testing
- Name test methods descriptively: `shouldReturnEmptyList_whenNoResultsFound()`
- Follow Arrange-Act-Assert (AAA) structure in every test
- One assertion concept per test method — multiple `assert` calls are fine if they verify one behavior
- Use `@ParameterizedTest` for testing multiple inputs against the same logic
- Prefer `assertThat` (AssertJ) over `assertEquals` / `assertTrue` for readable assertions
- Mock external dependencies only — do not mock the class under test

```java
// Correct: descriptive name, AAA structure, AssertJ
@Test
void shouldReturnActiveUsers_whenStatusFilterIsActive() {
    // Arrange
    var users = List.of(activeUser, inactiveUser);
    when(userRepository.findAll()).thenReturn(users);

    // Act
    var result = userService.findByStatus(Status.ACTIVE);

    // Assert
    assertThat(result).containsExactly(activeUser);
}
```

## Dependency Injection
- Use constructor injection exclusively — never field injection (`@Autowired` on fields)
- Mark injected fields `final`
- Use `@RequiredArgsConstructor` (Lombok) or explicit constructors for injection
- Prefer interface types in constructor parameters: `List` over `ArrayList`, `UserService` over `UserServiceImpl`

```java
// Correct: constructor injection with final fields
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final PaymentGateway paymentGateway;
}

// Incorrect: field injection
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
}
```

## Logging
- Use SLF4J with parameterized messages — never string concatenation
- Log at appropriate levels: `ERROR` for failures, `WARN` for recoverable issues, `INFO` for business events, `DEBUG` for troubleshooting
- Include correlation IDs and entity identifiers in log messages
- Never log sensitive data: passwords, tokens, PII, credit card numbers

```java
// Correct: parameterized SLF4J
log.info("Order created: orderId={}, userId={}", order.getId(), userId);

// Incorrect: string concatenation
log.info("Order created: " + order.getId() + " for user " + userId);
```

## Concurrency
- Use `ExecutorService` or `CompletableFuture` over raw `Thread` creation
- Prefer `ConcurrentHashMap` over `Collections.synchronizedMap()`
- Use `AtomicInteger` / `AtomicReference` over `synchronized` blocks for simple atomic operations
- Make shared mutable state explicit and documented — prefer immutable data structures

## API Design
- Use meaningful HTTP status codes in REST endpoints
- Validate request payloads at the controller layer with `@Valid` and Bean Validation annotations
- Return consistent response envelopes for error responses
- Use `@PathVariable` for resource identity, `@RequestParam` for filtering/sorting
- Version APIs via URL path (`/api/v1/`) only when breaking changes are unavoidable
