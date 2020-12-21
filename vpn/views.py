from re import sub
from subprocess import run, PIPE

from django.shortcuts import render

commands = {"connected_users": "echo '1234' | sudo -S pivpn -c",}

def get_connected_users():
    """
    Get the list of connected users, by parsing the output of pivpn -c.

    Returns:
        connected_users(list): List of connected users.
    """

    # Format of output
    #
    # · Case when there are no active users (line below is the first)
    # : NOTE : The output below is NOT real-time!
    # :      : It may be off by a few minutes.
    # 
    #   ::: Client Status List :::
    #   Name                     Remote IP      Virtual IP      Bytes Received      Bytes Sent      Connected Since
    #   No Clients Connected!
    #
    # · Case where there are connected users (line below is the first)
    # : NOTE : The output below is NOT real-time!
    # :      : It may be off by a few minutes.
    # 
    # ::: Client Status List :::
    # Name      Remote IP            Virtual IP      Bytes Received      Bytes Sent      Connected Since
    # test2     127.0.0.1:57697      10.8.0.3        3,0KiB              2,8KiB          Dec 20 2020 - 22:10:25
    # test      127.0.0.1:58212      10.8.0.2        2,9KiB              2,7KiB          Dec 20 2020 - 22:05:53


    connected_users = []
    result = run(commands["connected_users"], stdout=PIPE, shell=True).stdout.decode("utf-8").strip().split("\n")[5:]
    if "No Clients Connected" in result:
        return connected_users
    else:
        for client in result:
            client = sub("[\s]{2,}","|", client).split("|")
            connected_users.append({"name": client[0],
                                    "remote_ip": client[1],
                                    "virtual_ip": client[2],
                                    "bytes_received": client[3],
                                    "bytes_sent": client[4],
                                    "connected_since": client[5]})
        return connected_users
