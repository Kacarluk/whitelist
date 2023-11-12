import json
import sqlite3

# Definování cesty JSON souboru
json_file_path = '3_164941_164845.json'

# Cesta k SQL souboru
sqlite_db_path = f'{json_file_path}.db' #Zkopíruje i příponu!

# Přečtení JSON souboru
with open(json_file_path, 'r') as file:
    data = json.load(file)
    
def create_and_populate_db(data, sqlite_db_path):
    
    # Kód pro vytváření a naplňování databáze
    contracts_new_data = data.get('Contracts.New', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS contracts_new;"
    create_table_command = """
    CREATE TABLE contracts_new (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        ConId INTEGER,
        WLIdentId INTEGER,
        WLValidFrom TEXT,
        WLValidTo TEXT,
        DiscountCard_CP BYTE,
        DiscountCard_NetworkID INTEGER,
        DiscountCard_WLIDType BYTE,
        DiscountCard_WLIDLogicalNum STRING,
        TimeCoupon_CP BYTE,
        TimeCoupon_TP BYTE,
        TimeCoupon_WLZones TEXT,
        TimeCoupon_WLSupZones TEXT,
        TimeCoupon_NetworkID INTEGER,
        TimeCoupon_WLIDType BYTE,
        TimeCoupon_WLIDLogicalNum STRING
    );
    """
    
    # Vytvoření SQL databáze na disku
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    # Smazání staré tabulky, pokud existuje
    cursor.execute(drop_table_command)
    # Vytvoření nové tabulky dle parametrů
    cursor.execute(create_table_command)
    
    # Definování funkce na vložení dat do tabulky
    def insert_contracts(contracts_new):
        # Kontrola 'None' hodnot pro 'TimeCoupon' and 'DiscountCard'
        time_coupon_new = contracts_new['TimeCoupon'] if 'TimeCoupon' in contracts_new and contracts_new['TimeCoupon'] is not None else {}
        discount_card_new = contracts_new['DiscountCard'] if 'DiscountCard' in contracts_new and contracts_new['DiscountCard'] is not None else {}
        
        # Příprava dat pro vložení
        data_tuple = (
            contracts_new.get('ConId'),
            contracts_new.get('WLIdentId'),
            contracts_new.get('WLValidFrom'),
            contracts_new.get('WLValidTo'),
            discount_card_new.get('CP'),
            discount_card_new.get('NetworkID'),
            discount_card_new.get('WLIDType'),
            discount_card_new.get('WLIDLogicalNum'),
            time_coupon_new.get('CP'),
            time_coupon_new.get('TP'),
            time_coupon_new.get('WLZones'),
            time_coupon_new.get('WLSupZones'),
            time_coupon_new.get('NetworkID'),
            time_coupon_new.get('WLIDType'),
            time_coupon_new.get('WLIDLogicalNum')  
        )
        
        # Vložení dat
        cursor.execute("""
        INSERT INTO contracts_new (
            ConId, WLIdentId, WLValidFrom, WLValidTo,
            DiscountCard_CP, DiscountCard_NetworkID,
            DiscountCard_WLIDType, DiscountCard_WLIDLogicalNum,
            TimeCoupon_CP, TimeCoupon_TP, TimeCoupon_WLZones,
            TimeCoupon_WLSupZones, TimeCoupon_NetworkID, 
            TimeCoupon_WLIDLogicalNum, TimeCoupon_WLIDType
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)
                
        # Commit
        conn.commit()
    
    # Vložení do tabulky
    for contracts_new in contracts_new_data:
        insert_contracts(contracts_new)
    
    conn.close()

# Zavolání funkce
create_and_populate_db(data, sqlite_db_path)
