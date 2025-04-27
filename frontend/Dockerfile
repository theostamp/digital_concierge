# Use Node image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install deps
COPY package.json package-lock.json* ./
RUN npm install

# Copy rest of the code
COPY . .

# Expose frontend dev server port
EXPOSE 3000

# Start dev server with Turbopack
CMD ["npm", "run", "dev"]
