

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
###################   LEVELS / USER RESOURCES / VALUE    ####################
#############################################################################


CREATE TABLE main_level (
    user_id bigint NOT NULL,
    level integer DEFAULT 0,
    exp integer DEFAULT 0,
    last_xp timestamp,
    PRIMARY KEY (user_id)
);


CREATE TABLE skill_level (
    user_id bigint NOT NULL,
    combat integer DEFAULT 1,
    c_exp integer DEFAULT 0,
    mining integer DEFAULT 1,
    m_exp integer DEFAULT 0,
    herbalism integer DEFAULT 1,
    h_exp integer DEFAULT 0,
    woodcuting integer DEFAULT 1,
    w_exp integer DEFAULT 0,
    fishing integer DEFAULT 1,
    f_exp integer DEFAULT 0,
    PRIMARY KEY (user_id)
);


CREATE TABLE currency (
    user_id bigint NOT NULL,
    coins integer DEFAULT 500,
    taxed integer DEFAULT 0,
    spent integer DEFAULT 0,
    paid integer DEFAULT 0,
    PRIMARY KEY (user_id)
);


CREATE TABLE stats (
    user_id bigint NOT NULL,
    location varchar(50),
    health integer DEFAULT 100,
    mana integer DEFAULT 20,
    energy integer DEFAULT 10,
    armour varchar(50),
    weapon varchar(50),
    axe varchar(50), 
    rod varchar(50),
    PRIMARY KEY (user_id)
);


CREATE TABLE quests (
    user_id bigint NOT NULL,
    main_quest varchar(50),
    side_quest varchar(50),
    PRIMARY KEY (user_id)
);


###########################################################################
####################  COMBAT / INVENTORY / ITEMS  #########################
###########################################################################


CREATE TABLE ores (
    user_id bigint NOT NULL,
    coal integer DEFAULT 0,
    copper integer DEFAULT 0,
    tin integer DEFAULT 0,
    iron integer DEFAULT 0,
    silver integer DEFAULT 0,
    gold integer DEFAULT 0,
    tungsten integer DEFAULT 0,
    platinum integer DEFAULT 0,
    mithril integer DEFAULT 0,
    phelgem integer DEFAULT 0,
    PRIMARY KEY (user_id)
);


CREATE TABLE plants (
    user_id bigint NOT NULL,
    potato integer DEFAULT 0,
    carrot integer DEFAULT 0,
    wheat integer DEFAULT 0,
    dandelion integer DEFAULT 0,
    watermelon integer DEFAULT 0,
    catnip integer DEFAULT 0,
    marijuana integer DEFAULT 0,
    PRIMARY KEY (user_id)
);



CREATE TABLE wood (
    user_id bigint NOT NULL,
    oak integer DEFAULT 0,
    birch integer DEFAULT 0,
    spruce integer DEFAULT 0,
    mahogany integer DEFAULT 0,
    mystical integer DEFAULT 0,
    anima integer DEFAULT 0,
    PRIMARY KEY (user_id)
);


CREATE TABLE fish (
    user_id bigint NOT NULL,
    salmon integer DEFAULT 0,
    cod integer DEFAULT 0,
    tuna integer DEFAULT 0,
    anglerfish integer DEFAULT 0,
    rainbow integer DEFAULT 0,
    pufferfish integer DEFAULT 0,
    swordfish integer DEFAULT 0,
    greatwhite integer DEFAULT 0,
    goldenfish integer DEFAULT 0,
    whale integer DEFAULT 0,
    PRIMARY KEY (user_id)
);



###########################################################################
#########################     SERVERS / GUILD    ##########################
###########################################################################


CREATE TABLE timers (
    guild_id bigint NOT NULL,
    last_nitro_reward TIMESTAMP,
    PRIMARY KEY (guild_id)
);










SCP GITHUB KEY:

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