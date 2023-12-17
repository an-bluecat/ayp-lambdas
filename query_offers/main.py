import logging
from google.cloud import firestore
from flask import jsonify
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)


def query_offers(request):
    request_json = request.get_json(silent=True)
    db = firestore.Client()

    # Extract parameters
    offer_provider = request_json.get('offerProvider', None)
    offer_merchant = request_json.get('offerMerchant', None)
    include_expired = request_json.get('includeExpired', False)
    # Query setup
    query_ref = db.collection('creditCardPerks')
    if offer_provider:
        query_ref = query_ref.where('offerProvider', '==', offer_provider)
    elif offer_merchant:
        query_ref = query_ref.where('offerMerchant', '==', offer_merchant)

    # Execute query
    try:
        docs = query_ref.stream()
        results = []
        current_date = datetime.now()

        for doc in docs:
            try:
                doc_data = doc.to_dict()

                # Log the document data

                offer_expiration = doc_data.get('offerExpireDate')
                # Log the expiration date
                # Add logging to check the document data
                # logging.info(
                #     f"Processing document {doc.id} with data: {doc_data}")

                # Check if offer_expiration is a datetime object
                if isinstance(offer_expiration, datetime):
                    if include_expired or offer_expiration > current_date:
                        results.append(doc_data)
                elif offer_expiration is None and include_expired:
                    results.append(doc_data)
            except Exception as doc_error:
                logging.error(
                    f"[query offer] Error processing document {doc.id}: {doc_error}")

        # logging.info(f"Query completed. Number of results: {len(results)}")
        # logging.info(f"Sample Results: {results[:1]}")
        return jsonify(results)
    except Exception as e:
        logging.error(f'[query offer] Error querying document: {e}')
        return f'Error querying document: {e}', 500


# sample request body and run this function locally
# if __name__ == '__main__':
#     request = {
#         "offerProvider": "Amex",
#         "offerMerchant": None
#     }
#     import json
#     request = json.dumps(request)

#     print(query_offers(request))
