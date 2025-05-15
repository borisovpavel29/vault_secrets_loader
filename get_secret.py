import sys
import json
import requests

def get_vault_token(vault_url, role_id, secret_id):
    login_url = f"{vault_url}/v1/auth/approle/login"
    payload = {
        "role_id": role_id,
        "secret_id": secret_id
    }

    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status()
        return response.json()["auth"]["client_token"]
    except Exception as e:
        print(f"Error obtaining Vault token: {e}", file=sys.stderr)
        sys.exit(1)

def get_secret_value(vault_url, token, secret_path, secret_key):
    secret_url = f"{vault_url}/v1/{secret_path}"
    headers = {"X-Vault-Token": token}

    try:
        response = requests.get(secret_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # Поддержка версии 2 хранилища Vault
        secret_data = data["data"]["data"] if "data" in data and "data" in data["data"] else data["data"]
        return secret_data.get(secret_key, "")
    except Exception as e:
        print(f"Error obtaining secret: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: vault_secret.py <VAULT_URL> <VAULT_ROLE_ID> <VAULT_SECRET_ID> <VAULT_SECRET_PATH> <SECRET_KEY>")
        sys.exit(1)

    vault_url, role_id, secret_id, secret_path, secret_key = sys.argv[1:6]

    token = get_vault_token(vault_url, role_id, secret_id)
    secret_value = get_secret_value(vault_url, token, secret_path, secret_key)

    print(secret_value)
