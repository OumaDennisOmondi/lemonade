#!/bin/bash
# Build the image
docker build -t laravel-app:prod .

# Run the container
docker run -d \
    --name laravel-app \
    -p 9000:9000 \
    -e APP_ENV=production \
    -e APP_KEY=base64:your-key-here \
    -e DB_HOST=your-db-host \
    -e DB_DATABASE=your-db-name \
    -e DB_USERNAME=your-db-user \
    -e DB_PASSWORD=your-db-password \
    laravel-app:prod