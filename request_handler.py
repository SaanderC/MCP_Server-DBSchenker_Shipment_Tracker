from playwright.async_api import async_playwright
import sys
from typing import Any



# Constants
DBSCHENKER_API_BASE = "https://www.dbschenker.com/app/tracking-public/?refNumber="
USER_AGENT = "shipment-tracker/1.0"


async def make_shipment_request(tracking_reference: str) -> dict[str, Any] | None:
    """
    Make a request to the DB Schenker tracking website, given a specific tracking reference.
    """

    target_url_fragment = "/api/public/tracking-public/shipments"
    captured_data = None

    # Open the browser with playwright, execute the scripts for the api call and collect the wanted json
    async with async_playwright() as p:

        # Start the browser inside the 'p' context
        browser = await p.firefox.launch(headless=True)

        # New context, no cookies, same behavior every time
        context = await browser.new_context() 
        page = await context.new_page()

        try:
            # Lambda function checks for the target api call.
            async with page.expect_response(
            lambda res: target_url_fragment in res.url and len(res.url) > len(f"{DBSCHENKER_API_BASE}{target_url_fragment}")
            and res.status == 200,
            timeout=45000
        ) as response_info:

                url = f"{DBSCHENKER_API_BASE}{tracking_reference}"
            
                # Load the page and wait until the network is idle
                await page.goto(url, wait_until="networkidle", timeout=45000)

                response = await response_info.value
                captured_data = await response.json()

                # Check to see that the data is in fact the correct one
                if "sttNumber" not in str(captured_data):
                    print("Wrong package", file=sys.stderr)
                    captured_data = None
                else:
                    print("Successfully captured the correct package", file=sys.stderr)

        except Exception as e:
            print(f"DEBUG: Failed to capture response: {e}", file=sys.stderr)
            captured_data = None

        #Close the browser after the function is done
        finally:
            await browser.close()

    return captured_data
    