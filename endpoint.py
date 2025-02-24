from fastapi import FastAPI
from pydantic import BaseModel
from call_llmm import call_llm
from fastapi.middleware.cors import CORSMiddleware

# Create a FastAPI app instance
app = FastAPI()

# Enable CORS for all origins. Adjust the parameters as needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for request validation
class QueryRequest(BaseModel):
    user_query: str

# Define the API endpoint which accepts a POST request.
@app.post("/api/query")
def query_endpoint(request: QueryRequest):
    # Extract user_query from the request
    user_query = request.user_query
    # Call the function with the user_query
    result = call_llm(user_query)
    print('llm result:',result)
    # Return the result as JSON
    return {"result": result}