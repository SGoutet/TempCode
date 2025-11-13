# General rules
- Use context7
- Set secrets and authentication tokens as environment variables
- Unit test all the code
- Save tests in "test" folder 
- Use 4 spaces indentation by default
- Documents modules, classes and functions with inputs and outputs
- Document the most complex parts of the code, but avoid inline documentation when not necessary
- Use the repository pattern
- Favor Separation of Concerns, reusability and maintainability
- Clearly separate front-end and back-end
- Adopt descriptive and meaningful names and avoid abbreviations where possible
- Provide specific examples from the code as a support
- Test that functions inputs conform to requirements


# Python rules
- Use type annotations
- Use PEP-8
- use camel case for classes, lower case with underscores for functions and variables
- Add docstrings to all functions, readable, not too long, but containing a short description and parameters types and description

# FastAPI rules

- Use type hints for all function parameters and return values
- Use Pydantic models for request and response validation
- Use appropriate HTTP methods with path operation decorators (@app.get, @app.post, etc.)
- Use dependency injection for shared logic like database connections and authentication
- Use background tasks for non-blocking operations
- Use proper status codes for responses (201 for creation, 404 for not found, etc.)
- Use APIRouter for organizing routes by feature or resource
- Use path parameters, query parameters, and request bodies appropriately
- Use robotframework for API testing


# Typescript and javascript coding and formatting rules
1. Indentation and Spacing
-	Use 2 spaces per indentation level (default in Prettier).
-	Always add a space after commas, colons, and semicolons.
-	Use spaces around operators (, , , etc.).
-	Avoid trailing spaces at the end of lines.
2. Semicolons
-	Always use semicolons to terminate statements. This avoids automatic semicolon insertion issues.
3. Quotation Marks
-	Prefer single quotes () over double quotes () for strings.
-	Use backticks () for template literals.
4. Line Length
-	Limit lines to 80–100 characters for better readability.
-	Break long function calls or object literals across multiple lines.
5. Braces and Blocks
-	Use curly braces for all blocks, even single-line , , or  statements.
-	Place opening braces on the same line as the statement.
6. Arrow Functions
-	Use arrow functions for anonymous callbacks and concise function expressions.
-	Prefer for declaring arrow functions.
7. Type Annotations
- Always annotate function parameters and return types.
- Use  or  for defining object shapes.
- Avoid using  unless absolutely necessary.
8. Imports and Exports
- Use ES module syntax ( / ) consistently.
- Group imports: third-party, internal modules, then styles/assets.
- Avoid default exports unless necessary — named exports are clearer.
9. Variable Declarations
- Use  for values that don’t change,  otherwise.
- Avoid  entirely.
- Use descriptive names and avoid abbreviations.
10. Comments
- Use  for inline comments and  for documentation.
- Leave a space after  and capitalize the first word.


# Testing Guidelines

## Testing Framework
- `vitest` is used for testing
- Tests are colocated next to the tested file
  - Example: `dir/format.ts` and `dir/format.test.ts`
- Use Cypress and Playwright for end to end testing

## Common Mocks

### Server-Only Mock
```ts
vi.mock("server-only", () => ({}));
```

### Prisma Mock
```ts
import { beforeEach } from "vitest";
import prisma from "@/utils/__mocks__/prisma";

vi.mock("@/utils/prisma");

describe("example", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("test", async () => {
    prisma.group.findMany.mockResolvedValue([]);
  });
});
```

## Best Practices
- Each test should be independent
- Use descriptive test names
- Mock external dependencies
- Clean up mocks between tests
- Avoid testing implementation details