*** Settings ***
Library  ../src/ot_miniprojekti_ryhma9/AppLibrary.py

*** Keywords ***
Syote New
    [Arguments]    ${type}    ${viitekoodi}    @{kentat}
    Input    new
    Input    ${type}
    Input    ${viitekoodi}
    FOR    ${kentta}    IN    @{kentat}
        Input    ${kentta}
    END
    Run Application

Syote List
    Input    list
    Run Application

Syote Edit All
    [Arguments]    ${viitekoodi}    @{kentat}
    Input    edit ${viitekoodi}
    FOR    ${kentta}    IN    @{kentat}
        Input    ${kentta}
    END
    Run Application

Syote Edit Single
    [Arguments]    ${viitekoodi}    ${kentta}    ${uusiarvo}
    Input    edit ${viitekoodi} ${kentta}
    Input    ${uusiarvo}
    Run Application