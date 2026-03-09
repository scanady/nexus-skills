---
applyTo: "backend/**/*.java"
---
# Java Backend Coding Guidelines

## PostgreSQL Enum Type Mapping

When mapping Java enums to PostgreSQL native enum types (created with `CREATE TYPE`), use Hibernate 6's built-in `PostgreSQLEnumJdbcType`:

```java
@Enumerated(EnumType.STRING)
@JdbcType(PostgreSQLEnumJdbcType.class)
@Column(name = "status", columnDefinition = "my_status_type")
private MyStatus status;
```

Required imports:
```java
import org.hibernate.annotations.JdbcType;
import org.hibernate.dialect.PostgreSQLEnumJdbcType;
```

**DO NOT** use just `@Enumerated(EnumType.STRING)` without `@JdbcType(PostgreSQLEnumJdbcType.class)` - this causes "column is of type X but expression is of type character varying" errors.

## Existing PostgreSQL Enum Types
- `offering_type` - AD_HOC, SESSION_PACKAGE, PREDEFINED_PROGRAM
- `component_type` - COACHING, WORKSHOP, ASSESSMENT, etc.
- `booking_status` - PENDING, CONFIRMED, CANCELLED, COMPLETED, NO_SHOW, RESCHEDULED

## JSON Columns
For JSONB columns:
```java
@JdbcTypeCode(SqlTypes.JSON)
@Column(name = "metadata", columnDefinition = "jsonb")
private Map<String, Object> metadata;
```

## Array Columns
For PostgreSQL TEXT arrays, you **MUST** use `@JdbcTypeCode(SqlTypes.ARRAY)`:
```java
@JdbcTypeCode(SqlTypes.ARRAY)
@Column(name = "delivery_modes", columnDefinition = "TEXT[]")
private List<String> deliveryModes;
```

Required import:
```java
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
```

**DO NOT** omit `@JdbcTypeCode(SqlTypes.ARRAY)` - this causes `IllegalArgumentException: Could not deserialize string to java type: java.util.List<java.lang.String>` errors at runtime.

## Lazy Loading & LazyInitializationException Prevention

**CRITICAL:** Hibernate's default `FetchType.LAZY` for `@ManyToOne` and `@OneToOne` associations causes `LazyInitializationException` when accessed outside a transaction/session. This is a recurring issue in this codebase.

### The Problem
When a DTO is created from an entity returned by a repository query, accessing lazy-loaded relationships **after** the transaction closes throws:
```
LazyInitializationException: could not initialize proxy [Entity#id] - no Session
```

### Common Pattern That Causes Issues
```java
// Repository returns entities with LAZY relationships
List<Booking> bookings = bookingRepository.findByCoachProfileId(coachId, pageable);

// DTO mapping happens OUTSIDE the transaction - LAZY LOAD FAILS
List<BookingResponse> responses = bookings.stream()
    .map(b -> BookingResponse.from(b, photoUrl))  // Accesses b.getCoachProfile().getDisplayName() → BOOM
    .toList();
```

### The Fix: Eager Fetch in Repository Queries
**Always** use `JOIN FETCH` in repository queries when the fetched entities will be mapped to DTOs:

```java
// ❌ BAD - Lazy relationships will fail when accessed in DTO mapping
@Query("SELECT b FROM Booking b WHERE b.coachProfileId = :coachId")
Page<Booking> findByCoachProfileId(@Param("coachId") UUID coachId, Pageable pageable);

// ✅ GOOD - Eagerly fetch all relationships needed for DTO mapping
@Query("SELECT b FROM Booking b " +
       "LEFT JOIN FETCH b.coachProfile cp " +
       "LEFT JOIN FETCH cp.user " +           // Fetch nested user!
       "LEFT JOIN FETCH b.clientProfile clp " +
       "LEFT JOIN FETCH clp.user " +          // Fetch nested user!
       "LEFT JOIN FETCH b.service " +
       "WHERE b.coachProfileId = :coachId")
Page<Booking> findByCoachProfileId(@Param("coachId") UUID coachId, Pageable pageable);
```

### Key Rules
1. **Trace the DTO mapping code** - Identify ALL entity relationships accessed during `Entity → DTO` conversion
2. **Fetch nested relationships** - If `Booking.coachProfile.user.displayName` is accessed, fetch BOTH `coachProfile` AND `coachProfile.user`
3. **Use LEFT JOIN FETCH** - Prevents null pointer exceptions when relationships are optional
4. **Add aliases for nested fetches** - `LEFT JOIN FETCH b.coachProfile cp LEFT JOIN FETCH cp.user` (alias `cp` is required to fetch nested `user`)

### When to Use @Transactional Instead
Use `@Transactional(readOnly = true)` on the service method if:
- The query is complex and multiple lazy loads are acceptable
- You need to access many different lazy relationships conditionally
- The fetch join would create a Cartesian product (multiple collections)

```java
@Transactional(readOnly = true)
public List<BookingResponse> getBookingsWithDetails(UUID coachId) {
    // Session stays open, lazy loading works
    List<Booking> bookings = bookingRepository.findByCoachProfileId(coachId);
    return bookings.stream().map(this::toResponse).toList();
}
```

### DTO Mapping Checklist
Before writing a `SomeResponse.from(entity)` or `toResponse(entity)` method:
1. List ALL entity fields/relationships accessed in the mapping
2. Verify the repository query fetches them eagerly
3. If mapping accesses `entity.relationship.nestedRelationship`, ensure BOTH are fetched
