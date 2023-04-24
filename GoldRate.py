import requests
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

Kilo = 1000

Tola = 11.6638038

TroyOunce = 31.1034768

import GoldUnits


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
    def __init__(self, Purity=None, Unit=None, Currency=None):

        self.Currency = Currency
        self.Unit = Unit
        self.Purity = Purity
        self.bid = 0
        self.ask = 0
        self.percentageChhange = None
        self.c = CurrencyRates()
        self.code = None
        if self.Currency == "£":
            self.code = 'GBP'
        elif self.Currency == "€":
            self.code = 'EUR'

    def getLatestRate(self):
        data = requests.get("https://www.kitco.com/charts/livegold.html")
        soup = BeautifulSoup(data.text, 'html.parser')
        self.bid = str(soup.find("div", class_="data-blk bid").findAll("span"))
        self.bid = FormatRates(self.bid)
        self.ask = str(soup.find("div", class_="data-blk ask").findAll("span"))
        self.ask = FormatRates(self.ask)

        self.percentageChhange = str(soup.find("span", id="sp-chg-percent").text)

    # add get bid and get ask in a thread.
    def getBid(self):
        PerGram = getPureGoldPerGramInDollars(self.bid)
        Ratio = float(self.Purity) / 24
        RateForDifferentKarrots = Ratio * PerGram

        Rate = RateForDifferentKarrots
        if self.Unit == GoldUnits.troyounce:
            Rate = TroyOunce * RateForDifferentKarrots
        elif self.Unit == GoldUnits.tola:
            Rate = Tola * RateForDifferentKarrots
        elif self.Unit == GoldUnits.kilogram:
            Rate = Kilo * RateForDifferentKarrots
        elif self.Unit == GoldUnits.gram:
            Rate = RateForDifferentKarrots

        if self.Currency != "$":
            Rate = self.convertRateTo(Rate)

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

    def getLatestExchangeRate(self):
        self.Rate = 0
        base_currency = 'USD'
        target_currency = self.code

        response = requests.get(
            f'https://www.x-rates.com/calculator/?from={base_currency}&to={target_currency}&amount=1')

        if response.status_code != 200:
            return f"Error: Couldn't fetch data. Status code: {response.status_code}"

        soup = BeautifulSoup(response.content, 'html.parser')
        rate_element = soup.find('span', {'class': 'ccOutputTrail'}).previous_sibling
        if rate_element:
            rate = float(rate_element.string)
            self.Rate = rate
        else:
            return "Error: Couldn't find the exchange rate."

    def convertRateTo(self, Value):
        return self.Rate * Value

    def convertGtoDifferentUnit(self, weightInGram):
        if self.Unit == GoldUnits.troyounce:
            Weight = TroyOunce * weightInGram
        elif self.Unit == GoldUnits.tola:
            Weight = Tola * weightInGram
        elif self.Unit == GoldUnits.kilogram:
            Weight = Kilo * weightInGram
        elif self.Unit == GoldUnits.gram:
            Weight = weightInGram
        return Weight

    def getAsk(self):
        PerGram = getPureGoldPerGramInDollars(self.ask)
        Ratio = float(self.Purity) / 24
        RateForDifferentKarrots = Ratio * PerGram

        Rate = RateForDifferentKarrots

        if self.Unit == GoldUnits.troyounce:
            Rate = TroyOunce * RateForDifferentKarrots
        elif self.Unit == GoldUnits.tola:
            Rate = Tola * RateForDifferentKarrots
        elif self.Unit == GoldUnits.kilogram:
            Rate = Kilo * RateForDifferentKarrots
        elif self.Unit == GoldUnits.gram:
            Rate = RateForDifferentKarrots

        if self.Currency != "$":
            Rate = self.convertRateTo(Rate)

        return round(Rate, 2)

    def changeUnit(self, Unit):
        self.Unit = Unit

    def getAskinGrams(self):
        PerGram = getPureGoldPerGramInDollars(self.ask)
        Ratio = float(self.Purity) / 24
        RateForDifferentKarrots = Ratio * PerGram

        Rate = RateForDifferentKarrots
        if self.Currency != "$":
            Rate = self.convertRateTo(Rate)

        return Rate

    def getBidinGrams(self):
        PerGram = getPureGoldPerGramInDollars(self.bid)
        Ratio = float(self.Purity) / 24
        RateForDifferentKarrots = Ratio * PerGram

        Rate = RateForDifferentKarrots
        if self.Currency != "$":
            Rate = self.convertRateTo(Rate)

        return Rate

    def convertRate(self, RateInGram):
        Rate = 0
        if RateInGram is None:
            return
        if self.Unit == GoldUnits.troyounce:
            Rate = TroyOunce * RateInGram
        elif self.Unit == GoldUnits.tola:
            Rate = Tola * RateInGram
        elif self.Unit == GoldUnits.kilogram:
            Rate = Kilo * RateInGram
        elif self.Unit == GoldUnits.gram:
            Rate = RateInGram
        return Rate

    def converttToRateInGram(self, RateInUnit):
        Rate = 0
        if RateInUnit is None:
            return
        if self.Unit == GoldUnits.troyounce:
            Rate = RateInUnit / TroyOunce
        elif self.Unit == GoldUnits.tola:
            Rate = RateInUnit / Tola
        elif self.Unit == GoldUnits.kilogram:
            Rate = RateInUnit / Kilo
        elif self.Unit == GoldUnits.gram:
            Rate = RateInUnit
        return Rate

    def convertRateFromTroyOunce(self, RateInOunce):
        if RateInOunce is None:
            return
        RateInGram = RateInOunce / TroyOunce
        return self.convertRate(RateInGram)

    def convertWeight(self, WeightInGram):
        Weight = 0
        if WeightInGram is None:
            return
        if self.Unit == GoldUnits.troyounce:
            Weight = WeightInGram / TroyOunce
        elif self.Unit == GoldUnits.tola:
            Weight = WeightInGram / Tola
        elif self.Unit == GoldUnits.kilogram:
            Weight = WeightInGram / Kilo
        elif self.Unit == GoldUnits.gram:
            Weight = WeightInGram
        return Weight

    def getCurrency(self):
        return self.Currency

    def getPercentageChange(self):
        return self.percentageChhange


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