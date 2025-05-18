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
    animal_subject VARCHAR(100) NOT NULL,
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
