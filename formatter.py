

def format_actors(shipment: dict) -> str:
    """
    Format the Sender and Receiver information into a neat and easily readable format
    """

    collectFrom = shipment.get("location", "Unknown").get("collectFrom", "Unknown")
    deliverTo = shipment.get("location", "Unknown").get("deliverTo", "Unknown")
    return f"""
Sent from: {collectFrom.get("postCode", "Unknown")}, {collectFrom.get("city", "Unknown")}, \
{collectFrom.get("country", "Unknown")}
Sent to: {deliverTo.get("postCode", "Unknown")}, {deliverTo.get("city", "Unknown")}, \
{deliverTo.get("country", "Unknown")}
"""


def format_package_info(packageDetails: dict) -> str:
    """
    Format the package information, such as Pieces, Weight, Dimensions etc. into a easily readable format.
    """

    pieces = (
        f"Pieces: {packageDetails.get("pieces", "")}\n"
        if packageDetails.get("pieces")
        else "")
    volume = (
        f"Volume: {packageDetails.get("volume", "").get("value")} {packageDetails.get("volume", "").get("unit", "")}\n" 
        if packageDetails.get("pieces") 
        else "")
    weight = (
        f"Weight: {packageDetails.get("weight", "").get("value")} {packageDetails.get("weight", "").get("unit", "")}\n" 
        if packageDetails.get("weight") 
        else "")
    # I couldnt find an instance of a package with dimensions given from the test reference numbers, so I dont know
    # what format they come in, so this might will probably need to be adjusted a bit after we've seen
    # the format
    dimensions = (
        f"Dimensions: {packageDetails.get("dimensions", "")}\n" 
        if packageDetails.get("dimensions") 
        else "")
    loadingMeters = (
        f"Loading Meters: {packageDetails.get("loadingMeters", "").get("value")} {packageDetails.get("loadingMeters", "").get("unit", "")}\n" 
        if packageDetails.get("loadingMeters") 
        else "")
    stackable = (
            f"Stackable: {packageDetails.get("stackable", "")}\n"
            if packageDetails.get("stackable")
            else "")
    chargeableWeight = (
        f"Chargeable weight: {packageDetails.get("chargeableWeight", "").get("value")} {packageDetails.get("chargeableWeight", "").get("unit", "")}\n" 
        if packageDetails.get("chargeableWeight") 
        else "")
    agreementDangerousRoad = (
            f"Agreement Dangerous Road: {packageDetails.get("agreementDangerousRoad", "")}\n"
            if packageDetails.get("agreementDangerousRoad")
            else "")
    customsDuty = (
            f"Customs duty: {packageDetails.get("customsDuty", "")}"
            if packageDetails.get("customsDuty")
            else "")
    return f"""\
{pieces}{volume}{weight}{dimensions}{loadingMeters}{stackable}\
{chargeableWeight}{agreementDangerousRoad}{customsDuty}"""
    
def format_package_events(events: list) -> str:
    """
    Format the events into a easily readable format.
    """


    eventsString = f"""
Shipment Status History:

Event       |   Date                |   Location        |   Reason
---------------------------------------------------------------------
"""
    for event in events:
        reasons = f""
        for reason in event.get("reasons", []):
            reasons += reason.get("description", "")
        eventsString += f"""\
{event.get("code", "")}       |   {event.get("date", "")} |   {event.get("location", "").get("name", "")}\
        |   {reasons}\n"""
    return eventsString

def format_response(shipment: dict) -> str:
    """Format the final response into a easily readable format."""

    actorsInfo = format_actors(shipment)
    packageDetails = shipment.get("goods", "Unknown")
    packageInfo = format_package_info(packageDetails)
    events = shipment.get("events", [])
    eventsInfo = format_package_events(events)
    return f"""
{actorsInfo}
    
Package details: 
{packageInfo}

{eventsInfo}
"""