from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.app.models.response import AskResponse
from backend.app.models.python_response import PythonResponse
from backend.app.service import (
    adaptive_retriever,
    document_ingestor,
    conversation_memory,
)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("data/artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Adaptive RAG",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():

    return {
        "status": "healthy",
    }


@app.post("/ask")
async def ask(
    question: str = Form(...),
    files: list[UploadFile] | None = File(None),
):

    uploaded_files = []

    if files:

        for file in files:

            file_path = UPLOAD_DIR / file.filename

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            uploaded_files.append(str(file_path))

            document_ingestor.ingest(
                str(file_path)
            )

    response = adaptive_retriever.invoke(
        question=question,
        uploaded_files=uploaded_files,
    )

    if isinstance(response, PythonResponse):

        artifact_names = []

        for artifact in response.artifacts:

            source = Path(artifact)

            if source.is_file():

                destination = ARTIFACT_DIR / source.name
                shutil.copy2(source, destination)
                artifact_names.append(destination.name)

        return AskResponse(
            answer=response.output,
            artifacts=artifact_names,
        )

    return AskResponse(
        answer=response,
    )


@app.get("/artifacts/{filename}")
def get_artifact(filename: str):

    file_path = ARTIFACT_DIR / filename

    if not file_path.exists():

        return {
            "error": "Artifact not found",
        }

    return FileResponse(file_path)

@app.post("/reset")
def reset():

    conversation_memory.clear()

    return {
        "message": "Conversation cleared."
    }