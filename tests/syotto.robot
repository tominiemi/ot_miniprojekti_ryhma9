*** Settings ***
Resource  resource.robot

*** Test Cases ***
Syote With Multiple Authors
    Syote New    book    Martin09    Martin, Robert    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.