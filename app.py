from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import subprocess
import os

app = FastAPI()

@app.get("/")
def health():
    return {"ok": True, "service": "pdf-extractor"}

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as d:
        pdf_path = os.path.join(d, "doc.pdf")
        txt_path = os.path.join(d, "doc.txt")

        content = await file.read()
        with open(pdf_path, "wb") as f:
            f.write(content)

        try:
            subprocess.check_call(["pdftotext", "-layout", pdf_path, txt_path])
        except subprocess.CalledProcessError:
            return JSONResponse({"ok": False, "error": "pdftotext failed"}, status_code=500)

        text = ""
        if os.path.exists(txt_path):
            with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        return {"ok": True, "text": text}
