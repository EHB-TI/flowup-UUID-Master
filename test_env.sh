cp init.sql.example init.sql
cp .env.example .env
sed -i '$d' .env
echo "MYSQL_ROOT_PASSWORD=toor" >> .env
docker-compose up -d
echo "starting tests in 15 seconds..."
sleep 15