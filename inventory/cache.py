from django.core.cache import cache


# PRODUCT_LIST_CACHE_KEY = "products:list"

#Cache configuration
CACHE_TIMEOUT = 300
CACHE_VERSION = 'v2'
CACHE_NAMESPACE = 'warehouse_api'



#key builders


def product_lsit_key():
    return(
        f'{CACHE_NAMESPACE}:'
        f"{CACHE_VERSION}:"
        f"products:list"
    )
def product_detail_key(product_id):
    return (
        f"{CACHE_NAMESPACE}:"
        f"{CACHE_VERSION}:"
        f"products:detail:{product_id}"
    )
def warehouse_list_key():
    return (
        f"{CACHE_NAMESPACE}:"
        f"{CACHE_VERSION}:"
        f"warehouses:list"
    )


def warehouse_detail_key(warehouse_id):
    return (
        f"{CACHE_NAMESPACE}:"
        f"{CACHE_VERSION}:"
        f"warehouses:detail:{warehouse_id}"
    )




def get_product_list_cache():
    return cache.get(product_lsit_key())

def set_product_list_cache(data):
    cache.set(
        product_lsit_key(),
        data,
        timeout=CACHE_TIMEOUT
    )

def invalidate_product_list_cache():
    cache.delete(
        product_lsit_key()
    )
def get_product_detail_cache(product_id):
    return cache.get(product_detail_key(product_id))


def set_product_detail_cache(product_id,data):
   
    cache.set(
        product_detail_key(product_id),
        data,
        timeout=CACHE_TIMEOUT,
    )

def invalidate_product_detail_cache(product_id):
    cache.delete(product_detail_key(product_id))




# WAREHOUSE_LIST_CACHE_KEY ="warehouse:list"

def get_warehouse_list_cache():
    return cache.get(
        warehouse_list_key()
    )
def set_warehouse_list_cache(data):
    cache.set(
        warehouse_list_key(),
        data,
        timeout=CACHE_TIMEOUT,
    )
def invalidate_warehouse_list_cache():
    cache.delete(
        warehouse_list_key()
    )

def get_warehouse_detail_cache(warehouse_id):

    return cache.get(warehouse_detail_key(warehouse_id))

def set_warehouse_detail_cache(warehouse_id,data):

    cache.set(
        warehouse_detail_key(warehouse_id),
        data,
        timeout=CACHE_TIMEOUT
    )
def invalidate_warehouse_detail_cache(warehouse_id):

    cache.delete(warehouse_detail_key(warehouse_id))