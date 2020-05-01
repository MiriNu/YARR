import mysql.connector
import os
import aiomysql
from dotenv import load_dotenv
load_dotenv()
# ----------------------


class DB_connection:

    def __init__(self, table_name):
        self.counter = 0
        self.timestamps = [0, 0, 0]
        self.db = os.getenv('DATABASE')
        self.tb = table_name
        self.DDAtb = "dda_"+table_name

    async def _init(self, number_of_players):
        self.pool = await aiomysql.create_pool(user=os.getenv('USER'),
                                               password=os.getenv('PASSWORD'),
                                               host=os.getenv('HOST'),
                                               db=self.db,
                                               auth_plugin='mysql_native_password')
        """self.cnx = await aiomysql.connect(user=os.getenv('USER'),
                                          password=os.getenv('PASSWORD'),
                                          host=os.getenv('HOST'),
                                          db=self.db,
                                          auth_plugin='mysql_native_password')"""
        # self.cursor = await self.pool.cursor()
        await self.create_DDA_table()
        await self.initialize_DDA_table(number_of_players)

    async def create_DDA_table(self):

        query = ("CREATE TABLE `" + self.db + "`.`" + self.DDAtb + "` ("
                 "`Id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "`PlayerID` INT UNSIGNED NOT NULL,"
                 "`Threshold` FLOAT NOT NULL,"
                 "`I_SpawnHeight_level` INT NOT NULL,"
                 "`I_SpawnHeight_skill` FLOAT NOT NULL,"
                 "`I_DestroyTimer_level` INT NOT NULL,"
                 "`I_DestroyTimer_skill` FLOAT NOT NULL,"
                 "`E_Precision_level` INT NOT NULL,"
                 "`E_Precision_skill` FLOAT NOT NULL,"
                 "`E_Speed_level` INT NOT NULL,"
                 "`E_Speed_skill` FLOAT NOT NULL,"
                 "`E_SpawnRate_level` INT NOT NULL,"
                 "`E_SpawnRate_skill` FLOAT NOT NULL,"
                 "PRIMARY KEY (`Id`))"
                 "DEFAULT CHARACTER SET = UTF8MB4;")

        async with self.pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(query)

    async def initialize_DDA_table(self, number_of_players):

        initial_SpawnHeight_skill = "3"
        initial_DestroyTimer_skill = "3"
        initial_Precision_skill = "2"
        initial_Speed_skill = "2"
        initial_SpawnRate_skill = "2"

        for i in range(number_of_players):
            query = ("INSERT INTO `" + self.db + "`.`" + self.DDAtb + "` (" +
                     "PlayerID, Threshold, I_SpawnHeight_level, " +
                     "I_SpawnHeight_skill, I_DestroyTimer_level, " +
                     "I_DestroyTimer_skill, E_Precision_level, " +
                     "E_Precision_skill, E_Speed_level, E_Speed_skill, " +
                     "E_SpawnRate_level, E_SpawnRate_skill)" +
                     "VALUES (" + str(i + 1) + ", 0, 0, " +
                     initial_SpawnHeight_skill + ", 0, " +
                     initial_DestroyTimer_skill + ", 0, " +
                     initial_Precision_skill + ", 0, " + initial_Speed_skill +
                     ", 0, " + initial_SpawnRate_skill + ")")

            async with self.pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(query)
                    await con.commit()

    async def get_DDA_last_player_skill(self, skill, player_id):
        try:
            query = ("SELECT " + skill + " FROM " + self.db + "."
                     + self.DDAtb + " WHERE PlayerID = " + str(player_id) +
                     " ORDER BY Id ASC LIMIT 1")

            async with self.pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(query)
                    fetch = await cursor.fetchone()
                    return fetch
        except Exception as e:
            print("last_skill exception: " + str(e))
            return [0]

    async def remove_DDA_table(self):
        query = ("DROP TABLE `" + self.db + "`.`" + self.DDAtb + "`")

        async with self.pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(query)

    async def close_connection(self):
        await self.remove_DDA_table()
        self.pool.close()
        await self.pool.wait_closed()
    
    async def get_timestamp(self):
        query = ("SELECT Timestamp From " + self.db + "." + self.tb +
                 " ORDER BY Timestamp DESC LIMIT 1")
        
        async with self.pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(query)
                fetch = await cursor.fetchone()
                return fetch

    async def count_last_pickup_events(self, player_id, tstamp, limit):
        try:
            query = ("SELCT count(Event) FROM (select Event from " + self.db +
                     "." + self.tb + " WHERE (Event = 'pickup' OR Event = " +
                     "'failPickup') AND Timestamp > " +
                     str(self.timestamps[player_id - 1]) +
                     "  AND Timestamp <= " + str(tstamp) + " AND PlayerID = " +
                     str(player_id) + " AND Item = " + str(player_id) +
                     " ORDER BY Timestamp DESC LIMIT " + str(limit) +
                     ") AS limitTable WHERE Event = 'Pickup'")

            async with self.pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(query)
                    fetch = await cursor.fetchone()
                    return fetch
        except Exception as e:
            print("count_total exception: " + str(e))
            return [0]

    async def count_total_player_events(self, event, player_id, tstamp,
                                        spawnItemFlag, playerFlag):

        try:
            query = ("SELECT count(Event) FROM " + self.db + "." + self.tb +
                     " WHERE Event = '" + event + "' AND Timestamp > " +
                     str(self.timestamps[player_id - 1]) +
                     " AND Timestamp <= " + str(tstamp) + " AND PlayerID = " +
                     str(player_id))

            if event == "pickup":
                if playerFlag is True:
                    query += " AND Item = " + str(player_id)
                else:
                    query += " AND Item != " + str(player_id)

            if event == "spawn":
                if spawnItemFlag is True:
                    query += " AND Enemy = 0"
                else:
                    query += " AND Item = 0"

            async with self.pool.acquire() as con:
                async with con.cursor() as cursor:
                    await cursor.execute(query)
                    fetch = await cursor.fetchone()
                    return fetch

        except Exception as e:
            print("count_total exception: " + str(e))
            return [0]

    # NOT USED
    """async def count_total_team_events(self, value, event):
        query = ("SELECT count(" + value + ") FROM `" + self.tb +
                 "` WHERE Event = " + event)

        async with self.pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(query)
                fetch = await cursor.fetchall()
                return fetch"""

    async def insert_DDA_table(self, PlayerID, Threshold, I_SpawnHeight_level,
                               I_SpawnHeight_skill, I_DestroyTimer_level,
                               I_DestroyTimer_skill, E_Precision_level,
                               E_Precision_skill, E_Speed_level, E_Speed_skill,
                               E_SpawnRate_level, E_SpawnRate_skill):

        query = ("INSERT INTO `" + self.db + "`.`" + self.DDAtb + "` (" +
                 "PlayerID, Threshold, I_SpawnHeight_level, " +
                 "I_SpawnHeight_skill, I_DestroyTimer_level, " +
                 "I_DestroyTimer_skill, E_Precision_level, " +
                 "E_Precision_skill, E_Speed_level, E_Speed_skill, " +
                 "E_SpawnRate_level, E_SpawnRate_skill)" +
                 "VALUES (" + str(PlayerID) + ", " + str(Threshold) + ", " +
                 str(I_SpawnHeight_level) + ", " + str(I_SpawnHeight_skill) +
                 ", " + str(I_DestroyTimer_level) + ", " +
                 str(I_DestroyTimer_skill) + ", " + str(E_Precision_level) +
                 ", " + str(E_Precision_skill) + ", " + str(E_Speed_level) +
                 ", " + str(E_Speed_skill) + ", " + str(E_SpawnRate_level) +
                 ", " + str(E_SpawnRate_skill) + ")")

        async with self.pool.acquire() as con:
            async with con.cursor() as cursor:
                await cursor.execute(query)
                await con.commit()


"""class DB_connection:

    def __init__(self, table_name, number_of_players):
        self.counter = 0
        self.db = os.getenv('DATABASE')
        self.tb = table_name
        self.DDAtb = "dda_"+table_name
        self.cnx = mysql.connector.connect(user=os.getenv('USER'),
                                           password=os.getenv('PASSWORD'),
                                           host=os.getenv('HOST'),
                                           database=self.db,
                                           auth_plugin='mysql_native_password')
        self.cursor = self.cnx.cursor(buffered=True)
        self.create_DDA_table()
        self.initialize_DDA_table(number_of_players)

    def create_DDA_table(self):
        query = ("CREATE TABLE `" + self.db + "`.`" + self.DDAtb + "` ("
                 "`Id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                 "`PlayerID` INT UNSIGNED NOT NULL,"
                 "`Threshold` FLOAT NOT NULL,"
                 "`I_SpawnHeight_level` INT NOT NULL,"
                 "`I_SpawnHeight_skill` FLOAT NOT NULL,"
                 "`I_DestroyTimer_level` INT NOT NULL,"
                 "`I_DestroyTimer_skill` FLOAT NOT NULL,"
                 "`E_Precision_level` INT NOT NULL,"
                 "`E_Precision_skill` FLOAT NOT NULL,"
                 "`E_Speed_level` INT NOT NULL,"
                 "`E_Speed_skill` FLOAT NOT NULL,"
                 "`E_SpawnRate_level` INT NOT NULL,"
                 "`E_SpawnRate_skill` FLOAT NOT NULL,"
                 "PRIMARY KEY (`Id`))"
                 "DEFAULT CHARACTER SET = utf8;")

        self.cursor.execute(query)

    def initialize_DDA_table(self, number_of_players):

        initial_SpawnHeight_skill = "3"
        initial_DestroyTimer_skill = "3"
        initial_Precision_skill = "2"
        initial_Speed_skill = "2"
        initial_SpawnRate_skill = "2"

        for i in range(number_of_players):
            query = ("INSERT INTO `" + self.db + "`.`" + self.DDAtb + "` (" +
                     "PlayerID, Threshold, I_SpawnHeight_level, " +
                     "I_SpawnHeight_skill, I_DestroyTimer_level, " +
                     "I_DestroyTimer_skill, E_Precision_level, " +
                     "E_Precision_skill, E_Speed_level, E_Speed_skill, " +
                     "E_SpawnRate_level, E_SpawnRate_skill)" +
                     "VALUES (" + str(i + 1) + ", 0, 0, " +
                     initial_SpawnHeight_skill + ", 0, " +
                     initial_DestroyTimer_skill + ", 0, " +
                     initial_Precision_skill + ", 0, " + initial_Speed_skill +
                     ", 0, " + initial_SpawnRate_skill + ")")

            self.cursor.execute(query)
            self.cnx.commit()

    def get_DDA_last_player_skill(self, skill, player_id):
        try:
            query = ("SELECT " + skill + " FROM " + self.db + "."
                     + self.DDAtb + " WHERE PlayerID = " + str(player_id) +
                     " ORDER BY Id ASC LIMIT 1")
            self.cursor.execute(query)
            return self.cursor.fetchone()
        except Exception as e:
            print("last_skill exception: " + str(e))
            return [0]

    def remove_DDA_table(self):
        query = ("DROP TABLE `" + self.db + "`.`" + self.DDAtb + "`")
        self.cursor.execute(query)

    def close_connection(self):
        self.remove_DDA_table()
        self.cursor.close()
        self.cnx.close()

    def count_total_player_events(self, event, player_id):
        try:
            query = ("SELECT count(Event) FROM " + self.db + "." + self.tb +
                     " WHERE Event = '" + event + "' AND PlayerID = " +
                     str(player_id))
            self.cursor.execute(query)
            fetch = self.cursor.fetchone()
            return fetch
        except Exception as e:
            print("count_total exception: " + str(e))
            return [0]

    def count_total_team_events(self, value, event):
        query = ("SELECT count(" + value + ") FROM `" + self.tb +
                 "` WHERE Event = " + event)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_DDA_table(self, PlayerID, Threshold, I_SpawnHeight_level,
                         I_SpawnHeight_skill, I_DestroyTimer_level,
                         I_DestroyTimer_skill, E_Precision_level,
                         E_Precision_skill, E_Speed_level, E_Speed_skill,
                         E_SpawnRate_level, E_SpawnRate_skill):

        query = ("INSERT INTO `" + self.db + "`.`" + self.DDAtb + "` (" +
                 "PlayerID, Threshold, I_SpawnHeight_level, " +
                 "I_SpawnHeight_skill, I_DestroyTimer_level, " +
                 "I_DestroyTimer_skill, E_Precision_level, " +
                 "E_Precision_skill, E_Speed_level, E_Speed_skill, " +
                 "E_SpawnRate_level, E_SpawnRate_skill)" +
                 "VALUES (" + str(PlayerID) + ", " + str(Threshold) + ", " +
                 str(I_SpawnHeight_level) + ", " + str(I_SpawnHeight_skill) +
                 ", " + str(I_DestroyTimer_level) + ", " +
                 str(I_DestroyTimer_skill) + ", " + str(E_Precision_level) +
                 ", " + str(E_Precision_skill) + ", " + str(E_Speed_level) +
                 ", " + str(E_Speed_skill) + ", " + str(E_SpawnRate_level) +
                 ", " + str(E_SpawnRate_skill) + ")")

        self.cursor.execute(query)
        self.cnx.commit()"""
