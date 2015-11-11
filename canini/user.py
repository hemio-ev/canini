from canini import *

def load(args, conn):
    cur = conn.cursor()
    
    if args.list is not None:
        action_list(args, cur)

    if args.appoint_deputy is not None:
        action_appoint_deputy(args, cur)

    if args.revoke_deputy is not None:
        action_revoke_deputy(args, cur)

    conn.commit()

def action_list(args, cur):

    cur.execute("""
     SELECT owner, login, contact_email, 
      ARRAY(SELECT deputy::varchar FROM "user".deputy WHERE represented=owner) AS deputies
     FROM "user"."user"
     WHERE owner LIKE %(name)s
     ORDER BY owner
    """, {'name': args.list})
    utils.printCurAsTable(cur)

def action_appoint_deputy(args, cur):

    cur.execute("""
     INSERT INTO "user".deputy (deputy, represented) VALUES (%(deputy)s, %(represented)s)
    """, { 'deputy': args.appoint_deputy[0], 'represented': args.appoint_deputy[1]})

def action_revoke_deputy(args, cur):

    cur.execute("""
     DELETE FROM "user".deputy WHERE deputy=%(deputy)s AND represented=%(represented)s
    """, { 'deputy': args.revoke_deputy[0], 'represented': args.revoke_deputy[1]})

    if cur.rowcount != 1:
        print("Error, deputy not found")

