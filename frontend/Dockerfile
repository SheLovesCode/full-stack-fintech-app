FROM node:20-alpine AS builder
WORKDIR /app

# Copy package.json first
COPY frontend/package*.json ./


# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ ./

# Build the project
RUN npm run build


# Stage 2: Serve with NGINX
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY ../nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
