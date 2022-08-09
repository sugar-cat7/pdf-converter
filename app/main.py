from fastapi import FastAPI
from fastapi.responses import FileResponse, Response

from opt.sample import convert_main

app = FastAPI()

file_path = "/root/opt/images/output.pdf"


@app.get("/create_pdf")
async def create_pdf():
    try:
        convert_main()
        return FileResponse(file_path)
    except ValueError:
        return {"ValueError": "ValueError"}


@app.get("/get_pdf")
def read_root():
    return FileResponse(file_path)
