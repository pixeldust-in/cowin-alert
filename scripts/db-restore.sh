#!/usr/bin/env bash
# Restore your PSQL database.

set -e
set -o pipefail

backup_path="/var/lib/sendy-backup"
BUCKET_NAME="$(grep -o "DB_BACKUP_BUCKET=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
file_name="${1}"
export PGDATABASE="${2}"
restore_path="/tmp/${file_name}"

app_env_file="/srv/cowin-alert/.env"
export PGHOST="$(grep -o "DB_HOST=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export PGUSER="$(grep -o "POSTGRES_USER=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export PGPASSWORD="$(grep -o "POSTGRES_PASSWORD=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export AWS_ACCESS_KEY_ID="$(grep -o "AWS_ACCESS_KEY_ID=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export AWS_SECRET_ACCESS_KEY="$(grep -o "AWS_SECRET_ACCESS_KEY=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export AWS_DEFAULT_REGION="$(grep -o "AWS_DEFAULT_REGION=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
BUCKET_NAME="$(grep -o "DB_BACKUP_BUCKET=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"


/usr/bin/aws s3 cp s3://${BUCKET_NAME}/backups/${file_name} ${restore_path} --sse

error_message="You must supply a file and db name, example: ${0} $(date +%F-%H-%M-%S)_cowin-alert.tar test-db"

if [ -z "${filename}" ]; then
    echo error_message
    exit 1
fi

if [ -z "${PGDATABASE}" ]; then
    echo error_message
    exit 1
fi

if [ ! -f "${restore_path}" ]; then
    echo "'${restore_path}' not found"
    exit 1
fi

read -p "Restoring is going to wipe your current database, are you sure (y/n)? " -n 1 -r
echo
if [[ ! "${REPLY}" =~ ^[yY]$ ]]; then
    echo "The '${PGDATABASE}' database was not restored because you didn't type y or Y."
    exit 1
fi

pg_restore --no-owner --role=${PGUSER} "${restore_path}" -v
rm ${restore_path}

echo "The '${PGDATABASE}' database was successfully restored from '${file_name}'"