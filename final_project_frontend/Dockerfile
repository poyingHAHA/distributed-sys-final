# 使用輕量級的 Nginx 基礎映像
FROM nginx:stable-alpine

# 複製 React 構建文件到 Nginx 靜態文件目錄
COPY build /usr/share/nginx/html

# 暴露 Nginx 默認端口
EXPOSE 80

# 啟動 Nginx
CMD ["nginx", "-g", "daemon off;"]
