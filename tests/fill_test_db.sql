DROP TABLE IF EXISTS `table_one`;

CREATE TABLE `table_one` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `something_not_null`    TEXT NOT NULL,
    `something_null`    TEXT
);

INSERT INTO `table_one` (id, something_not_null, something_null)
VALUES (?, 'apple', null);
INSERT INTO `table_one` (id, something_not_null, something_null)
VALUES (?, 'orange', null);
INSERT INTO `table_one` (id, something_not_null, something_null)
VALUES (?, 'pear', 'shaped');
INSERT INTO `table_one` (id, something_not_null, something_null)
VALUES (?, 'mango', 'chutney');
INSERT INTO `table_one` (id, something_not_null, something_null)
VALUES (?, 'lemon', 'lime');