# Monbot
A Discord-based Pokemon-style game. Summon elementals and battle them one-on-one versus AI or other players.

# Running unit tests
Run the `run_me!.py` file in the tests directory.

# Run your own instance of Monbot
Dependencies:
- Boto3 and AWS (for storing data)

1) Clone this repository.
2) Add an application to your Discord Developer Portal, if you haven't already. You can do so at <https://discordapp.com/developers/applications/>.
3) Generate a Bot Token and hook it up. We'll need to make a minor modification to the src files for this. 
  - In your newly-created Monbot application, you can generate a Bot Token under "Bot" in the sidebar.
  - In the `src` folder of this repository, create a file called `discord_token.py`.
  - Add the token as a string variable called TOKEN. For example, all that's contained in your `discord_token.py` file should be
  ```
  TOKEN = 'DSDH7109...' # Your token here.
  ```
4) The tough part: setting up the backend. Currently, Monbot only supports DynamoDB for its server-side data storage. Monbot will attempt to connect to Dynamo, but if it fails, all back-end related calls won't work.
Monbot expects three tables that you can create in your AWS Console:
- Elementals
- Players
- Inventories

5) Add your new bot to a server of choice.
6) Launch Monbot by running the Monbot.py file!
