import os
import sys
from pathlib import Path
import logging
from typing import Optional

# Add the parent directory to sys.path to import the existing modules
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from orchestration import ContentOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Content Generator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContentRequest(BaseModel):
    topic: str
    output_format: Optional[str] = "pdf"

class ContentResponse(BaseModel):
    status: str
    message: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "AI Content Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/generate-content", response_model=ContentResponse)
async def generate_content(request: ContentRequest, background_tasks: BackgroundTasks):
    try:
        logger.info(f"Received content generation request for topic: {request.topic}")
        orchestrator = ContentOrchestrator()
        result = orchestrator.generate_content(request.topic)
        if result.get("success"):
            file_path = result.get("file_path")
            if file_path and os.path.exists(file_path):
                download_url = f"/api/download/{os.path.basename(file_path)}"
                return ContentResponse(
                    status="success",
                    message="Content generated successfully",
                    file_path=file_path,
                    download_url=download_url
                )
            else:
                raise HTTPException(status_code=500, detail="Generated file not found")
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Content generation failed"))
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    try:
        file_path = Path(__file__).parent.parent / "output" / filename
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="application/pdf"
        )
    except Exception as e:
        logger.error(f"Error downloading file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@app.get("/api/files")
async def list_generated_files():
    try:
        output_dir = Path(__file__).parent.parent / "output"
        files = []
        if output_dir.exists():
            for file_path in output_dir.glob("*.pdf"):
                files.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "created": file_path.stat().st_ctime,
                    "download_url": f"/api/download/{file_path.name}"
                })
        return {"files": files}
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
