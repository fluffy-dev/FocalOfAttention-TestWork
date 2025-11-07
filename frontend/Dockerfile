# ---- Stage 1: Build the React App ----
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application source code
COPY . .

# Build the production-ready static files
RUN npm run build

# ---- Stage 2: Serve the App with Nginx ----
FROM nginx:1.25-alpine

# Copy the built static files from the 'build' stage
COPY --from=build /app/build /usr/share/nginx/html

# Remove the default Nginx welcome page
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d

# Expose port 80 for the Nginx server
EXPOSE 80

# The command to start Nginx
CMD ["nginx", "-g", "daemon off;"]