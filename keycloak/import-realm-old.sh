#!/bin/bash

set -a

# Disable automatic export
set +a

#!/bin/bash

# JSON existance checking
JSON_FILE="/tmp/import/realm-config-initial.json"
if [[ ! -f "$JSON_FILE" ]]; then
  echo "File $JSON_FILE is not found!"
  exit 1
fi

# Create output file
OUTPUT_FILE="/tmp/import/realm-config.json"
cp "$JSON_FILE" "$OUTPUT_FILE"

# Env substitution
# Using grep for variables search and sed substitution
for var in $(grep -o '\${[^}]*}' "$JSON_FILE" | tr -d '${}'); do
  value=${!var}
  if [ -n "$value" ]; then
    sed -i "s|\${$var}|$value|g" "$OUTPUT_FILE"
  else
    echo "Warning: env $var is not found."
  fi
done

echo "Envs are substituted. Result is saved in $OUTPUT_FILE"

sleep 5
echo $KC_REALM_NAME
echo $KC_REALM_COMMON
echo $KEYCLOAK_ADMIN
echo $KEYCLOAK_ADMIN_PASSWORD
sleep 3

# Variables
REALM_JSON_FILE="/tmp/import/realm-config.json"
KEYCLOAK_URL="http://localhost:8080"

echo "Starting the script..."

/opt/keycloak/bin/kc.sh start-dev &

sleep 22

echo "25 seconds have passed."

# Log in to Keycloak
/opt/keycloak/bin/kcadm.sh config credentials --server $KEYCLOAK_URL --realm $KC_REALM_NAME --user $KEYCLOAK_ADMIN --password $KEYCLOAK_ADMIN_PASSWORD

sleep 5

echo "25 seconds have passed."

echo "Keycloak started and Admin CLI configured."

# Check if the realm exists
if /opt/keycloak/bin/kcadm.sh get realms/$KC_REALM_COMMON > /dev/null 2>&1; then
    echo "Realm '$KC_REALM_COMMON' already exists. Skipping import."
else
    echo "Realm '$KC_REALM_COMMON' does not exist. Importing..."
    /opt/keycloak/bin/kcadm.sh create realms -f $REALM_JSON_FILE
    echo "Realm '$KC_REALM_COMMON' imported successfully."
fi

wait
