#!/bin/bash

# Lista de aplicaciones a cerrar
apps_to_close=(
    "ChatGPT Atlas"
    "uTorrent Web"
    "Google Chrome"
)

echo "Cerrando aplicaciones..."

for app in "${apps_to_close[@]}"; do
    echo "Cerrando $app..."
    osascript -e "tell application \"$app\" to quit"
done

echo "¡Listo!"
