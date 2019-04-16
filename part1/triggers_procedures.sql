DELIMITER $$
CREATE TRIGGER new_bet BEFORE INSERT ON bet
FOR EACH ROW
BEGIN
DECLARE msg VARCHAR(200);
IF (NEW.event_oid IN
	(SELECT event_oid
	 FROM bet
	 WHERE bet.user_2_oid = NEW.user_2_oid))
THEN SET msg = 'O utilizador ja apostou nesse evento!';
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
END IF;
END;$$

DELIMITER $$
CREATE TRIGGER bet_add_coins BEFORE INSERT ON bet
FOR EACH ROW
BEGIN
DECLARE msg VARCHAR(200);
IF ((SELECT coins FROM user_2 WHERE user_2.oid=NEW.user_2_oid)-NEW.amount>0)
THEN UPDATE user_2 SET user_2.coins=user_2.coins-NEW.amount WHERE user_2.oid=NEW.user_2_oid;
ELSE SET msg = 'O utilizador nao tem saldo suficiente!';
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
END IF;
END;$$

DELIMITER $$
CREATE TRIGGER bet_rem_coins AFTER DELETE ON bet
FOR EACH ROW
BEGIN
UPDATE user_2 SET user_2.coins=user_2.coins+OLD.amount WHERE user_2.oid=OLD.user_2_oid;
END;$$

DELIMITER $$
CREATE TRIGGER bet_add_odd_profit BEFORE INSERT ON bet
FOR EACH ROW
BEGIN
DECLARE oddAposta DOUBLE DEFAULT 0;
IF
NEW.result=1
THEN
SET oddAposta = (SELECT betess.event.oddv FROM event WHERE NEW.event_oid=event.oid);
END IF;

IF 
NEW.result=2
THEN
SET oddAposta = (SELECT betess.event.odde FROM event WHERE NEW.event_oid=event.oid);
END IF;

IF 
NEW.result=3
THEN
SET oddAposta = (SELECT betess.event.oddd FROM event WHERE NEW.event_oid=event.oid);
END IF;

SET NEW.odd=oddAposta;

SET NEW.profit=oddAposta*NEW.amount;
END;$$


DELIMITER $$
CREATE TRIGGER new_user BEFORE INSERT ON user_2
FOR EACH ROW
BEGIN
DECLARE msg VARCHAR(200);
IF (NEW.username IN
	(SELECT username
	 FROM user_2
	 WHERE user_2.username = NEW.username))
THEN SET msg = 'Username ja existe!';
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
END IF;
IF (NEW.email IN
	(SELECT email
	 FROM user_2
	 WHERE user_2.email = NEW.email))
THEN SET msg = 'Email ja existe!';
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
END IF;
END;$$

DELIMITER $$
DROP TRIGGER bet_add_odd;
$$


DELIMITER $$
CREATE PROCEDURE rem_equipa_comp
(IN equipa_id INT,
 IN comp_id INT)
BEGIN
DECLARE erro BOOL DEFAULT 0;
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET erro = 1;
START TRANSACTION;
	DELETE FROM betess.competition_team WHERE competition_oid=comp_id AND team_oid=equipa_id;
IF erro
THEN ROLLBACK;
ELSE COMMIT;
END IF;
END;$$

DELIMITER $$
CREATE PROCEDURE add_equipa_comp
(IN equipa_id INT,
 IN comp_id INT)
BEGIN
DECLARE erro BOOL DEFAULT 0;
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET erro = 1;
START TRANSACTION;
	INSERT INTO competition_team VALUES (comp_id, equipa_id);
IF erro
THEN ROLLBACK;
ELSE COMMIT;
END IF;
END;$$

DELIMITER $$
CREATE PROCEDURE add_coins
(IN user_id INT,
 IN cns INT)
BEGIN
DECLARE erro BOOL DEFAULT 0;
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET erro = 1;
START TRANSACTION;
	UPDATE user_2 SET user_2.coins=user_2.coins+cns WHERE user_2.oid=user_id;
IF erro
THEN ROLLBACK;
ELSE COMMIT;
END IF;
END;$$





DELIMITER $$
CREATE PROCEDURE rem_coins
(IN user_id INT,
 IN cns INT)
BEGIN
DECLARE erro BOOL DEFAULT 0;
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET erro = 1;
START TRANSACTION;
	UPDATE user_2 SET user_2.coins=user_2.coins-cns WHERE user_2.oid=user_id;
IF erro
THEN ROLLBACK;
ELSE COMMIT;
END IF;
END;$$