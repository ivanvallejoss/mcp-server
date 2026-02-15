import os
import sys
import subprocess
import psycopg2
import shlex
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
from typing import List


# ==========================================
#          INITIAL CONFIGURATION
# ==========================================
load_dotenv()

# Definimos la carpeta segura.
WORKSPACE_DIR = Path(os.getcwd()) / "agent_workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

# Declaramos el servidor MCP
mcp = FastMCP("Backend Lab Agent - Code Interpreter")


# ==========================================
#               UTILITIES
# ==========================================

def get_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )
    conn.autocommit = True
    return conn

def validar_ruta(nombre_archivo: str) -> Path:
    """
    Valida que los archivos no salgan del workspace.
    """
    ruta_destino = (WORKSPACE_DIR / nombre_archivo).resolve()
    if not ruta_destino.is_relative_to(WORKSPACE_DIR.resolve()):
        raise ValueError(f"ACCESO DENEGADO: No puedes salir del workspace.")
    return ruta_destino


# ==========================================
#               DB TOOLS
# ==========================================
@mcp.tool()
def db_listar_tablas() -> str:
    """Lista tablas en la BD."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        rows = cur.fetchall()
        conn.close()
        return f"Tablas: {', '.join([r[0] for r in rows])}" if rows else "BD vacía."
    except Exception as e: return f"Error DB: {e}"

@mcp.tool()
def db_ejecutar_sql(query: str) -> str:
    """Ejecuta SQL seguro (Sin DROP/TRUNCATE)."""
    if any(x in query.upper() for x in ["DROP", "TRUNCATE", "DELETE FROM"]):
        return "❌ BLOQUEADO: Operación destructiva."
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query)
        if query.upper().strip().startswith("SELECT"):
            res = cur.fetchall()
            conn.close()
            return str(res)
        conn.close()
        return "✅ SQL Ejecutado."
    except Exception as e: return f"Error SQL: {e}"


# ==========================================
#         FILE MANAGER TOOL
# ==========================================
@mcp.tool()
def fs_listar_archivos() -> str:
    try:
        archivos = list(WORKSPACE_DIR.glob("*"))
        if not archivos: return "Workspace vacío."
        return "Archivos:\n" + "\n".join([f"- {f.name}" for f in archivos])
    except Exception as e: return f"Error FS: {e}"

@mcp.tool()
def fs_escribir_archivo(nombre_archivo: str, contenido: str) -> str:
    try:
        ruta = validar_ruta(nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        return f"✅ Guardado: {nombre_archivo}"
    except Exception as e: return f"Error: {e}"

@mcp.tool()
def fs_leer_archivo(nombre_archivo: str) -> str:
    try:
        ruta = validar_ruta(nombre_archivo)
        if not ruta.exists(): return "❌ Archivo no existe."
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e: return f"Error: {e}"


# ==========================================
#           COMMANDS & SCRIPTS
# ==========================================
@mcp.tool()
def sys_ejecutar_script(nombre_archivo: str) -> str:
    """Ejecuta un script de Python que esté en el workspace y devuelve el Output."""
    try:
        ruta = validar_ruta(nombre_archivo)
        if not ruta.exists():
            return "❌ El archivo no existe en el workspace."
        
        # Ejecutamos usando el MISMO python que está corriendo el agente (el del venv)
        resultado = subprocess.run(
            [sys.executable, str(ruta)],
            capture_output=True,
            text=True,
            timeout=30 # Seguridad: Mata el proceso si tarda más de 30s
        )
        
        output = ""
        if resultado.stdout:
            output += f"--- STDOUT ---\n{resultado.stdout}\n"
        if resultado.stderr:
            output += f"--- STDERR ---\n{resultado.stderr}\n"
            
        if not output:
            return "El script se ejecutó pero no imprimió nada."
            
        return output

    except subprocess.TimeoutExpired:
        return "❌ ERROR: El script tardó demasiado (timeout 30s)."
    except Exception as e:
        return f"❌ Error de ejecución: {e}"

@mcp.tool()
def run_command(command: str) -> str:
    """
    Ejecuta un comando de terminal (Bash) en el sistema.
    REQUIERE autorizacion del usuario en el cliente.

    Args:
        command: El comando a ejecutar (ej: 'ls -al', 'docker ps')
    """
    # Utilizamos la ruta tipo sandbox creada para la ejecucion de scripts
    SAFE_CWD = WORKSPACE_DIR

    try:
        # shlex.split maneja correctamente los espacios en argumentos
        args = shlex.split(command)

        # Ejecutamos un timeout de 60s para evitar procesos colgados
        result = subprocess.run(
            args,
            cwd=SAFE_CWD,
            capture_output=True,
            text=True,
            timeout=60
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        output_msg = []
        if stdout:
            output_msg.append(f"STDOUT:\n{stdout}")
        if stderr:
            output_msg.append(f"STDERR:\n{stderr}")

        if not stdout and not stderr and result.returncode == 0:
            return "SUCCESS: Command executed successfully with no output."

        return "\n".join(output_msg)

    except FileNotFoundError:
        return f"Error: El comando '{args[0]}' no existe o no esta instalado"
    except subprocess.TimeoutExpired:
        return "Error: El comando excedio el tiempo limite de 60 segundos."
    except Exception as e:
        return f"Error critico ejecutnado comando: {str(e)}"


# ==========================================
#             SKILLS ON AGENTS
# ==========================================

# Por ahora hardcodeamos la carpeta de .gemini y, en un futuro, implementaremos tools dentro de cada agente
# De esta forma estara dentro de la carpeta raiz del agente y, donde ellos mismos esperan buscar la tool
SKILLS_DIR = "agent_workspace/.gemini/SKILLS"

@mcp.tool()
def request_context_bundle(requested_skills: List[str]) -> str:
    """
Carga y devuelve al agente el contenido de los skills necesarios para la tarea a realizar
Args:
     requested_skills: Lista de nombres de skills (sin extension .md) requeridas para la tarea
     Ejemplo: ['react', 'docker', 'git-flow']
Returns:
     Las rutas exactas a cada skill para la tarea requerida
     Ejemplo: [ .agents/skills/[skill-nombre], .gemini/skills/[skill-nombre], .claude/skills/[skill-nombre] ]
    """
    bundle_content = []
    errors = []
    
    # Obtener el inventario 
    available_skills = {d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d)) }
    
    found_paths = []
    missing_skills = []

    # 2. Validar y construir las rutas
    for skill in requested_skills:
        if skill in available_skills:
            # Construimos la ruta al archivo de la skill
            # Asumimos que siempre habra un archivo SKILL.md
            skill_path = os.path.join(SKILL_DIR, "SKILL.md")
            found_paths.append(skill_path)
        else:
            missing_skills.append(skill)

    response_lines = []
    if found_paths:
        response_lines.append("STOP! CRITICAL INSTRUCTION:")
        response_lines.append("The requested task CANNOT be completed without the context from this files.")
        response_lines.append("You MUST read the following files immediately using your file_reader tool:")
        for path in found_paths:
            response_lines.append(f"- {path}")

    if missing_skills:
        response.lines.append("\n WARNING: The following were not found in te registry: {missing_skills}")

    return "\n".join(response_lines)


if __name__ == "__main__":
    mcp.run()
