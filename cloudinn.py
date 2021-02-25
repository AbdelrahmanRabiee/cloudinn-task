#!/usr/bin/python
import psycopg2
import requests


class SearchUnit:
    def __init__(self, keyword):
        self.keyword = keyword

    def _get_db_connection(self):
        """
        Establishing the connection with postgres
        """
        connection = psycopg2.connect(
            database="cloudinndb", user='cloudinnuser', password='password', host='127.0.0.1', port='5432'
        )
        return connection

    def _check_table_exists(self):
        """
        Check if tables is exists or not before creating them
        """
        sql_query = """SELECT * FROM information_schema.tables WHERE table_name=%s"""
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql_query, ('units', ))
        exists = bool(cursor.rowcount)
        cursor.close()
        connection.close()
        return exists

    def _create_tables(self):
        """
        Create database tables
        """
        exists = self._check_table_exists()
        if not exists:
            sql_commands = (
                """CREATE TABLE units (
                unit_id SERIAL PRIMARY KEY,
                unit_name VARCHAR (50),
                description TEXT,
                expansion VARCHAR (50),
                age VARCHAR (50),
                created_in VARCHAR (150),
                build_time INTEGER NULL,
                line_of_sight INTEGER NULL,
                reload_time DECIMAL (5,2) NULL,
                attack_delay DECIMAL (5,2) NULL,
                movement_rate DECIMAL (5,2) NULL,
                hit_points INTEGER NULL,
                unit_range VARCHAR (50) NULL,
                attack INTEGER NULL,
                armor VARCHAR (50) NULL,
                attack_bonus TEXT [] NULL,
                accuracy VARCHAR (150) NULL 
                )""",
                """CREATE TABLE costs (
                cost_id SERIAL PRIMARY KEY,
                unit_id INTEGER NOT NULL,
                wood INTEGER NULL,
                food INTEGER NULL,
                stone INTEGER NULL,
                gold INTEGER NULL,
                FOREIGN KEY (unit_id)
                REFERENCES units (unit_id)
                ON UPDATE CASCADE ON DELETE CASCADE
                )""",
            )

            connection = self._get_db_connection()
            cursor = connection.cursor()
            for command in sql_commands:
                cursor.execute(command)
            cursor.close()
            connection.commit()
            connection.close()

    def _retrieve_data_from_api(self):
        """retrieve units data from cloudinn API"""
        res = requests.get('https://tasks.cloudinn.net/api/v1/units')
        json_data = res.json()
        return json_data['units']

    def _check_inserted_data(self):
        """Check if table has data or not to skip inserting more data"""
        sql_query = """SELECT COUNT(*) FROM units WHERE unit_id=%s;"""
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql_query, (1, ))
        result = cursor.rowcount
        cursor.close()
        connection.commit()
        connection.close()
        return result == 1

    def _insert_data(self):
        """insert units that was retrieved from cloudinn API"""
        if not self._check_inserted_data():
            units = self._retrieve_data_from_api()
            sql_query_unit = """INSERT INTO units(
            unit_name, description,
             expansion, age,
              created_in, build_time,
               line_of_sight, reload_time,
                attack_delay, movement_rate,
                 hit_points, unit_range,
                  attack, armor,
                   attack_bonus, accuracy) VALUES(
                   %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s
                    ) RETURNING unit_id;"""

            connection = self._get_db_connection()
            cursor = connection.cursor()

            # insert units values into table
            for unit in units:
                unit_name = unit['name']
                description = unit['description']
                expansion = unit['expansion']
                age = unit['age']
                created_in = unit['created_in']
                build_time = unit['build_time'] if 'build_time' in unit else None
                line_of_sight = unit['line_of_sight'] if 'line_of_sight' in unit else None
                reload_time = unit['reload_time'] if 'reload_time' in unit else None
                attack_delay = unit['attack_delay'] if 'attack_delay' in unit else None
                movement_rate = unit['movement_rate'] if 'movement_rate' in unit else None
                hit_points = unit['hit_points'] if 'hit_points' in unit else None
                unit_range = unit['range'] if 'range' in unit else None
                attack = unit['attack'] if 'attack' in unit else None
                armor = unit['armor'] if 'armor' in unit else None
                accuracy = unit['accuracy'] if 'accuracy' in unit else None
                attack_bonus = unit['attack_bonus'] if 'attack_bonus' in unit else None

                cursor.execute(
                    sql_query_unit,
                    (
                        unit_name, description,
                        expansion, age,
                        created_in, build_time,
                        line_of_sight, reload_time,
                        attack_delay, movement_rate,
                        hit_points, unit_range,
                        attack, armor,
                        attack_bonus, accuracy
                    ))
                unit_id = cursor.fetchone()[0]

                wood = unit['cost']['Wood'] if 'Wood' in unit['cost'] else None
                food = unit['cost']['Food'] if 'Food' in unit['cost'] else None
                stone = unit['cost']['Stone'] if 'Stone' in unit['cost'] else None
                gold = unit['cost']['Gold'] if 'Gold' in unit['cost'] else None

                sql_qury_cost = """INSERT INTO costs(unit_id, wood, food, stone, gold) VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql_qury_cost, (unit_id, wood, food, stone, gold))

            cursor.close()
            connection.commit()
            connection.close()

    def search(self):
        """search for units with unit name"""
        self._create_tables()
        self._insert_data()

        sql_query = """SELECT * FROM units WHERE unit_name ILIKE %s;"""
        connection = self._get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql_query, ('%{}%'.format(self.keyword), ))

        result = cursor.fetchall()
        cursor.close()
        connection.commit()
        connection.close()
        return result


if __name__ == '__main__':
    print('write q to exist:\n')
    keyword = input("Please input unit name:\n")
    while keyword != 'q':
        unit = SearchUnit(keyword=keyword)
        data = unit.search()
        print(data)
        if data == []:
            print('your search keyword: {} doesnt match any record!'.format(keyword))
        units_fields = ['id', 'name', 'description', 'expansion', 'age', 'created_in', 'build_time', 'line_of_sight', 'reload_time']
        for obj in data:
            print(units_fields[0], ': ', obj[0])
            print(units_fields[1], ': ', obj[1])
            print(units_fields[2], ': ', obj[2])
            print(units_fields[3], ': ', obj[3])
            print(units_fields[4], ': ', obj[4])
            print(units_fields[5], ': ', obj[5])
            print(units_fields[6], ': ', obj[6])
            print(units_fields[7], ': ', obj[7])
            print(units_fields[8], ': ', obj[8])
            print('\n')

        keyword = input("Please input unit name:\n")

