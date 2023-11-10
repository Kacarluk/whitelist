import json
import sqlite3

import tkinter as tk
from tkinter import simpledialog

def open_json_file():
    # Zobrazí vyskakovací okno pro zadání názvu souboru
    json_file_name = simpledialog.askstring("Otevřít JSON soubor", "Zadejte název JSON souboru:")
    if json_file_name:
        json_file_path = os.path.join(os.getcwd(), json_file_name)

        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                create_and_populate_db(json_data)  # Předá načtená data funkci create_and_populate_db
        except FileNotFoundError:
            print(f"Soubor '{json_file_name}' nebyl nalezen.")
        except json.JSONDecodeError:
            print(f"Soubor '{json_file_name}' není platný JSON soubor.")
        except Exception as e:
            print(f"Chyba při zpracování souboru '{json_file_name}': {e}")

def create_and_populate_db(json_data):
    # Kód pro vytváření a naplňování databáze
    contracts_new = json_data.get('Contracts.New', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS contract_new;"
    create_table_command = """
    CREATE TABLE contracts_new (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        ConId INTEGER,
        WLIdentId INTEGER,
        WLValidFrom DATETIME,
        WLValidTo DATETIME,
        DiscountCard_CP BYTE,
        DiscountCard_NetworkID INTEGER,
        DiscountCard_WLIDType BYTE,
        DiscountCard_WLIDLogicalNum INTEGER,  #Dle specifikace MOS string
        TimeCoupon_CP BYTE,
        TimeCoupon_TP BYTE,
        TimeCoupon_WLZones TEXT,            #String jako TEXT
        TimeCoupon_WLSupZones TEXT,
        TimeCoupon_NetworkID INTEGER,
        TimeCoupon_WLIDType BYTE,
        TimeCoupon_WLIDLogicalNum INTEGER  #Dle specifikace MOS string
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

# Cesta k SQL souboru
sqlite_db_path = f'{json_file_name}.db'

# Call the function with the paths to the JSON file and SQLite database
create_and_populate_db(json_file_path, sqlite_db_path)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Skryje hlavní okno tkinter
    open_json_file()
