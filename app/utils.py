from passlib.context import CryptContext


# hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# adding www to urls with https
def add_www(url):
    if url.startswith("https://"):
        return f"https://www.{url[8:]}"
    else:
        return url