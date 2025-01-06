# Step 1: Use PHP-FPM with specific version
FROM php:8.1-fpm

# Step 2: Set working directory
WORKDIR /var/www

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    mbstring \
    exif \
    pcntl \
    bcmath \
    gd \
    zip \
    opcache

# Step 4: Configure PHP for production
COPY docker/php/production.ini /usr/local/etc/php/conf.d/production.ini
COPY docker/php/opcache.ini /usr/local/etc/php/conf.d/opcache.ini

# Step 5: Install Composer
COPY --from=composer:2.6 /usr/bin/composer /usr/bin/composer

# Step 6: Create non-root user for security
ARG USER=laravel
ARG UID=1000
RUN useradd -G www-data,root -u $UID -d /home/$USER $USER
RUN mkdir -p /home/$USER/.composer && \
    chown -R $USER:$USER /home/$USER

# Step 7: Copy application files
COPY --chown=$USER:$USER . /var/www
COPY --chown=$USER:$USER .env.production /var/www/.env

# Step 8: Set proper permissions
RUN chmod -R 775 /var/www/storage /var/www/bootstrap/cache && \
    chown -R $USER:$USER /var/www

# Step 9: Switch to non-root user
USER $USER

# Step 10: Install dependencies and optimize
RUN composer install --no-dev --optimize-autoloader --no-scripts && \
    php artisan optimize && \
    php artisan view:cache && \
    php artisan config:cache && \
    php artisan route:cache

# Step 11: Switch back to root for FPM
USER root

# Step 12: Configure PHP-FPM for production
COPY docker/php/www.conf /usr/local/etc/php-fpm.d/www.conf

# Step 13: Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:9000/ || exit 1

# Step 14: Expose port
EXPOSE 9000

# Step 15: Start PHP-FPM
CMD ["php-fpm"]