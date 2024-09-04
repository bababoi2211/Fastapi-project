from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:

        from_attributes = True
# region post/product


class PostBase(BaseModel):
    id: int
    name: str
    price: int
    inventory: int = 1
    inorder: bool = True
    

class PostCreate(PostBase):

    owner_info: UserOut

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: PostCreate
    votes: int


class PostResponse(BaseModel):
    name: str
    price: int
    stored_at: datetime

    class Config:
        from_attributes = True


class UpdatePost(BaseModel):

    def extract_data(data):
        DATA = {"name": "", "price": None, "inventory": None, "inorder": None}
        DATA["name"] = data.name
        DATA["price"] = data.price
        DATA["inventory"] = data.inventory
        DATA["inorder"] = data.inorder
        return DATA
    name: Optional[str] = ""
    price: int = 0
    inventory: int = 0
    inorder: bool = True
# endregion

# region user/login


class UserCreate(BaseModel):
    store_name: str
    email: EmailStr
    password: str


class UserIn(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]
# endregion


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class VotesOut(BaseModel):
    user_id: int
    count: int
