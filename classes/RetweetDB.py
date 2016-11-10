import pyodbc


class RetweetDB:
    def __init__(self, driver, hostname, port, dbname, username, password, context):
        self.driver = driver
        self.username = username
        self.password = password
        self.hostname = hostname
        self.dbname = dbname
        self.port = port
        self.context = context

        self.retweeter_dsn = "DRIVER={};" \
                             "SERVER={};" \
                             "PORT={};" \
                             "DATABASE={};" \
                             "UID={};" \
                             "PWD={};".format(self.driver, self.hostname, self.port, self.dbname,
                                              self.username, self.password)

        self.conn = pyodbc.connect(self.retweeter_dsn)

    def log_tweet(self, twitter_id, source):
        cursor = self.conn.cursor()

        if not self.is_tweet_logged(twitter_id):
            sql = "INSERT INTO retweeter_bot.tweets (twitter_id, context, source) VALUES (?, ?, ?)"
            cursor.execute(sql, twitter_id, self.context, source)
            cursor.commit()

    def is_tweet_logged(self, twitter_id):
        cursor = self.conn.cursor()

        sql = '''
        SELECT
            stamp
        FROM
            retweeter_bot.tweets
        WHERE
            twitter_id = ?
            AND context = ?
        '''

        cursor.execute(sql, twitter_id, self.context)
        row = cursor.fetchone()

        if row is None:
            # print "This has not yet been tweeted!"
            return False
        else:
            # print "This was retweeted on {}".format(row[0])
            return True
