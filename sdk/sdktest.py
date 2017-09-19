
from openstack import connection

#install sdk:$pip install openstacksdk
#http://git.openstack.org/cgit/openstack/python-openstacksdk/tree/examples/compute/list.py
#https://developer.openstack.org/sdks/python/openstacksdk/users/guides/logging.html

if __name__ == '__main__':

    auth_args = {
        'auth_url': 'http://192.168.1.102:5000/v3',
        'project_name': 'admin',
        'username': 'admin',
        'password': '8e5b16aae8c24e59',
        'user_domain_name': 'default',
        'project_domain_name': 'default',
    }
    conn = connection.Connection(**auth_args)
    conn.authorize()

    print("List Servers:")

    for server in conn.compute.servers():
        print(server)
