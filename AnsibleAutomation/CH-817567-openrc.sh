#!/usr/bin/env bash
export OS_AUTH_URL=https://kvm.tacc.chameleoncloud.org:5000/v3
export OS_IDENTITY_API_VERSION=3
export OS_INTERFACE=public
export OS_PROJECT_ID="11b23a03af1b4fcbb16a21a86ce2a65d"
export OS_USERNAME="dass19@vanderbilt.edu"
export OS_PROTOCOL="openid"
export OS_AUTH_TYPE="v3oidcpassword"
echo "($OS_USERNAME) Please enter your Chameleon CLI password: "
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT
export OS_IDENTITY_PROVIDER="chameleon"
export OS_DISCOVERY_ENDPOINT="https://auth.chameleoncloud.org/auth/realms/chameleon/.well-known/openid-configuration"
export OS_CLIENT_ID="keystone-kvm-prod"
export OS_ACCESS_TOKEN_TYPE="access_token"
export OS_CLIENT_SECRET="none"
export OS_REGION_NAME="KVM@TACC"
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi