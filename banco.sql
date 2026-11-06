USE `projeto-sound-room`;

-- perfis vem antes de usuarios, porque usuarios aponta para ele (chave estrangeira).
CREATE TABLE IF NOT EXISTS perfis (
    id_perfil     BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL UNIQUE,
    descricao     VARCHAR(255),
    criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em   DATETIME NULL                         -- soft-delete (Capítulo 13.1)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario      BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(255) NOT NULL,
    email           VARCHAR(255) NOT NULL UNIQUE,
    senha           VARCHAR(255) NOT NULL,      -- guarda o HASH, nunca a senha
    celular         VARCHAR(20),
    data_nascimento DATE,
    cpf             VARCHAR(14) UNIQUE,         -- gravado como 000.000.000-00
    perfil_id       BIGINT UNSIGNED NOT NULL,
    cep             VARCHAR(9),
    endereco        VARCHAR(255),
    numero          VARCHAR(20),
    complemento     VARCHAR(100),
    cidade          VARCHAR(100),
    estado          CHAR(2),
    criado_em       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em     DATETIME NULL,                      -- soft-delete (Capítulo 13.1)
    CONSTRAINT fk_usuarios_perfis
        FOREIGN KEY (perfil_id) REFERENCES perfis (id_perfil)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

