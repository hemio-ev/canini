import psycopg2
import yaml
import os
import os.path
import json
import jsonschema
import sys

import canini

def add_commands_to_parser(subparsers):
    cmd = subparsers.add_parser('service', help='Service').add_subparsers()

    # reload
    cmd_reload = cmd.add_parser('reload', help='reload')
    cmd_reload.set_defaults(func=reload)

    # list-subservice
    cmd_list_subservice = cmd.add_parser('list-subservice', help='List subservices')
    cmd_list_subservice.set_defaults(func=list_subservice)

    # list-subservice-entities
    cmd_list_subservice_entity = cmd.add_parser('list-subservice-entity', help='List subservice entities')
    cmd_list_subservice_entity.set_defaults(func=list_subservice_entity)

def list_subservice(args, conn):
    cur = conn.cursor()
    cur.execute("SELECT service, subservice FROM system.subservice")
    canini.utils.printCurAsTable(cur)

def list_subservice_entity(args, conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT service_entity_name, service, subservice
        FROM system.subservice_entity
        ORDER BY service_entity_name, service, subservice
        """)
    canini.utils.printCurAsTable(cur)

def reload(args, conn):
    schema = {
        'type': "object",
        'additionalProperties': False,
        'properties': {
            "machines": {
                'type': "array",
                'items': {
                    'type': "object",
                    'additionalProperties': False,
                    'required': ["name"],
                    'properties': {
                        "name": { 'type': "string" },
                        "auth_roles": {
                            'type': "array",
                            'items': { 'type': "string" }
                        }
                    }
                }
            },

            "services": {
                'type': "array",
                'items': {
                    'type': "object",
                    'additionalProperties': False,
                    'required': ["service", "subservices", "machines", "dns", "entity_name"],
                    'properties': {
                        'service': { 'type': "string" },
                        'subservices': {
                            'type': "array",
                            'items': { 'type': "string" }
                        },
                        'entity_name': { 'type': "string" } ,
                        'machines': {
                            'type': "array",
                            'items': { 'type': "string" }
                        },
                        'dns': {
                            'type': "array",
                            'items': {
                                'type': "object",
                                'additionalProperties': False,
                                'required': ['type', 'rdata'],
                                'properties': {
                                    "type": { 'type': "string" },
                                    "rdata": { 'type': "object" },
                                    "domain_prefix": { 'type': "string" },
                                    "ttl": { 'type': "integer" }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


    config = {"services":[], "machines":[]}

    for p in os.scandir('/etc/carnivora/service.d'):
        with open(p.path) as f:
            c = yaml.safe_load(f)

            try:
                jsonschema.validate(c, schema)
            except jsonschema.ValidationError as e:
                print("Error in config ", p.path, file=sys.stderr)
                print("Setting ", list(e.absolute_path), file=sys.stderr)
                sys.exit(e.message)

            config['services'] += c.get('services', [])
            config['machines'] += c.get('machines', [])

    tables = [
         'system.service_entity'
        , 'backend.machine'
        , 'backend.auth'
    ]

    cur = conn.cursor()

    for table in tables:
        cur.execute(
            """UPDATE {} SET option = option || '{{"__DELETE": true}}'"""
            .format(table)
            )

    cur.execute("DELETE FROM system.service_entity_dns")

    for machine in config['machines']:
        cur.execute("""
INSERT INTO backend.machine AS t (name) VALUES (%(name)s)
 ON CONFLICT (name) DO UPDATE
  SET option = t.option - '__DELETE'
  WHERE t.name = excluded.name""", machine)

        for role in machine.get('auth_roles', []):
            cur.execute("""
INSERT INTO backend.auth AS t (machine, role) VALUES (%(name)s, %(role)s)
 ON CONFLICT (role) DO UPDATE
  SET option = t.option - '__DELETE'
  WHERE t.role = excluded.role""", {**machine, 'role': role})

    for service in config['services']:
        cur.execute("""
INSERT INTO system.service_entity AS t (service, service_entity_name)
 VALUES (%(service)s, %(entity_name)s)
 ON CONFLICT (service, service_entity_name) DO UPDATE
  SET option = t.option - '__DELETE'
  WHERE t.service = excluded.service
   AND t.service_entity_name = excluded.service_entity_name""", service)

        for machine in service['machines']:
            cur.execute("""
INSERT INTO system.service_entity_machine AS t (service, service_entity_name, machine_name)
 VALUES (%(service)s, %(entity_name)s, %(machine)s)
 ON CONFLICT (service, service_entity_name, machine_name) DO UPDATE
  SET option = t.option - '__DELETE'
  WHERE t.service = excluded.service
   AND t.service_entity_name = excluded.service_entity_name
   AND t.machine_name = excluded.machine_name""", {**service,'machine':machine})

        for subservice in service['subservices']:
            cur.execute("""
INSERT INTO system.subservice_entity AS t (service, service_entity_name, subservice)
 VALUES (%(service)s, %(entity_name)s, %(subservice)s)
 ON CONFLICT (service, service_entity_name, subservice) DO UPDATE
  SET option = t.option - '__DELETE'
  WHERE t.service = excluded.service
   AND t.service_entity_name = excluded.service_entity_name
   AND t.subservice = excluded.subservice""", {**service,'subservice':subservice})

        for dns in service['dns']:
            cur.execute("""
INSERT INTO system.service_entity_dns
    (service_entity_name, service, type, rdata, ttl, domain_prefix)
    VALUES (%(entity_name)s, %(service)s, %(type)s, %(rdata)s, %(ttl)s, %(domain_prefix)s)
""", {**service, 'type': dns['type'], 'rdata': json.dumps(dns['rdata']), 'ttl': dns.get('ttl', None), 'domain_prefix': dns.get('domain_prefix', None)})


    for table in tables:
        cur.execute(
            "DELETE FROM {} WHERE option->'__DELETE' IS NOT NULL"
            .format(table)
            )

    conn.commit()

