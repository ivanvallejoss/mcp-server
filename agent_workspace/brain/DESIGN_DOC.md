# BIG_PLAN.md: Multi-Agent Orchestration Architecture

## 1. Project Mission
To build a modular, cost-efficient, and scalable software development system powered by AI agents. The system runs on AWS EC2 (Dockerized) and uses a centralized Orchestrator to manage specialized Sub-agents. The architecture is designed to be "engine-agnostic," allowing future migration to advanced orchestration platforms like Google Antigravity.

## 2. Core Architecture

### The Hierarchy
[User] <--> [Orchestrator (Router)] <--> [Shared State (Memory)]
                                     |
                                     +--> [Frontend Agent]
                                     +--> [Backend Agent]
                                     +--> [DevOps Agent]

### The Flow (Granular Execution)
1.  **Input:** User sends a request to the Orchestrator.
2.  **Routing:** Orchestrator analyzes the request against `BIG_PLAN.md` and `PROJECT_STATE.md`.
3.  **Delegation:** Orchestrator spawns a specific Sub-agent (e.g., DevOps) with a targeted `Context` and restricted `Tools`.
4.  **Execution:** Sub-agent performs the task and writes the result to `PROJECT_STATE.md`.
5.  **Termination:** Sub-agent shuts down (saving tokens).
6.  **Feedback:** Orchestrator reads the updated state and reports back to the User.

## 3. The Agent Roster (Roles & Responsibilities)

### Orchestrator (The Manager)
* **Role:** Project Manager & Router.
* **Context Source:** `BIG_PLAN.md`, `PROJECT_STATE.md`.
* **Tools:** `fs_read_file` (Read-only), `agent_spawn` (Create sub-agents).
* **Constraint:** CANNOT write code or execute system commands. MUST delegate.

### Frontend Agent (The UI Specialist)
* **Role:** React/Next.js Developer.
* **Context Source:** `brain/contexts/frontend.md` (Contains Design System, Tailwind rules).
* **Tools:** `fs_write_file`, `fs_read_file` (Scoped to `/src` folder).
* **Goal:** Implement UI components and manage client-side logic.

### Backend Agent (The API Specialist)
* **Role:** Python/Node.js Developer.
* **Context Source:** `brain/contexts/backend.md` (Contains DB Schema, API routes).
* **Tools:** `fs_write_file`, `fs_read_file`, `db_query_tool`.
* **Goal:** Manage business logic, database migrations, and API endpoints.

### evOps Agent (The Operator)
* **Role:** SysAdmin & Infrastructure Manager.
* **Context Source:** `brain/contexts/devops.md` (Contains AWS, Docker, Nginx configs).
* **Tools:** `sys_exec_command`, `docker_tool`, `fs_write_file` (Scoped to config files).
* **Goal:** Deployments, server maintenance, log analysis, and auto-healing.

## 4. State Protocol (The Memory)

All agents must adhere to the **"Write-to-State"** rule.
* **File:** `workspace/brain/PROJECT_STATE.md`
* **Format:**
    * **## Current Phase:** (e.g., "Phase 2: MVP Deployment")
    * **## Active Tasks:** List of pending items.
    * **## Changelog:** Chronological log of major actions taken by agents.
    * **## Critical Context:** (e.g., "Server IP is X", "DB Port is Y").

* **Rule:** If a Sub-agent fixes a bug, it MUST append a log entry to `PROJECT_STATE.md` before terminating. The Orchestrator relies on this file to know what happened.

## 5. Tooling Strategy (Security & Cost)

* **Orchestration Layer:** High-level logic tools only. No raw execution.
* **Execution Layer (Sub-agents):** * Restricted file system access (Sandbox).
    * Model Routing (Future): The system will select the most cost-effective LLM (Gemini Flash, etc.) based on the complexity of the task.

## 6. Future Roadmap (Antigravity Readiness)
* **Structured Inputs:** All agent prompts will be structured to allow easy mapping to Google Antigravity's expected JSON schemas.
* **Observability:** All interactions are logged to prepare for advanced debugging and tracing.
