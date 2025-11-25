CREATE TABLE Patient (
    id VARCHAR(36) PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(255),
    daily_caloric_intake INT,
    physical_activity_level VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Disease (
    id VARCHAR(36) PRIMARY KEY,
    patient_id VARCHAR(36) NOT NULL,
    type VARCHAR(255) NOT NULL,
    severity VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patient(id) ON DELETE CASCADE
);

CREATE TABLE BMI (
    id VARCHAR(36) PRIMARY KEY,
    patient_id VARCHAR(36) NOT NULL,
    weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patient(id) ON DELETE CASCADE
);

CREATE TABLE Food (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Nutritional_values (
    id VARCHAR(36) PRIMARY KEY,
    food_id VARCHAR(36) NOT NULL,
    calories FLOAT,
    protein FLOAT,
    carbohydrates FLOAT,
    fat FLOAT,
    fiber FLOAT,
    sugars FLOAT,
    sodium FLOAT,
    cholesterol FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
);

CREATE TABLE Meal (
    id VARCHAR(36) PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    water_intake FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Consumption (
    id VARCHAR(36) PRIMARY KEY,
    meal_id VARCHAR(36) NOT NULL,
    food_id VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (meal_id) REFERENCES Meal(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
);