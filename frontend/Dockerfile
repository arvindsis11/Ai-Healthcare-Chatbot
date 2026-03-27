FROM node:20-alpine AS deps
WORKDIR /app
COPY frontend/package.json /app/package.json
RUN npm install

FROM node:20-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules /app/node_modules
COPY frontend /app
ARG BACKEND_URL=http://backend:8000
ENV BACKEND_URL=${BACKEND_URL}
RUN npm run build

FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app /app
EXPOSE 3000
CMD ["npm", "run", "start"]
