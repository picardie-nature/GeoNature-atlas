from .. import utils
from sqlalchemy.sql import text

def getLastsItems(connection, limit = 3):
    sql = "SELECT * FROM pn_news.feed WHERE 'clicnat' = ANY(keywords) ORDER BY pubdate DESC LIMIT {}".format(limit)
    req = connection.execute(text(sql))
    return req
