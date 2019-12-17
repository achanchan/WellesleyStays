use achan_db;

drop table if exists availability;
drop table if exists pic;
drop table if exists place;
drop table if exists request;
drop table if exists user;


CREATE TABLE user (
    bnumber char(9),
    email varchar(30),
    name varchar(30),
    countrycode varchar(3),
    phonenum char(10),
    primary key (bnumber)
) ENGINE = InnoDB;

CREATE TABLE place (
    pid int auto_increment,
    bnumber char(9),
    city varchar(20),
    country varchar(20),
    street1 varchar(40),
    street2 varchar(40),
    state varchar(20),
    maxguest int,
    postalcode varchar(10),
    primary key (pid),
    foreign key (bnumber) references user(bnumber) 
        on delete cascade
        on update cascade
) ENGINE = InnoDB;

CREATE TABLE availability (
    aid int auto_increment,
    pid int,
    start date,
    end date,
    primary key (aid, start),
    foreign key (pid) references place(pid)
        on delete cascade
        on update cascade
) ENGINE = InnoDB;

CREATE TABLE request (
    rid int auto_increment,
    bnumber char(9),
    isfilled boolean not null default FALSE,
    guestnum int,
    city varchar(20),
    country varchar(20),
    start date,
    end date,
    primary key (rid),
    foreign key (bnumber) references user(bnumber)
        on delete cascade
        on update cascade
) ENGINE = InnoDB;

CREATE TABLE pic (
    pid int,
    filename varchar(50),
    primary key (pid),
    foreign key (pid) references place(pid)
        on delete cascade
        on update cascade
) ENGINE = InnoDB;