

###########################################################################
#####################  ADMINISTRATIVE INFORMATION    ######################
###########################################################################


CREATE TABLE moderation (
    user_id bigint NOT NULL,
    adult boolean DEFAULT false,
    child boolean DEFAULT false,
    muted boolean DEFAULT false,
    image_banned boolean DEFAULT false,
    PRIMARY KEY (user_id)
);


CREATE TABLE tracking (
    user_id bigint NOT NULL,
    messages integer DEFAULT 0,
    vc_mins integer DEFAULT 0,
    last_bump timestamp,
    color integer,
    PRIMARY KEY (user_id)
);


CREATE TABLE sticky (
    channel_id BIGINT NOT NULL,
    message_id BIGINT,
    PRIMARY KEY (guild_id)
);

CREATE TABLE staff_track (
    user_id bigint NOT NULL,
    mutes INT,
    memes INT,
    nsfws INT,
    purges INT,
    messages INT,
    messages_month INT,
    mail_sonas INT,
    PRIMARY KEY (user_id)
);


CREATE TABLE tempmute_timeout (
    user_id bigint NOT NULL,
    unmute_time TIMESTAMP,
    PRIMARY KEY (user_id)
);


#############################################################################
##################### LEVELS / USER RESOURCES / VALUE  ######################
#############################################################################

CREATE TABLE levels (
    user_id bigint NOT NULL,
    level integer NOT NULL DEFAULT 0,
    exp integer NOT NULL DEFAULT 0,
    last_xp timestamp,
    PRIMARY KEY (user_id)
);

CREATE TABLE daily (
    user_id bigint NOT NULL,
    last_daily TIMESTAMP,
    daily INT NOT NULL DEFAULT 0,
    premium BOOLEAN DEFAULT False,
    PRIMARY KEY (user_id)
);

CREATE TABLE items (
    user_id BIGINT NOT NULL,
    thief_gloves INT,
    party_popper INT,
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
    lot_tickets Integer DEFAULT 0,
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
    color integer,
    likes VARCHAR(25),
    PRIMARY KEY (user_id)
);

CREATE TABLE nsfw_sonas (
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
    color integer,
    likes VARCHAR(25),
    PRIMARY KEY (user_id)
);



###########################################################################
#########################     SERVERS / SPECIAL    ########################
###########################################################################


CREATE TABLE timers (
    guild_id bigint NOT NULL,
    last_nitro_reward TIMESTAMP,
    PRIMARY KEY (guild_id)
);


CREATE TABLE IF NOT EXISTS public.starboard
(
    user_id bigint NOT NULL,
    message_id bigint,
    reference_channel_id bigint NOT NULL,
    reference_message_id bigint NOT NULL,
    jump_link text COLLATE pg_catalog."default" NOT NULL,
    star_count smallint NOT NULL DEFAULT 1,
    attachment_messages bigint[],
    CONSTRAINT starboard_pkey PRIMARY KEY (reference_message_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.starboard
    OWNER to root;

COMMENT ON COLUMN public.starboard.user_id
    IS 'Discord user ID';

COMMENT ON COLUMN public.starboard.message_id
    IS 'The ID of the message sent in the starboard channel';

COMMENT ON COLUMN public.starboard.reference_channel_id
    IS 'Channel ID where the original message was sent';

COMMENT ON COLUMN public.starboard.reference_message_id
    IS 'Original message''s Discord ID';

COMMENT ON COLUMN public.starboard.attachment_messages
    IS 'List of Discord message IDs';




SCP GITHUB KEY:
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


SERPENT GUTHUB KEY:
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

SERPENTS GARDEN DISCORD BOT #1 KEY:
NzY0NzY5NDgxNDEwMjE1OTY3.GF6dLc.ojUUNd9gAQSPzgyd0Dn7wL159EIaJr7eHo4KCc