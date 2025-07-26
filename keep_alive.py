
from fastapi import FastAPI
import uvicorn
import threading

app = FastAPI()

@app.get("/")
def ping():
    return {"status": "alive"}

def start_keep_alive_server():
    def run_server():
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
        
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    print("🌐 HTTP сервер запущен на порту 8000")
