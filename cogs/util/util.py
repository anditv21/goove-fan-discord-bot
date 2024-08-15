import discord
from discord import app_commands
from discord.ext import commands
import requests
import uuid

from helpers.config import get_config_value

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = None
        self.device_id = None
        self.sku = None

    async def get_device_config(self):
        """Load device configuration from the config file."""
        self.api_key = get_config_value('api_key')
        self.device_id = get_config_value('device_id')
        self.sku = get_config_value('sku')

    def handle_error(self, response):
        """Handle API errors and print relevant messages."""
        error_messages = {
            400: 'Bad Request - Check your request parameters.',
            404: 'Not Found - Device or instance not found.',
            429: 'Too Many Requests - Rate limit exceeded.',
        }
        code = response.status_code
        message = error_messages.get(code, 'An unknown error occurred.')
        print(f'Error {code}: {message}')

    def control_device(self, device_id, sku, capability_type, instance, value):
        """Send a control command to the device."""
        headers = {'Govee-API-Key': self.api_key, 'Content-Type': 'application/json'}
        payload = {
            "requestId": str(uuid.uuid4()),
            "payload": {
                "sku": sku,
                "device": device_id,
                "capability": {
                    "type": capability_type,
                    "instance": instance,
                    "value": value
                }
            }
        }
        response = requests.post('https://openapi.api.govee.com/router/api/v1/device/control', json=payload, headers=headers)
        if response.status_code != 200:
            self.handle_error(response)

    def query_device_state(self, device_id, sku):
        """Query the current state of the device."""
        headers = {'Govee-API-Key': self.api_key, 'Content-Type': 'application/json'}
        payload = {
            "requestId": str(uuid.uuid4()),
            "payload": {
                "sku": sku,
                "device": device_id
            }
        }
        response = requests.post('https://openapi.api.govee.com/router/api/v1/device/state', json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            self.handle_error(response)
            return None

    @app_commands.command(name="fan_on", description="Turn on the fan")
    async def fan_on(self, interaction: discord.Interaction):
        """Command to turn on the fan."""
        if interaction.user.id != 854024514781315082:
            await interaction.response.send_message("You are not authorized to use this command.")
            return

        # Send an initial deferred response
        await interaction.response.defer()

        try:
            await self.get_device_config()
            if self.device_id and self.sku:
                self.control_device(self.device_id, self.sku, 'devices.capabilities.on_off', 'powerSwitch', 1)
                await interaction.followup.send("Fan turned on.")
            else:
                await interaction.followup.send("Failed to configure the device.")
        except Exception as e:
            print(f"An error occurred: {e}")
            if not interaction.response.is_done():
                await interaction.followup.send("An error occurred while trying to turn on the fan.")

    @app_commands.command(name="fan_off", description="Turn off the fan")
    async def fan_off(self, interaction: discord.Interaction):
        """Command to turn off the fan."""
        if interaction.user.id != 854024514781315082:
            await interaction.response.send_message("You are not authorized to use this command.")
            return

        await interaction.response.defer()

        try:
            await self.get_device_config()
            if self.device_id and self.sku:
                self.control_device(self.device_id, self.sku, 'devices.capabilities.on_off', 'powerSwitch', 0)
                await interaction.followup.send("Fan turned off.")
            else:
                await interaction.followup.send("Failed to configure the device.")
        except Exception as e:
            print(f"An error occurred: {e}")
            if not interaction.response.is_done():
                await interaction.followup.send("An error occurred while trying to turn off the fan.")

    @app_commands.command(name="set_speed", description="Set the fan speed")
    @app_commands.describe(speed="Speed (1-8)")
    async def set_speed(self, interaction: discord.Interaction, speed: int):
        """Command to set the fan speed."""
        if interaction.user.id != 854024514781315082:
            await interaction.response.send_message("You are not authorized to use this command.")
            return

        if 1 <= speed <= 8:
            await interaction.response.defer()
            try:
                await self.get_device_config()
                if self.device_id and self.sku:
                    self.control_device(self.device_id, self.sku, 'devices.capabilities.work_mode', 'workMode', {'workMode': 1, 'modeValue': speed})
                    await interaction.followup.send(f"Fan speed set to {speed}.")
                else:
                    await interaction.followup.send("Failed to configure the device.")
            except Exception as e:
                print(f"An error occurred: {e}")
                if not interaction.response.is_done():
                    await interaction.followup.send("An error occurred while trying to set the fan speed.")
        else:
            await interaction.response.send_message("Invalid speed value. Please enter a number between 1 and 8.")

    @app_commands.command(name="toggle_oscillation", description="Toggle fan oscillation")
    @app_commands.describe(toggle="1 to turn on, 0 to turn off")
    async def toggle_oscillation(self, interaction: discord.Interaction, toggle: int):
        """Command to toggle fan oscillation."""
        if interaction.user.id != 854024514781315082:
            await interaction.response.send_message("You are not authorized to use this command.")
            return

        if toggle in [0, 1]:
            await interaction.response.defer()
            try:
                await self.get_device_config()
                if self.device_id and self.sku:
                    self.control_device(self.device_id, self.sku, 'devices.capabilities.toggle', 'oscillationToggle', toggle)
                    await interaction.followup.send(f"Oscillation {'enabled' if toggle else 'disabled'}.")
                else:
                    await interaction.followup.send("Failed to configure the device.")
            except Exception as e:
                print(f"An error occurred: {e}")
                if not interaction.response.is_done():
                    await interaction.followup.send("An error occurred while trying to toggle the oscillation.")
        else:
            await interaction.response.send_message("Invalid input. Enter 0 or 1.")


    @app_commands.command(name="query_state", description="Query the current state of the fan")
    async def query_state(self, interaction: discord.Interaction):
        """Command to query the current state of the fan."""
        if interaction.user.id != 854024514781315082:
            await interaction.response.send_message("You are not authorized to use this command.")
            return

        await interaction.response.defer()
        try:
            await self.get_device_config()
            if self.device_id and self.sku:
                state = self.query_device_state(self.device_id, self.sku)
                if state:
                    await interaction.followup.send(f"Current Device State: {state}")
                else:
                    await interaction.followup.send("Failed to retrieve the device state.")
            else:
                await interaction.followup.send("Failed to configure the device.")
        except Exception as e:
            print(f"An error occurred: {e}")
            if not interaction.response.is_done():
                await interaction.followup.send("An error occurred while trying to query the device state.")

async def setup(bot):
    await bot.add_cog(Util(bot))
