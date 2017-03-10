GRANT SELECT,INSERT,UPDATE,DELETE ON retweeter_bot.* TO 'retweeter' IDENTIFIED BY '#password-in-yaml-file';
FLUSH PRIVILEGES;

CREATE TABLE `tweets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `twitter_id` varchar(45) NOT NULL,
  `context` varchar(45) NOT NULL,
  `stamp` datetime NOT NULL DEFAULT NOW(),
  `source` varchar(45) NOT NULL,
  `tweeter` varchar(45) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `longitude` varchar(45) DEFAULT NULL,
  `latitude` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=185 DEFAULT CHARSET=utf8;


