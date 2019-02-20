#!/usr/bin/python

import ldap_tools
from ldaplookup import LDAP

def get_ldap_usernames(ldap):
    # Query and get all the usernames from open ldap server
    ldap_users = ldap_tools.parse_ldap_list(
        ldap.get_objs_of_type('OpenLDAPuser'))

    ldap_usernames = []
    for user in ldap_users:
        ldap_usernames.append(user['username'])

    return ldap_usernames


def update_ldap_users_from_ad():
    # Setup the ldap connection
    dn = "cn=admin,dc=canvas,dc=virtue,dc=com"
    ldap = LDAP('', '')
    ldap.get_ldap_connection()
    # FIXME - Figure out a soluton for the Hardcoded password
    # TODO - Fix Hardcoded password for ldap and AD connection
    ldap.conn.simple_bind_s(dn, "Test123!")

    # Bind the AD connection
    ad = LDAP('slapd@virtue.gov', 'Test123!')
    ad.bind_ad()

    # Query AD for all users
    ad_users = ad.query_ad('objectClass', 'user')

    ldap_usernames = get_ldap_usernames(ldap)

    # Go through all users in AD
    for user in ad_users:
        cn = user[1]['cn'][0]
        ad_username = user[1]['sAMAccountName'][0]
        # If a username in AD is not found in ldap then add it
        if ad_username not in ldap_usernames:
            new_user = {'username': ad_username, 'authorizedRoleIds': [], 'name': cn}
            new_ldap_user = ldap_tools.to_ldap(new_user, 'OpenLDAPuser')
            ldap.add_obj(new_ldap_user, 'users', 'cusername', throw_error=True)

            if (not os.path.exists('{0}/galahad-keys'.format(os.environ['HOME']))):
                os.mkdir('{0}/galahad-keys'.format(os.environ['HOME']))

            # Temporary code:
            shutil.copy('{0}/default-user-key.pem'.format(os.environ['HOME']),
                        '{0}/galahad-keys/{1}.pem'.format(os.environ['HOME'], username))

            # TODO: Future code will look like this:
            '''subprocess.run(
                ['ssh-keygen', '-t', 'rsa', '-f', '~/galahad-keys/{0}.pem'.format(username),
                 '-C', '"For Virtue user {0}"'.format(username), '-N', '""'],
                check=True
            )'''

    return ldap
