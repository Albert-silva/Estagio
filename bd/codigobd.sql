CREATE SCHEMA IF NOT EXISTS `compsis`;

CREATE TABLE `compsis`.sis_usuario (
	usuarioid INT auto_increment NOT NULL,
	usuario varchar(50) NOT NULL,
	nome varchar(100) NOT NULL,
	senha varchar(100) NOT NULL,
	datacriacao DATETIME NOT NULL,
	dataalteracao DATETIME NULL,
	CONSTRAINT sis_usuario_PK PRIMARY KEY (usuarioid)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;

CREATE TABLE `compsis`.sis_grupo (
	grupoid INT auto_increment NOT NULL,
	nome varchar(100) NOT NULL,
	datacriacao DATETIME NOT NULL,
	dataalteracao DATETIME NULL,
	CONSTRAINT sis_grupo_PK PRIMARY KEY (grupoid)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;

CREATE TABLE `compsis`.sis_grupo_usuario (
	grupoid INT NOT NULL,
	usuarioid INT NOT NULL,
	CONSTRAINT sis_grupo_usuario_FK FOREIGN KEY (usuarioid) REFERENCES compsis.sis_usuario(usuarioid),
	CONSTRAINT sis_grupo_usuario_FK_1 FOREIGN KEY (grupoid) REFERENCES compsis.sis_grupo(grupoid)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4;
