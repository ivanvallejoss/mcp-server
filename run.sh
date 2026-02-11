#!/bin/bash

# 1. Navegar a la carpeta (usando ruta absoluta para evitar ambigüedad)
cd /home/ubuntu/mcp-backend

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Ejecutar el servidor (exec reemplaza el proceso actual)
exec python3 tools.py
