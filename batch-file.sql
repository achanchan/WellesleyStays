use wstays_db;

-- USER SAMPLE DATA
insert into user(bnumber, email, name, countrycode, phonenum) 
    values('B20860410','achan@wellesley.edu','Amy Chan','1', '6462401065');

insert into user(bnumber, email, name, countrycode, phonenum)
    values('B20856852', 'dhahm@wellesley.edu', 'Debbie Hahm', '1', '7813541150');

insert into user(bnumber, email, name, countrycode, phonenum) 
    values('B20857037', 'nli2@wellesley.edu', 'Nicole Li', '1', '6503808687');

-- PLACE SAMPLE DATA
insert into place(city, country, street1, street2, state, maxguest, postalcode, bnumber)
    values('Lexington', 'USA', '49 Eldred Street', '', 'MA', 4, '02420', 'B20856852');

insert into place(city, country, street1, street2, state, maxguest, postalcode, bnumber)
    values('Wellesley', 'USA', '106 Central Street', 'Bates 407', 'MA', 1, '02481', 'B20856852');

insert into place(city, country, street1, street2, state, maxguest, postalcode, bnumber)
    values('Wellesley', 'USA', '106 Central Street', 'Munger 234', 'MA', 1, '02481', 'B20860410');

insert into place(city, country, street1, street2, state, maxguest, postalcode, bnumber)
    values('Elmhurst', 'USA', '5101 Jacobus Street', '', 'NY', 1, '11373', 'B20860410');

insert into place(city, country, street1, street2, state, maxguest, postalcode, bnumber)
    values('Wellesley', 'USA', '106 Central Street', 'McAfee 118', 'MA', 1, '02481', 'B20857037');

insert into place(city, country, street1, street2, state, maxguest, postalcode, bnumber)
    values('Los Altos', 'USA', '470 Gabilan Street', 'Apartment 4', 'CA', 1, '94022', 'B20857037');

-- AVAILABILITY SAMPLE DATA
insert into availability(pid, start, end)
    values(1, '2019-11-28', '2019-12-01');

insert into availability(pid, start, end)
    values(1, '2019-12-18', '2019-12-24');

insert into availability(pid, start, end)
    values(2, '2020-01-01', '2020-06-01');

-- REQUEST SAMPLE DATA
insert into request(bnumber, guestnum, city, country, start, end)
    values ('B20860410', 2, 'Montreal', 'CAN', '2019-11-29', '2019-11-30');

insert into request(bnumber, isfilled, guestnum, city, country, start, end)
    values ('B20857037', TRUE, 2, 'Singapore', 'SGP', '2019-12-25', '2020-01-01');

