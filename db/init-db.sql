-- Create tables for Muse Observatory application

-- Table for daily fun facts
CREATE TABLE IF NOT EXISTS daily_facts (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    muse VARCHAR(10) NOT NULL,
    day_of_week VARCHAR(10) NOT NULL,
    celestial_body VARCHAR(20) NOT NULL,
    color VARCHAR(20) NOT NULL,
    note VARCHAR(5) NOT NULL,
    social_cause VARCHAR(50) NOT NULL,
    kingdoms_life_subject VARCHAR(100) NOT NULL,
    fun_fact TEXT NOT NULL,
    question_asked TEXT NOT NULL,
    fact_check_link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add index for date lookups
CREATE INDEX IF NOT EXISTS idx_daily_facts_date ON daily_facts(date);

-- Table for user inspirations
CREATE TABLE IF NOT EXISTS inspirations (
    date DATE NOT NULL,
    id VARCHAR(50) PRIMARY KEY,
    day_of_week VARCHAR(10) NOT NULL,
    social_cause VARCHAR(50) NOT NULL,
    muse VARCHAR(10) NOT NULL,
    user_inspiration TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for lookups
CREATE INDEX IF NOT EXISTS idx_inspirations_date ON inspirations(date);
CREATE INDEX IF NOT EXISTS idx_inspirations_social_cause ON inspirations(social_cause);

-- Table for project
CREATE TABLE IF NOT EXISTS projects (
    id VARCHAR(50) PRIMARY KEY,
    project_name VARCHAR(250),
    organisation VARCHAR(250),
    geographical_level VARCHAR(50),
    link_to_organisation VARCHAR(250),
    sk_inspiration VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add indexes for lookups
CREATE INDEX IF NOT EXISTS idx_project_id ON projects(id);
CREATE INDEX IF NOT EXISTS idx_project_sk_inspiration ON projects(sk_inspiration);

-- Final table for cleaned project
CREATE TABLE IF NOT EXISTS cleaned_projects (
    id VARCHAR(50) PRIMARY KEY,
    project_name VARCHAR(250),
    organisation VARCHAR(250),
    geographical_level VARCHAR(50),
    link_to_organisation VARCHAR(250),
    project_source VARCHAR(15) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cleaned_project_id ON projects(id);

-- Track daily OpenAI token usage for quota enforcement
CREATE TABLE IF NOT EXISTS openai_token_usage (
    usage_date DATE PRIMARY KEY,
    tokens_used BIGINT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS openai_usage_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    endpoint VARCHAR(100),
    tokens_used BIGINT,
    model VARCHAR(50),
    status VARCHAR(20),
    error TEXT
);
