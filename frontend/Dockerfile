FROM node:18

WORKDIR /app

COPY package.json .
COPY src ./src/
COPY angular.json .
COPY tsconfig.app.json .
COPY tsconfig.json .
COPY tsconfig.spec.json .

RUN npm install && \
    npm install -g serve && \
    npm install -g @angular/cli && \
    npm install --save-dev @angular-devkit/build-angular && \
    npm run build

# nginx setup
FROM nginx:stable-alpine
COPY --from=0 /app/dist/frontend_angular /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx","-g","daemon off;"]
