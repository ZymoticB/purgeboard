from tornpsql import Connection
import xml.etree.ElementTree as ET
import requests
from datetime import timedelta, date
import settings


DB = Connection('localhost', 'purgeboard', user=settings.PSQL_USER, password=settings.PSQL_PASSWORD)
CORP_FW_STATS_URL='https://api.eveonline.com/corp/FacWarStats.xml.aspx'

def create_tables():
    query = """
    CREATE TABLE IF NOT EXISTS crossfire_fw_stats
    (
        factionID bigint,
        factionName varchar(100),
        enlisted varchar(20),
        pilots int,
        killsToday int,
        killsTotal int,
        victoryPointsToday int,
        victoryPointsTotal int,
        date varchar(8),
        PRIMARY KEY (date)
    )
    """
    DB.execute(query)

def yesterday_string():
    yesterday_obj = date.today() + timedelta(days=-1)
    yesterday = yesterday_obj.strftime('%Y%m%d')
    return yesterday


def main():
    create_tables()
    stats = requests.post(CORP_FW_STATS_URL, data={'keyID': settings.CROSSFIRE_KEYID,
                                            'vCode': settings.CROSSFIRE_VCODE}).content
    root = ET.fromstring(stats)
    for child in root:
        if child.tag == 'result':
            result = child
            break
    else:
        raise SystemExit("Can find result tag")

    shit = {}
    date = yesterday_string()
    for kid in result:
        if kid.tag == 'factionID':
            shit['factionID'] = kid.text
        elif kid.tag == 'factionName':
            shit['factionName'] = kid.text
        elif kid.tag == 'enlisted':
            shit['enlisted'] = kid.text
        elif kid.tag == 'pilots':
            shit['pilots'] = kid.text
        elif kid.tag == 'killsYesterday':
            shit['killsToday'] = kid.text
        elif kid.tag == 'killsTotal':
            shit['killsTotal'] = kid.text
        elif kid.tag == 'victoryPointsYesterday':
            shit['victoryPointsToday'] = kid.text
        elif kid.tag == 'victoryPointsTotal':
            shit['victoryPointsTotal'] = kid.text


    if DB.get("""SELECT * from crossfire_fw_stats WHERE date=%s""", (date)):
        DB.execute("""UPDATE crossfire_fw_stats SET factionID=%s,
                                                    factionName=%s,
                                                    enlisted=%s,
                                                    pilots=%s,
                                                    killsToday=%s,
                                                    killsTotal=%s,
                                                    victoryPointsToday=%s,
                                                    victoryPointsTotal=%s""",
                                                    (shit['factionID'],
                                                    shit['factionName'],
                                                    shit['enlisted'],
                                                    shit['pilots'],
                                                    shit['killsToday'],
                                                    shit['killsTotal'],
                                                    shit['victoryPointsToday'],
                                                    shit['victoryPointsTotal']))
    else:
        DB.execute("""INSERT INTO crossfire_fw_stats (factionID,
                                                    factionName,
                                                    enlisted,
                                                    pilots,
                                                    killsToday,
                                                    killsTotal,
                                                    victoryPointsToday,
                                                    victoryPointsTotal,
                                                    date) VALUES
                                                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                                    (shit['factionID'],
                                                    shit['factionName'],
                                                    shit['enlisted'],
                                                    shit['pilots'],
                                                    shit['killsToday'],
                                                    shit['killsTotal'],
                                                    shit['victoryPointsToday'],
                                                    shit['victoryPointsTotal'],
                                                    date))
if __name__ == "__main__":
    main()
