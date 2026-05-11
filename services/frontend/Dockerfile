# 1. build 阶段
FROM node:20 as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

# 2. nginx 运行阶段
FROM nginx:alpine

# ❗把 React build 放进 nginx
COPY --from=build /app/build /usr/share/nginx/html

# ❗覆盖 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]