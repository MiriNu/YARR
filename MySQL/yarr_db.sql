CREATE SCHEMA IF NOT EXIST yarr;

CREATE TABLE IF NOT EXIST `yarr`.`researchers` (
  `ResearcherId` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `UserName` VARCHAR(45) NOT NULL,
  `HashedPassword` VARCHAR(45) NOT NULL,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ResearcherId`));
  
CREATE TABLE IF NOT EXIST `yarr`.`studies` (
  `StudyId` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `ResearcherId` INT UNSIGNED NOT NULL,
  `Title` VARCHAR(1024) NOT NULL,
  `StudyQuestions` VARCHAR(4096) NOT NULL,
  `Description` VARCHAR(4096) NOT NULL,
  PRIMARY KEY (`StudyId`),
  INDEX `ResearcherId_idx` (`ResearcherId` ASC) VISIBLE,
  CONSTRAINT `ResearcherId`
    FOREIGN KEY (`ResearcherId`)
    REFERENCES `yarr`.`researchers` (`ResearcherId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);
	
CREATE TABLE `yarr`.`experiments` (
  `ExperimentId` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `StudyId` INT UNSIGNED NOT NULL,
  `CreationDate` VARCHAR(45) NOT NULL,
  `Status` VARCHAR(45) NOT NULL,
  `Title` VARCHAR(45) NOT NULL,
  `Details` VARCHAR(4096) NOT NULL,
  `RoundsNumber` INT UNSIGNED NOT NULL,
  `RoundDuration` INT UNSIGNED NOT NULL,
  `Disability` INT UNSIGNED NOT NULL,
  `CharacterType` INT UNSIGNED NOT NULL,
  `ColorSettings` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`ExperimentId`),
  INDEX `StudyId_idx` (`StudyId` ASC) VISIBLE,
  CONSTRAINT `StudyId`
    FOREIGN KEY (`StudyId`)
    REFERENCES `yarr`.`studies` (`StudyId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);

CREATE TABLE `yarr`.`rounds` (
  `RoundId` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `ExperimentId` INT UNSIGNED NOT NULL,
  `RoundNumber` INT UNSIGNED NOT NULL,
  `GameMode` INT UNSIGNED NOT NULL,
  `Difficulty` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`RoundId`),
  INDEX `ExperimentId_idx` (`ExperimentId` ASC) VISIBLE,
  CONSTRAINT `ExperimentId`
    FOREIGN KEY (`ExperimentId`)
    REFERENCES `yarr`.`experiments` (`ExperimentId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);

CREATE TABLE `yarr`.`study_insights_mirror` (
  `ResearcherId` INT UNSIGNED NOT NULL,
  `StudyId` INT UNSIGNED NOT NULL,
  `AxisTime` DOUBLE NULL,
  `AxisEngagement` DOUBLE NULL,
  `BreakdownType` ENUM("mode", "skin", "difficultyType") NULL,
  `BreakdownName` VARCHAR(45) NOT NULL);

INSERT INTO yarr.study_insights_mirror (ResearcherId, StudyId, AxisTime, AxisEngagement, BreakdownType,BreakdownName)
VALUES (1,1,9,3,"mode","comp"),(1,1,12,3,"mode","comp"),(1,1,15,3,"mode","comp"),(1,1,18,5,"mode","comp"),(1,1,21,5,"mode","comp"),(1,1,24,3,"mode","comp"),
(1,1,9,1,"mode","coop"),(1,1,12,1,"mode","coop"),(1,1,15,1,"mode","coop"),(1,1,18,2,"mode","coop"),(1,1,21,3,"mode","coop"),(1,1,24,4,"mode","coop"),
(1,1,9,1,"skin","color"),(1,1,12,1,"skin","color"),(1,1,15,1,"skin","color"),(1,1,18,2,"skin","color"),(1,1,21,3,"skin","color"),(1,1,24,4,"skin","color"),
(1,1,9,1,"skin","shape"),(1,1,12,1,"skin","shape"),(1,1,15,1,"skin","shape"),(1,1,18,2,"skin","shape"),(1,1,21,3,"skin","shape"),(1,1,24,4,"skin","shape");


CREATE TABLE `yarr`.`study_insights_radar` (
  `ResearcherId` INT UNSIGNED NOT NULL,
  `StudyId` INT UNSIGNED NOT NULL,
  `ExperimentId` INT UNSIGNED NOT NULL,
  `ExperimentTitle` VARCHAR(45) NOT NULL,
  `HighestEngagement` DOUBLE NOT NULL,
  `MeanEngagement` DOUBLE NOT NULL,
  `MedianEngagement` DOUBLE NOT NULL,
  `ModeEngagement` DOUBLE NOT NULL,
  `RangeEngagement` DOUBLE NOT NULL,
  `RoundDuration` INT UNSIGNED NULL,
  `RoundsNumber` INT NULL,
  `RoundsAmountComp` INT NULL,
  `RoundsAmountCoop` INT NULL,
  `CharacterType` INT UNSIGNED NOT NULL,
  `Disability` INT UNSIGNED NOT NULL,
  `ColorSettings` INT UNSIGNED NOT NULL);

INSERT INTO yarr.study_insights_radar 
VALUES (1,1,1,"Green-Red cBlindness", 9, 3,4,3,8,100,3,3,0,1,1,1),
 (1,1,2,"Green cBlindness", 10, 2,4,4,9,100,3,0,3,1,1,2);

CREATE TABLE `yarr`.`study_insights_mixed` (
  `ResearcherId` INT UNSIGNED NOT NULL,
  `StudyId` INT UNSIGNED NOT NULL,
  `ExperimentId` INT UNSIGNED NOT NULL,
  `ExperimentTitle` VARCHAR(45) NOT NULL,
  `TimeAxis` DOUBLE NULL,
  `Clicks` INT NOT NULL,
  `ResponseTime` DOUBLE NOT NULL,
  `DifficultyChange` INT NOT NULL);

CREATE TABLE `yarr`.`study_insights_pie` (
  `ResearcherId` INT UNSIGNED NOT NULL,
  `StudyId` INT UNSIGNED NOT NULL,
  `Mode` VARCHAR(45) NOT NULL,
  `PercentItemsTaken` DOUBLE NULL,
  `PercentItemsMissed` DOUBLE NOT NULL,
  `PercentEnemiesAvoid` DOUBLE NOT NULL,
  `PercentEnemiesHit` DOUBLE NOT NULL,
  `PercentEnemiesBlock` DOUBLE NOT NULL);