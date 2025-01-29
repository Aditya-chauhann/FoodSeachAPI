Food Search API with FastAPI
This project provides a FastAPI-powered Food Search API that integrates with the FatSecret API. It allows users to search for food items, filter results, and retrieve detailed nutritional information with OAuth2 authentication.

Features
Food Search: Search food items with various filters.
OAuth2 Authentication: Secure access with token-based authentication.
Token Management: Automatic token generation and validation with expiry handling.
Customizable Results: Control the number of results, pagination, and food details.
Requirements
Python 3.7 or higher
FastAPI
Requests library
Uvicorn (for running the app)
Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/food-search-api.git
Navigate to the project folder:

bash
Copy
Edit
cd food-search-api
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Setup
Add your FatSecret API credentials in the API_KEY and API_SECRET variables in the main.py file.
Start the FastAPI application:
bash
Copy
Edit
uvicorn main:app --reload
API Endpoints
1. /foods/search
Search for food items.

Method: GET

Query Parameters:

query: Search expression for food.
max_results: Maximum number of results per page (max 50).
page_number: Zero-based page number.
include_sub_categories: Include sub-categories (default False).
include_food_images: Include images of food items (default False).
include_food_attributes: Include dietary preferences and allergens (default False).
flag_default_serving: Flag default serving (default False).
region: Region for results (optional).
language: Language for results (optional).
format: Response format (default json).
Response:

JSON object containing search results and nutritional information.
2. /token
Generate a new access token.

Method: POST

Response:

JSON object containing access_token and token_type.
Testing the API
Test Token Generation: First, call the /token endpoint to get a bearer token.
Search Food Items: Use the /foods/search endpoint with the valid token to search for food.
License
MIT License. See LICENSE for more details.
