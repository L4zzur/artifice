ARG NODE_VERSION=22.21

FROM node:${NODE_VERSION}-alpine AS builder

RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app
COPY package.json pnpm-lock.yaml* ./

RUN pnpm install --frozen-lockfile

COPY . .

RUN pnpm exec svelte-kit sync
RUN pnpm run build

FROM node:${NODE_VERSION}-alpine AS runner

RUN apk add --no-cache wget
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

COPY package.json pnpm-lock.yaml* ./

RUN pnpm install --prod --frozen-lockfile

COPY --from=builder /app/build ./build
COPY --from=builder /app/.svelte-kit ./.svelte-kit

ENV NODE_ENV=development
ENV PORT=3000
ENV PUBLIC_API_URL=http://localhost:8000

EXPOSE 3000

CMD ["node", "build"]
