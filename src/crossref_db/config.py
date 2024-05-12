from pydantic import BaseModel, SecretStr


class ConfigDB(BaseModel):
    url: str


class ConfigFTP(BaseModel):
    host: str
    login: str
    password: SecretStr
    directory: str
    tmpdir: str


class ConfigLocal(BaseModel):
    directory: str


class Config(BaseModel):
    db: ConfigDB
    ftp: ConfigFTP | None
    local: ConfigLocal | None
