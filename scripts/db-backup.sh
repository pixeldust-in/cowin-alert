#!/usr/bin/env bash
# Backup your local PSQL database to a compressed file.

set -e
set -o pipefail

app_env_file="/srv/cowin-alert/.env"
export PGHOST="$(grep -o "DB_HOST=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export PGUSER="$(grep -o "POSTGRES_USER=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export PGPASSWORD="$(grep -o "POSTGRES_PASSWORD=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export PGDATABASE="$(grep -o "POSTGRES_DB=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export AWS_ACCESS_KEY_ID="$(grep -o "AWS_ACCESS_KEY_ID=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export AWS_SECRET_ACCESS_KEY="$(grep -o "AWS_SECRET_ACCESS_KEY=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
export AWS_DEFAULT_REGION="$(grep -o "AWS_DEFAULT_REGION=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"
BUCKET_NAME="$(grep -o "DB_BACKUP_BUCKET=.*" $app_env_file | cut -d "=" -f 2 | sed "s/'//g;s/ //g")"

backup_file_name=$(date +%F-%H-%M-%S)-cowin-alert.tar
/usr/bin/pg_dump -F t -b --no-owner -f "/tmp/${backup_file_name}"

aws s3 cp /tmp/${backup_file_name} s3://${DB_BACKUP_BUCKET}/backups/${backup_file_name} --sse

rm /tmp/${backup_file_name}
