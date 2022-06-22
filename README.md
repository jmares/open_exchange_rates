# Open Exchange Rates

The purpose of this project is to have some fun with the data from **Open Exchange Rates** using a free account.

Site: [Open Exchange Rates](https://openexchangerates.org/)

The data you can download with a free account is limited compared to the paying accounts, but more than enough for a hobby project.

## Project

### Phase 1

- create database with two tables: one for the currencies and another for the rates (base = USD)
- download data and insert into database
- take into account new currencies
- basic logging
- basic exception handling
- documentation

### Phase 2

- add table for the average daily rate of currencies (base EUR)
- create static webpage with table for a select few currencies

### Phase 3

- static site with charts and table per currency

### Phase 4

- add javascript to selecy currency

### Phase 5

- dynamic site with Django or Flask or ...


## Versions

### 2022-06-22

Basic working version:

- the data (currencies and latest rates) are downloaded and added to an SQLite database
- exception handling
- logging