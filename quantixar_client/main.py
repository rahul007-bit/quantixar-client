import json
from sentence_transformers import SentenceTransformer
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
from quantixar_client.utils.read_parquent import read_parquet,get_embeddings
from quantixar_client.client.client import QuantixarClient

client = QuantixarClient()
payloads = []
model = SentenceTransformer('clip-ViT-B-32')
async def init(request):
    global payloads
    count = 0 
    if request.app.state.initialized:
        return JSONResponse({"message": "Already initialized"})
    if len(payloads) == 0:
        payloads = read_parquet("../top_1000_2.parquet")
    for payload in payloads:
        await client.insert(payload["vectors"], payload["payload"])
        count += 1
        if count % 100 == 0:
            print(count)
        if count == 1000:
            break
    return JSONResponse({"message": "Insert successful"})

async def query(request):
    # Your query logic here
    qurey = request.query_params['s']
    embeddings = get_embeddings(model, qurey)
    result = client.query(embeddings.tolist())

    return JSONResponse(result)

async def insert(request):
    body: bytes = await request.body()
    data = json.loads(body)
    print(data)
    return JSONResponse({"message": "Insert successful"})

async def index(request):
    return JSONResponse({"message": "Hello, world!"})

app = Starlette(debug=True, routes=[
    Route("/", index),
    Route("/init", init, methods=["POST"]),
    Route("/query", query, methods=["POST"]),
])
app.state.client = client
app.state.initialized = False


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True,)