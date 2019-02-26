import psycopg2
from psycopg2 import Error
from faker import Faker
fake = Faker()

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "postgres",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")
    cursor = connection.cursor()

    create_table_query = ''' DROP TABLE IF EXISTS accounts CASCADE;
                            CREATE TABLE accounts(
                            account_id serial  PRIMARY KEY,
                            balance numeric,
                            creation TIMESTAMP NOT NULL);

                            DROP TABLE IF EXISTS customers CASCADE;
                            CREATE TABLE customers(
                            customer_id SERIAL PRIMARY KEY,
                            first_name VARCHAR (50),
                            last_name varchar (50),
                            address Varchar (255),
                            city VARCHAR (50),
                            state VARCHAR(20),
                            zip VARCHAR  (10),
                            creation TIMESTAMP NOT NULL);

                            DROP TABLE IF EXISTS account_customer CASCADE;
                            CREATE TABLE account_customer(    
                            customer_id integer NOT NULL,
                            account_id integer NOT NULL,
                            PRIMARY KEY (account_id, customer_id),
                              CONSTRAINT customer_id_fk FOREIGN KEY (customer_id)
                                  REFERENCES customers(customer_id) MATCH SIMPLE
                               ON UPDATE NO ACTION ON DELETE NO ACTION,
                              CONSTRAINT account_id_fk FOREIGN KEY (account_id)
                                  REFERENCES accounts (account_id) MATCH SIMPLE
                            ON UPDATE NO ACTION ON DELETE NO ACTION
                            );
                            Drop table if exists all_join;
                            '''
    
    cursor.execute(create_table_query)

    fake.random.seed(1993)
    for i in range (1, 501): 
        first_name = fake.first_name()
        last_name = fake.last_name()
        address =fake.address()
        city = fake.city()
        state = fake.state()
        balance = fake.random_number()
        zipcode= fake.zipcode()
        timestamp = fake.iso8601(tzinfo=None, end_datetime=None)
        timestamp2 = fake.iso8601(tzinfo=None, end_datetime=None)
        cursor.execute("INSERT INTO customers ( first_name, last_name, address, city, state, zip, creation )VALUES(%s, %s, %s, %s, %s, %s, %s)",
                       ( first_name, last_name, address, city, state, zipcode, timestamp));
  

        cursor.execute("INSERT INTO accounts( balance, creation )VALUES( %s, %s)",
                       ( balance, timestamp2));

#Might need to change the path
    with open('customer_account.csv', 'r') as f:
    
            next(f)  # Skip the header row.
            cursor.copy_from(f, 'account_customer', sep=',')

    connection.commit()
    print("Table created successfully in PostgreSQL ")
    print("Data Inserted successfully in  tables")
    
    query_1 = """select cu.customer_id, cu.state  from customers cu join account_customer ca
                    on cu.customer_id= ca.customer_id join accounts ac on ca.account_id= ac.account_id
                    group by  ac.account_id, cu.customer_id order by avg(ac.balance) DESC limit 10;"""
                            
    cursor.execute(query_1)

    result_1= cursor.fetchall()
    print("\n Customer_id | State\n")
    for r in result_1:
        print( "   ", r[0], "  ", r[1])

    query_2 = """select cu.first_name || ' ' || cu.last_name as Customer, sum(ac.balance) as total
                from customers cu join account_customer ca on cu.customer_id= ca.customer_id join accounts ac
                on ca.account_id= ac.account_id group by  cu.customer_id order by total DESC limit 10;"""

    cursor.execute(query_2)

    result_2= cursor.fetchall()
    print("\n Customer Name|Balance\n")
    for r in result_2:
        print( "   ", r[0], "  ", r[1])

    query_3 = """select cu.first_name || ' ' || cu.last_name as Customer, sum(ac.balance) as total
                from customers cu join account_customer ca on cu.customer_id= ca.customer_id join accounts ac
                on ca.account_id= ac.account_id group by cu.customer_id order by total ASC limit 10;"""
    
    cursor.execute(query_3)

    result_3= cursor.fetchall()
    print("\n Customer Name| Balance\n")
    for r in result_3:
        print( "   ", r[0], "  ", r[1])

    query_4 = """
                Begin;
                select cu.customer_id, cu.first_name || ' ' || cu.last_name as Customer , ac.account_id ,
                ac.balance, ac.balance/10 as one_tenth into all_join from customers cu join account_customer ca 
                on cu.customer_id= ca.customer_id join accounts ac on ca.account_id= ac.account_id 
                group by  cu.customer_id,ac.account_id  order by ac.balance desc ;

                update accounts as ac set balance = balance - sub.one_tenth from (Select account_id, one_tenth from all_join limit 10)
                as sub(account_id, one_tenth) WHERE sub.account_id =ac.account_id;

                update accounts as ac set balance = balance + (select sum(one_tenth) from all_join) from
                (Select account_id from all_join order by balance asc limit 10)
                as sub WHERE sub.account_id =ac.account_id;
                Drop table all_join;
                Commit;

                """
    cursor.execute(query_4)
    print("\n Transaction Completed Successfully")
    
except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while executing queries", error)


finally:
    if(connection):
        cursor.close()

        connection.close()
        print("PostgreSQL connection is closed")



