import secrets
 # Generates a 64-character hex string

SECRET_KEY = secrets.token_hex(32)  # Generates a 64-character hex string
print(f"Generated secret key: {SECRET_KEY}") 
 
 