import cProfile
import io
import pstats
import json
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog

def get_json_file_path():
    root = tk.Tk()
    root.withdraw()  # Skryje hlavní okno tkinter

    # Získání názvu souboru od uživatele pomocí vyskakovacího okna
    json_file_path = filedialog.askopenfilename(title="Vyberte JSON soubor", filetypes=[("JSON files", "*.json")])

    return json_file_path

# Získání názvu JSON souboru od uživatele
json_file_path = get_json_file_path()

# Odstranění přípony .json z názvu souboru
base_name = os.path.splitext(json_file_path)[0]

# Cesta k SQL souboru
sqlite_db_path = f'{base_name}.db'

# Definice profileru
profiler = cProfile.Profile()

# Spuštění profilování
profiler.enable()

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
        WLValidFrom DATE,
        WLValidTo DATE,
        DiscountCard_CP BYTE,
        DiscountCard_NetworkID INTEGER,
        DiscountCard_WLIDType BYTE,
        DiscountCard_WLIDLogicalNum STRING,
        TimeCoupon_CP BYTE,
        TimeCoupon_TP BYTE,
        TimeCoupon_WLZones STRING,
        TimeCoupon_WLSupZones STRING,
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
    def insert_contracts_new(contracts_new):
        # Kontrola 'None' hodnot pro 'TimeCoupon' and 'DiscountCard'
        time_coupon_new = contracts_new['TimeCoupon'] if 'TimeCoupon' in contracts_new and contracts_new['TimeCoupon'] is not None else {}
        discount_card_new = contracts_new['DiscountCard'] if 'DiscountCard' in contracts_new and contracts_new['DiscountCard'] is not None else {}
        
        # Příprava dat pro vložení
        data_tuple = (
            contracts_new.get('ConId'),
            contracts_new.get('WLIdentId'),
            contracts_new.get('WLValidFrom'),
            contracts_new.get('WLValidTo'),
            discount_card_new.get('Cp'),
            discount_card_new.get('NetworkID'),
            discount_card_new.get('WLIDType'),
            discount_card_new.get('WLIDLogicalNum'),
            time_coupon_new.get('Cp'),
            time_coupon_new.get('Tp'),
            time_coupon_new.get('WLZones'),
            time_coupon_new.get('WLSupZones'),
            time_coupon_new.get('NetworkID'),
            time_coupon_new.get('WLIDType'),
            time_coupon_new.get('WLIDLogicalNum')  
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO contracts_new (
            ConId, 
            WLIdentId, 
            WLValidFrom, 
            WLValidTo,
            DiscountCard_CP, 
            DiscountCard_NetworkID,
            DiscountCard_WLIDType, 
            DiscountCard_WLIDLogicalNum,
            TimeCoupon_CP, 
            TimeCoupon_TP, 
            TimeCoupon_WLZones,
            TimeCoupon_WLSupZones, 
            TimeCoupon_NetworkID, 
            TimeCoupon_WLIDLogicalNum, 
            TimeCoupon_WLIDType
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)
                  
    # Vložení do tabulky
    for contracts_new in contracts_new_data:
        insert_contracts_new(contracts_new)

    # Commit
    conn.commit()
        
    ################################### CONTRACTS CHANGE
    
    # Kód pro vytváření a naplňování databáze
    contracts_change_data = data.get('Contracts.Change', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS contracts_change;"
    create_table_command = """
    CREATE TABLE contracts_change (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        ConId INTEGER,
        WLIdentId INTEGER,
        WLValidFrom DATE,
        WLValidTo DATE,
        DiscountCard_CP BYTE,
        DiscountCard_NetworkID INTEGER,
        DiscountCard_WLIDType BYTE,
        DiscountCard_WLIDLogicalNum STRING,
        TimeCoupon_CP BYTE,
        TimeCoupon_TP BYTE,
        TimeCoupon_WLZones STRING,
        TimeCoupon_WLSupZones STRING,
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
    def insert_contracts_change(contracts_change):
        # Kontrola 'None' hodnot pro 'TimeCoupon' and 'DiscountCard'
        time_coupon_change = contracts_change['TimeCoupon'] if 'TimeCoupon' in contracts_change and contracts_change['TimeCoupon'] is not None else {}
        discount_card_change = contracts_change['DiscountCard'] if 'DiscountCard' in contracts_change and contracts_change['DiscountCard'] is not None else {}
        
        # Příprava dat pro vložení
        data_tuple = (
            contracts_change.get('ConId'),
            contracts_change.get('WLIdentId'),
            contracts_change.get('WLValidFrom'),
            contracts_change.get('WLValidTo'),
            discount_card_change.get('Cp'),
            discount_card_change.get('NetworkID'),
            discount_card_change.get('WLIDType'),
            discount_card_change.get('WLIDLogicalNum'),
            time_coupon_change.get('Cp'),
            time_coupon_change.get('Tp'),
            time_coupon_change.get('WLZones'),
            time_coupon_change.get('WLSupZones'),
            time_coupon_change.get('NetworkID'),
            time_coupon_change.get('WLIDType'),
            time_coupon_change.get('WLIDLogicalNum')  
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO contracts_change (
            ConId, 
            WLIdentId, 
            WLValidFrom, 
            WLValidTo,
            DiscountCard_CP, 
            DiscountCard_NetworkID,
            DiscountCard_WLIDType, 
            DiscountCard_WLIDLogicalNum,
            TimeCoupon_CP, 
            TimeCoupon_TP, 
            TimeCoupon_WLZones,
            TimeCoupon_WLSupZones, 
            TimeCoupon_NetworkID, 
            TimeCoupon_WLIDLogicalNum, 
            TimeCoupon_WLIDType
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)
                
    
    # Vložení do tabulky
    for contracts_change in contracts_change_data:
        insert_contracts_change(contracts_change)   
        
    # Commit
    conn.commit()
    
    ################################### CONTRACTS DELETE
    
    # Kód pro vytváření a naplňování databáze
    contracts_delete_data = data.get('Contracts.Delete', [])
    
    # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS contracts_delete;"
    create_table_command = """
    CREATE TABLE contracts_delete (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        ConId INTEGER
        );
        """

    # Vytvoření SQL databáze na disku
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Smazání staré tabulky, pokud existuje
    cursor.execute(drop_table_command)
    # Vytvoření nové tabulky dle parametrů
    cursor.execute(create_table_command)

    # Vložení do tabulky
    for contracts_delete in contracts_delete_data:
        cursor.execute('INSERT INTO contracts_delete (ConId) VALUES (?)', (contracts_delete,))
    

    # Commit the changes to the database
    conn.commit()
    
    ###################################### IDENTIFIERS NEW
    
    # Kód pro vytváření a naplňování databáze
    identifiers_new_data = data.get('Identifiers.New', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS identifiers_new;"
    create_table_command = """
    CREATE TABLE identifiers_new (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        WLMOSIdentId INTEGER,
        WLToken1 TEXT,
        WLToken1Ver BYTE,
        WLCardType BYTE,
        WLCardStatus BYTE,
        WLCardExpdate DATE,
        WLMOSPssngrAcct INTEGER,
        WLToken2 TEXT,
        WLToken2Ver BYTE
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
    def insert_identifiers_new(identifiers_new):
        
        # Příprava dat pro vložení
        data_tuple = (
        identifiers_new.get('WLIdentId'),
        identifiers_new.get('WLToken1'),
        identifiers_new.get('WLToken1Ver'),
        identifiers_new.get('WLCardType'),
        identifiers_new.get('WLCardStatus'),
        identifiers_new.get('WLCardExpdate'),
        identifiers_new.get('WLMOSPssngrAcct'),
        identifiers_new.get('WLToken2'),
        identifiers_new.get('WLToken2Ver')
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO identifiers_new (
            WLMOSIdentId,
            WLToken1,
            WLToken1Ver,
            WLCardType,
            WLCardStatus,
            WLCardExpdate,
            WLMOSPssngrAcct,
            WLToken2,
            WLToken2Ver
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)
                
    
    # Vložení do tabulky
    for identifiers_new in identifiers_new_data:
        insert_identifiers_new(identifiers_new)   
        
    # Commit
    conn.commit()
    
    ###################################### IDENTIFIERS CHANGE
    
    # Kód pro vytváření a naplňování databáze
    identifiers_change_data = data.get('Identifiers.Change', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS identifiers_change;"
    create_table_command = """
    CREATE TABLE identifiers_change (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        WLMOSIdentId INTEGER,
        WLToken1 TEXT,
        WLToken1Ver BYTE,
        WLCardType BYTE,
        WLCardStatus BYTE,
        WLCardExpdate DATE,
        WLMOSPssngrAcct INTEGER,
        WLToken2 TEXT,
        WLToken2Ver BYTE
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
    def insert_identifiers_change(identifiers_change):
        
        # Příprava dat pro vložení
        data_tuple = (
        identifiers_change.get('WLIdentId'),
        identifiers_change.get('WLToken1'),
        identifiers_change.get('WLToken1Ver'),
        identifiers_change.get('WLCardType'),
        identifiers_change.get('WLCardStatus'),
        identifiers_change.get('WLCardExpdate'),
        identifiers_change.get('WLMOSPssngrAcct'),
        identifiers_change.get('WLToken2'),
        identifiers_change.get('WLToken2Ver')
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO identifiers_change (
            WLMOSIdentId,
            WLToken1,
            WLToken1Ver,
            WLCardType,
            WLCardStatus,
            WLCardExpdate,
            WLMOSPssngrAcct,
            WLToken2,
            WLToken2Ver
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)
                
    
    # Vložení do tabulky
    for identifiers_change in identifiers_change_data:
        insert_identifiers_change(identifiers_change)   
        
    # Commit
    conn.commit()
    
    ################################### IDENTIFIERS DELETE
    
    # Kód pro vytváření a naplňování databáze
    identifiers_delete_data = data.get('Identifiers.Delete', [])
    
    # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS identifiers_delete;"
    create_table_command = """
    CREATE TABLE identifiers_delete (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        VLMOSIdentId INTEGER
        );
        """

    # Vytvoření SQL databáze na disku
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Smazání staré tabulky, pokud existuje
    cursor.execute(drop_table_command)
    # Vytvoření nové tabulky dle parametrů
    cursor.execute(create_table_command)

    # Vložení do tabulky
    for identifiers_delete in identifiers_delete_data:
        cursor.execute('INSERT INTO identifiers_delete (VLMOSIdentId) VALUES (?)', (identifiers_delete,))
    

    # Commit the changes to the database
    conn.commit()
    
      ################################### CLIENTS NEW
    
    # Kód pro vytváření a naplňování databáze
    clients_new_data = data.get('Clients.New', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS clients_new;"
    create_table_command = """
    CREATE TABLE clients_new (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        WLMOSPssngrAcct INTEGER,
        PersonalData TEXT
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
    def insert_clients_new(clients_new):
        
        # Příprava dat pro vložení
        data_tuple = (
        clients_new.get('WLMOSPssngrAcct'),
        " "
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO clients_new (
            WLMOSPssngrAcct,
            PersonalData
        ) VALUES (?, ?);
        """, data_tuple)
                
    
    # Vložení do tabulky
    for clients_new in clients_new_data:
        insert_clients_new(clients_new)   
        
    # Commit
    conn.commit()
    
    ################################### CLIENTS CHANGE
    
    # Kód pro vytváření a naplňování databáze
    clients_change_data = data.get('Clients.Change', [])

   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS clients_change;"
    create_table_command = """
    CREATE TABLE clients_change (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        WLMOSPssngrAcct INTEGER,
        PersonalData TEXT
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
    def insert_clients_change(clients_change):
        
        # Příprava dat pro vložení
        data_tuple = (
        clients_change.get('WLMOSPssngrAcct'),
        " "
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO clients_change (
            WLMOSPssngrAcct,
            PersonalData
        ) VALUES (?, ?);
        """, data_tuple)
                
    
    # Vložení do tabulky
    for clients_change in clients_change_data:
        insert_clients_change(clients_change)   
        
    # Commit
    conn.commit()
    
    ################################### CLIENTS DELETE
    
    # Kód pro vytváření a naplňování databáze
    clients_delete_data = data.get('Clients.Delete', [])
    
    # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS clients_delete;"
    create_table_command = """
    CREATE TABLE clients_delete (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        WLMOSPssngrAcct INTEGER
        );
        """

    # Vytvoření SQL databáze na disku
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    # Smazání staré tabulky, pokud existuje
    cursor.execute(drop_table_command)
    # Vytvoření nové tabulky dle parametrů
    cursor.execute(create_table_command)

    # Vložení do tabulky
    for clients_delete in clients_delete_data:
        cursor.execute('INSERT INTO clients_delete (WLMOSPssngrAcct) VALUES (?)', (clients_delete,))
    

    # Commit the changes to the database
    conn.commit()
    
      ################################### HEADER
    
    # Kód pro vytváření a naplňování databáze
    header_data = data.get('Header', {})
    footer_data = data.get('Footer', {})


   # Definování SQL
    drop_table_command = "DROP TABLE IF EXISTS header;"
    create_table_command = """
    CREATE TABLE header (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        WLVer	BYTE,
        WLFormatVer	BYTE,
        Seq	INTEGER,
        SeqPrev	INTEGER,
        WLScopeTimeTo	DATE,
        WLTokenVer	BYTE,
        WLTest	CHAR,
        SigNo	BYTE,
        Sig TEXT
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
    def insert_data(header, footer):
        # Příprava dat pro vložení
        data_tuple = (
            header.get('WLVer'),
            header.get('WLFormatVer'),
            header.get('Seq'),
            header.get('SeqPrev'),
            header.get('WLScopeTimeTo'),
            header.get('WLTokenVer'),
            header.get('WLTest'),
            header.get('SigNo'),
            footer.get('Sig')
        )
        
        # Vložení dat - nadefinování
        cursor.execute("""
        INSERT INTO header (
        WLVer,
        WLFormatVer,
        Seq,
        SeqPrev,
        WLScopeTimeTo,
        WLTokenVer,
        WLTest,
        SigNo,
        Sig
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, data_tuple)
                
    
    # Vložení do tabulky
    insert_data(header_data, footer_data)
        
    # Commit
    conn.commit()
    
    conn.close()

# Zavolání funkce
create_and_populate_db(data, sqlite_db_path)

# Zastavení profilování
profiler.disable()

# Vytvoření textového souboru pro výsledky profileru
output_file_path = 'profilovani_vysledky.txt'
with io.StringIO() as stream:
    # Zápis výsledků profilování do textového souboru
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats()
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(stream.getvalue())

print(f'Výsledky profilování byly uloženy do souboru: {output_file_path}')
