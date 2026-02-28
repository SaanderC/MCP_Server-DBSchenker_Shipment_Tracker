# MCP Server for shipment tracking

A MCP server with tools that, given a order reference number, returns shipment information of a DBSchenker order.

## Installation and dependencies

The installation instructions are made for Linux/macOS. If you are on Windows, the commands will differ.

### uv package manager

Install the uv Python package manager, if you don't have it already.

Run the following command in your terminal:

    $ curl -LsSf https://astral.sh/uv/install.sh | sh

Then make sure to restart your terminal afterwards and ensure that the uv command gets picked up.

Navigate to the root directory of the project, and run "uv sync".

### Browser binaries

The tool uses firefox to fetch the shipment details. To install those, simply run:

    $ uv run playwright install firefox

### Configure your MCP Client

You now have to configure your client so that it can detect the server. If you are on Claude Desktop, you can edit your configuration file by running:

    $ nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

If you are using Gemini Cli, use:

    $ nano ~/.gemini/settings.json

Then add the following configuration:

    {

        "mcpServers": {

            "shipment tracking": {

            "command": "uv",

            "args": [

                "--directory",

                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/shipment_tracker",

                "run",

                "shipment_tracker.py"

            ]

            }

        }
    
    }

This will notify your client of the server, where it is, and how to run it.