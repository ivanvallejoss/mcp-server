---
name: python-backend-standards
description: >
  Estándares de desarrollo Backend con Python, manejo de errores y tipado.
  Trigger: Cuando se escriba lógica de negocio, servicios o scripts en Python.
license: Private
metadata:
  author: Ivan Vallejos
  version: "1.0"
  stack: [Python 3.11+, Pydantic, Typing]
  auto_invoke: "Writing Python scripts"
---

## Strong Typing (REQUIRED)

```python
# ✅ SIEMPRE: Usa Type Hints y retornos explícitos
from typing import List, Optional

def calculate_total(items: List[dict], tax: float = 0.21) -> float:
    return sum(i['price'] for i in items) * (1 + tax)

# ❌ NUNCA: Código "pelado" sin tipos
def calculate_total(items, tax=0.21):
    return sum(i['price'] for i in items) * (1 + tax)
Error Handling & Logging (REQUIRED)
Python
# ✅ SIEMPRE: Logs estructurados y excepciones específicas
import logging
logger = logging.getLogger(__name__)

try:
    user = db.get_user(user_id)
except UserNotFoundError:
    logger.warning("User not found during payment", extra={"user_id": user_id})
    raise

# ❌ NUNCA: Print o catch genérico
try:
    user = db.get_user(user_id)
except Exception as e:
    print(f"Error: {e}") # El print se pierde en producción
Environment Variables
Python
# ✅ SIEMPRE: Usa pydantic-settings o os.getenv con validación
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str
    debug_mode: bool = False

settings = Settings()

# ❌ NUNCA: Hardcodear secretos
db_url = "postgres://user:password@localhost:5432/db"
```