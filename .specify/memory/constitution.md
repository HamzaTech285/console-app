<!-- Sync Impact Report:
Version change: 1.0.0 → 2.0.0
Modified principles:
  - Clean Python Code (PEP8 Style) → Clean & Modular Multi-Stack Code
  - Comprehensive Testing → Automated Testing & Quality Assurance
  - User-Friendly CLI Design → Responsive & Accessible Interface
Added sections:
  - IV. API-First Design & Decoupled Architecture
  - V. Security & User Isolation
  - VI. Performance & Scalability
  - VII. Spec-Driven Monorepo Development
Removed sections:
  - Dependency Management (merged into VII)
  - Error Handling and User Feedback (merged into I and II)
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: Ensure JWT-based Better Auth implementation details are finalized in Phase 2 specs.
-->
# Todo App Constitution

## Core Principles

### I. Clean & Modular Multi-Stack Code
The codebase follows a modular clean architecture to ensure maintainability and high quality.
- **Backend (FastAPI/SQLModel):** Must be type-safe, maintain PEP8 compliance, and use linting (flake8/black).
- **Frontend (Next.js/Tailwind):** Must adhere to React best practices, use consistent styling patterns, and maintain strict accessibility standards.
Rationale: A clean, modular design reduces technical debt and allows independent scaling of frontend and backend components.

### II. Automated Testing & Quality Assurance
Thorough automated testing is non-negotiable for every feature and bug fix.
- **Backend:** Unit and integration tests for all API endpoints using pytest.
- **Frontend:** Component and E2E tests for critical user journeys.
- **Minimum Coverage:** 80% across the monorepo, with 100% coverage for security and data persistence paths.
Rationale: Automated tests prevent regressions and ensure system reliability during rapid development.

### III. Responsive & Accessible Interface
The system provides a seamless user experience across all devices and screen sizes.
- **Responsiveness:** The UI must be mobile-first and optimized for performance.
- **Accessibility:** Must comply with WCAG 2.1 AA standards to ensure inclusivity.
Rationale: A responsive and accessible interface ensures that the application is usable by everyone, regardless of their device or ability.

### IV. API-First Design & Decoupled Architecture
The system is built as a decoupled monorepo where communication happens exclusively via a secure API.
- **Structure:** Decoupled frontend (Next.js 16+) and backend (FastAPI/SQLModel).
- **API Contracts:** All routes must follow the `/api/{user_id}/tasks` format.
- **Separation:** Logic remains separate from the UI to allow for multiple client types (CLI, Web, Mobile).
Rationale: This architecture ensures scalability and allows the backend to serve as a single source of truth for all clients.

### V. Security & User Isolation
Security is a foundational requirement, ensuring absolute user isolation and data protection.
- **Authentication:** Must use JWT-based Better Auth for secure session management.
- **User Isolation:** Each user must only be able to access and modify their own tasks. No cross-user data leaks are permitted.
- **Secrets:** Never hardcode tokens or credentials; use secure environment management for database (Neon PostgreSQL) and API keys.
Rationale: User trust is paramount; rigorous isolation prevents unauthorized access and data breaches.

### VI. Performance & Scalability
The application must maintain fast response times and efficient resource usage.
- **Backend Performance:** FastAPI responses must be optimized (target p95 < 200ms).
- **Database:** Efficient querying on Neon PostgreSQL with proper indexing for user-task relationships.
- **Frontend Performance:** Optimized bundle sizes and lazy loading for fast initial page loads.
Rationale: Performance directly impacts user retention and system cost-efficiency.

### VII. Spec-Driven Monorepo Development
The project follows Spec-Driven Development (SDD) to ensure all implementations align with business requirements.
- **Monorepo Management:** Uses `uv` for backend environment management and established JS package managers for frontend.
- **Lifecycle:** Every feature follows the Spec → Plan → Tasks → Implement workflow.
- **Consistency:** All technical decisions must be documented as ADRs and linked in the prompt history records (PHR).
Rationale: SDD minimizes scope creep and ensures architectural consistency across the entire full-stack ecosystem.

## Additional Constraints

The project uses Neon PostgreSQL for primary data storage and requires CI/CD verification for all merges. No code shall be merged without passing linting, testing, and security scans.

## Development Workflow

1. **Specify:** Define feature requirements in `specs/`.
2. **Plan & Document:** Create technical plans and register ADRs for significant decisions.
3. **Tasks:** Generate dependency-ordered task lists.
4. **Implement:** Write modular code with continuous testing and PHR tracking.
5. **Review:** Peer or AI review to ensure constitutional compliance.

## Governance

This constitution governs all technical and design decisions for the Todo Web Application. Amendments require a MAJOR version bump and must be justified with technical rationale and impact analysis. compliance reviews are mandatory at the end of each development sprint.

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-02
