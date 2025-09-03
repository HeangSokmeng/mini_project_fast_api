from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: str = None


class RoleCreate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    role: RoleResponse

    class Config:
        from_attributes = True
