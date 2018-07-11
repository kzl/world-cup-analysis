drop table WorldCups;
create table WorldCups (
	ChampionshipYear int2 unsigned not null,
    Country varchar(256) not null,
    Winner varchar(256) not null,
    SecondPlace varchar(256) not null,
    ThirdPlace varchar(256) not null,
    FourthPlace varchar(256) not null,
    GoalsScored int2 unsigned not null,
    QualifiedTeams int1 unsigned not null,
    MatchesPlayed int2 unsigned not null,
    Attendance int unsigned not null,
    primary key (ChampionshipYear)
);

create index country_index on WorldCups(Country);
create index winner_index on WorldCups(Winner);
create index goals_index on WorldCups(GoalsScored);
create index attendance_index on WorldCups(Attendance);

load data infile 'C:/WorldCups.csv'
into table WorldCups
columns terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 rows;

drop table WorldCupPlayers;
create table WorldCupPlayers (
	RoundID int unsigned not null,
    MatchID int8 unsigned not null,
    TeamInitials varchar(3) not null,
    CoachName varchar(256) not null,
    LineUp varchar(1) not null,
    ShirtNumber int1 unsigned not null,
    PlayerName varchar(256) not null,
    PlayerPosition varchar(256),
    PlayerEvent varchar(256),
    primary key (MatchID, TeamInitials, ShirtNumber, PlayerName)
);

create index round_index on WorldCupPlayers(RoundID);
create index match_index on WorldCupPlayers(MatchID);
create index team_index on WorldCupPlayers(TeamInitials);

load data infile 'C:/WorldCupPlayers.csv'
ignore into table WorldCupPlayers
columns terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 rows;

drop table WorldCupMatches;
create table WorldCupMatches (
	ChampionshipYear int2 unsigned not null,
    MatchDateTime datetime not null,
    Stage varchar(256) not null,
    Stadium varchar(256) not null,
    City varchar(256) not null,
	HomeTeam varchar(256) not null,
    HomeTeamGoals int1 unsigned not null,
    AwayTeamGoals int1 unsigned not null,
    AwayTeam varchar(256) not null,
    WinConditions varchar(256),
    Attendance int unsigned not null,
    HalftimeHomeTeamGoals int1 unsigned not null,
    HalftimeAwayTeamGoals int1 unsigned not null,
    Referee varchar(256) not null,
    Assistant1 varchar(256) not null,
    Assistant2 varchar(256) not null,
    RoundID int unsigned not null,
    MatchID int8 unsigned not null,
	HomeTeamInitials varchar(3) not null,
    AwayTeamInitials varchar(3) not null,
    primary key (MatchID)
);

create index year_index on WorldCupMatches(ChampionshipYear);
create index datetime_index on WorldCupMatches(MatchDateTime);
create index stage_index on WorldCupMatches(Stage);
create index location_index on WorldCupMatches(Stadium, City);
create index teams_index on WorldCupMatches(HomeTeam, AwayTeam);
create index goals_index on WorldCupMatches(HomeTeamGoals, AwayTeamGoals);

load data infile 'C:/WorldCupMatchesFixed.csv'
ignore into table WorldCupMatches
columns terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 rows
(ChampionshipYear, @MatchDateTime, Stage, Stadium, City, HomeTeam, HomeTeamGoals, AwayTeamGoals, AwayTeam, WinConditions, Attendance, 
 HalftimeHomeTeamGoals, HalftimeAwayTeamGoals, Referee, Assistant1, Assistant2, RoundID, MatchID, HomeTeamInitials, AwayTeamInitials)
 set MatchDateTime = str_to_date(@MatchDateTime, '%d %b %Y - %H:%i ');
 