create table test (a int primary key, b text);

\copy  test(a, b) FROM '/docker-entrypoint-initdb.d/data.csv' DELIMITER ',' CSV HEADER;
