# owl-bot
I have an inside joke on my friends' Discord server. Whenever anyone mentions the string literal "who," they are assigned a Discord role called "Owl." This is a manual process and this bot, Dockerized so I can run it on my server, automates it!

Very simple set-up (this is not a microservices application, eventually going to get this running on a K8S cluster).
0. Install Docker and `docker-compose`.
1. Clone this repository.
2. Rename the file `.env.example` to `.env` and add your Discord token (you can find that under the Bot subcategory in the Dev portal. _When scoping your Discord bot, make sure it has the `Server Members Intent` and `Message Content Intent.` When setting up an OAuth invite. and scope the OAuth invite link to include `bot` and `manage roles`._
3. On your host machine, you can use the following `docker-compose.yml` to get started:
```
version: '3.8'
services:
  owl-bot:
    build: .
    container_name: discord_owl_bot
    restart: always
    env_file:
      - .env
```
That's it! 
