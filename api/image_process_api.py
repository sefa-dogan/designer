import base64
from fastapi import FastAPI, HTTPException
from .body_model import DesignRequest
from graph.graph import app

api=FastAPI()

@api.post("/design")
async def read_root(body:DesignRequest ):
    # print("raw_image",body.raw_image)
    try:

        processed_img = await process_image(body.raw_image)
    except Exception as e:
        print("Error processing image:", e)
        raise HTTPException(status_code=500, detail="Error processing image")
    return {
        "encoded_processed_image": processed_img,
    }
    
async def process_image(raw_image: str):
    # print("func: ")
    graph_result= app.invoke(input={"encoded_raw_image":raw_image})

    # print(graph_result["encoded_processed_image"])
    base64_string = graph_result["encoded_processed_image"]
    base64_string = base64_string.split(',')[-1]
    # Dosyaya yazılacak çıktı dosya adı (uzantıya dikkat!)
    output_file = "output_image.png"

    # Base64 string'ini decode edip dosyaya yaz
    with open(output_file, "wb") as f:
        f.write(base64.b64decode(base64_string))
    return graph_result["encoded_processed_image"]