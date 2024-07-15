CREATE TABLE "system_role" (
    "id" UUID PRIMARY KEY,
    "title" text,
    "layer" int AUTO_INCREMENT,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "system_role" ("id");

CREATE TABLE "permissions" (
    "id" UUID PRIMARY KEY,
    "supervise_id" UUID,
    "approval" BOOLEAN,
    "approval_timestamp" TIMESTAMPTZ DEFAULT Now(),
    "system_access" JSON,
    "project_id" UUID,
    "user_id" UUID,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);


CREATE INDEX ON "permissions" ("id");

CREATE INDEX ON "permissions" ("project_id");

CREATE INDEX ON "permissions" ("user_id");

CREATE INDEX ON "permissions" ("supervise_id");

ALTER TABLE
    "permissions"
ADD
    FOREIGN KEY ("project_id") REFERENCES "projects" ("id");

ALTER TABLE
    "permissions"
ADD
    FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE
    "permissions"
ADD
    FOREIGN KEY ("supervise_id") REFERENCES "system_role" ("id");

CREATE TABLE "permission_types" (
    "id" UUID PRIMARY KEY,
    "name" text,
    "symbol" text,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "permission_types" ("id");


CREATE TABLE "system_parts" (
    "id" UUID PRIMARY KEY,
    "name" text,
    "created_at" TIMESTAMPTZ DEFAULT Now(),
    "updated_at" TIMESTAMPTZ DEFAULT Now()
);

CREATE INDEX ON "system_parts" ("id");