from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from src.services.product import ProductService
from src.schemas.product import Product, ProductCreate, ProductUpdate
from src.utils.auth import api_key_auth

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/", response_model=Product,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(api_key_auth)])
async def create_product(product: ProductCreate,
                         service: ProductService = Depends()):
    return await service.create(product)


@router.get("/", response_model=list[Product],
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(api_key_auth)])
async def get_all(service: ProductService = Depends()):
    db_products = await service.get_all()
    if len(db_products) == 0:
        raise HTTPException(status_code=404, detail="Products not found.")
    return db_products


@router.get("/{product_id}",
            response_model=Product,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(api_key_auth)])
async def get_product(product_id: int, service: ProductService = Depends()):
    db_product = await service.get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.put("/{product_id}",
            response_model=Product,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(api_key_auth)])
async def update_product(product_id: int, product: ProductUpdate, service: ProductService = Depends()):
    try:
        return await service.update(product_id, product)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.patch("/{product_id}",
              response_model=Product,
              status_code=status.HTTP_200_OK,
              dependencies=[Depends(api_key_auth)])
async def patch_product_quantity(product_id: int, quantity: float, service: ProductService = Depends()):
    try:
        return await service.update_quantity(product_id, quantity)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/{product_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(api_key_auth)])
async def delete_product(product_id: int, service: ProductService = Depends()):
    db_product = await service.get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await service.delete(db_product)
