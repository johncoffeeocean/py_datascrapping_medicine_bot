from cryptography.fernet import Fernet
import json

# Generate a secret key
# key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456'
key = b'BVS232_SShPNERqBB1GeNROVpPeP8p5GoDDh-GGuveQ='
print(key)

# Create a Fernet cipher object with the key
cipher = Fernet(key)

# Define your JSON object
json_obj = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}

# Encrypt the values of your JSON object
encrypted_obj = {}
for k, v in json_obj.items():
    encrypted_obj[k] = cipher.encrypt(v.encode()).decode()

# json2str
encrypted_obj = json.dumps(encrypted_obj)

# Print the encrypted JSON string
print(encrypted_obj)

decrypted_obj = {}
# str2json
encrypted_obj = json.loads(encrypted_obj)
for k, v in encrypted_obj.items():
    decrypted_obj[k] = cipher.decrypt(v.encode()).decode()

print(decrypted_obj)