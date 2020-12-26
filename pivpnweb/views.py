from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from psutil import cpu_percent, cpu_freq, virtual_memory

from vpn.views import get_connected_users, get_list_users

def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


@login_required
def index(request):
    valid_users = []
    revoked_users = []
    for user in get_list_users():
        if user.get("status", None).lower() == "valid":
            valid_users.append(user)
        else:
            revoked_users.append(user)
    context = {"cpu_percent": cpu_percent(interval=None),
               "cpu_freq": round(cpu_freq().current, 2),
               "memory_total": bytes2human(virtual_memory().total),
               "memory_free": bytes2human(virtual_memory().available),
               "memory_percent": round((virtual_memory().available/virtual_memory().total)*100, 2),
               "connected_users": get_connected_users(),
               "valid_users": valid_users,
               "revoked_users": revoked_users}
    return render(request, "pivpnweb/index.html", context=context)

