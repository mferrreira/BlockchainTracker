# Use official node image as a base
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json /app/
RUN npm install

# Copy the frontend files
COPY . /app

# Expose the Vite dev server port
EXPOSE 3000

# Run the frontend (Vite dev server)
CMD ["npm", "run", "dev"]
