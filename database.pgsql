


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
    gold_coin integer,
    good_coin integer,
    evil_coin integer,
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
    last_reward_type varchar(50),
    last_reward_amount integer,
    PRIMARY KEY (channel_id)
);



CREATE TABLE tempmute_timeout (
    user_id bigint NOT NULL,
    unmute_time TIMESTAMP,
    PRIMARY KEY (user_id)
);



CREATE TABLE timers (
    guild_id bigint NOT NULL,
    last_nitro_reward TIMESTAMP,
    PRIMARY KEY (guild_id)
);

