##generating code_verifier,sha256, code_challenge
import string, secrets, hashlib, base64

def create_code_verifier_challenge(code_verifier = None, code_challenge = None):
    
    if code_verifier is None and code_challenge is None:
        alphabet = string.ascii_letters + string.digits 
        code_verifier= ''.join(secrets.choice(alphabet) for i in range(50))
        hashed = hashlib.sha256(code_verifier.encode('utf-8'))
        hashed_rawbytes = hashed.digest()
        code_challenge = base64.urlsafe_b64encode(hashed_rawbytes).replace(b'=',b'')
        return code_verifier, code_challenge

    else:
        return code_verifier, code_challenge
