# This file is responsible for uploading files to ImageKit cloud


from fastapi import APIRouter , UploadFile, File , HTTPException
from app.core.imagekit import imagekit
import uuid
import base64

router = APIRouter(prefix="/upload")


@router.post("/")
async def upload_file(file : UploadFile = File(...)):
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are allowed")
    
    file_bytes = await file.read()
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    
    try:
        result = imagekit.files.upload(
            file=file_bytes,
            file_name=unique_filename
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Image upload failed")
    
    # url = result.response_metadata.raw.get("url")
    url = result.url

    if not url:
        raise HTTPException(status_code=500, detail="Upload failed")

    return {
        "filename": unique_filename,
        # "filename": file.filename,
        "url": url
        
    }

