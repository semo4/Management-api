CREATE TABLE "workplace" (
    "id" UUID PRIMARY KEY,
    "title" text,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "workplace" ("id");

CREATE TABLE "sections" (
    "id" UUID PRIMARY KEY,
    "name" text,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "sections" ("id");

CREATE TABLE "categories" (
    "id" UUID PRIMARY KEY,
    "title" text,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "categories" ("id");

CREATE TABLE "workers" (
    "id" UUID PRIMARY KEY,
    "name" text,
    "profession" text,
    "daily_amount" float,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "workers" ("id");

CREATE INDEX ON "workers" ("name");

CREATE TABLE "projects" (
    "id" UUID PRIMARY KEY,
    "name" text UNIQUE,
    "section_id" UUID,
    "place" text,
    "description" text,
    "start_date" TIMESTAMPTZ,
    "end_date" TIMESTAMPTZ,
    "project_evaluation" float,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "projects" ("id");

CREATE INDEX ON "projects" ("name");

ALTER TABLE
    "projects"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

CREATE TABLE "partners" (
    "id" UUID PRIMARY KEY,
    "name" text,
    "section_id" UUID,
    "amount" float,
    "pre_amount" float,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "partners" ("id");

CREATE INDEX ON "partners" ("name");

ALTER TABLE
    "partners"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

CREATE TABLE "covenants_cash" (
    "id" UUID PRIMARY KEY,
    "partner_id" UUID,
    "name" text unique,
    "price" float,
    "date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "covenants_cash" ("id");

CREATE INDEX ON "covenants_cash" ("name");

ALTER TABLE
    "covenants_cash"
ADD
    FOREIGN KEY ("partner_id") REFERENCES "partners" ("id");

CREATE TABLE "covenants_devices" (
    "id" UUID PRIMARY KEY,
    "worker_id" UUID,
    "title" text UNIQUE,
    "desc" text,
    "date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "covenants_devices" ("id");

CREATE INDEX ON "covenants_devices" ("title");

ALTER TABLE
    "covenants_devices"
ADD
    FOREIGN KEY ("worker_id") REFERENCES "workers" ("id");

CREATE TABLE "bills" (
    "id" UUID PRIMARY KEY,
    "project_id" UUID,
    "store_name" text,
    "buyer_name" text,
    "item" text,
    "amount" float,
    "bill_number" int,
    "bill_picture" text,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "bills" ("id");

CREATE INDEX ON "bills" ("store_name");

CREATE INDEX ON "bills" ("buyer_name");

CREATE INDEX ON "bills" ("bill_number");

ALTER TABLE
    "bills"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

CREATE TABLE "contractors" (
    "id" UUID PRIMARY KEY,
    "name" text UNIQUE,
    "section_id" UUID,
    "project_id" UUID,
    "amount" float,
    "paid_amount" float,
    "rest_amount" float,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "contractors" ("id");

CREATE INDEX ON "contractors" ("name");

ALTER TABLE
    "contractors"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

ALTER TABLE
    "contractors"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

CREATE TABLE "incomes" (
    "id" UUID PRIMARY KEY,
    "project_id" UUID,
    "section_id" UUID,
    "receiving_person" text,
    "gave_person" text,
    "check_number" int,
    "payment_number" int,
    "amount" float,
    "way_of_receiving" text,
    "description" text,
    "receiving_date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "incomes" ("id");

ALTER TABLE
    "incomes"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "incomes"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

CREATE TABLE "outcomes" (
    "id" UUID PRIMARY KEY,
    "buyer_name" text,
    "amount_payed" float,
    "project_id" UUID,
    "category_id" UUID,
    "reason" text,
    "date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "outcomes" ("id");

ALTER TABLE
    "outcomes"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "outcomes"
ADD
    FOREIGN KEY ("category_id") REFERENCES "categories" ("id");

CREATE TABLE "operations" (
    "id" UUID PRIMARY KEY,
    "section_id" UUID,
    "project_id" UUID,
    "worker_id" UUID,
    "work_place_id" UUID,
    "working_hours" int,
    "payment_amount" float,
    "description" text,
    "operation_add_date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "operations" ("id");

ALTER TABLE
    "operations"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

ALTER TABLE
    "operations"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "operations"
ADD
    FOREIGN KEY ("worker_id") REFERENCES "workers" ("id");

ALTER TABLE
    "operations"
ADD
    FOREIGN KEY ("work_place_id") REFERENCES "workplace" ("id");

CREATE TABLE "salaries" (
    "id" UUID PRIMARY KEY,
    "project_id" UUID,
    "worker_id" UUID,
    "section_id" UUID,
    "salary_type" text,
    "amount" float,
    "date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "salaries" ("id");

ALTER TABLE
    "salaries"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

ALTER TABLE
    "salaries"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "salaries"
ADD
    FOREIGN KEY ("worker_id") REFERENCES "workers" ("id");

CREATE TABLE "withdraw_contractors" (
    "id" UUID PRIMARY KEY,
    "section_id" UUID,
    "project_id" UUID,
    "contractor_id" UUID,
    "amount" float,
    "date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "withdraw_contractors" ("id");

ALTER TABLE
    "withdraw_contractors"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

ALTER TABLE
    "withdraw_contractors"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "withdraw_contractors"
ADD
    FOREIGN KEY ("contractor_id") REFERENCES "contractors" ("id");

CREATE TABLE "withdraw" (
    "id" UUID PRIMARY KEY,
    "section_id" UUID,
    "project_id" UUID,
    "partner_id" UUID,
    "amount" float,
    "date" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "withdraw" ("id");

ALTER TABLE
    "withdraw"
ADD
    FOREIGN KEY ("section_id") REFERENCES "sections" ("id");

ALTER TABLE
    "withdraw"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "withdraw"
ADD
    FOREIGN KEY ("partner_id") REFERENCES "partners" ("id");

CREATE Table "users" (
    "id" UUID PRIMARY KEY,
    "first_name" TEXT,
    "last_name" TEXT,
    "username" TEXT,
    "email" TEXT UNIQUE,
    "password" TEXT,
    "is_super_admin" BOOLEAN,
    "is_admin" BOOLEAN,
    "is_active" BOOLEAN,
    "is_stuff" BOOLEAN,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "users" ("id");

CREATE INDEX ON "users" ("email");

CREATE INDEX ON "users" ("username");