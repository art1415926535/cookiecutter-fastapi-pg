import prometheus_client
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


PASSWORD_VERIFICATION = prometheus_client.Summary(
    "{{cookiecutter.author_name}}_password_verification_seconds",
    "Time spent on password verification",
)
PASSWORD_HASHING = prometheus_client.Summary(
    "{{cookiecutter.author_name}}_password_hashing_seconds",
    "Time spent hashing password",
)


@PASSWORD_VERIFICATION.time()
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


@PASSWORD_HASHING.time()
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
