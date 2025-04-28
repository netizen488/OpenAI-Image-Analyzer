import os
import base64
import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI, AsyncOpenAI # Use AsyncOpenAI for async FastAPI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
MAX_FILE_SIZE_MB = 20 # Corresponds to OpenAI's limit

# --- OpenAI Client ---
# Use AsyncClient for compatibility with async FastAPI functions
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# --- FastAPI App ---
app = FastAPI()

# --- Helper Function ---
def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encodes image bytes to Base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")

# --- API Endpoint ---
@app.post("/analyze-image/") # Matches the path in script.js and Nginx config
async def analyze_image(file: UploadFile = File(...)):
    """
    Receives an uploaded image file, sends it to OpenAI o4-mini for analysis,
    and returns the analysis text.
    """
    print(f"Received file: {file.filename}, Content-Type: {file.content_type}")

    # --- Input Validation ---
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
        )

    # Read file content
    try:
        contents = await file.read()
        file_size = len(contents)
        print(f"File size: {file_size / (1024*1024):.2f} MB")

        if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
             raise HTTPException(
                status_code=413, # Payload Too Large
                detail=f"File size exceeds the limit of {MAX_FILE_SIZE_MB}MB."
            )

    except Exception as e:
         print(f"Error reading file: {e}")
         raise HTTPException(status_code=500, detail="Error reading uploaded file.")
    finally:
        await file.close() # Ensure file is closed

    # --- Prepare for OpenAI ---
    try:
        base64_image = encode_image_to_base64(contents)
        mime_type = file.content_type # Get the actual mime type

        # Construct the payload according to OpenAI API reference for image inputs
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        # You can customize this prompt
                        "text": "Describe this image in detail. What is happening? What objects are present? What is the overall mood or context?"
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{base64_image}",
                        # o4-mini uses the 'detail' parameter like gpt-4o
                        # 'low' costs 2833 base tokens, 'high' costs more based on size
                        # Let's start with 'auto' or 'low' to manage cost. 'high' gives better detail.
                        "detail": "auto" # or "low" or "high"
                    },
                ],
            }
        ]

        print("Sending request to OpenAI...")
        # --- Call OpenAI API ---
        response = await client.responses.create(
            model="o4-mini", # Use the specified o4-mini model
            input=messages,
            # max_tokens=300 # Optional: Limit response length
        )

        print("Received response from OpenAI.")
        analysis_text = response.output_text

        if not analysis_text:
            print("Warning: OpenAI returned an empty analysis.")
            analysis_text = "Analysis could not be generated."


    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Avoid exposing detailed internal errors or API keys to the client
        raise HTTPException(status_code=503, detail="Failed to analyze image due to an external service error.")

    # --- Return Result ---
    print(f"Analysis result: {analysis_text[:100]}...") # Log snippet
    return JSONResponse(content={"analysis": analysis_text})

# --- Root endpoint (optional, for testing) ---
@app.get("/")
async def read_root():
    return {"message": "Image Analyzer API is running!"}