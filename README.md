# Govee Bot

Govee Bot is a Discord bot designed to control Govee devices, specifically for managing a fan. With this bot, you can send commands to your fan to turn it on or off, adjust the speed and control oscillation.

## Prerequisites

- A Discord bot token
- A Govee API key
- Device ID and SKU for your Govee device

## Setup Guide

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and give your application a name.
3. Navigate to the "Bot" section and click "Add Bot."
4. Copy the bot token. You'll need this for configuration.

### 2. Obtain a Govee API Key

1. Visit the [Govee Developer API](https://developer.govee.com/reference/apply-you-govee-api-key) page.
2. Apply for an API key and copy it.

### 3. Retrieve Device ID and SKU

1. Use the following `curl` command to get the Device ID and SKU for your Govee device:

    ```bash
    curl -X GET "https://openapi.api.govee.com/router/api/v1/user/devices" \
    -H "Content-Type: application/json" \
    -H "Govee-API-Key: YOUR_GOVEE_API_KEY"
    ```

2. Note the `device_id` and `sku` from the response.

### 4. Configure the Bot

1. Create a file named `config.json` in the root directory of your project.
2. Add the following content to the file, replacing the placeholders with your actual values:

    ```json
    {
        "token": "YOUR_DISCORD_BOT_TOKEN",
        "api_key": "YOUR_GOVEE_API_KEY",
        "device_id": "YOUR_DEVICE_ID",
        "sku": "YOUR_SKU"
    }
    ```

### 5. Install Dependencies

Ensure you have Python 3 and pip installed. Install the required Python packages:

```bash
pip install discord.py aiohttp requests
