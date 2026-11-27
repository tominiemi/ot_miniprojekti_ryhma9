*** Settings ***
Resource  resource.robot
Library     OperatingSystem

*** Test Cases ***
Syote With Multiple Authors Alphabetically
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.

Syote Edit All Fields
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.
    Syote Edit All   Martin09    Pasi, Antti    ${EMPTY}    ${EMPTY}    ${EMPTY}    ${EMPTY}    
    Syote List
    Output Should Contain    Martin09: Antti, Pasi (2008). Clean Code. Prentice Hall.

Syote Edit Single Field
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.
    Syote Edit Single   Martin09    year    1923
    Output Should Contain    Reference updated
    Syote List
    Output Should Contain    Martin09: Martin, Robert (1923). Clean Code. Prentice Hall.

Syote Delete Reference
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.
    Syote Delete    Martin09
    Output Should Contain    ${EMPTY}

Syote Help
    Syote Help
    Output Should Contain    Available commands: types / new / list / delete / edit / exit / bibtex
    Syote Help    new
    Output Should Contain    Start adding a new citation (new [type])
    Syote Help    bibtex
    Output Should Contain    Creates .bib file from current citations

Syote Output Bibtex File
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.
    Syote Bibtex
    Output Should Contain    BibTeX file created!
    File Should Exist    viitteet.bib
    ${sisalto}=    Get File    viitteet.bib
    Should Contain    ${sisalto}    @book{Martin09,
    Should Contain    ${sisalto}    author = {Robert and Martin}
    Should Contain    ${sisalto}    editor = {Kalle}
    Should Contain    ${sisalto}    title = {Clean Code}
    Should Contain    ${sisalto}    publisher = {Prentice Hall}
    Should Contain    ${sisalto}    year = {2008}
    [Teardown]    Remove File    viitteet.bib
