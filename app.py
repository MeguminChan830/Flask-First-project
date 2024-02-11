from sqlalchemy import create_engine, text
import os
db_connection= os.environ["DB_CONNECTION"]
engine=create_engine(
    db_connection,
    connect_args={
        "ssl":{
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)
def setup_hello_world():
    with engine.connect() as conn:
        # conn.execute(text("""
        #     create table message(
        #         id int auto_increment primary key,
        #         content varchar(255)
        #     )
        # """))
        result =conn.execute(text("select * from message"))
        print(result.rowcount)
        # if result.rowcount==0:
        # conn.execute(text("insert into message (content) values(\'Hello world!\')")) 
        # conn.execute(text("insert into message (content) values('From python')"))
        conn.commit()
        print("Insert!")
def load_hello_world():
    with engine.connect() as conn:
        result = conn.execute(text("select content, num from message"))
        for row in result:
            print( "{0} : {1}".format(row[0], row[1]))
if __name__=='__main__':
    setup_hello_world()
    load_hello_world()