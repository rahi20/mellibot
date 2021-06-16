# Description of the data

**endocrinos.csv** contains a list of endocrinologists in Morocco, it was scrapped from http://smedian.ma/endocrinos/ using the script **endocrinos_scrapper.py**. The table has the following fields : <br>
<img align="center" src="https://github.com/rahi20/chatbot-project-pfa/blob/main/data/endoc_table.png">

<br>

**create_db_endocrinos.py** is a script to create a database for the endocrinologists. It needs your **mysql** credentials which you can update in **db_cred.json** : The script was created only for testing, **endocrinos.csv** is enough in our case.
