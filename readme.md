# AYP Credit Card Perks Processor

A Google Cloud Function for processing and storing credit card perks data in Python.

## Prerequisites
- Python 3.7+
- Google Cloud SDK
- Google Cloud Platform access

## Installation
1. Clone the repository:
   ```bash
   git clone [REPO_URL]
Install dependencies:

pip install -r requirements.txt

Local Development
Run python main.py to start the local server.

## Deployment
Deploy using Google Cloud Functions:

```gcloud functions deploy process_perks --runtime python39 --trigger-http --allow-unauthenticated --entry-point=process_perks ```




