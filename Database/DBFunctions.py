import fnmatch
import os
import shutil
import sqlite3

import pandas as pd
from xlsxwriter import Workbook
from Database import SetUpFile, User, Investment, Statement

from Database import Log, Archive


def saveSnapshot(FolderName):
    folder_name = os.path.basename(FolderName)
    if os.path.exists(FolderName):
        # Use shutil.rmtree() to delete the directory and all its contents
        shutil.rmtree(FolderName)

    os.makedirs(FolderName)
    os.makedirs(os.path.join(FolderName, "DBSupportFiles"))
    # take snapshot before importing files.
    conn = sqlite3.connect(SetUpFile.DBName)

    # Create a file object to store the snapshot
    FilePath = f"{FolderName}/{folder_name}{SetUpFile.DBName}"
    print(FilePath)
    snapshot_file = sqlite3.connect(FilePath)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(SetUpFile.DBArchiveName)

    # Create a file object to store the snapshot
    FilePath = f"{FolderName}/{SetUpFile.DBArchiveName}"
    snapshot_file = sqlite3.connect(FilePath)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(SetUpFile.DBLog)

    # Create a file object to store the snapshot
    FilePath = f"{FolderName}/{SetUpFile.DBLog}"
    snapshot_file = sqlite3.connect(FilePath)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()


def save(FolderName, Profile):
    folder_name = os.path.basename(FolderName)
    if os.path.exists(FolderName):
        # Use shutil.rmtree() to delete the directory and all its contents
        shutil.rmtree(FolderName)

    os.makedirs(FolderName)

    User1 = User.User()
    User1.SelectProfile(Profile)
    User1.saveState(FolderName)

    Investment1 = Investment.Investment()
    Investment1.setProfile(Profile)
    Investment1.saveState(FolderName)

    Statement1 = Statement.Statement()
    Statement1.setProfile(Profile)
    Statement1.saveState(FolderName)

    Log1 = Log.Log()
    Log1.SelectProfile(Profile)
    Log1.saveState(FolderName)

    InvestmentLog = Log.Log.InvestmentLog()
    InvestmentLog.saveState(FolderName, Profile)

    UserLog = Log.Log.UserLog()
    UserLog.saveState(FolderName, Profile)

    MoneyLog = Log.Log.Money()
    MoneyLog.saveState(FolderName, Profile)

    ArchiveUser = Archive.UserArchive()
    ArchiveUser.saveState(FolderName, Profile)

    ArchiveInvestment = Archive.InvestmentArchive()
    ArchiveInvestment.saveState(FolderName, Profile)


def isFileFormatCorrect(folder_path):
    all_entries = os.listdir(folder_path)
    file_count = sum(os.path.isfile(os.path.join(folder_path, entry)) for entry in all_entries)
    print(file_count)
    if not file_count == 9:
        return False
    files_to_check = ['Investment.xlsx', 'InvestmentLog.xlsx', 'Log.xlsx', 'MoneyLog.xlsx', 'Statement.xlsx',
                      'User.xlsx', 'UserLog.xlsx', 'ArchiveInvestment.xlsx', 'ArchiveUser.xlsx']
    files_in_folder = os.listdir(folder_path)
    if not all(file in files_in_folder for file in files_to_check):
        return False
    return True


def load(FolderName, Profile):
    if not isFileFormatCorrect(FolderName):
        print("Wrong format")
        return

    print(f"Folder name: {FolderName} Profile: {Profile}")
    User1 = User.User()
    User1.SelectProfile(Profile)
    User1.deleteUser()
    User1.loadState(FolderName)
    #
    Statement1 = Statement.Statement()
    Statement1.loadState(FolderName)

    Investment1 = Investment.Investment()
    Investment1.loadState(FolderName)

    Log1 = Log.Log()
    Log1.loadState(FolderName)

    InvestmentLog = Log.Log.InvestmentLog()
    InvestmentLog.loadState(FolderName)

    UserLog = Log.Log.UserLog()
    UserLog.loadState(FolderName)

    MoneyLog = Log.Log.Money()
    MoneyLog.loadState(FolderName)

    ArchiveUser = Archive.UserArchive()
    ArchiveUser.loadState(FolderName)

    ArchiveInvestment = Archive.InvestmentArchive()
    ArchiveInvestment.loadState(FolderName)


def getUserIDForLoadedFile(FolderName):
    df = pd.read_excel(f"{FolderName}/User.xlsx")
    UserID = df["User_ID"][0]
    return UserID


def getUserHashedPass(FolderName):
    df = pd.read_excel(f"{FolderName}/User.xlsx")
    UserID = df["Password"][0]
    return UserID


def IsFileCorrect(FolderName):
    # Specify the directory path and directory name to check
    parent_directory_path = FolderName
    directory_name = "DBSupportFiles"

    # use os.path.join() to create the path to the directory you want to check for
    dir_path = os.path.join(parent_directory_path, directory_name)

    # use os.path.isdir() to check if the directory exists
    if os.path.isdir(dir_path):
        print("The directory exists.")
    else:
        return False


    file_extension = "*.db"
    # Use a loop to iterate over all files in the directory and its subdirectories
    for root, dirs, files in os.walk(FolderName):
        for file in files:
            # Check if the file has the specified extension
            if not fnmatch.fnmatch(file, file_extension):
                return False
    return True


def Load(FolderName):
    if not IsFileCorrect(FolderName):
        return

    # remove files that exist
    os.remove("Database.db")
    dir_path = "DBSupportFiles"
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)

    file = [f for f in os.listdir(FolderName) if
            fnmatch.fnmatch(f, "*.db") and os.path.isfile(os.path.join(FolderName, f))]
    print(file[0])

    conn = sqlite3.connect(f"{FolderName}/{file[0]}")

    # Create a file object to store the snapshot
    FilePath = f"{SetUpFile.DBName}"
    print(FilePath)
    snapshot_file = sqlite3.connect(FilePath)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()
    #
    conn = sqlite3.connect(f"{FolderName}/{SetUpFile.DBArchiveName}")

    # Create a file object to store the snapshot
    FilePath = f"{SetUpFile.DBArchiveName}"
    snapshot_file = sqlite3.connect(FilePath)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()

    conn = sqlite3.connect(f"{FolderName}/{SetUpFile.DBLog}")

    # Create a file object to store the snapshot
    FilePath = f"{SetUpFile.DBLog}"
    snapshot_file = sqlite3.connect(FilePath)

    # Take a snapshot of the database
    conn.backup(snapshot_file)

    # Close the file object and the database connection
    snapshot_file.close()
    conn.close()


def convertToExcel(tableName, Database, RemoveFirstColumn=True):
    workbook = Workbook(SetUpFile.ExcelFileName)
    worksheet = workbook.add_worksheet()
    # Write column names to the worksheet
    col = __getColumnName(tableName, Database, RemoveFirstColumn=RemoveFirstColumn)
    print(col)
    data = __getData(tableName, Database, RemoveFirstColumn=RemoveFirstColumn)
    print(data)
    for col_num, column_name in enumerate(col):
        worksheet.write(0, col_num, column_name)

    for i, row in enumerate(data, 1):
        for j, value in enumerate(row):
            worksheet.write(i, j, value)
    workbook.close()
    os.system(SetUpFile.ExcelFileName)


def __getColumnName(tableName, Database, RemoveFirstColumn=True):
    # Open a connection to the database
    conn = sqlite3.connect(Database)

    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info('{0}')".format(tableName))
    columns = [column[1] for column in cursor.fetchall()]
    # remove first element
    if RemoveFirstColumn is True:
        columns.pop(0)
    conn.close()
    return columns


def __getData(tableName, Database, RemoveFirstColumn=True):
    # Open a connection to the database
    columns = __getColumnName(tableName, Database, RemoveFirstColumn=RemoveFirstColumn)
    conn = sqlite3.connect(Database)

    # Create a cursor object
    cursor = conn.cursor()
    cursor.execute('SELECT {} FROM {}'.format(', '.join(columns), tableName))
    data = cursor.fetchall()
    conn.close()
    return data


def __ClearArchive():
    from Database import Archive
    UserArchive = Archive.UserArchive()
    InvestmentArchive = Archive.InvestmentArchive()
    UserArchive.dropTable()
    InvestmentArchive.dropTable()


def ClearTables():
    from Database import Log
    Log = Log.Log()
    Log.dropTable()
    __ClearArchive()


def previousStage(UserID, num=None):
    from Database import Log
    Log = Log.Log()
    print(f"UserID: {UserID}")
    Log.SelectProfile(UserID)
    if num is not None:
        for i in range(0, num):
            Log.previousStage()
    else:
        Log.previousStage()
