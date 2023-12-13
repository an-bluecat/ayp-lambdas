from google.cloud import firestore
# from flask import escape


def process_perks(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'offerDetail' in request_json:
        data = request_json
    elif request_args and 'offerDetail' in request_args:
        data = request_args
    else:
        return 'Invalid data format', 400

    # Initialize Firestore DB
    db = firestore.Client()
    try:
        # Add data to Firestore
        doc_ref = db.collection('creditCardPerks').add(data)
        return f'Perk added with ID: {doc_ref[1].id}'
    except Exception as e:
        return f'Error adding document: {e}', 500
