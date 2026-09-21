from fastapi import Response, FastAPI
import uvicorn
from tools import send_and_forget, Packet


app = FastAPI()

@app.post("/telegram")
async def _admin(input: Packet):
    send_and_forget(input.chat, input.token, input.text)
    return Response(status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3306)
