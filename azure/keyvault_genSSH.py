#!/usr/bin/env python3
import argparse
import subprocess
import os
import stat
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.realpath(__file__))))
import keyvault

keyvault_name = 'og-kv'

def generateRetrieveSsh(key_name, out_dir):
    kv_pubKey = 'ssh-pubkey-' + key_name
    kv_privKey = 'ssh-privkey-' + key_name
    pubkeyPath = os.path.join(out_dir, 'id_' + key_name + '.pub')
    privkeyPath = os.path.join(out_dir, 'id_' + key_name)

    priv_result = keyvault.getSecretFile(keyvault_name, kv_privKey, privkeyPath)
    pub_result = keyvault.getSecretFile(keyvault_name, kv_pubKey, pubkeyPath)
    if not (priv_result['returncode'] and pub_result['returncode']):
        os.chmod(privkeyPath, stat.S_IRUSR | stat.S_IWUSR)
        print 'Public SSH key restored to "' + pubkeyPath + '"'
        print 'Private SSH key restored to "' + privkeyPath + '"'
        return 0

    useShell = False
    if os.name == 'nt':
        useShell = True

    p = subprocess.Popen(['ssh-keygen', '-t', 'rsa', '-C', '', '-b', '4096', '-N', '', '-f', privkeyPath], shell=useShell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    
    os.chmod(privkeyPath, stat.S_IRUSR | stat.S_IWUSR)
    priv_result = keyvault.putSecretFile(keyvault_name, kv_privKey, privkeyPath)
    pub_result = keyvault.putSecretFile(keyvault_name, kv_pubKey, pubkeyPath)
    if priv_result['returncode']:
        print 'Failed to upload private key to keyvault'
    if pub_result['returncode']:
        print 'Failed to upload public key to keyvault'
    print 'Public SSH key generated in "' + pubkeyPath + '"'
    print 'Private SSH key generated in "' + privkeyPath + '"'
    return priv_result and pub_result

def main():
    parser = argparse.ArgumentParser(description='Restore an ssh key from keyvault or create a new one and check it in')
    parser.add_argument('-k', '--key-name', dest='key_name', required=True, help='The name of the ssh key to retrieve or generate')
    parser.add_argument('-o', '--out-dir', dest='out_dir', help='The directory to save the keys to')
    args = parser.parse_args()

    if not args.out_dir:
        args.out_dir = './'
    args.out_dir = os.path.abspath(args.out_dir)
    return generateRetrieveSsh(args.key_name, args.out_dir)

if __name__ == "__main__":
    main()
