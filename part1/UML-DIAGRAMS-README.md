# HBnB Part 2 - UML Diagrams

This directory contains all UML diagrams for the HBnB project Part 2 implementation.

## Overview

These diagrams document the architecture, relationships, and behavior of the HBnB application using Mermaid syntax.

## Diagram Files

### 1. Package Diagram (`1-package-diagram.mmd`)
**Purpose:** Shows the 3-layer architecture with Facade pattern

**Layers:**
- **Presentation Layer (API)**: Flask RESTx endpoints
- **Business Logic Layer**: Models and Facade
- **Persistence Layer**: Repository pattern

**Key Concept:** The Facade acts as the single entry point from API to Business Logic, simplifying communication and hiding complexity.

---

### 2. Class Diagram (`2-class-diagram.mmd`)
**Purpose:** Shows all entity models, their attributes, methods, and relationships

**Classes:**
- `BaseModel` - Base class with common attributes (id, timestamps)
- `User` - User entity
- `Amenity` - Amenity entity (WiFi, Pool, etc.)
- `Place` - Place entity (rental property)
- `Review` - Review entity
- `MemoryRepository` - Data storage
- `HbnbFacade` - Business logic orchestrator

**Relationships:**
- Place → User (owner_id)
- Place → Amenity (amenity_ids - many-to-many)
- Review → User (user_id)
- Review → Place (place_id)

---

### 3. Sequence Diagram: Create Place (`3-sequence-create-place.mmd`)
**Purpose:** Shows the flow when creating a new place

**Flow:**
1. Client sends POST request with place data
2. API calls Facade
3. Facade validates owner exists
4. Facade validates all amenities exist
5. Facade creates and validates Place model
6. Facade saves to repository
7. Facade expands response with owner and amenity details
8. API returns 201 Created

**Key Validations:**
- Owner must exist
- All amenities must exist
- Price, coordinates must be valid

---

### 4. Sequence Diagram: Get Place Reviews (`4-sequence-get-place-reviews.mmd`)
**Purpose:** Shows the flow when getting all reviews for a specific place

**Flow:**
1. Client requests reviews for place_id
2. API calls Facade
3. Facade queries repository with predicate filter
4. Repository returns matching reviews
5. API returns 200 OK with review list

**Key Feature:** Uses predicate filtering in repository layer

---

### 5. Sequence Diagram: Create User (`5-sequence-create-user.mmd`)
**Purpose:** Shows the complete flow including validation and error handling

**Flow:**
1. Client sends POST with user data
2. API calls Facade
3. Facade checks for duplicate email
4. If duplicate: return 409 Conflict
5. If unique: create User model
6. User validates itself (email format, required fields)
7. Facade saves to repository
8. Facade removes password from response
9. API returns 201 Created

**Key Features:**
- Duplicate email detection
- Email format validation
- Password excluded from response

---

### 6. Sequence Diagram: Update Place (`6-sequence-update-place.mmd`)
**Purpose:** Shows the complex validation when updating a place

**Flow:**
1. Client sends PUT with updates
2. API calls Facade
3. Facade retrieves existing place (404 if not found)
4. If owner_id changed: validate new owner exists
5. If amenity_ids changed: validate all amenities exist
6. Update place attributes
7. Call place.validate()
8. Update timestamp with touch()
9. Save to repository
10. Expand response with owner and amenities
11. Return 200 OK

**Key Features:**
- Partial updates allowed
- Foreign key validation
- Automatic timestamp update
- Extended response with related data

---

### 7. Sequence Diagram: Delete Review (`7-sequence-delete-review.mmd`)
**Purpose:** Shows the DELETE operation (only available for reviews)

**Flow:**
1. Client sends DELETE request
2. API calls Facade
3. Facade checks if review exists
4. If not found: return 404
5. If exists: delete from repository
6. Return 204 No Content

**Key Note:** Review is the only entity with DELETE in Part 2

---

## How to View These Diagrams

### Option 1: GitHub/GitLab
If you push to GitHub or GitLab, Mermaid diagrams render automatically in `.md` or `.mmd` files.

### Option 2: VS Code
Install the **Mermaid Preview** extension:
1. Open VS Code
2. Install "Markdown Preview Mermaid Support" or "Mermaid Editor"
3. Right-click `.mmd` file → "Open Preview"

### Option 3: Online Mermaid Editor
1. Visit https://mermaid.live/
2. Copy the content of any `.mmd` file
3. Paste and view the rendered diagram

### Option 4: Mermaid CLI
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Render diagram to PNG
mmdc -i 1-package-diagram.mmd -o package-diagram.png

# Render all diagrams
for file in *.mmd; do mmdc -i "$file" -o "${file%.mmd}.png"; done
```

### Option 5: Documentation Tools
Many documentation generators support Mermaid:
- **MkDocs** with `mkdocs-mermaid2-plugin`
- **Sphinx** with `sphinxcontrib-mermaid`
- **Docusaurus** has built-in support
- **Notion** supports Mermaid blocks

---

## Understanding the Architecture

### The 3-Layer Pattern

```
┌─────────────────────────────────┐
│   Presentation Layer (API)       │
│   - HTTP requests/responses      │
│   - JSON serialization           │
│   - Input validation             │
└──────────────┬──────────────────┘
               │ Uses
               ▼
┌─────────────────────────────────┐
│   Business Logic Layer           │
│   - Models (User, Place, etc.)   │
│   - Validation rules             │
│   - Business rules               │
│   - Facade (orchestration)       │
└──────────────┬──────────────────┘
               │ Uses
               ▼
┌─────────────────────────────────┐
│   Persistence Layer              │
│   - Data storage (memory/DB)     │
│   - Repository pattern           │
└─────────────────────────────────┘
```

### The Facade Pattern

The Facade acts as a **simplified interface** to the Business Logic:

**Without Facade:**
```
API → User Model
API → Place Model → User Model → Repository
API → Repository
API → Amenity Model → Repository
API → Review Model → Place Model → User Model
```

**With Facade:**
```
API → Facade → {handles all the complexity}
```

Benefits:
- API stays simple
- Business logic changes don't affect API
- Single point of coordination
- Easier to test

### Key Design Decisions

1. **Dataclasses** - Clean, modern Python with less boilerplate
2. **Repository Pattern** - Easy to swap in-memory for database
3. **Extended Responses** - Places include full owner + amenities (not just IDs)
4. **Validation in Models** - Each model validates itself
5. **Password Security** - Never returned in responses
6. **Foreign Key Validation** - Ensures data integrity

---

## Diagram Conventions

### Sequence Diagrams
- **Solid arrows (→)**: Synchronous calls
- **Dashed arrows (- -)**: Returns
- **Note boxes**: Important logic or validation
- **alt/else**: Conditional flows (if/else)
- **loop**: Repeated operations

### Class Diagrams
- **+** Public attribute/method
- **-** Private attribute/method
- **Inheritance** (|--): BaseModel is parent
- **Association** (→): One class uses another

### Package Diagrams
- **Boxes**: Layers or modules
- **Arrows**: Dependencies/usage

---

## Relationship Types

### One-to-Many
- **User → Places**: One user owns many places
- **Place → Reviews**: One place has many reviews
- **User → Reviews**: One user writes many reviews

### Many-to-Many
- **Place ↔ Amenities**: Many places have many amenities, and amenities belong to many places

---

## Error Handling Flows

All sequence diagrams show error handling:

**Common Error Codes:**
- `400 Bad Request` - Validation failed, invalid data
- `404 Not Found` - Resource doesn't exist
- `409 Conflict` - Duplicate email (future feature)

**Error Flow Example:**
```
Client → API → Facade → Repository
                ↓ (resource not found)
Client ← API ← raise NotFound
(404)
```

---

## Testing with Diagrams

Use these diagrams to:
1. **Understand expected behavior** before coding
2. **Design test cases** based on sequence flows
3. **Debug issues** by tracing the flow
4. **Document** your implementation decisions

---

## Extending the Diagrams

If you add new features in Part 3:

### For new endpoints:
1. Add to package diagram (new namespace)
2. Update class diagram if new models
3. Create sequence diagram for complex flows

### For database integration:
1. Update persistence layer in package diagram
2. Add SQLAlchemy classes to class diagram
3. Update sequence diagrams to show DB transactions

### For authentication:
1. Add auth middleware to package diagram
2. Update sequence diagrams to show token validation
3. Document JWT flow with new sequence diagram

---

## Quick Reference

| Diagram | Use Case | Key Insight |
|---------|----------|-------------|
| Package | Understanding overall structure | 3 layers + Facade |
| Class | Entity relationships | How models connect |
| Create Place | Complex validation | Multi-step foreign key checks |
| Get Reviews | Simple query | Filtering with predicates |
| Create User | Error handling | Duplicate detection |
| Update Place | Partial updates | Selective validation |
| Delete Review | DELETE operation | Only entity with delete |

---

## Additional Resources

- **Mermaid Documentation**: https://mermaid.js.org/
- **UML Overview**: https://www.uml.org/
- **Sequence Diagrams**: https://mermaid.js.org/syntax/sequenceDiagram.html
- **Class Diagrams**: https://mermaid.js.org/syntax/classDiagram.html
- **Architecture Patterns**: Martin Fowler's patterns catalog

---

## Next Steps

1. **Review each diagram** to understand the flow
2. **Compare with actual code** in part2/
3. **Trace a request** through all layers using sequence diagrams
4. **Plan Part 3 changes** by updating these diagrams first

Good luck with your implementation! 🚀
