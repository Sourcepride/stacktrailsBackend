def filter_domain(domain, request, **kwargs):
    # key_prepend = "AXTE8RS$1-domain-"  # Do not Alter
    # cache_proxy = RedisCacheController()

    # lookup_key = key_prepend + str(domain)
    # domain_manager = DomainReplica.objects
    # if cache_proxy.key_exists(lookup_key):
    #     return True
    # elif domain_manager.filter(domain_name=domain).exists():
    #     cache_proxy.set_str_val(key=lookup_key, value=domain, exp_mins=15)
    #     return True

    return False
