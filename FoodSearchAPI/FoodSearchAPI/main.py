import time
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
import requests

# Initialize FastAPI app
app = FastAPI()

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# FatSecret API details
BASE_URL = "https://platform.fatsecret.com/rest/foods/search/v3"
API_KEY =  "e4da3360682741c8b63eecb6ae23b487"
API_SECRET ="29b993fcb1b44f7d9a4cae3dd17049f9"
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

# In-memory token storage for simplicity (consider persistent storage for production)
access_token = None
token_expiry_time = 0  # Will store the token expiry time in epoch format

# Function to get a new access token
def get_access_token():
    global access_token, token_expiry_time
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=data, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        # Calculate the expiry time (current time + expires_in)
        token_expiry_time = time.time() + token_data.get("expires_in")
        return access_token
    else:
        raise HTTPException(status_code=401, detail="Unable to retrieve access token")

# Dependency to get a valid access token
def get_valid_token():
    global access_token, token_expiry_time
    # If the token doesn't exist or has expired, get a new one
    if not access_token or time.time() > token_expiry_time:
        return get_access_token()
    return access_token

@app.get("/foods/search")
async def search_foods(
    query: str = Query(None, description="Search expression for foods"),
    max_results: int = Query(20, description="Maximum number of results per page (max 50)"),
    page_number: int = Query(0, description="Zero-based page number"),
    include_sub_categories: bool = Query(False, description="Include sub categories associated with food"),
    include_food_images: bool = Query(False, description="Include food images if available"),
    include_food_attributes: bool = Query(False, description="Include dietary preferences and allergens if available"),
    flag_default_serving: bool = Query(False, description="Flag the default serving if available"),
    region: str = Query(None, description="Filter results by region (e.g., 'FR')"),
    language: str = Query(None, description="Language for results (ignored unless region is specified)"),
    format: str = Query("json", description="Desired response format (default 'json')"),
    token: str = Depends(oauth2_scheme)
):
    if max_results > 50:
        raise HTTPException(status_code=400, detail="max_results cannot exceed 50")

    token = get_valid_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "method": "foods.search.v3",
        "search_expression": query,
        "max_results": max_results,
        "page_number": page_number,
        "include_sub_categories": str(include_sub_categories).lower(),
        "include_food_images": str(include_food_images).lower(),
        "include_food_attributes": str(include_food_attributes).lower(),
        "flag_default_serving": str(flag_default_serving).lower(),
        "region": region,
        "language": language,
        "format": format
    }

    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch food data")

@app.post("/token")
async def generate_token():
    return {"access_token": get_access_token(), "token_type": "bearer"}
