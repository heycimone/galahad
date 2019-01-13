#!/usr/bin/env python

import os
import sys
import argparse

file_path = os.path.realpath(__file__)
base_excalibur_dir = os.path.dirname(
    (os.path.dirname(os.path.dirname(file_path)))) + '/excalibur'
sys.path.insert(0, base_excalibur_dir)

from website.valor import ValorManager
from website.controller import AssembleRoleThread
from website.ldaplookup import LDAP


def create_valor_standby_pool():
    valor_manager = ValorManager()

    valor_manager.get_empty_valor()


def create_role_image_file_standby_pool(unity_image_size):
    inst = LDAP('', '')
    dn = 'cn=admin,dc=canvas,dc=virtue,dc=com'
    inst.get_ldap_connection()
    inst.conn.simple_bind_s(dn, 'Test123!')

    # Call a controller thread to create and assemble the new image
    new_role = {}
    role = AssembleRoleThread(inst.email, inst.password,
                              new_role, unity_image_size,
                              use_ssh=True)
    role.create_standby_roles()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        '--valors',
                        action="store_true",
                        required=False,
                        help="Create standby valors.")
    parser.add_argument('-r',
                        '--role_image_files',
                        action="store_true",
                        required=False,
                        help="Create standby role image files. Please specify "
                             "unity_image_size option.")
    parser.add_argument('-u',
                        '--unity_image_size',
                        type=str,
                        required=False,
                        help="The unity image size for which standby pools "
                             "will be created")

    args = parser.parse_args()

    return args


if (__name__ == '__main__'):

    args = parse_args()

    if args.valors:
        create_valor_standby_pool()
    elif args.role_image_files and args.unity_image_size:
        create_role_image_file_standby_pool(args.unity_image_size)
    else:
        print("Incorrect parameters specified.\n"
              "Please specify the following options:\n"
              "--valors\n"
              "OR\n"
              "--role_image_files AND --unity_image_size")
