

###########################################################################
#####################  DISCORD USER INFORMATION    ########################
###########################################################################


CREATE TABLE settings (
    user_id bigint NOT NULL,
    vc_msgs integer,
    vc_lvls integer,
    color integer,
    PRIMARY KEY (user_id)
);


CREATE TABLE moderation (
    user_id bigint NOT NULL,
    adult boolean DEFAULT false,
    child boolean DEFAULT false,
    PRIMARY KEY (user_id)
);


CREATE TABLE tracking (
    user_id bigint NOT NULL,
    messages integer DEFAULT 0,
    vc_mins integer DEFAULT 0,
    last_image timestamp,
    PRIMARY KEY (user_id)
);


#############################################################################
##################### LEVELS / USER RESOURCES / VALUE  ######################
#############################################################################


CREATE TABLE leveling (
    user_id bigint NOT NULL,
    level integer DEFAULT 0,
    exp integer DEFAULT 0,
    last_xp timestamp,
    PRIMARY KEY (user_id)
);


CREATE TABLE character (
    user_id bigint NOT NULL,
    key_card integer DEFAULT 0,
    role_id integer DEFAULT 0,
    scp integer DEFAULT 0,
    PRIMARY KEY (user_id)
);



CREATE TABLE currency (
    user_id bigint NOT NULL,
    coins integer DEFAULT 500,
    taxed integer DEFAULT 0,
    spent integer DEFAULT 0,
    earned integer DEFAULT 0,
    PRIMARY KEY (user_id)
);



###########################################################################
#########################     SERVERS / SPECIAL    ########################
###########################################################################


CREATE TABLE timers (
    guild_id bigint NOT NULL,
    last_nitro_reward TIMESTAMP,
    last_daily TIMESTAMP,
    last_weekly TIMESTAMP,
    last_monthly TIMESTAMP,
    PRIMARY KEY (guild_id)
);


CREATE TABLE scps (
    scp_id bigint NOT NULL,
    zone_id bigint NOT NULL,
    last_action TIMESTAMP,
    last_move TIMESTAMP,
    var_1 integer DEFAULT 0,
    var_2 boolean DEFAULT false,
    var_3 TIMESTAMP,
    PRIMARY KEY (scp_id)
);









SCP GITHUB KEY:

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

SERPENT GUTHUB KEY:

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