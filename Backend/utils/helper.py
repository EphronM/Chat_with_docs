from fastapi import FastAPI, HTTPException, UploadFile, File, Form









async def process_uploaded_file(file: UploadFile):
    # Get the content length of the file
    file.file.seek(0, 2)  # Move the cursor to the end of the file
    file_size = file.file.tell()  # Get the file size
    file.file.seek(0)  # Reset the cursor to the beginning of the file

    # Check if file size exceeds 100MB
    if file_size > 100 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File size exceeds 100MB")

    # Check supported file types
    allowed_extensions = ['txt', 'csv', 'docx', 'pdf']
    file_extension = file.filename.split('.')[-1]
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    # Read file content
    file_content = await file.read()
    return file_content, file_extension