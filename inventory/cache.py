from django.core.cache import cache


PRODUCT_LIST_CACHE_KEY = "products:list"


CACHE_TIMEOUT = 300

def get_product_list_cache():
    return cache.get(PRODUCT_LIST_CACHE_KEY)

def set_product_list_cache(data):
    cache.set(
        PRODUCT_LIST_CACHE_KEY,
        data,
        timeout=CACHE_TIMEOUT
    )

def invalidate_product_list_cache():
    cache.delete(
        PRODUCT_LIST_CACHE_KEY
    )
def get_product_detail_cache(product_id):
    key = f'products:{product_id}'
    return cache.get(key)


def set_product_detail_cache(product_id,data):
    key = f'products:{product_id}'
    cache.set(
        key,
        data,
        timeout=CACHE_TIMEOUT,
    )

def invalidate_product_detail_cache(product_id):
    key = f"products:{product_id}"
    cache.delete(key)




WAREHOUSE_LIST_CACHE_KEY ="warehouse:list"

def get_warehouse_list_cache():
    return cache.get(
        WAREHOUSE_LIST_CACHE_KEY
    )
def set_warehouse_list_cache(data):
    cache.set(
        WAREHOUSE_LIST_CACHE_KEY,
        data,
        timeout=CACHE_TIMEOUT,
    )
def invalidate_warehouse_list_cache():
    cache.delete(
        WAREHOUSE_LIST_CACHE_KEY
    )

def get_warehouse_detail_cache(warehouse_id):
    key = f'warehouses:{warehouse_id}'

    return cache.get(key)

def set_warehouse_detail_cache(warehouse_id,data):
    key = f'warehouses:{warehouse_id}'

    cache.set(
        key,
        data,
        timeout=CACHE_TIMEOUT
    )
def invalidate_warehouse_detail_cache(warehouse_id):
    key = f'warehouse:{warehouse_id}'

    cache.delete(key)