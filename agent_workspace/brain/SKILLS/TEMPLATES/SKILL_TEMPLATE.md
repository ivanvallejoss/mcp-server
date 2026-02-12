---
name: [nombre-tecnologia]-standard
description: >
  [Descripción corta de 1 línea].
  Trigger: Cuando el usuario pida [X], cuando se detecte [Y].
metadata:
  author: ivan-vallejos
  version: "1.0"
  priority: high
allowed-tools: [file_reader, file_writer] # Define qué puede usar el agente aquí
---

## 🎯 When to Use (Trigger Conditions)
Load this skill exclusively when:
- The task involves [Condition 1]
- The user specifically requests [Condition 2]

## 🧠 Critical Patterns (The "Do's")

### Pattern 1: [Nombre del Patrón]
> **Why:** [Explicación breve de por qué esto es mejor, ej: performance, seguridad]

```python
# ✅ GOOD: Clear typing and error handling
def example(data: dict) -> bool:
    try:
        return process(data)
    except ValueError:
        return False

Pattern 2: [Nombre del Patrón]
Python
# ✅ GOOD: Using context managers
with open("file.txt") as f:
    content = f.read()

🚫 Anti-Patterns (The "Don'ts")
Instructs the model on what to avoid strictly.
Don't: [Nombre del error común]
Risk: [Explica el riesgo: Memory Leak, Race Condition, Security Flaw]
Python
# ❌ BAD: Never leave file handles open
f = open("file.txt")
content = f.read()
# missing close()

⚡ Quick Reference
Task     Command/Pattern     Note
Install  pip install X      Use virtualenv
Test     pytest             Flag -v for verbose
Deploy   ./deploy.sh        Check .env first

