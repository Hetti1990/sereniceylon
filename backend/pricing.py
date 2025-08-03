from models import Currency, Hotel, Transport, Sightseeing, EntranceFee

def calculate_total_cost(itinerary_details, target_currency_code):
    """
    Calculates the total cost of an itinerary in the target currency.

    :param itinerary_details: A dictionary containing the details of the itinerary.
                              Example:
                              {
                                  "hotels": [{"id": 1, "nights": 2}],
                                  "transports": [{"id": 1}],
                                  "sightseeing": [{"id": 1, "pax": 2, "include_entrance_fee": True}],
                                  "pax": 2
                              }
    :param target_currency_code: The code of the target currency (e.g., "USD").
    :return: The total cost in the target currency.
    """
    total_cost = 0.0

    # --- Currency Conversion ---
    target_currency = Currency.query.filter_by(code=target_currency_code).first()
    if not target_currency:
        raise ValueError(f"Target currency '{target_currency_code}' not found.")

    def convert_to_target_currency(amount, source_currency_code):
        if source_currency_code == target_currency_code:
            return amount

        source_currency = Currency.query.filter_by(code=source_currency_code).first()
        if not source_currency:
            raise ValueError(f"Source currency '{source_currency_code}' not found.")

        # Convert source to base currency (e.g., USD), then to target currency.
        # This assumes a common base currency is used for exchange rates.
        # For simplicity, let's assume all exchange rates are relative to a base currency (e.g., USD).
        # To convert from currency A to B: (amount_A / rate_A) * rate_B
        if source_currency.exchange_rate == 0:
            raise ValueError(f"Exchange rate for '{source_currency_code}' cannot be zero.")

        return (amount / source_currency.exchange_rate) * target_currency.exchange_rate

    # --- Hotel Costs ---
    if 'hotels' in itinerary_details:
        for hotel_info in itinerary_details['hotels']:
            hotel = Hotel.query.get(hotel_info['id'])
            if hotel:
                # Assuming hotel rate is per night and in USD.
                hotel_cost_usd = hotel.rate * hotel_info.get('nights', 1)
                cost_in_target_currency = convert_to_target_currency(hotel_cost_usd, 'USD')
                total_cost += cost_in_target_currency

    # --- Transport Costs ---
    if 'transports' in itinerary_details:
        for transport_info in itinerary_details['transports']:
            transport = Transport.query.get(transport_info['id'])
            if transport:
                cost_in_target_currency = convert_to_target_currency(transport.cost, transport.currency)
                total_cost += cost_in_target_currency

    # --- Sightseeing Costs ---
    if 'sightseeing' in itinerary_details:
        for activity_info in itinerary_details['sightseeing']:
            sight = Sightseeing.query.get(activity_info['id'])
            if sight and sight.is_paid and activity_info.get('include_entrance_fee'):
                entrance_fee = EntranceFee.query.filter_by(sightseeing_id=sight.id).first()
                if entrance_fee:
                    pax = activity_info.get('pax', 1)
                    cost_in_target_currency = convert_to_target_currency(entrance_fee.cost, entrance_fee.currency)
                    total_cost += cost_in_target_currency * pax

    return total_cost
