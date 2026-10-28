import pandas as pd
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_client import Region
from recombee_api_client.api_requests import  SetItemValues, Batch, GetItemValues
from recombee_api_client.exceptions import APIException

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
DB_NAME = 'gutadanalexandru-dev'
PRIVATE_TOKEN = 'gBityqm2M6mFFH9CYxUltEeQOBhPq6e731Gywu0iRIYvhXoiXTc7LupwDMUTS2a4'
REGION = 'eu-west'

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region.EU_WEST)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = 'laptop_price.csv'

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")
    
    requests = []
    
    for index, row in df.iterrows():
        # TODO 3: Extrageti ID-ul unic al produsului din coloana corespunzatoare din CSV
        item_id = str(row['laptop_ID'])
        #print(item_id)

        # TODO 4: Mapati proprietatile definite anterior cu valorile din randul curent
        # Exemplu:
        properties = {
            "Company": str(row['Company']),
            "Product": str(row['Product']),
            "TypeName": str(row['TypeName']),
            "Inches": float(row['Inches']),
            "ScreenResolution": str(row['ScreenResolution']),
            "Cpu": str(row['Cpu']),
            "Ram": str(row['Ram']),
            "Memory": str(row['Memory']),
            "Gpu": str(row['Gpu']),
            "OpSys": str(row['OpSys']),
            "Weight": str(row['Weight']),
            "Price_euros": float(row['Price_euros'])
        }
        #print(properties)

        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            client.send(Batch(requests))
            requests = []
            print("S-a trimis un lot de 100 item-uri...")
            
    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        client.send(Batch(requests))
        print("S-a trimis ultimul lot de item-uri.")
        
    print("Toate item-urile au fost trimise cu succes!")

if __name__ == "__main__":
    send_items()