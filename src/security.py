import hashlib
import hmac
from src.config import settings
from src.exceptions import RegraDeNegocioError

SALT_BYTES = settings.SECRET_SALT.encode('utf-8')

def gerar_hash_senha(senha: str) -> str:
    
    if not senha or len(senha) < 6:
        raise RegraDeNegocioError("A senha precisa ter pelo menos 6 caracteres.")

    senha_bytes = senha.encode('utf-8')

    hash_bytes = hashlib.scrypt(
        senha_bytes,
        salt=SALT_BYTES,
        n=16384,
        r=8,
        p=1
    )
    return hash_bytes.hex()


def verificar_senha(senha_plana_digitada: str, hash_salvo_no_banco: str) -> bool:
    
    if not senha_plana_digitada or len(senha_plana_digitada) < 6:
        return False

    tentativa_hash = gerar_hash_senha(senha_plana_digitada)
    return hmac.compare_digest(tentativa_hash, hash_salvo_no_banco)