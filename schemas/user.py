from pydantic import BaseModel, EmailStr, SecretStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
