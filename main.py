from User import User
from Investment import Investment
User = User()
User.deleteTable()
User.createTable()
User.insertIntoTable("Muhammad" , "Abubakar" , 100, 100)
User.insertIntoTable("Kanishka", "Jay", 10, 10)
User.insertIntoTable("Kabubakar", "J" , 1, 1)
User.showTable()

Investment = Investment()
Investment.deleteTable()
Investment.createTable()
Investment.insertIntoTable("1","ma",123,123)
Investment.insertIntoTable("2", "ma" , 1,1)
# Investment.deleteRecord("ma")

User.deleteRecord("ma")
User.deleteRecord("kj")
Investment.showTable()
User.showTable()

