-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema proyecto_pizzaTime
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema proyecto_pizzaTime
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `proyecto_pizzaTime` DEFAULT CHARACTER SET utf8 ;
USE `proyecto_pizzaTime` ;

-- -----------------------------------------------------
-- Table `proyecto_pizzaTime`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_pizzaTime`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `email` VARCHAR(200) NULL,
  `direccion` TEXT NULL,
  `password` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_pizzaTime`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_pizzaTime`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `total` INT NULL,
  `metodo_entrega` VARCHAR(45) NULL,
  `favorito` TINYINT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `proyecto_pizzaTime`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_pizzaTime`.`pizzas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_pizzaTime`.`pizzas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `size` VARCHAR(45) NULL,
  `corteza` VARCHAR(45) NULL,
  `cantidad` VARCHAR(45) NULL,
  `total` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `order_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_items_orders1_idx` (`order_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_orders1`
    FOREIGN KEY (`order_id`)
    REFERENCES `proyecto_pizzaTime`.`orders` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_pizzaTime`.`category_toppings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_pizzaTime`.`category_toppings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_pizzaTime`.`toppings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_pizzaTime`.`toppings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `category_topping_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_toppings_category_toppings1_idx` (`category_topping_id` ASC) VISIBLE,
  CONSTRAINT `fk_toppings_category_toppings1`
    FOREIGN KEY (`category_topping_id`)
    REFERENCES `proyecto_pizzaTime`.`category_toppings` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_pizzaTime`.`pizzas_has_toppings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proyecto_pizzaTime`.`pizzas_has_toppings` (
  `pizza_id` INT NOT NULL,
  `topping_id` INT NOT NULL,
  PRIMARY KEY (`pizza_id`, `topping_id`),
  INDEX `fk_pizzas_has_toppings_toppings1_idx` (`topping_id` ASC) VISIBLE,
  INDEX `fk_pizzas_has_toppings_pizzas1_idx` (`pizza_id` ASC) VISIBLE,
  CONSTRAINT `fk_pizzas_has_toppings_pizzas1`
    FOREIGN KEY (`pizza_id`)
    REFERENCES `proyecto_pizzaTime`.`pizzas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pizzas_has_toppings_toppings1`
    FOREIGN KEY (`topping_id`)
    REFERENCES `proyecto_pizzaTime`.`toppings` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

/*Categoria Toppings*/
INSERT INTO category_toppings(id, name) VALUES(1, 'Vegetales');
INSERT INTO category_toppings(id, name) VALUES(2, 'Proteinas');
INSERT INTO category_toppings(id, name) VALUES(3, 'Salsas');

/*1 Categoria Vegetales*/
INSERT INTO toppings(name, category_topping_id) VALUES('Aceituna', 1);
INSERT INTO toppings(name, category_topping_id) VALUES('Tomate', 1);
INSERT INTO toppings(name, category_topping_id) VALUES('Cebolla', 1);

/*2 Categoria Proteinas*/
INSERT INTO toppings(name, category_topping_id) VALUES('Pepperoni', 2);
INSERT INTO toppings(name, category_topping_id) VALUES('Carne', 2);
INSERT INTO toppings(name, category_topping_id) VALUES('Pollo', 2);

/*3 Categoria Salsa*/
INSERT INTO toppings(name, category_topping_id) VALUES('Salsa blanca', 3);
INSERT INTO toppings(name, category_topping_id) VALUES('Salsa de tomate', 3);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
