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

create table tabelaLeitos (
idLeitos int primary key auto_increment,
nomeLeito varchar(100) not null,
sexoLeito varchar (3) not null,
disponibilidade varchar(10) not null,
ocupacao varchar(10) not null,
precaucao varchar (10) not null,
nomePaciente varchar(50),
prontPaciente int,
idSetor int,
constraint fk_SetorLeito foreign key (idSetor) references tabelaSetores (idSetor)
);

drop table tabelaLeitos;

create table tabelaPaciente(
prontPaciente int primary key not null,
nomePaciente varchar(50),
sexo varchar(3) not null,
precaucao varchar (10) not null,
idLeito int,
constraint fk_LeitoPaciente foreign key (idLeito) references tabelaLeitos (idLeitos)
);