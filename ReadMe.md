
# Managing the Container

## All Commands run as sudo

  rootless docker is painful!

## Start in detached mode (runs in background)

  sudo docker compose up -d

## View logs

  sudo docker compose logs

## Follow logs in real-time

  sudo docker compose logs -f

## View logs for specific service

  sudo docker compose logs -f quart_app

## Stop the container

  sudo docker compose down

# Restart after code changes (if auto-reload doesn't work)

  sudo docker compose restart quart_app

# Check status

  sudo docker compose ps -a

## Starting the container

  cd /home/picontrol/Code/robot_simulation
  
  sudo docker compose up -d

## On Code Change and Pull

  After pulling code changes, Quart detects the change and reloads automatically

## Restart manually

  sudo docker compose restart quart_app


  
