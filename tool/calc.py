"""import sism data into qadb"""
import logging
import argparse
import untangle
import zlib
import base64
import json
from suds.client import Client
from sqlalchemy.exc import DBAPIError
from qadb import sqlalchemy_session, transaction

# pylint: disable=locally-disabled, line-too-long, invalid-name, not-context-manager, no-member
_logger = logging.getLogger(__name__)


def get_servers_hana():
    """This function returns lpars from the QADB."""
    session = sqlalchemy_session()
    with transaction(session):
        select_statement = """ SELECT "HOST" \
                               FROM "TESTER"."servers.data.tables::hosts" \
                               WHERE NOT "HOST" LIKE 'lsh%' \
                               ORDER BY 1 """
        rows = session.execute(select_statement)
        return set([row['host'] for row in rows])


def get_servers_sism(username, password):
    service_team = {
        "item": {
            "Sign":'I',
            "Option":"EQ",
            "Low":"00319"
        }
    }

    object_type = {
        "item": {
            "Sign":'I',
            "Option":"EQ",
            "Low":"ZSISM_CL_PHYSICAL"
        }
    }

    status = {
        "item": {
            "Sign":'I',
            "Option":"NE",
            "Low":"TURNDOWN"
        }
    }

    client = Client(url='https://pi-internal.wdf.sap.corp/dir/wsdl?p=ic/c613adc7ecf73176b8356ef0ccbbb398&endp_url=https://pi-internal.wdf.sap.corp',
                username=username, 
                password=password)

    response = client.service.SmartSearchHead_sync(ServiceTeam = service_team, ObjectType = object_type, Status = status).item[0]["Data"]["GzippedXmlLineItems"]["value"]

    decompressed_response = zlib.decompress(base64.b64decode(response), 16 + zlib.MAX_WBITS)

    server_list = untangle.parse(decompressed_response)

    return set(server_data.SERVER.cdata.encode('utf-8').split('.')[0] for server_data in server_list.asx_abap.asx_values.DATA_NODE.item)


def insert(new_hosts):
    """Do the QADB insert.

    Hosts in SISM not included in QADB will
    be inserted into QADB.
    """
    session = sqlalchemy_session()
    _logger.debug(new_hosts)
    with transaction(session):
        for new_host in new_hosts:
            _logger.info("insert host %(host)s into qadb", {"host": new_host})
            insert_host_statement = """ insert into "TESTER"."servers.data.tables::hosts" \
            values (:hostname,'wdf.sap.corp') """
            session.execute(insert_host_statement, {'hostname': new_host})
            insert_label_statement = """ insert into "TESTER"."servers.data.tables::custom_labels" \
            values (:hostname,'added_by_syncbot') """
            try:
                session.execute(insert_label_statement, {'hostname': new_host})
            except DBAPIError as exc:
                if exc.orig.errorcode != 301:
                    raise


def main():
    """main"""
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter('%(asctime)s %(funcName)s %(levelname)s: %(message)s')
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()

    servers = get_servers_sism(args.username, args.password)
    servershana = get_servers_hana()
    newservers = servers - servershana
    insert(newservers)


if __name__ == '__main__':
    main()
