FROM node:20

WORKDIR /opt/prae-fe/

COPY . .

RUN ["npm", "ci"]

EXPOSE 5173

CMD ["npm", "run", "dev", "--host"]

