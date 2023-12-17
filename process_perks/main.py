import logging
from google.cloud import firestore
from datetime import datetime
from dateutil import parser


def process_perks(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'offerDetail' in request_json:
        data = request_json
    elif request_args and 'offerDetail' in request_args:
        data = request_args
    else:
        return 'Invalid data format', 400

    # Logging and processing offerExpireDate
    if 'offerExpireDate' in data:
        try:
            # Check if offerExpireDate is already a datetime object
            if isinstance(data['offerExpireDate'], datetime):
                # logging.info("offerExpireDate is already a datetime object.")
                pass

            # If offerExpireDate is a string, try to parse it as a datetime object
            elif isinstance(data['offerExpireDate'], str):
                data['offerExpireDate'] = parser.parse(data['offerExpireDate'])
                # logging.info("Parsed offerExpireDate from string to datetime.")

            # If offerExpireDate is a numeric value, treat it as milliseconds since epoch
            elif isinstance(data['offerExpireDate'], (int, float)):
                expire_date_seconds = int(data['offerExpireDate']) // 1000
                data['offerExpireDate'] = datetime.fromtimestamp(
                    expire_date_seconds)
                # logging.info(
                #     "Converted offerExpireDate from milliseconds to datetime.")

            else:
                logging.error(
                    "[process offer] Unrecognized type for offerExpireDate; leaving as is.")

        except Exception as e:
            logging.error(f"Error parsing offerExpireDate: {e}")
            logging.info(
                "Using current datetime as fallback for offerExpireDate.")
            # Fallback to current datetime
            data['offerExpireDate'] = datetime.now()

    # Initialize Firestore DB
    db = firestore.Client()
    try:
        # Add data to Firestore
        doc_ref = db.collection('creditCardPerks').add(data)
        return f'Perk added with ID: {doc_ref[1].id}'
    except Exception as e:
        logging.error(f'[process offer] Error adding document: {e}')
        return f'Error adding document: {e}', 500
