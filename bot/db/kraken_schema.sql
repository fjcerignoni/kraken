DROP TABLE IF EXISTS servers;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS permited;
DROP TABLE IF EXISTS albion_guilds;

CREATE TABLE servers (
    server_id INTEGER PRIMARY KEY NOT NULL,
    server_name TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    owner_name TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
);

CREATE TABLE roles (
role_id INTEGER PRIMARY KEY NOT NULL,
role_name TEXT NOT NULL);

CREATE TABLE permited (
    member_id INTEGER NOT NULL,
    member_name TEXT NOT NULL,
    server_id INTEGER NOT NULL,
    role_id INTEGER DEFAULT 1,
    PRIMARY KEY (member_id, server_id),
    FOREIGN KEY(server_id) REFERENCES servers(server_id),
    FOREIGN KEY(role_id) REFERENCES roles(role_id)
);

CREATE TABLE albion_guilds (
    guild_id TEXT PRIMARY KEY NOT NULL,
    guild_name TEXT NOT NULL,
    server_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(server_id) REFERENCES servers(server_id)
);

INSERT INTO roles (role_id, role_name)
VALUES (1, 'user'), (2, 'moderator'), (3, 'admin');

-- CREATE TABLE taxes (
-- tax_id INTEGER PRIMARY KEY NOT NULL,
-- -- player_id TEXT NOT NULL,
-- member_id INT NOT NULL,
-- silver INTEGER NOT NULL,
-- ref DATE NOT NULL,
-- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- updated_at DATETIME,
-- FOREIGN KEY(member_id) REFERENCES players(player_id));

-- CREATE TABLE members (
-- member_id INTEGER PRIMARY KEY NOT NULL,
-- -- member_name TEXT NOT NULL,
-- -- member_nick TEXT,
-- server_id INTEGER NOT NULL,
-- role_id INTEGER NOT NULL DEFAULT 1,
-- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- updated_at DATETIME,
-- FOREIGN KEY(server_id) REFERENCES servers(server_id),
-- FOREIGN KEY(role_id) REFERENCES roles(role_id));

-- CREATE TABLE guilds (
-- guild_id TEXT PRIMARY KEY NOT NULL,
-- guild_name TEXT NOT NULL,
-- server_id INTEGER NOT NULL,
-- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY(server_id) REFERENCES servers(server_id));

-- CREATE TABLE players (
-- player_id TEXT PRIMARY KEY NOT NULL,
-- player_name TEXT NOT NULL,
-- guild_id TEXT NOT NULL,
-- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY(guild_id) REFERENCES guilds(guild_id));


-- CREATE TABLE members_players (
-- member_id INTEGER PRIMARY KEY NOT NULL,
-- player_id TEXT NOT NULL,
-- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
-- FOREIGN KEY(member_id) REFERENCES members(member_id),
-- FOREIGN KEY(player_id) REFERENCES players(player_id));