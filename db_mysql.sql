create database pL;
use pL;

create table tbHospitais(
idHosp int primary key auto_increment,
nomeHosp varchar(30) not null unique
);

create table tbSetores(
idSetor int primary key auto_increment,
hospSetor varchar(30) not null,
nomeSetor varchar(30) not null
);

create table tbQuartos(
idQuarto int primary key auto_increment,
hospQuarto varchar(30) not null,
setorQuarto varchar(30) not null,
nomeSetor varchar(30) not null
);

create table tbLeitos(
idLeito int primary key auto_increment,
hospLeito varchar(30) not null,
setorLeito varchar(30) not null,
quartoLeito varchar(30) not null,
numLeito varchar(30) not null,
disponLeito varchar(10) not null,
ocupLeito varchar(10) not null,
prontPaciente char(10) unique,
sexoPaciente varchar(3),
contamPaciente varchar(10)
);

create table tbPacientes(
idPaciente int primary key auto_increment,
hospPaciente varchar(30),
setorPaciente varchar(30),
quartoPaciente varchar(30),
leitoPaciente varchar(30),
nomePaciente varchar(30) not null,
prontPaciente varchar(10) not null,
sexoPaciente varchar(10) not null,
contamPaciente varchar(10) not null,
filaEspera varchar(3) not null,
origemPaciente varchar(10),
destinoPaciente varchar(10)
);