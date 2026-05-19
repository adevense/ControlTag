import os
import json


APP_NAME = "ControlTag_BDGC"
DEFAULT_DATA_DIR = os.path.join(os.environ["APPDATA"], APP_NAME)
CONFIG_FILE = os.path.join(DEFAULT_DATA_DIR, "settings.json")
DEFAULT_BACKUP_DIR = os.path.join(DEFAULT_DATA_DIR, "backups")


def garantir_diretorios():
    """Cria os diretórios de dados e backup se não existirem."""
    os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)
    os.makedirs(DEFAULT_BACKUP_DIR, exist_ok=True)


def carregar_config():
    """Carrega as configurações do arquivo JSON. Retorna dict padrão se não existir."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"language": "pt"}


def salvar_config(dados):
    """Salva as configurações no arquivo JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(dados, f)
