import os
import shutil

DB_DIR = "tmp"
DB_FILE = os.path.join(DB_DIR, "storage.db")

def reset_db():
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print(f"✅ Banco de dados removido: {DB_FILE}")
        except Exception as e:
            print(f"❌ Erro ao remover banco de dados: {e}")
            print("Certifique-se de que o agente (agent.py) não está rodando.")
    else:
        print(f"ℹ️ Nenhum banco de dados encontrado em {DB_FILE}")

    # Opcional: remover todo o diretório tmp se estiver vazio
    if os.path.exists(DB_DIR) and not os.listdir(DB_DIR):
        os.rmdir(DB_DIR)
        print(f"✅ Diretório limpo: {DB_DIR}")

if __name__ == "__main__":
    reset_db()
