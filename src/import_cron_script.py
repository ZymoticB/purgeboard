from tornpsql import Connection
import xml.etree.ElementTree as ET
import requests
from datetime import timedelta, date
import settings

FW_STATS_URL="https://api.eveonline.com/eve/FacWarTopStats.xml.aspx"
DB = Connection('localhost', 'purgeboard', user=settings.PSQL_USER, password=settings.PSQL_PASSWORD)
KEYS = {
    "char": "characterID",
    "corp": "corporationID",
    "faction": "factionID",
}
NAMES = {
    "char": "characterName",
    "corp": "corporationName",
    "faction": "factionName",
}

def create_tables():
    queries = [
        """CREATE TABLE IF NOT EXISTS char_kills_daily
        (
            characterID bigint NOT NULL,
            characterName varchar(100),
            date varchar(8) NOT NULL,
            kills int,
            PRIMARY KEY (characterID, date)
        )
        """,
        """CREATE TABLE IF NOT EXISTS char_kills_total
        (
            characterID bigint PRIMARY KEY,
            characterName varchar(100),
            kills int
        )
        """,
        """CREATE TABLE IF NOT EXISTS char_vp_daily
        (
            characterID bigint NOT NULL,
            characterName varchar(100),
            date varchar(8) NOT NULL,
            victoryPoints int,
            PRIMARY KEY (characterID, date)
        )
        """,
        """CREATE TABLE IF NOT EXISTS char_vp_total
        (
            characterID bigint PRIMARY KEY,
            characterName varchar(100),
            victoryPoints int
        )
        """,
        """CREATE TABLE IF NOT EXISTS corp_kills_daily
        (
            corporationID bigint NOT NULL,
            corporationName varchar(100),
            date varchar(8) NOT NULL,
            kills int,
            PRIMARY KEY (corporationID, date)
        )
        """,
        """CREATE TABLE IF NOT EXISTS corp_kills_total
        (
            corporationID bigint PRIMARY KEY,
            corporationName varchar(100),
            kills int
        )
        """,
        """CREATE TABLE IF NOT EXISTS corp_vp_daily
        (
            corporationID bigint NOT NULL,
            corporationName varchar(100),
            date varchar(8) NOT NULL,
            victoryPoints int,
            PRIMARY KEY (corporationID, date)
        )
        """,
        """CREATE TABLE IF NOT EXISTS corp_vp_total
        (
            corporationID bigint PRIMARY KEY,
            corporationName varchar(100),
            victoryPoints int
        )
        """,
        """CREATE TABLE IF NOT EXISTS faction_kills_daily
        (
            factionID bigint NOT NULL,
            factionName varchar(100),
            date varchar(8) NOT NULL,
            kills int,
            PRIMARY KEY (factionID, date)
        )
        """,
        """CREATE TABLE IF NOT EXISTS faction_kills_total
        (
            factionID bigint PRIMARY KEY,
            factionName varchar(100),
            kills int
        )
        """,
        """CREATE TABLE IF NOT EXISTS faction_vp_daily
        (
            factionID bigint NOT NULL,
            factionName varchar(100),
            date varchar(8) NOT NULL,
            victoryPoints int,
            PRIMARY KEY (factionID, date)
        )
        """,
        """CREATE TABLE IF NOT EXISTS faction_vp_total
        (
            factionID bigint PRIMARY KEY,
            factionName varchar(100),
            victoryPoints int
        )
        """,
    ]
    for q in queries:
        DB.execute(q)


def yesterday_string():
    yesterday_obj = date.today() + timedelta(days=-1)
    yesterday = yesterday_obj.strftime('%Y%m%d')
    return yesterday

def handle_chars(char_node):
    handle_all('char', char_node)

def handle_corps(corp_node):
    handle_all('corp', corp_node)

def handle_factions(faction_node):
    handle_all('faction', faction_node)

def handle_all(table_name, node):
    yesterday = yesterday_string()
    key = KEYS[table_name]
    name = NAMES[table_name]
    for kid in node:
        if kid.attrib['name'] == 'KillsYesterday':
            for leader in kid:
                attrs = leader.attrib
                print attrs
                if DB.get("""SELECT {key} from {table_name}_kills_daily
                        WHERE {key}=%s AND date=%s""".format(table_name=table_name, key=key),
                        (attrs[key], yesterday)):
                    DB.execute("""UPDATE {table_name}_kills_daily SET kills=%s WHERE {key}=%s and date=%s""".format(table_name=table_name, key=key),
                        (attrs['kills'], attrs[key], yesterday))
                else:
                    DB.execute("""INSERT INTO {table_name}_kills_daily
                            ({key}, {name}, kills, date)
                            VALUES (%s, %s, %s, %s)""".format(table_name=table_name, key=key, name=name),
                                (attrs[key], attrs[name], attrs['kills'], yesterday))
        elif kid.attrib['name'] == 'KillsTotal':
            for leader in kid:
                attrs = leader.attrib
                date = yesterday
                if DB.get("""SELECT {key} from {table_name}_kills_total WHERE {key}=%s""".format(table_name=table_name, key=key),
                        (attrs[key])):
                    DB.execute("""UPDATE {table_name}_kills_total SET kills=%s WHERE {key}=%s""".format(table_name=table_name, key=key),
                        (attrs['kills'], attrs[key]))
                else:
                    DB.execute("""INSERT INTO {table_name}_kills_total
                            ({key}, {name}, kills)
                            VALUES (%s, %s, %s)""".format(table_name=table_name, key=key, name=name),
                                (attrs[key], attrs[name], attrs['kills']))

def main():
    create_tables()
    stats = requests.get(FW_STATS_URL).content
    root = ET.fromstring(stats)
    for child in root:
        if child.tag == 'result':
            result = child
            break
    else:
        raise SystemExit("Can find result tag")

    for kid in result:
        if kid.tag == "characters":
            handle_chars(kid)
        elif kid.tag == "corporations":
            handle_corps(kid)
        elif kid.tag == "factions":
            handle_factions(kid)
        else:
            raise SystemExit("Unknown stat type {_type}".format(_type=kid.tag))

if __name__ == "__main__":
    main()
