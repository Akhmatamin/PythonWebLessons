CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY NOT NULL,
    title TEXT,
    created_at DATETIME,
    is_completed BOOLEAN,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)  -- to define a relationship with the users table
);

