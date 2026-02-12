
#!/bin/bash

# ==========================================
# AGENT ENVIRONMENT BOOTSTRAPPER
# Autor: Ivan Vallejos
# Propósito: Configurar el entorno de un cliente IA (ej: .agents) 
# vinculándolo al "Brain" central mediante enlaces simbólicos.
# ==========================================

# Detener el script si hay errores
set -e

# 1. Validar Argumentos
if [ -z "$1" ]; then
    echo "❌ Error: Debes especificar el nombre del directorio del cliente."
    echo "Uso: ./setup.sh <nombre_cliente>"
    echo "Ejemplo: ./setup.sh .agents"
    exit 1
fi

CLIENT_NAME=$1

# 2. Definimos Rutas (Dinámicas)
# Obtenemos la ruta absoluta de donde está ESTE script (dentro de brain/)
# La raíz del workspace es un nivel arriba de brain/
# El directorio destino para el cliente

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$WORKSPACE_DIR/$CLIENT_NAME"

echo "🤖 Iniciando configuración para: $CLIENT_NAME"
echo "📂 Origen (Brain): $SCRIPT_DIR"
echo "📂 Destino (Cliente): $TARGET_DIR"

# 3. Crear el directorio del cliente si no existe
if [ ! -d "$TARGET_DIR" ]; then
    echo "✨ Creando directorio: $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
else
    echo "ℹ️  El directorio ya existe. Actualizando enlaces..."
fi

# 4. Función para crear enlaces simbólicos relativos
link_resource() {
    RESOURCE_NAME=$1
    
    # Verificamos si el recurso existe en brain/
    if [ -e "$SCRIPT_DIR/$RESOURCE_NAME" ]; then
        # Creamos el enlace simbólico
        # -s: simbólico
        # -f: forzar (sobrescribir si ya existe, útil para corregir rutas)
        # Usamos "../brain/$RESOURCE_NAME" para mantener la portabilidad
        ln -sf "../brain/$RESOURCE_NAME" "$TARGET_DIR/$RESOURCE_NAME"
        echo "✅ Link creado: $CLIENT_NAME/$RESOURCE_NAME -> ../brain/$RESOURCE_NAME"
    else
        echo "⚠️  Advertencia: '$RESOURCE_NAME' no encontrado en brain/. Se omitió."
    fi
}

# 5. Ejecutar vinculación de recursos críticos
echo "🔗 Vinculando recursos del cerebro..."

link_resource "AGENTS.md"
link_resource "SKILLS"        # Esto vinculará la carpeta completa
link_resource "PROJECT_STATE.md"
link_resource "DESIGN_DOC.md" # Agregado por si el agente necesita contexto de diseño

# 6. Crear un archivo .gitkeep o README básico para que el cliente sepa qué es esto
echo "# Espacio de Trabajo para $CLIENT_NAME
Este directorio es una proyección del cerebro central.
NO MODIFICAR LOS ARCHIVOS VINCULADOS DIRECTAMENTE SI NO ES NECESARIO.
Utiliza las tools para proponer cambios." > "$TARGET_DIR/README_CLIENT.md"

echo "🚀 Configuración finalizada con éxito."
