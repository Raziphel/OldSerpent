
CREATE TABLE levels (
    user_id bigint NOT NULL,
    level integer DEFAULT 0,
    exp integer DEFAULT 0,
    last_xp timestamp,
    prestige integer DEFAULT 0,
    PRIMARY KEY (user_id)
);



CREATE TABLE settings (
    user_id bigint NOT NULL,
    vc_msgs integer,
    vc_lvls integer,
    color integer,
    PRIMARY KEY (user_id)
);



CREATE TABLE currency (
    user_id bigint NOT NULL,
    emerald integer,
    diamond integer,
    ruby integer,
    sapphire integer,
    amethyst integer,
    crimson integer,
    PRIMARY KEY (user_id)
);



CREATE TABLE moderation (
    user_id bigint NOT NULL,
    adult boolean DEFAULT false,
    child boolean DEFAULT false,
    marks integer DEFAULT 0,
    PRIMARY KEY (user_id)
);



CREATE TABLE tracking (
    user_id bigint NOT NULL,
    messages integer DEFAULT 0,
    vc_mins integer DEFAULT 0,
    last_image timestamp,
    PRIMARY KEY (user_id)
);



CREATE TABLE mines (
    channel_id bigint NOT NULL,
    last_msg bigint,
    last_user bigint,
    last_reward_type varchar(25),
    last_reward_amount integer,
    PRIMARY KEY (channel_id)
);



CREATE TABLE abilities (
    user_id bigint NOT NULL,
    ability1 varchar(25),
    cooldown1 timestamp,
    ability2 varchar(25),
    cooldown2 timestamp,
    ability3 varchar(25),
    cooldown3 timestamp,
    PRIMARY KEY (user_id)
);





CREATE TABLE slots (
    slot_id bigint NOT NULL,
    user_id integer,
    bet_amount integer,
    earnings integer,
    PRIMARY KEY (slot_id)
);




CREATE TABLE achievements (
    user_id bigint NOT NULL,
    completed integer DEFAULT 0,
    a1 boolean DEFAULT FALSE,
    a2 boolean DEFAULT FALSE,
    a3 boolean DEFAULT FALSE,
    a4 boolean DEFAULT FALSE,
    a5 boolean DEFAULT FALSE,
    a6 boolean DEFAULT FALSE,
    a7 boolean DEFAULT FALSE,
    a8 boolean DEFAULT FALSE,
    a9 boolean DEFAULT FALSE,
    b1 boolean DEFAULT FALSE,
    b2 boolean DEFAULT FALSE,
    b3 boolean DEFAULT FALSE,
    b4 boolean DEFAULT FALSE,
    b5 boolean DEFAULT FALSE,
    b6 boolean DEFAULT FALSE,
    b7 boolean DEFAULT FALSE,
    b8 boolean DEFAULT FALSE,
    b9 boolean DEFAULT FALSE,
    c1 boolean DEFAULT FALSE,
    c2 boolean DEFAULT FALSE,
    c3 boolean DEFAULT FALSE,
    PRIMARY KEY (user_id)
);

