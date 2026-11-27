*** Settings ***
Resource  resource.robot

*** Test Cases ***
Syote With Multiple Authors Alphabetically
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.

Syote Edit
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

Syote Delete
    Syote New    book    Martin09    Robert, Martin    Kalle    Clean Code    Prentice Hall    2008
    Syote List
    Output Should Contain    Martin09: Martin, Robert (2008). Clean Code. Prentice Hall.
    Syote Delete    Martin09
    Output Should Contain    ${EMPTY}

Syote Help
    Syote Help
    Output Should Contain    Available commands: types / new / list / delete / edit / help / exit
    Syote Help    new
    Output Should Contain    Start adding a new citation (new [type])
    Syote Help    bibtex
    Output Should Contain    Creates .bib file from current citations
