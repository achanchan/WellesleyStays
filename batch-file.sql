use wstays_db;

-- USER SAMPLE DATA
insert into user(bnumber, email, name, countrycode, phonenum) 
    values('B20860410','achan@wellesley.edu','Amy Chan','1', '6462401065');

insert into user(bnumber, email, name, countrycode, phonenum)
    values('B20856852', 'dhahm@wellesley.edu', 'Debbie Hahm', '1', '7813541150');

insert into user(bnumber, email, name, countrycode, phonenum) 
    values('B20857037', 'nli2@wellesley.edu', 'Nicole Li', '1', '6503808687');

-- PLACE SAMPLE DATA
insert into place(city, country, street1, street2, state, maxguest, postalcode)
    values('Lexington', 'USA', '49 Eldred Street', '', 'MA', 4, '02420');
insert into place(city, country, street1, street2, state, maxguest, postalcode)
    values('Wellesley', 'USA', '106 Central Street', 'Bates 407', 'MA', 1, '02481');

insert into place(city, country, street1, street2, state, maxguest, postalcode)
    values('Wellesley', 'USA', '106 Central Street', 'Munger 234', 'MA', 1, '02481');

insert into place(city, country, street1, street2, state, maxguest, postalcode)
    values('Elmhurst', 'USA', '5101 Jacobus Street', '', 'NY', 1, '11373');

insert into place(city, country, street1, street2, state, maxguest, postalcode)
    values('Wellesley', 'USA', '106 Central Street', 'McAfee 118', 'MA', 1, '02481');

insert into place(city, country, street1, street2, state, maxguest, postalcode)
    values('Los Altos', 'USA', '470 Gabilan Street', 'Apartment 4', 'CA', 1, '94022');


-- PLACEOWNER DATA
insert into placeowner(bnumber, pid)
    values('B20856852', 1);
insert into placeowner(bnumber, pid)
    values('B20856852', 2);
insert into placeowner(bnumber, pid)
    values('B20860410', 3);
insert into placeowner(bnumber, pid)
    values('B20860410', 4);
insert into placeowner(bnumber, pid)
    values('B20857037', 5);
insert into placeowner(bnumber, pid)
    values('B20857037', 6);