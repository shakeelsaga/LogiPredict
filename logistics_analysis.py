import datetime

# I'm defining some constants here to make my code more readable.
# These are the codes I'm using to identify different types of events.
TRANSIT_CODES = {'DP', 'IT', 'OD', 'IX'}
ARRIVAL_CODES = {'AR', 'DL'}

def parse_mongo_date(date_obj):
    # I created this function to parse the date format I'm getting from my data source.
    # It's a bit of a weird format, so I needed a custom function to handle it.
    try:
        if isinstance(date_obj, dict) and "$numberLong" in date_obj:
            timestamp_ms = float(date_obj["$numberLong"])
            return datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
        return None
    except (KeyError, ValueError, TypeError):
        return None

def process_shipment_data(data):
    # This is the main function I'm using to process my shipment data.
    # It takes the raw JSON data and turns it into a clean list of dictionaries.
    shipment_data = []

    for item in data:
        track_details_list = item.get('trackDetails')
        if not track_details_list:
            continue
        
        track_detail = track_details_list[0]
        
        # Here, I'm extracting the basic information about the shipment.
        tracking_number = track_detail.get('trackingNumber')
        service_type = track_detail.get('service', {}).get('type', 'UNKNOWN')
        package_weight = track_detail.get('packageWeight', {}).get('value', 0)
        
        shipper_addr = track_detail.get('shipperAddress', {})
        origin_city = shipper_addr.get('city', 'Unknown').upper()
        
        dest_addr = track_detail.get('destinationAddress', {})
        dest_city = dest_addr.get('city', 'Unknown').upper()

        # Now, I'm processing the events associated with the shipment.
        events = track_detail.get('events', [])
        # I'm sorting the events by timestamp to make sure they're in chronological order.
        events.sort(key=lambda x: float(x.get('timestamp', {}).get('$numberLong', 0)))

        pickup_time = None
        delivery_time = None
        
        for event in events:
            event_type = event.get('eventType')
            evt_time = parse_mongo_date(event.get('timestamp'))
            
            if event_type == 'PU':
                pickup_time = evt_time
            elif event_type == 'DL':
                delivery_time = evt_time

        # Finally, I'm calculating the transit time.
        transit_hours = 0.0
        if pickup_time and delivery_time:
            transit_time = delivery_time - pickup_time
            transit_hours = round(transit_time.total_seconds() / 3600, 2)

        # I'm adding the processed data to my list.
        shipment_data.append({
            'tracking_number': tracking_number,
            'service_type': service_type,
            'weight_kg': package_weight,
            'origin_city': origin_city,
            'destination_city': dest_city,
            'transit_hours': transit_hours,
            'status': 'Delivered' if delivery_time else 'In Transit'
        })

    return shipment_data