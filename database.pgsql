

###########################################################################
#####################  DISCORD USER INFORMATION    ########################
###########################################################################


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
    color integer,
    PRIMARY KEY (user_id)
);


#############################################################################
##################### LEVELS / USER RESOURCES / VALUE  ######################
#############################################################################


CREATE TABLE character (
    user_id bigint NOT NULL,
    role_id integer DEFAULT 0,
    location_id integer DEFAULT 0,
    scp integer DEFAULT 0,
    last_action TIMESTAMP,
    last_move TIMESTAMP,
    PRIMARY KEY (user_id)
);



CREATE TABLE currency (
    user_id bigint NOT NULL,
    coins integer DEFAULT 500,
    coins_earned integer DEFAULT 0,
    last_coin TIMESTAMP,
    xp integer DEFAULT 1,
    xp_earned integer DEFAULT 0,
    last_xp TIMESTAMP,
    PRIMARY KEY (user_id)
);


CREATE TABLE inventory (
    user_id bigint NOT NULL,
    key_level integer DEFAULT 0,
    slot1 VARCHAR(50),
    slot2 VARCHAR(50),
    slot3 VARCHAR(50),
    slot4 VARCHAR(50),
    slot5 VARCHAR(50),
    PRIMARY KEY (user_id)
);



CREATE TABLE sonas (
    user_id BIGINT NOT NULL,
    slot INT NOT NULL,
    verified BOOLEAN DEFAULT false,
    name VARCHAR(25),
    age INT,
    gender VARCHAR(25),
    sexuality VARCHAR(25),
    bio VARCHAR(1000),
    image VARCHAR(1000),
    species VARCHAR(25),
    height VARCHAR(25),
    weight VARCHAR(25),
    archive_id BIGINT,
    fursona_id BIGINT,
    PRIMARY KEY (user_id)
);



CREATE TABLE interactions (
    user_id BIGINT NOT NULL,
    premium BOOLEAN DEFAULT false,
    upvotes_given INT,
    upvotes_received INT,
    pats_given INT,
    pats_received INT,
    hugs_given INT,
    hugs_received INT,
    kisses_given INT,
    kisses_received INT,
    licks_given INT,
    licks_received INT,
    boops_given INT,
    boops_received INT,
    bites_given INT,
    bites_received INT,
    stabs_given INT,
    stabs_received INT,
    flirts_given INT,
    flirts_received INT,
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
    threat_level int DEFAULT 0,
    location_id bigint NOT NULL,
    last_action TIMESTAMP,
    last_move TIMESTAMP,
    contained boolean True,
    var_1 integer DEFAULT 0,
    var_2 boolean DEFAULT False,
    var_3 TIMESTAMP,
    PRIMARY KEY (scp_id)
);


CREATE TABLE channels (
    channel_id bigint NOT NULL,
    zone_desc VARCHAR(50),
    lights boolean DEFAULT True,
    doors INT DEFAULT 1,
    last_event TIMESTAMP,
    PRIMARY KEY (channel_id)
)







SCP GITHUB KEY:
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


SERPENT GUTHUB KEY:
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