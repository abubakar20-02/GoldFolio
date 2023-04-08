from PyQt5.QtWidgets import QPushButton

Background = "background-color: rgb(255, 244, 230)"

Banner = "background-color:  rgb(75, 56, 50);image: url(Resources/logo.png);"

ComboBox = ("QComboBox {\n"
            "border: 1px solid black;\n"
            "border-radius: 4px;\n"
            "padding: 1px 18px 1px 3px;\n"
            "min-width: 3em;\n"
            "}\n"
            "\n"
            "QComboBox:editable {\n"
            "background:white;\n"
            "}\n"
            "\n"
            "QComboBox:!editable, QComboBox::drop-down:editable {\n"
            "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "stop: 0 #FFFFFF, stop: 0.4 #FFFFFF,\n"
            "stop: 0.5 #FFFFFF, stop: 1.0 #FFFFFF);\n"
            "}\n"
            "\n"
            "/* QComboBox gets the \"on\" state when the popup is open */\n"
            "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
            "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
            "stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
            "stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
            "}\n"
            "\n"
            "QComboBox:on { /* shift the text when the popup opens */\n"
            "padding-top: 3px;\n"
            "padding-left: 4px;\n"
            "}\n"
            "\n"
            "QComboBox::drop-down {\n"
            "subcontrol-origin: padding;\n"
            "subcontrol-position: top right;\n"
            "width: 15px;\n"
            "\n"
            "border-left-width: 1px;\n"
            "border-left-color: darkgray;\n"
            "border-left-style: solid; /* just a single line */\n"
            "border-top-right-radius: 4px; /* same radius as the QComboBox */\n"
            "border-bottom-right-radius: 4px;\n"
            "}\n"
            "\n"
            "QComboBox::down-arrow {\n"
            "image: url(Resources/expand logo.png);\n"
            "}\n"
            "\n"
            "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
            "top: 1px;\n"
            "left: 1px;\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "border: 2px solid grey;\n"
            "selection-background-color: darkblue;\n"
            "}\n"
            "")

Icon = 'Resources/logo.png'

MenuBar = "QMenuBar{background-color: white}""QMenu{background-color: white}""QMenu::item:selected { ""background" \
          "-color: #1261A0;color: rgb(255,255,255);} "

PositiveChangeTextColor = ("QLabel{\n"
                           "    border: 1px solid;\n"
                           "    border-style: outset;\n"
                           "    border-width: 1px;\n"
                           "    border-radius: 10px;\n"
                           "    \n"
                           "    background-color: rgb(255, 255, 255);\n"
                           "color: rgb(31,255,15) "
                           "     }")

NegativeChangeTextColor = ("QLabel{\n"
                           "    border: 1px solid;\n"
                           "    border-style: outset;\n"
                           "    border-width: 1px;\n"
                           "    border-radius: 10px;\n"
                           "    \n"
                           "    background-color: rgb(255, 255, 255);\n"
                           "color: rgb(238,75,43) "
                           "     }")

NoChangeTextColor = ("QLabel{\n"
                     "    border: 1px solid;\n"
                     "    border-style: outset;\n"
                     "    border-width: 1px;\n"
                     "    border-radius: 10px;\n"
                     "    \n"
                     "    background-color: rgb(255, 255, 255);\n"
                     "color: rgb(0,0,0) "
                     "     }")

PositiveChange = ("QLabel{\n"
                  "color: rgb(31,255,15);\n"
                  "background-color: white;\n"
                  "     }")

NegativeChange = ("QLabel{\n"
                  "color: rgb(238,75,43);\n"
                  "background-color: white;\n"
                  "     }")

Rate = ("QLabel{\n"
        "     border: 1px solid;\n"
        "    border-style: outset;\n"
        "    border-width: 1px;\n"
        "    border-radius: 10px;\n"
        "    \n"
        "    background-color: rgb(255, 255, 255);\n"
        "     }")

GoldColor = '#FFD700'

BlueColor = '#1AA7EC'

Button = ("QPushButton {\n"
          "    background-color: rgb(107, 0, 0);\n"
          "    border-style: outset;\n"
          "    border-width: 1px;\n"
          "    border-radius: 10px;\n"
          "    border-color:white;\n"
          "    color: rgb(255, 241, 171);\n"
          "    font: bold 12px;\n"
          "    min-width: 10em;\n"
          "    padding: 6px;\n"
          "}\n"
          "QPushButton:hover {\n"
          "    color: white;\n"
          "}")

DateEdit = ("""
            QDateEdit {
                background-color: white;
            }
            """)

DoubleSpinBox = ("QDoubleSpinBox{\n"
                 "    border-style: outset;\n"
                 "    border-width: 1px;\n"
                 "    border-color:black;\n"
                 "    color: solid black;\n"
                 "    background-color: white;\n"
                 "    }")

Title = ("""
        QLabel {\n
        font-size: 24px;\n
        font-weight: bold;\n
        background-color: white;\n
        }""")

Label = ("""
        QLabel {\n
        background-color: white;\n
        }""")
