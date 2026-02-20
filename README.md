# Cloud Resume Challenge — Backend (AWS SAM)

Serverless backend for my Cloud Resume Challenge website.  
It powers the live visitor counter on: **https://gauthamkartha.com**

## Architecture
- **API Gateway (HTTP API)** exposes `GET /count`
- **AWS Lambda (Python)** increments and returns visitor count
- **DynamoDB** stores the counter

Flow:
Browser → API Gateway → Lambda → DynamoDB

## Tech
- AWS SAM (Infrastructure as Code)
- Python 3.12
- boto3
- pytest + moto (unit tests)

## API
- `GET /count` → returns:
```json
{ "count": 123 }
