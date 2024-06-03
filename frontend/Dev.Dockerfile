FROM node:18

WORKDIR /opt/prae-fe/frontend
COPY . .

RUN corepack enable
RUN corepack prepare pnpm@latest-9 --activate
RUN pnpm config set store-dir .pnpm-store
RUN pnpm install

EXPOSE 3000

CMD ["pnpm", "run", "dev", "--host"]
