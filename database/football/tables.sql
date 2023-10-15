create table if not exists team (
    id serial primary key,
    name varchar(256) unique not null,
    town varchar(256) not null,
    website varchar(256) null,
    createddttm timestamp with time zone default current_timestamp
);

create table if not exists fixture (
    id serial primary key,
    hometeam_fk integer references team(id) not null,
    awayteam_fk integer references team(id) not null,
    fixturedttm timestamp,
    createddttm timestamp with time zone default current_timestamp
);

create table if not exists competition (
    id serial primary key,
    name varchar(256) unique not null,
    country varchar(256) not null,
    createddttm timestamp with time zone default current_timestamp
);

create table if not exists season (
    id serial primary key,
    name varchar(256) unique not null,
    competition_fk integer references competition(id) not null,
    firstfixturedt date not null,
    lastfixturedt date not null,
    createddttm timestamp with time zone default current_timestamp
);

create table if not exists division (
    id serial primary key,
    name varchar(256) unique not null,
    season_fk integer references season(id) not null,
    rank integer not null,
    createddttm timestamp with time zone default current_timestamp
);

create table if not exists team_division (
    team_fk integer references team(id) not null,
    division_fk integer references division(id) not null,
    fromdt date not null,
    todt date not null,
    createddttm timestamp with time zone default current_timestamp
 );

grant all privileges on all tables in schema public to guest;
grant all privileges on all sequences in schema public to guest;
grant all privileges on all functions in schema public to guest;