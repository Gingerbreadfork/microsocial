from cryptography.fernet import Fernet

def decrypt_str_with_key(key, encrypted_msg):
    decryption_type = Fernet(key)
    decrypted_message = decryption_type.decrypt(encrypted_msg.encode('utf8'))
    return decrypted_message.decode("utf-8")

def encrypt_str_with_key(key, message):
    encryption_type = Fernet(key)
    converted_string = str.encode(message)
    encrypted_message = encryption_type.encrypt(converted_string)
    return encrypted_message