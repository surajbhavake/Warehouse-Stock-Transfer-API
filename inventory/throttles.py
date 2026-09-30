from rest_framework.throttling import(
    AnonRateThrottle,
    UserRateThrottle,
    SimpleRateThrottle
)


#here we only recored the histroy it doesn't do the limiting
class LoginRateThrottle(SimpleRateThrottle):

    scope = 'login'

    def get_cache_key(self,request,view):
        ident = self.get_ident(request)

        return self.cache_format % {
            'scope':self.scope,
            'ident':ident,
        }


class WarehouseAnonRateThrottle(AnonRateThrottle):
    scope = 'anonymous'


class WarehouseUserRateThrottle(UserRateThrottle):
    scope = 'user'