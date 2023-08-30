import routeros_api
import traceback

def get_login(mikrotik_ip_address, mikrotik_user, mikrotik_password,text_plain=True,_ssl_verify=False):
    connection = routeros_api.RouterOsApiPool(
        mikrotik_ip_address, 
        username = mikrotik_user, 
        password = mikrotik_password,
        port=8728,
        use_ssl=False,
        plaintext_login=text_plain,
        ssl_verify=_ssl_verify,
        #ssl_verify_hostname=True,
        ssl_context=None,
        )
    print(connection)
    return connection

def connect_to_mikrotik(mikrotik_ip_address, mikrotik_user, mikrotik_password):
    connection = get_login(mikrotik_ip_address, mikrotik_user, mikrotik_password)
    try:
        api = connection.get_api()
        print(f'Cononected to {mikrotik_ip_address} :{connection.connected}')
        raw_host_name = api.get_resource('/system/identity')
        host_name = raw_host_name.get()
        raw_registration_table = api.get_resource("/interface/wireless/registration-table")
        registration_table = raw_registration_table.get()
        print("Sin Texto plano")
        print(host_name)
        connection.disconnect()
        return []
    except:
        print("error")   
        connection = get_login(mikrotik_ip_address, mikrotik_user, mikrotik_password, text_plain=False, _ssl_verify=True)
        api = connection.get_api()
        print(f'Cononected to {mikrotik_ip_address} :{connection.connected}')        
        raw_host_name = api.get_resource('/system/identity')
        host_name = raw_host_name.get()
        raw_registration_table = api.get_resource("/interface/wireless/registration-table")
        registration_table = raw_registration_table.get()
        connection.disconnect()
        print("Con Texto plano")        
        print(host_name)
        return registration_table

lista_de_access_points = open("lista_de_access_points.txt","r")

total_mikrotiks_wireless_clients = 0
for access_point in lista_de_access_points: 
    registration_table = connect_to_mikrotik(access_point.strip(), "n1mbu5", "n3tw0rks")
    print(f'\n{"*"*8} Wireless Clients on device: {access_point} {"*"*8}\n')
    if (len(registration_table) > 0):
        for num, wireless_clients in enumerate(registration_table):
            print(f'{num+1} Mac: {wireless_clients["mac-address"]} Signal: {wireless_clients["signal-strength"]}')
    print(f'\nTotal Wireless Clients = {len(registration_table)}')
    total_mikrotiks_wireless_clients += len(registration_table)
print(f'\n\n///////TOTAL WIRELESS CLIENTS {total_mikrotiks_wireless_clients}///////')