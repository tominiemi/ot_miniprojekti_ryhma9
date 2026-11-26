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