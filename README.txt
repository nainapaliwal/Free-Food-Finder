# How to run the project -

# Run these commands to setup an python virtualenv -

py -m pip --version
pip 9.0.1 from c:\python36\lib\site-packages (Python 3.6.1)
py -m pip install --upgrade pip
py -m pip install --user virtualenv
py -m virtualenv env
.\env\Scripts\activate

# Install pyhton packages mentioned in 'requirements.txt' by running the file using `pip install -r requirements.txt`. 

# Need to install postgresql and pgAdmin. Following are the credentials to connect to the database -

user = "postgres",
password = "postgres",
host = "localhost",
port = "5432",
database = "postgres"

# Accounts and Customer table are loaded using Faker but account_customer (associative table) is loaded 
manually using a customer_account.csv file. Might need to change the file path if not found (usually works).

# Locate python folder using `where pyhton` and run `pyhton test.py`. The script sgould run successfully, 
if not error will be displayed. The script show output of first three queries for demo.

# The last query (operation robin hood) executes without producing any result but displays "Transaction Completed Successfully" 
message after execution. To verify that all the queries worked, I have pasted the queries with their results (screenshots)
in a Word document (Naina_Paliwal_Test) for your reference.




