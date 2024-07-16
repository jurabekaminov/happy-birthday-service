from typing import Annotated

from fastapi import Depends, Query


async def common_parameters(
    skip: int = Query(ge=0, default=0),
    limit: int = Query(ge=1, le=100, default=100),
):
    return {"skip": skip, "limit": limit}


CommonsDep = Annotated[dict, Depends(common_parameters)]
