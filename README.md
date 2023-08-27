# Signal Dalle 💬

Signal bot to make using OpenAI DALL-E model easy. 

Communication with DALL-E is done via Signal group conversation.

## Functions
- 🪄 **Generate image** - simply by writing message to group
- 🪄 **Generate image variations** - simply by sending image to group
- 🪄 **Generate image edit** - simply by sending image with caption. Draw with white pencil to specify mask.

## Setup

### Step 1: Connect with your signal account
Start containers using bellow command:
```
docker compose -f compose/docker-compose.connect.yml
```

Then visit `http://127.0.0.1:37899/v1/qrcodelink?device_name=<device-name>`

Connect with your signal account using visible QR code.

This will create config directory containing your credentials.

### Step 2: Get group identifiers

Create `.env` file by copying `example.env`:

```
cp compose/example.env compose/.env
```

Inside `.env` fill your phone number and run bellow command:

```
docker compose -f compose/docker-compose.group.yml
```

Note `id` and `internal id` of group which You want to use and fill approprivate variables in `.env`


### Step 3: Launch bot

Fill remaining variables in `.env` and run bellow command.

```
docker compose -f compose/docker-compose.bot.yml
```
