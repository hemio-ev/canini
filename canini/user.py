from canini import *
import crypt

def add_commands_to_parser(subparsers):
    cmd = subparsers.add_parser('user', help='User account management').add_subparsers()
   
    # create 
    cmd_create = cmd.add_parser('create', help='Creates user')
    
    cmd_create.set_defaults(func=create)
    cmd_create.add_argument('username', metavar='<username>')
    cmd_create.add_argument('--login', action='store_true', help='Allows user login and sets random password')
    cmd_create.add_argument('--email', help='Email contact for user')

    # delete
    cmd_delete = cmd.add_parser('delete', help='Deletes user')
    cmd_delete.set_defaults(func=delete)
    cmd_delete.add_argument('username', metavar='<username>')

    # password
    cmd_password = cmd.add_parser('password', help='Sets new random password')
    cmd_password.set_defaults(func=password)
    cmd_password.add_argument('username', metavar='<username>')

    # update
    cmd_update = cmd.add_parser('update', help='Updates user')
    cmd_update.set_defaults(func=update)
    cmd_update.add_argument('username', metavar='<username>')
    cmd_update.add_argument('--no-login', action='store_true', help='Disables login (deletes password)')
    cmd_update.add_argument('--email', help='Sets email contact')

    # list
    cmd_list = cmd.add_parser('list', help='Lists existing users')
    cmd_list.set_defaults(func=list)
    cmd_list.add_argument('user_pattern', nargs='?', default='%', metavar='user_pattern')
    
    # appoint-deputy
    cmd_appoint_deputy = cmd.add_parser('appoint-deputy', help='Appoints <deputy> as deputy for <represented>')
    cmd_appoint_deputy.set_defaults(func=appoint_deputy)
    cmd_appoint_deputy.add_argument('deputy', metavar='<deputy>')
    cmd_appoint_deputy.add_argument('represented', metavar='<represented>')
    
    # revoke-deputy
    cmd_revoke_deputy = cmd.add_parser('revoke-deputy', help='Revokes <deputy> as deputy for <represented>')
    cmd_revoke_deputy.set_defaults(func=revoke_deputy)
    cmd_revoke_deputy.add_argument('deputy', metavar='<deputy>')
    cmd_revoke_deputy.add_argument('represented', metavar='<represented>')
    

def create(args, conn):
    if args.login:
    	pw = crypt.mksalt(crypt.METHOD_SHA512)[-10:]
    else:
        pw = None

    print("Username: {0}\nPassword: {1}".format(args.username, pw))

    cur = conn.cursor()
    cur.execute("""
     INSERT INTO "user"."user" (owner, password, contact_email)
      VALUES (
       %(username)s, 
       -- if supplied password is null do not hash password and insert NULL instead
       CASE WHEN %(password)s IS NOT NULL THEN commons._hash_password(%(password)s) END, 
       %(email)s
      )
    """, dict(vars(args), password=pw))
    conn.commit()

def delete(args, conn):
    cur = conn.cursor()
    cur.execute("""
     DELETE FROM "user"."user"  WHERE owner = %(username)s
    """, vars(args))

    if cur.rowcount != 1:
        print("Error, user not found")

    conn.commit()

def password(args, conn):
    pw = crypt.mksalt(crypt.METHOD_SHA512)[-10:]
    print("Username: {0}\nPassword: {1}".format(args.username, pw))

    cur = conn.cursor()
    cur.execute("""
     UPDATE "user"."user" SET password=commons._hash_password(%(password)s)
     WHERE owner=%(username)s 
    """, dict(vars(args), password=pw))

    if cur.rowcount != 1:
        print("Error, user not found")

    conn.commit()

def update(args, conn):
    cur = conn.cursor()

    if args.no_login:
        cur.execute("""
         UPDATE "user"."user" SET password=NULL
         WHERE owner=%(username)s 
        """, vars(args))

    if args.email:
        cur.execute("""
         UPDATE "user"."user" SET contact_email=%(email)s
         WHERE owner=%(username)s 
        """, vars(args))

    if cur.rowcount != 1:
        print("Error, user not found")

    conn.commit()

def list(args, conn):
    cur = conn.cursor()
    cur.execute("""
     SELECT
      owner, 
      contact_email,
      password IS NOT NULL AS login,
      ARRAY(SELECT deputy::varchar FROM "user".deputy WHERE represented=owner ORDER BY deputy)
      AS deputies
     FROM "user"."user"
     WHERE owner LIKE %(user_pattern)s
     ORDER BY owner
    """, vars(args))
    utils.printCurAsTable(cur)

def appoint_deputy(args, conn):
    cur = conn.cursor()
    cur.execute("""
     INSERT INTO "user".deputy (deputy, represented) VALUES (%(deputy)s, %(represented)s)
    """, vars(args))
    conn.commit()

def revoke_deputy(args, conn):
    cur = conn.cursor()
    cur.execute("""
     DELETE FROM "user".deputy WHERE deputy=%(deputy)s AND represented=%(represented)s
    """, vars(args))

    if cur.rowcount != 1:
        print("Error, deputy not found")

    conn.commit()

