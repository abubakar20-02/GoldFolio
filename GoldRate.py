import requests
from bs4 import BeautifulSoup

Kilo = 1000

Tola = 11.6638038

TroyOunce = 31.1034768


# convert string to correct format for the rates.
def FormatRates(rates):
    # type cast to float for later calculations.
    return float(rates[19] + rates[21:27])


def FormatCurrency(currency):
    # type cast to float for later calculations.
    # used split to separate words with spaces and select the first one.
    return float(currency[38:].split(' ')[0])


# class defined for all data of gold.
def getPureGoldPerGramInDollars(DollarsPerOuncePure):
    return DollarsPerOuncePure / TroyOunce


class Gold:
    def __init__(self, Purity, Unit, Currency):

        self.Currency = Currency
        self.Unit = Unit
        self.Purity = Purity

        data = requests.get("https://www.kitco.com/charts/livegold.html")

        soup = BeautifulSoup(data.text, 'html.parser')

        self.bid = str(soup.find("div", class_="data-blk bid").findAll("span"))
        self.bid = FormatRates(self.bid)

        self.ask = str(soup.find("div", class_="data-blk ask").findAll("span"))
        self.ask = FormatRates(self.ask)

    # add get bid and get ask in a thread.
    def getBid(self):
        PerGram = getPureGoldPerGramInDollars(self.bid)
        Ratio = float(self.Purity) / 24
        RateForDifferentKarrots = Ratio * PerGram

        Rate = RateForDifferentKarrots
        if self.Unit == "Troy ounce":
            Rate = TroyOunce * RateForDifferentKarrots
        elif self.Unit == "Tola":
            Rate = Tola * RateForDifferentKarrots
        elif self.Unit == "Kilogram":
            Rate = Kilo * RateForDifferentKarrots
        elif self.Unit == "Gram":
            Rate = RateForDifferentKarrots

        if self.Currency == "Bahraini Dinars":
            c = Curreny()
            Rate = c.GetRateinBHD(Rate)
        return str(round(Rate, 2))

        # if self.Currency == "BHD":
        #     ans = rate * ans
        #
        # if self.Unit == "Oz":
        #     Rate = TroyOunce * RatePerGram
        # elif self.Unit == "Tola":
        #     Rate = Tola * RatePerGram
        # elif self.Unit == "Kilo":
        #     Rate = Kilo * RatePerGram
        # else:
        #     Rate = RatePerGram
        # return str(round(Rate, 2)) + Currency
        # # return str(round(self.bid, 2)) + " BD"  # per gram cost

    def getAsk(self):
        PerGram = getPureGoldPerGramInDollars(self.ask)
        Ratio = float(self.Purity) / 24
        RateForDifferentKarrots = Ratio * PerGram

        Rate = RateForDifferentKarrots

        if self.Unit == "Troy ounce":
            Rate = TroyOunce * RateForDifferentKarrots
        elif self.Unit == "Tola":
            Rate = Tola * RateForDifferentKarrots
        elif self.Unit == "Kilogram":
            Rate = Kilo * RateForDifferentKarrots
        elif self.Unit == "Gram":
            Rate = RateForDifferentKarrots

        if self.Currency == "Bahraini Dinars":
            c = Curreny()
            Rate = c.GetRateinBHD(Rate)
        return round(Rate, 2)

    def changeUnit(self, Unit):
        self.Unit = Unit


class Curreny:
    def __init__(self):
        data = requests.get(
            "https://www.currency.me.uk/convert/usd/bhd"
        )
        soup = BeautifulSoup(data.text, 'html.parser')
        self.ConversionRateOfUSDToBHD = str(soup.find("span", class_="mini ccyrate"))
        self.ConversionRateOfUSDToBHD = FormatCurrency(self.ConversionRateOfUSDToBHD)

    def GetRateinBHD(self, RateinDollars):
        return round(RateinDollars * self.ConversionRateOfUSDToBHD, 2)
