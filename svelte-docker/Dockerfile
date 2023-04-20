FROM node:12 AS build

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app
RUN npm install
COPY . /app
RUN npm run dev

# FROM nginx:1.19-alpine
# COPY --from=build /app/public /usr/share/nginx/html