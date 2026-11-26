*** Settings ***
Resource  resource.robot

*** Test Cases ***
Syote With Multiple Authors
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.

Syote Edit
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.
    Syote Edit   Martin09    Pasi, Antti    ${empty}    ${empty}    ${empty}    ${empty}    
    Syote List
    Output Should Contain    Martin09: Antti, Pasi (2008). Clean Code. Prentice Hall.

#Edit yksittäinen asia
#Syote delete
#List aakkosjärjestys
#Help komento testi