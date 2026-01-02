# ADR-0001: CLI Application Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-02
- **Feature:** todo-app-cli
- **Context:** The project required a robust, maintainable, and testable command-line interface (CLI) for managing todo tasks with persistent storage. The architecture needed to support complex features like recurring tasks and priority systems while maintaining performance and cross-platform compatibility.

## Decision

The application follows a layered modular architecture designed for high testability and separation of concerns:

- **Language:** Python 3.13+
- **CLI Framework:** Built-in `argparse` for standardized command handling.
- **Project Packaging:** `pyproject.toml` with `uv` for modern, fast dependency and environment management.
- **Layered Design:**
    - **Models:** `Task` (data structure/validation) and `TaskManager` (business logic/storage interface).
    - **CLI Layer:** `parsers.py` (argument definitions) and `commands.py` (CLI action handlers).
    - **Utility Layer:** `serializers.py` (JSON persistence) and `validators.py` (shared input validation).
- **Storage Strategy:** JSON-based local file persistence for high portability and human-readability without external database dependencies.
- **Testing Strategy:** `pytest` for comprehensive unit and integration testing (44 tests total).

## Consequences

### Positive

- **Separation of Concerns:** Business logic in `TaskManager` is independent of the CLI layer, allowing for future interfaces (e.g., a web API) without rewriting core logic.
- **High Testability:** Logic is isolated in small, pure functions and methods that are easy to unit test.
- **Portability:** JSON storage requires no setup (like SQL) and works identically across all operating systems.
- **Modern Tooling:** `uv` provides extremely fast environment setup and reliable dependency resolution.
- **Standardized UI:** `argparse` generates consistent help messages and handles common CLI patterns (subcommands, flags) automatically.

### Negative

- **File System Locking:** JSON file storage lacks the concurrent write protections found in databases (acceptable for a single-user CLI).
- **Boilerplate:** Layered architecture requires more initial files and "plumbing" compared to a single-script approach.
- **Performance at Scale:** JSON parsing becomes slower as the task list grows (mitigated by the 1000-task soft limit).

## Alternatives Considered

**Alternative A: Single-file Script with SQLite**
- **Pros:** Extremely simple to distribute; SQL provides better querying/concurrency.
- **Cons:** Harder to maintain as complexity grows; SQL adds overhead for simple todo data; logic becomes tightly coupled with SQL queries making unit testing harder.
- **Rationale for rejection:** Prioritized clean architecture and ease of testing over SQL features that weren't strictly necessary for the scale.

**Alternative B: Click or Typer CLI Frameworks**
- **Pros:** More "magic" features, decorative syntax.
- **Cons:** Adds external dependencies; might be overkill for this scope.
- **Rationale for rejection:** Chose `argparse` to keep dependencies minimal—using standard library features where they are sufficient and robust.

## References

- Feature Spec: [specs/001-todo-app-cli/spec.md](specs/001-todo-app-cli/spec.md)
- Implementation Plan: [specs/001-todo-app-cli/plan.md](specs/001-todo-app-cli/plan.md)
- Related ADRs: none
- Evaluator Evidence: 44 passing tests in `tests/`
