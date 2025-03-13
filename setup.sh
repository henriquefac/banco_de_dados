DIR=".env"

if [[ ! -d "$DIR" ]]; then
    python3 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
    echo "Ambiente criado"
    bash start.sh
else
    echo "O ambiente já existe"
fi
