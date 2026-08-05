# Этап 1: сборка Nuxt-приложения
FROM oven/bun:1-alpine AS build
WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build

# Этап 2: лёгкий рантайм — только собранный .output
FROM oven/bun:1-alpine
WORKDIR /app

ENV NODE_ENV=production \
    NITRO_HOST=0.0.0.0 \
    NITRO_PORT=3000

COPY --from=build /app/.output ./.output

EXPOSE 3000
CMD ["bun", ".output/server/index.mjs"]
