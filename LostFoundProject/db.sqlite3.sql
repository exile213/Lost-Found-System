BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "AccountsApp_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"first_name"	varchar(150) NOT NULL,
	"last_name"	varchar(150) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"phone_number"	varchar(15),
	"student_id"	varchar(20),
	"department"	varchar(100),
	"role"	varchar(10) NOT NULL,
	"profile_picture"	varchar(100),
	"date_joined"	datetime NOT NULL,
	"email"	varchar(254) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "AccountsApp_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	bigint NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "AccountsApp_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "AccountsApp_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	bigint NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "AccountsApp_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ClaimsApp_claimrequest" (
	"id"	integer NOT NULL,
	"reason"	text NOT NULL,
	"additional_proof"	varchar(100),
	"is_verified"	bool NOT NULL,
	"submitted_at"	datetime NOT NULL,
	"verified_at"	datetime,
	"claimer_id"	bigint NOT NULL,
	"item_id"	bigint NOT NULL,
	"verified_by_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("claimer_id") REFERENCES "AccountsApp_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("item_id") REFERENCES "ReportsApp_itemreport"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("verified_by_id") REFERENCES "AccountsApp_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "ReportsApp_itemreport" (
	"id"	integer NOT NULL,
	"title"	varchar(100) NOT NULL,
	"description"	text NOT NULL,
	"category"	INTEGER,
	"location"	INTEGER,
	"date_lost_or_found"	date NOT NULL,
	"time_lost_or_found"	time,
	"status"	varchar(10) NOT NULL,
	"image"	varchar(100),
	"timestamp_reported"	datetime NOT NULL,
	"reporter_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("reporter_id") REFERENCES "AccountsApp_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	bigint NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "AccountsApp_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_plotly_dash_dashapp" (
	"id"	integer NOT NULL,
	"instance_name"	varchar(100) NOT NULL UNIQUE,
	"slug"	varchar(110) NOT NULL UNIQUE,
	"base_state"	text NOT NULL,
	"creation"	datetime NOT NULL,
	"update"	datetime NOT NULL,
	"save_on_change"	bool NOT NULL,
	"stateless_app_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("stateless_app_id") REFERENCES "django_plotly_dash_statelessapp"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_plotly_dash_statelessapp" (
	"id"	integer NOT NULL,
	"app_name"	varchar(100) NOT NULL UNIQUE,
	"slug"	varchar(110) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
INSERT INTO "AccountsApp_user" VALUES (1,'pbkdf2_sha256$1000000$1eMCOhRUvFCziEgx7quYOX$VTJcsnvKGfjwc3ySen1YY3MprdDYbaOuKwrGmHKw6xk=','2025-06-15 13:24:23.833733',1,'admin','','',1,1,NULL,NULL,NULL,'student','','2025-06-11 22:50:28.707626','admin@gmail.com');
INSERT INTO "AccountsApp_user" VALUES (3,'pbkdf2_sha256$1000000$ZxYIWcknMEJbsW99st3YWM$9543xsWAQqtvYBb8Fifh0N4N/cqElJXJJMTDpya4nhU=','2025-06-14 12:26:03.693981',0,'trial','try name','try name',0,1,'0996969439','20220548','Computer Science','student','profile_pics/yotsuba.png','2025-06-12 00:13:45.946994','try@gmail.com');
INSERT INTO "AccountsApp_user" VALUES (4,'pbkdf2_sha256$1000000$jzTN7qL3v8dlYc49HtuQYJ$C8mLyXcGEUa6BOXPjYm3ss5hNU6+89uPEB/wfTOwT3Q=','2025-06-14 19:42:46.297123',0,'emil123','Emil Joaquin','Diaz',0,1,'09695282766','20220583','College Of Computer Science','staff','','2025-06-13 01:41:36.897803','diaz@gmail.com');
INSERT INTO "AccountsApp_user" VALUES (5,'pbkdf2_sha256$1000000$JsXPIUxTRIVlK2KCLiu9XN$/Dzc4FDWC1TX7Fvy+jZGpc8VBr82Z9wZVjuT0OYI0nI=','2025-06-14 08:33:35.137389',0,'trial234','try','student 2',0,1,'09540853945','2022052','College Of Computer Science','student','','2025-06-14 08:23:41.299959','try2@gmail.com');
INSERT INTO "ClaimsApp_claimrequest" VALUES (1,'this belongs to emil','',1,'2025-06-14 08:33:50.150407','2025-06-14 08:34:26.608490',5,6,4);
INSERT INTO "ReportsApp_itemreport" VALUES (1,'LAPTOP','BLACK LAPTOP',NULL,NULL,'2025-06-11',NULL,'lost','','2025-06-12 06:07:12.212360',3);
INSERT INTO "ReportsApp_itemreport" VALUES (2,'LAPTOP','BLACK LAPTOP',NULL,NULL,'2025-06-12',NULL,'lost','','2025-06-12 06:08:57.320262',3);
INSERT INTO "ReportsApp_itemreport" VALUES (3,'LAPTOP','BLACK LAPTOP',NULL,NULL,'2025-06-12',NULL,'lost','','2025-06-12 06:09:10.369771',3);
INSERT INTO "ReportsApp_itemreport" VALUES (4,'laptop','black laptop',NULL,NULL,'2025-06-12',NULL,'lost','','2025-06-12 06:09:52.095387',3);
INSERT INTO "ReportsApp_itemreport" VALUES (5,'Laptop','black laptop',NULL,NULL,'2025-06-12',NULL,'lost','item_images/V_for_vendettax.jpg','2025-06-12 07:32:12.060058',3);
INSERT INTO "ReportsApp_itemreport" VALUES (6,'Black Laptop','black laptop',NULL,NULL,'2025-06-12',NULL,'claimed','item_images/batman.jpg','2025-06-12 08:05:48.582849',3);
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (14,4,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (15,4,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (16,4,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (17,5,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (18,5,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (19,5,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (20,5,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (21,6,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (22,6,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (23,6,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (24,6,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (25,7,'add_itemreport','Can add item report');
INSERT INTO "auth_permission" VALUES (26,7,'change_itemreport','Can change item report');
INSERT INTO "auth_permission" VALUES (27,7,'delete_itemreport','Can delete item report');
INSERT INTO "auth_permission" VALUES (28,7,'view_itemreport','Can view item report');
INSERT INTO "auth_permission" VALUES (29,8,'add_claimrequest','Can add claim request');
INSERT INTO "auth_permission" VALUES (30,8,'change_claimrequest','Can change claim request');
INSERT INTO "auth_permission" VALUES (31,8,'delete_claimrequest','Can delete claim request');
INSERT INTO "auth_permission" VALUES (32,8,'view_claimrequest','Can view claim request');
INSERT INTO "auth_permission" VALUES (33,9,'add_dashapp','Can add dash app');
INSERT INTO "auth_permission" VALUES (34,9,'change_dashapp','Can change dash app');
INSERT INTO "auth_permission" VALUES (35,9,'delete_dashapp','Can delete dash app');
INSERT INTO "auth_permission" VALUES (36,9,'view_dashapp','Can view dash app');
INSERT INTO "auth_permission" VALUES (37,10,'add_statelessapp','Can add stateless app');
INSERT INTO "auth_permission" VALUES (38,10,'change_statelessapp','Can change stateless app');
INSERT INTO "auth_permission" VALUES (39,10,'delete_statelessapp','Can delete stateless app');
INSERT INTO "auth_permission" VALUES (40,10,'view_statelessapp','Can view stateless app');
INSERT INTO "django_admin_log" VALUES (1,'1','admin (student)',2,'[]',6,1,'2025-06-11 23:01:24.080052');
INSERT INTO "django_admin_log" VALUES (2,'2','emil (student)',1,'[{"added": {}}]',6,1,'2025-06-11 23:02:51.460619');
INSERT INTO "django_admin_log" VALUES (3,'2','emil (staff)',2,'[{"changed": {"fields": ["Role"]}}]',6,1,'2025-06-13 01:00:33.218866');
INSERT INTO "django_admin_log" VALUES (4,'2','emil (staff)',3,'',6,1,'2025-06-13 01:40:45.051717');
INSERT INTO "django_admin_log" VALUES (5,'4','emil123 (staff)',1,'[{"added": {}}]',6,1,'2025-06-13 01:41:36.905310');
INSERT INTO "django_admin_log" VALUES (6,'5','trial234 (student)',1,'[{"added": {}}]',6,1,'2025-06-14 08:23:41.324048');
INSERT INTO "django_admin_log" VALUES (7,'5','trial234 (student)',2,'[{"changed": {"fields": ["password"]}}]',6,1,'2025-06-14 08:32:46.544508');
INSERT INTO "django_admin_log" VALUES (8,'5','trial234 (student)',2,'[{"changed": {"fields": ["First name", "Last name", "Phone number", "Student id", "Department"]}}]',6,1,'2025-06-14 08:33:06.911817');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (5,'sessions','session');
INSERT INTO "django_content_type" VALUES (6,'AccountsApp','user');
INSERT INTO "django_content_type" VALUES (7,'ReportsApp','itemreport');
INSERT INTO "django_content_type" VALUES (8,'ClaimsApp','claimrequest');
INSERT INTO "django_content_type" VALUES (9,'django_plotly_dash','dashapp');
INSERT INTO "django_content_type" VALUES (10,'django_plotly_dash','statelessapp');
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2025-06-11 22:44:10.224148');
INSERT INTO "django_migrations" VALUES (2,'contenttypes','0002_remove_content_type_name','2025-06-11 22:44:10.233145');
INSERT INTO "django_migrations" VALUES (3,'auth','0001_initial','2025-06-11 22:44:10.253375');
INSERT INTO "django_migrations" VALUES (4,'auth','0002_alter_permission_name_max_length','2025-06-11 22:44:10.264343');
INSERT INTO "django_migrations" VALUES (5,'auth','0003_alter_user_email_max_length','2025-06-11 22:44:10.272398');
INSERT INTO "django_migrations" VALUES (6,'auth','0004_alter_user_username_opts','2025-06-11 22:44:10.282422');
INSERT INTO "django_migrations" VALUES (7,'auth','0005_alter_user_last_login_null','2025-06-11 22:44:10.291181');
INSERT INTO "django_migrations" VALUES (8,'auth','0006_require_contenttypes_0002','2025-06-11 22:44:10.294247');
INSERT INTO "django_migrations" VALUES (9,'auth','0007_alter_validators_add_error_messages','2025-06-11 22:44:10.303789');
INSERT INTO "django_migrations" VALUES (10,'auth','0008_alter_user_username_max_length','2025-06-11 22:44:10.311209');
INSERT INTO "django_migrations" VALUES (11,'auth','0009_alter_user_last_name_max_length','2025-06-11 22:44:10.320457');
INSERT INTO "django_migrations" VALUES (12,'auth','0010_alter_group_name_max_length','2025-06-11 22:44:10.331212');
INSERT INTO "django_migrations" VALUES (13,'auth','0011_update_proxy_permissions','2025-06-11 22:44:10.338612');
INSERT INTO "django_migrations" VALUES (14,'auth','0012_alter_user_first_name_max_length','2025-06-11 22:44:10.344612');
INSERT INTO "django_migrations" VALUES (15,'AccountsApp','0001_initial','2025-06-11 22:44:10.361908');
INSERT INTO "django_migrations" VALUES (16,'ReportsApp','0001_initial','2025-06-11 22:44:10.374160');
INSERT INTO "django_migrations" VALUES (17,'ClaimsApp','0001_initial','2025-06-11 22:44:10.385961');
INSERT INTO "django_migrations" VALUES (18,'admin','0001_initial','2025-06-11 22:44:10.439246');
INSERT INTO "django_migrations" VALUES (19,'admin','0002_logentry_remove_auto_add','2025-06-11 22:44:10.450242');
INSERT INTO "django_migrations" VALUES (20,'admin','0003_logentry_add_action_flag_choices','2025-06-11 22:44:10.458271');
INSERT INTO "django_migrations" VALUES (21,'django_plotly_dash','0001_initial','2025-06-11 22:44:10.469336');
INSERT INTO "django_migrations" VALUES (22,'django_plotly_dash','0002_add_examples','2025-06-11 22:44:10.479345');
INSERT INTO "django_migrations" VALUES (23,'sessions','0001_initial','2025-06-11 22:44:10.488679');
INSERT INTO "django_migrations" VALUES (24,'AccountsApp','0002_alter_user_email','2025-06-11 22:47:48.967591');
INSERT INTO "django_session" VALUES ('fhx7mw4ks6flis21xoxg8a6bo25yazsb','.eJxVjEsOAiEQRO_C2hCQBsSle89AummQUQPJfFbGuyvJLHRZ9V7VS0Tc1hq3Jc9xYnEWRhx-O8L0yG0AvmO7dZl6W-eJ5FDkThd57Zyfl939O6i41LE2BVGTUwhJJYP-iGDQgs-FmbVztmStbKEANlMJ4Bi8USeyKXyDF-8PBCM4Mw:1uPVZt:qiudfU4D5WyLyJXwYYBXWslPNhYnGa4yyPc7HplAQ1o','2025-06-26 00:13:57.604469');
INSERT INTO "django_session" VALUES ('bgw5ohls1y2cpvm241vstu64q8025fdg','.eJxVjEsOAiEQRO_C2hCQBsSle89AummQUQPJfFbGuyvJLHRZ9V7VS0Tc1hq3Jc9xYnEWRhx-O8L0yG0AvmO7dZl6W-eJ5FDkThd57Zyfl939O6i41LE2BVGTUwhJJYP-iGDQgs-FmbVztmStbKEANlMJ4Bi8USeyKXyDF-8PBCM4Mw:1uQPxT:9Yy8-0kkiSPcEmMcGpbT9QWQ9IqSwXxWjOpwbTmIX3s','2025-06-28 12:26:03.706840');
INSERT INTO "django_session" VALUES ('bfx1ylprg4b9lhvyx617jox11m1pjz2w','.eJxVjEEOwiAQRe_C2hCYAQWX7j0DYZhBqqZNSrsy3l2bdKHb_977L5XyurS0dpnTwOqsrDr8bpTLQ8YN8D2Pt0mXaVzmgfSm6J12fZ1Ynpfd_Ttoubdv7WuMUcQF9FQcVnLlhJmqC54MoBWAowMCBA-BTc0mIAu7UKxH9KzeH9tXN2w:1uQnLT:8Ig9u9lJYRgcyyRZyQxQmZnw1HMWMxYDYmlljeknpPI','2025-06-29 13:24:23.879605');
CREATE INDEX IF NOT EXISTS "AccountsApp_user_groups_group_id_4535aae2" ON "AccountsApp_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "AccountsApp_user_groups_user_id_b15058ae" ON "AccountsApp_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "AccountsApp_user_groups_user_id_group_id_4f58f41a_uniq" ON "AccountsApp_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "AccountsApp_user_user_permissions_permission_id_4690c7e7" ON "AccountsApp_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "AccountsApp_user_user_permissions_user_id_284fa21b" ON "AccountsApp_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "AccountsApp_user_user_permissions_user_id_permission_id_15fd24a8_uniq" ON "AccountsApp_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "ClaimsApp_claimrequest_claimer_id_2bea06bc" ON "ClaimsApp_claimrequest" (
	"claimer_id"
);
CREATE INDEX IF NOT EXISTS "ClaimsApp_claimrequest_item_id_3a6025a4" ON "ClaimsApp_claimrequest" (
	"item_id"
);
CREATE INDEX IF NOT EXISTS "ClaimsApp_claimrequest_verified_by_id_2fc3d39c" ON "ClaimsApp_claimrequest" (
	"verified_by_id"
);
CREATE INDEX IF NOT EXISTS "ReportsApp_itemreport_reporter_id_bff59f05" ON "ReportsApp_itemreport" (
	"reporter_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_plotly_dash_dashapp_stateless_app_id_220444de" ON "django_plotly_dash_dashapp" (
	"stateless_app_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
COMMIT;
