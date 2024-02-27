# #!/bin/bash
# echo a;
# # while ! mysql -u root -psakip  -e --host=sakip_db";" ; do
# #        read -s -p "Can't connect, please retry: " mysqlRootPassword
# # done
#!/bin/sh
# wait-for-mysql.sh
status=1
while [ $status -gt 0 ]
do
  mysql -u $DB_USER -p$DB_PASSWORD --host=$DB_HOST -e '\q' > /dev/null 2>&1
  status=$?
  sleep 1
  echo "mysql is unavailable - sleeping"
done
echo "mysql is up - executing command"