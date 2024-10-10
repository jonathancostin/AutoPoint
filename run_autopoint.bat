@echo off
docker run -it --rm --name autopoint -v autopoint_data:/app/data jonathancostin/autopoint %*
