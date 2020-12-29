from re import sub
from subprocess import run, PIPE

from django.shortcuts import render


class PiVPN:
    def __init__(self, request):
        self.password = request.session["password"]

    def get_connected_users(self):
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

        command = "".join(("echo '", self.password, "' | sudo -S pivpn -c"))
        connected_users = []
        result = run(command, stdout=PIPE, shell=True).stdout.decode("utf-8").strip().split("\n")[5:]
        if "No Clients Connected" in result[0]:
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

    def get_list_users(self):
        """
        Get the list of users, valids and revoked; by parsing the output of pivpn -l.

        Returns:
            list_users(list): List of users.
        """
        
        # Format of output (line below is the first):
        # : NOTE : The first entry should always be your valid server!
        # 
        # ::: Certificate Status List :::
        # Status      Name                                            Expiration
        # Valid       pivpn_022be4ab-f3ca-4067-8a4c-2838bb6f19c6      sep 08 2030
        # Valid       test                                            dic 06 2023
        # Valid       test2                                           dic 06 2023

        command = "".join(("echo '", self.password, "' | sudo -S pivpn -l"))
        list_users = []
        result = run(command, stdout=PIPE, shell=True).stdout.decode("utf-8").strip().split("\n")[4:]
        for user in result:
            user = sub("[\s]{2,}","|", user).split("|")
            list_users.append({"status": user[0],
                            "name": user[1],
                            "expiration": user[2]})
        return list_users
