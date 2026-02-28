from mcp.server.fastmcp import FastMCP
from formatter import format_response
from request_handler import make_shipment_request

# Initialize FastMCP server
mcp = FastMCP("shipment tracking")

@mcp.tool()
async def get_shipment_details(tracking_reference: str) -> str:
    """Get shipment details for a specific package.

    Args:
        tracking_reference: A 10-digit reference number for a package.
    """


    shipment = await make_shipment_request(tracking_reference)

    # Double check that it is the correct json
    if not shipment or "sttNumber" not in shipment:
        return "Unable to fetch shipment details or no shipments found."


    response = format_response(shipment)
    return response

"""
async def main():
    # Initialize and run the server
    mcp.run(transport="stdio")
    ref = "1806203236"
    shipment = await make_shipment_request(ref)
    if not shipment or "sttNumber" not in shipment:
        print("Fel block", file = sys.stderr)
        return "Unable to fetch shipment details or no shipments found."

    response = format_response(shipment)
    print(response)
"""

if __name__ == "__main__":

    #For manual debugging:
    #asyncio.run(main())

    mcp.run(transport="stdio")
