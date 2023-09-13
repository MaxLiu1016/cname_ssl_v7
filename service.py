# -*- coding: utf-8 -*-
import pexpect
import time
import re
import os
from urllib.parse import urlparse
from pymongo import MongoClient


def request_certificate(domain):
    uri = "mongodb+srv://Max:AA951753@bat.zcefrvy.mongodb.net/bat?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)

    db = client['cname_ssl']

    collection = db['SSLJobs']

    email = "a0958057936@gmail.com"

    os.system(f'sudo mkdir /home/ubuntu/cname_ssl_v7/workshop/{domain}')
    os.system(
        f'sudo openssl req -new -newkey rsa:2048 -nodes -keyout /home/ubuntu/cname_ssl_v7/workshop/{domain}/privkey.pem -out /home/ubuntu/cname_ssl_v7/workshop/{domain}/csr.pem -subj "/CN={domain}"')
    os.chdir(f'/home/ubuntu/cname_ssl_v7/workshop/{domain}')
    time.sleep(3)
    try:
        child = pexpect.spawn(
            f'sudo certbot certonly --staging --email {email} -d {domain} --no-eff-email --agree-tos --csr /home/ubuntu/cname_ssl_v7/workshop/{domain}/csr.pem --manual --config-dir /home/ubuntu/cname_ssl_v7/workshop/{domain}')
        response_index = child.expect(
            ["Certificate not yet due for renewal", 'Press Enter to Continue', '(Y)es/(N)o: \n',
             'too many registrations for this IP'])
        if response_index == 0:
            print("response_index == 0")
            time.sleep(3)
            child.sendline('2')
            recertificate_successfully_index = child.expect(
                ['These files will be updated when the certificate renews.'])
            if recertificate_successfully_index == 0:
                recertificate_successfully_index_data = child.before.decode('utf-8')
                paths = re.findall(r"/[^\s]*\.pem", recertificate_successfully_index_data)
                for path in paths:
                    real_path = os.path.realpath(path)
                    os.system(f'sudo chmod 777 /home/ubuntu/cname_ssl_v7/archive')
                    os.system(f'sudo chmod 777 /home/ubuntu/cname_ssl_v7/archive/{domain}')
                    os.system(f'sudo chmod 777 {real_path}')
                    key_name = ''
                    if ("fullchain" in real_path.split("/")[-1]):
                        key_name = "fullchain"
                    if ("privkey" in real_path.split("/")[-1]):
                        key_name = "privkey"
                    with open(real_path, 'r') as f:
                        content = f.read()
                        filter = {'domain': domain}
                        update = {
                            '$set': {
                                f'certificate.{key_name}': content,
                                "status": 'generated'
                            }
                        }
                        collection.find_one_and_update(
                            filter,
                            update
                        )
        if response_index == 1:
            print("response_index == 1")
            challengeData = child.before.decode('utf-8')
            data_match = re.search(r"just this data:\s*(.*?)\s*And", challengeData, re.DOTALL)
            url_match = re.search("(http[s]?://[^\s]+)", challengeData)
            if data_match is not None:
                data = data_match.group(1).strip()
            else:
                print("No data match found!")
                raise Exception("No data match found!")

            if url_match is not None:
                url = url_match.group(1).strip()
                parsed_url = urlparse(url)
                last_part_of_url = parsed_url.path.rsplit('/', 1)[-1]
            else:
                print("No URL match found!")
                raise Exception("No URL match found!")
            filter = {'domain': domain}
            update = {'$set': {
                "challengeRoute": last_part_of_url,
                "challengeData": data,
            }}
            collection.find_one_and_update(
                filter,
                update
            )
            time.sleep(2)
            try:
                child.sendline()
                end_res = child.expect(['Certificates created using', 'failed'], timeout=30)
                if end_res == 1:
                    print("Certificate creation failed.")
                    raise Exception("Certificate creation failed.")
                else:
                    print("Certificate creation confirmed.")
            except pexpect.exceptions.TIMEOUT:
                print("Confirmation not found. Something might have gone wrong.")
        if response_index == 2:
            print("response_index == 2")
            child.sendline('Y')
            index = child.expect(["Certificate not yet due for renewal", 'Press Enter to Continue'])
            if response_index == 1:
                challengeData = child.before.decode('utf-8')
                data_match = re.search(r"just this data:\s*(.*?)\s*And", challengeData, re.DOTALL)
                url_match = re.search("(http[s]?://[^\s]+)", challengeData)
                if data_match is not None:
                    data = data_match.group(1).strip()
                else:
                    print("No data match found!")
                if url_match is not None:
                    url = url_match.group(1).strip()
                    parsed_url = urlparse(url)
                    last_part_of_url = parsed_url.path.rsplit('/', 1)[-1]
                else:
                    print("No URL match found!")
                filter = {'domain': domain}
                update = {'$set': {
                    "challengeRoute": last_part_of_url,
                    "challengeData": data,
                }}
                collection.find_one_and_update(
                    filter,
                    update
                )
                time.sleep(2)
                child.sendline()
                time.sleep(10)
                child.sendline()
                return True
        if response_index == 3:
            print("too many registrations for this IP")
            raise Exception("too many registrations for this IP")
    except pexpect.EOF:
        print("The subprocess finished without matching any expected string.")
        print("The output was:")
        print(child.before.decode('utf-8'))


def save_certificate(domain):
    uri = "mongodb+srv://Max:AA951753@bat.zcefrvy.mongodb.net/bat?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)

    db = client['cname_ssl']
    collection = db['SSLJobs']
    fullchain_path = f"/home/ubuntu/cname_ssl_v7/workshop/{domain}/0001_chain.pem"
    privkey_path = f"/home/ubuntu/cname_ssl_v7/workshop/{domain}/privkey.pem"
    paths = [fullchain_path, privkey_path]
    for path in paths:
        real_path = os.path.realpath(path)
        os.system(f'sudo chmod 777 /home/ubuntu/cname_ssl_v7/workshop')
        os.system(f'sudo chmod 777 /home/ubuntu/cname_ssl_v7/workshop/{domain}')
        os.system(f'sudo chmod 777 {real_path}')
        key_name = ''
        if ("0001_chain" in real_path.split("/")[-1]):
            key_name = "fullchain"
        if ("privkey" in real_path.split("/")[-1]):
            key_name = "privkey"
        with open(real_path, 'r') as f:
            content = f.read()
            filter = {'domain': domain}
            update = {'$set': {
                f'certificate.{key_name}': content,
                'status': 'success'
            }}
            collection.find_one_and_update(
                filter,
                update
            )

