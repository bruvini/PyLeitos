create database pyleitos;
use pyleitos;

create table tabelaHospitais (
    idHosp int primary key auto_increment,
    nomeHospital varchar(100) not null
);

create table tabelaSetores (
    idSetor int primary key auto_increment,
    nomeSetor varchar(100) not null,
    idHosp int,
    constraint fk_HospSetor foreign key (idHosp) references tabelaHospitais (idHosp)
);

create table tabelaQuartos (
    idQuarto int primary key auto_increment,
    nomeQuarto varchar(100) not null,
    idSetor int,
    constraint fk_SetorQuarto foreign key (idSetor) references tabelaSetores (idSetor)
);

create table tabelaLeitos (
    idLeito int primary key auto_increment,
    numLeito int not null,
    disponibilidade varchar(3) not null,
    idQuarto int, 
    constraint fk_QuartoLeito foreign key (idQuarto) references tabelaQuartos (idQuarto)
);

create table tabelaPacientes (
    prontPaciente int primary key not null,
    nomePaciente varchar(50),
    sexo varchar(3) not null,
    precaucao varchar(10) not null,
    idLeito int,
    constraint fk_LeitoPaciente foreign key (idLeito) references tabelaLeitos (idLeito)
);

drop table tabelaPaciente;
ALTER TABLE tabelaLeitos MODIFY disponibilidade varchar(8) NOT NULL;
SELECT * FROM tabelaQuartos;