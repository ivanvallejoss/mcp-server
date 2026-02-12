# REPOSITORY GUIDELINES

> **System Identity:** Ivan Vallejos Portfolio (Multi-Agent Architecture)
> **Stack:** Python/FastAPI (Backend), React (Frontend), MCP (Agent Protocol)

## 1. 🚨 Core Directives (The "Constitution")
*All agents must adhere to these rules. No exceptions.*

1.  **Context Hierarchy:** This file is the **Root Truth**.
    * For generic rules -> Read this file.
    * For specific tasks (e.g UI/API) -> **YOU MUST** switch context to the Sub-Agent Guides defined in Section 4.
2.  **Lazy Loading:** DO NOT hallucinate libraries or patterns. Use the `request_context_bundle` tool to load the specific skills listed below before writing code.

---

## 2. 🛠️ Skill Registry (The Menu)

**INSTRUCTION:** To use a skill, invoke `request_context_bundle(["skill_id"])`.
*DO NOT try to read the files manually unless the tool fails.*

### 🌐 Backend & Infrastructure (Python/AWS)
| Skill ID | Trigger / When to Use | Key Concepts |
| :--- | :--- | :--- |
| `python-backend` | Writing Python scripts, API logic, or automation. | Type hinting, Pydantic, Logging (No print). |
| `aws-ec2-opt` | Deploying, configuring Nginx, or Docker on EC2. | Cost-efficiency, memory limits, security groups. |
| `django-drf` | Creating/Modifying API Endpoints. | Serializers, ViewSets, Permissions. |

### 🎨 Frontend & UI (React)
| Skill ID | Trigger / When to Use | Key Concepts |
| :--- | :--- | :--- |
| `react-19` | Creating components, hooks, or views. | No `useMemo`, Server Components, Actions. |
| `typescript-strict` | Any .ts/.tsx file modification. | Interfaces, Generics, No `any`. |

### 🔧 Development Workflow
| Skill ID | Trigger / When to Use | Key Concepts |
| :--- | :--- | :--- |
| `git-conventional` | **MANDATORY** before any commit. | Conventional Commits standard. |
| `testing-pytest` | Writing tests for backend logic. | Fixtures, Mocking, Coverage. |

---

## 3. ⚡ Auto-Invoke Rules (Triggers)

**IF** the user asks for... **THEN** you MUST load these skills immediately:

* "Fix the bug in the login" -> `['python-backend', 'django-drf']`
* "Create a new dashboard card" -> `['react-19', 'typescript-strict']`
* "Deploy the changes" -> `['aws-ec2-opt', 'git-conventional']`

**AND** add any other generic or specific skills that matches with the request.

---

## 4. 🔀 Context Router (Sub-Agent Guidelines)

This project is a Monorepo. Detailed documentation lives in the sub-directories.
**Instruction:** If the task falls into a specific scope, READ the routing file first.

| Scope / Area | Description | Context File Path (Read this!) |
| :--- | :--- | :--- |
| **FRONTEND (UI)** | Next.js/React code, Styles, Components. | `portfolio-app/frontend/README_CONTEXT.md` |
| **BACKEND (API)** | Django/FastAPI, Database, Business Logic. | `portfolio-app/backend/README_CONTEXT.md` |
| **INFRA (DevOps)** | Docker, Nginx, CI/CD, Scripts. | `portfolio-app/infrastructure/README_CONTEXT.md` |

---

## 5. 📝 Project State & Logging

* **Current State:** Check `./PROJECT_STATE.md` to understand recent changes.
* **Logging:** After completing a task, you MUST append a summary to `./PROJECT_STATE.md` following the protocol:
    
    Update tasks: Make an [x] if you successfully complete the requested task.
    Register Log: Add a line on "Agent Execution Log" table with a technical summary.
        Format: | YYYY-MM-DD HH:MM | [ROLE] | [Tools need it] | [Summary of what you make] |
* **IF** you could not be able to complete the task, you **STILL** needs to make a log on that table but expressing **WHY** you were not able to accomplish it