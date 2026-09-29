from django.core.cache import cache


PRODUCT_LIST_CACHE_KEY = "products:list"
WAREHOUSE_LIST_CACHE_KEY ="warehouse:list"

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