CREATE TABLE IF NOT EXISTS public.config(
    support_url TEXT NOT NULL,
    referral_url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.faq(
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    type VARCHAR(4),
    lang VARCHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.admins(
    tg_id BIGINT NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS public.lucky_jet_signals(
    signals JSONB NOT NULL,
    last_signal_index INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.users(
    tg_id BIGINT PRIMARY KEY,
    dostup BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS public.referrals(
    user_id TEXT PRIMARY KEY,
    deposit BOOLEAN NOT NULL DEFAULT FALSE,
    tg_id BIGINT UNIQUE
);


CREATE TABLE IF NOT EXISTS public.statistic(
    total_referrals BIGINT NOT NULL DEFAULT 0,
    total_deposits BIGINT NOT NULL DEFAULT 0,

    today_referrals BIGINT NOT NULL DEFAULT 0,
    today_deposits BIGINT NOT NULL DEFAULT 0,

    today DATE NOT NULL DEFAULT CURRENT_DATE
);


