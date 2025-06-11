-- Users of the system
CREATE TABLE users (
    id INTEGER,
    username TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('admin', 'user')) DEFAULT 'user',
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL UNIQUE,
    created_at NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id)
);

-- Available restaurant tables
CREATE TABLE tables (
    id INTEGER,
    name TEXT NOT NULL CHECK(name IN ('table_1', 'table_2', 'table_3', 'table_4')),
    capacity INTEGER NOT NULL CHECK(capacity = 4),
    PRIMARY KEY(id)
);

-- Available time slots for reservations
CREATE TABLE time_slots (
    id INTEGER,
    label TEXT NOT NULL,
    start_time TEXT NOT NULL CHECK(start_time IN ('12:00:00', '13:30:00', '20:00:00', '21:30:00')),
    end_time TEXT NOT NULL CHECK(end_time IN ('13:30:00', '15:00:00', '21:30:00', '23:00:00')),
    PRIMARY KEY(id)
);

-- Reservations made by users
CREATE TABLE reservations (
    id INTEGER,
    user_id INTEGER,
    date NUMERIC NOT NULL,
    slot_id INTEGER,
    party_size INTEGER NOT NULL CHECK(party_size BETWEEN 1 AND 16),
    created_at NUMERIC NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK(status IN ('confirmed', 'cancelled')),
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(slot_id) REFERENCES time_slots(id)
);

-- Mapping many-to-many reservations to tables assigned
CREATE TABLE reservation_tables (
    reservation_id INTEGER,
    table_id INTEGER,
    PRIMARY KEY(reservation_id, table_id),
    FOREIGN KEY(reservation_id) REFERENCES reservations(id) ON DELETE CASCADE,
    FOREIGN KEY(table_id) REFERENCES tables(id) ON DELETE CASCADE
);

--Initial data inserts
INSERT INTO users (username, role, first_name, last_name, phone_number, email, hash)
VALUES
('admin1', 'admin', 'Daniel', 'López', '+34 666666666', 'gobernador2003@gmail.com', 'scrypt:32768:8:1$JuJt6ANrB87HDPQ5$cfccebf538da190b522b6780fa7855cbfd62eb9613846c13519b322a70a38a39b539b24a5bcf73c93eefdd2da366905630166d6cdde4d2712bdc789991319609');

INSERT INTO tables (name, capacity)
VALUES
('table_1', 4),
('table_2', 4),
('table_3', 4),
('table_4', 4);

INSERT INTO time_slots (label, start_time, end_time)
VALUES
('slot_1', '12:00:00', '13:30:00'),
('slot_2', '13:30:00', '15:00:00'),
('slot_3', '20:00:00', '21:30:00'),
('slot_4', '21:30:00', '23:00:00');