import sys

import snowflake.connector as sf


def sf_connect(username, password, account, warehouse):
    try:
        conn = sf.connect(
            user=username,
            password=password,
            account=account,
            warehouse=warehouse,
        )
        return conn, conn.cursor()
    except Exception as e:
        raise Exception(
            f"Exception occured whlie establishing connection to snowflake:\n{e}")


def check_log_table(cursor):
    query = "select count(*) from db.information_schema.tables where table_name = 'log_table'"
    cursor.execute(query)
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return create_log_table(cursor)


def log_table(cursor, file_name, sha, actor):
    if check_log_table(cursor=cursor):
        query = f"select file_name, count(*) from db.schema.log_table where file_name = '{file_name}' group by 1"
        cursor.execute(query)
        if cursor.fetchone()[1] > 1:
            raise Exception(
                f"Error in log table, duplicate entry for {file_name}")
        elif cursor.fetchone()[1] == 1:
            query = f"update db.schema.log_table set update_datetime = current_datetime, commit_user = '{actor}', commit_sha = '{sha}' where file_name = '{file_name}'"
            cursor.execute(query)
        else:
            query = f"insert into db.schema.log_table (file_name, created_datetime, update_datetime, commit_user, commit_sha ) values ('{file_name}', current_timestamp, current_timestamp, '{actor}', '{sha}')"
            cursor.execute(query)
    else:
        raise Exception(f"log table not available. Please create log table.")


def create_log_table(cursor):
    query = "create table db.schema.log_table(file_name varchar, created_datetime datetime, update_datetime datetime, commit_user varchar, commit_sha varchar)"
    cursor.execute(query)
    return True


if __name__ == "__main__":
    file_name = sys.argv[1]
    branch = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]
    account = sys.argv[5]
    warehouse = sys.argv[6]

    actor = sys.argv[7]
    sha = sys.argv[8]

    print(file_name)
    print(branch)
    print(username)
    print(password)
    print(account)
    print(warehouse)
    print(actor)
    print(sha)

    # branch_replacement = {"dev": "dev", "uat": "uat", "main": "prod"}
    # file_type = file_name.split(".")[1]
    # conn, cursor = sf_connect(
    #     username=username, password=password, account=account, warehouse=warehouse)
    # try:
    #     if file_type.lower() in ["yml", "py"]:
    #         sys.exit(0)
    #     else:
    #         print(f"Branch name: {branch}")
    #         print(f"{file_name} has been changed")
    #         query = ""
    #         with open(file_name, "r") as f:
    #             query = ''.join(line.rstrip() for line in f)
    #         query = query.replace("$env", branch_replacement[branch]).upper()
    #         print(query)
    #         cursor.execute(query)
    #         for x in cursor.fetchall():
    #             print(x)
    # except Exception as e:
    #     raise Exception(f"Exception occured while executing the query:\n{e}")
    # finally:
    #     cursor.close()
    #     conn.close()
