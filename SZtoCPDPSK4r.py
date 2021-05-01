
import csv
import requests
import json
import sys

CPFQDN = "cloudpath.my.domain" # Cloudpath FQDN or ip address
CPUSER = "john.murphy1@commscope.com" # Cloudpath user
CPPASSWORD = "password" # Cloudpath password
CPAPIKEY = "OxcCXXXuJwKz" # Cloupath API key
SZKEYFILE = "dpsk_20210501032622.csv" # .csv file with DPSKs exported from SZ (Clients/Dynamic PSK/Export All)
CPDPSKGUID = "AccountDpskPool-f7XXXXa-3ee9-4b87-a375-5963297eXXXX" # Cloudpath DPSK Pool Guid (Configuration/DPSK Pools)

# run using python3 SZtoCPDPSK4r.py

def readfile():
    print ("Reading CSV file")
    reader = csv.DictReader(open(SZKEYFILE))
    result = {}
    for row in reader:
        key = row.pop('\ufeff"User Name"')
        if key in result:
            # implement your duplicate row handling here
            pass
        result[key] = row
    return result

def getcptoken(username, password):
    print ("Getting API token")
    url = "https://"+CPFQDN+"/admin/apiv2/"+CPAPIKEY+"/token"
    body = {"userName":username, "password":password}
    response = requests.post(url, json=body)
    token = response.json()['token']
    return token

def createdpsks(olddpsk):
    url = "https://"+CPFQDN+"/admin/apiv2/"+CPAPIKEY+"/dpskPools/"+CPDPSKGUID+"/dpsks"
    for user in olddpsk:
        token = getcptoken(CPUSER, CPPASSWORD)
        print ('Creating EDPSK for user '+user)
        Passphrase = olddpsk[user]['Passphrase']
        VLAN = olddpsk[user]['VLAN ID']
        cpheaders = {"Content-Type":"application/json", "Authorization":token}
        body = {"name":user, "passphrase":Passphrase, "vlanid":VLAN}
        response = requests.post(url, headers=cpheaders, json=body)
        print (response)
    return

def main(argv):
    szkeys = readfile()
    createdpsks (szkeys)
    return

if __name__ == "__main__":
        main(sys.argv[1:])
