drop table if exists user;
drop table if exists place;
drop table if exists placeowner;
drop table if exists availability;

CREATE TABLE user (
    bnumber char(9),
    email varchar(30),
    name varchar(30),
    countrycode varchar(3),
    phonenum char(10),
    primary key (bnumber)
);

CREATE TABLE place {
    pid int auto_increment,
    city varchar(20),
    country varchar(20),
    street1 varchar(40),
    street2 varchar(40),
    state varchar(20),
    maxguest int,
    postalcode varchar(10),
    primary key (pid)
};

CREATE TABLE placeowner {
    bnumber char(9),
    pid int,
    primary key (bnumber, pid)
};

CREATE TABLE availability {
    pid int,
    start date,
    end date,
    primary key (pid, start)
}

CREATE TABLE request {
    rid int auto_increment,
    boolean isfilled,
    int guestnum,
    city varchar(20),
    country varchar(20),
    start date,
    end date,
    primary key (rid)
}

CREATE TABLE userrequest {
    bnumber char(9),
    rid int,
    primary key (bnumber, rid)
}