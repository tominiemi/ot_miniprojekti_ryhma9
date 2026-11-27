[![CI](https://github.com/tominiemi/ot_miniprojekti_ryhma9/actions/workflows/main.yml/badge.svg)](https://github.com/tominiemi/ot_miniprojekti_ryhma9/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/tominiemi/ot_miniprojekti_ryhma9/graph/badge.svg?token=LL2VR9XGNI)](https://codecov.io/gh/tominiemi/ot_miniprojekti_ryhma9)

# ot_miniprojekti_ryhma9
TEKA3003 Ohjelmistotuotanto miniprojektin repositorio ryhmälle 9

## Ryhmän jäsenet
- Maunuksela, Viola
- Niemi, Tomi
- Pekkanen, Miska
- Pirinen, Petri
- Suhonen, Lauri

## Backlog
[Linkki projektin backlogiin](https://jyu-my.sharepoint.com/:x:/g/personal/tsniemi_jyu_fi/IQBSWPW4fW00QbYaRjhJGizsAY0_ycqKrFx-kxDbhEjvBt8?e=04E1Bq)

## Hyväksymiskriteerien robot-testit
[Sprintti 2](https://github.com/tominiemi/ot_miniprojekti_ryhma9/blob/main/tests/syotto.robot)

## Definition of done
- Toteutetun koodin testikattavuuden tulee olla kohtuullinen
- Asiakas pääsee näkemään koko ajan koodin ja testien tilanteen CI-palvelusta
- Koodin ylläpidettävyyden tulee olla mahdollisimman hyvä
    - järkevä nimeäminen
    - järkevä/selkeä ja perusteltu arkkitehtuuri
    - yhtenäinen koodityyli (noudattaa pylintin avulla määriteltyjä sääntöjä)

## Asennus- ja käyttöohje
- Asenna koneellesi [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Lataa ja pura ohjelma
- Asenna riippuvuudet komennolla `uv sync`
- Suorita ohjelma komennolla `uv run python src/ot_miniprojekti_ryhma9/__init__.py`
- Aja ohjelmaa komennoilla `new` ja `list`

### Releasen asennus

- Aja komento ```uv tool install https://github.com/tominiemi/ot_miniprojekti_ryhma9/releases/download/v0.1.0/ot_miniprojekti_ryhma9-0.1.0-py3-none-any.whl```
- käynnistä sovellus komennolla ```ref```

## Lisenssi
Julkaistu MIT-lisenssillä. Katso lisätietoja tiedostosta [`LICENSE`](LICENSE).
