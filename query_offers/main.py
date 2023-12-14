from google.cloud import firestore
from flask import escape, jsonify
from datetime import datetime


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
                offer_expiration = doc_data.get('offerExpireDate')

                # Check if offer_expiration is a datetime object
                if isinstance(offer_expiration, datetime):
                    if include_expired or offer_expiration > current_date:
                        results.append(doc_data)
                elif offer_expiration is None and include_expired:
                    # Include offers without expiration date when include_expired is True
                    results.append(doc_data)
            except Exception as doc_error:
                print(f"Error processing document {doc.id}: {doc_error}")

        return jsonify(results)
    except Exception as e:
        return f'Error querying document: {e}', 500
