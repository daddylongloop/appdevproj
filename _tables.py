CREATE_RECIPE_TABLE = """
CREATE TABLE `RAW_RECIPES`.`Recipes` (`NID` INT NOT NULL AUTO_INCREMENT , 
`name` VARCHAR(100) NOT NULL , 
`id` INT NOT NULL , 
`minutes` INT NOT NULL , 
`nutrition` VARCHAR(1000) NOT NULL , 
`steps` VARCHAR(10000) NOT NULL , 
`description` VARCHAR(10000) NOT NULL , 
PRIMARY KEY (`NID`)) ENGINE = InnoDB;"""

CREATE_TAG_ASGN = """
CREATE TABLE `RAW_RECIPES`.`TagsASGN` (`ID` INT NOT NULL AUTO_INCREMENT , 
`recipeID` INT NOT NULL , 
`tagID` INT NOT NULL , 
PRIMARY KEY (`ID`)) ENGINE = InnoDB;"""

CREATE_TABLE_INGREDIENTS = """"
CREATE TABLE `RAW_RECIPES`.`Ingredients` (`ID` INT NOT NULL AUTO_INCREMENT , 
`name` VARCHAR(100) NOT NULL , 
PRIMARY KEY (`ID`)) ENGINE = InnoDB;"""

CREATE_TABLE_INGREDIENTS_ASGN = """
CREATE TABLE `RAW_RECIPES`.`IngredientsASGN` (`ID` INT NOT NULL AUTO_INCREMENT , 
`recipeID` INT NOT NULL , 
`ingredientID` INT NOT NULL , 
PRIMARY KEY (`ID`)) ENGINE = InnoDB;"""

CREATE_TABLE_TAGS = """
CREATE TABLE `tags` (
  `ID` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB

INSERT INTO `tags` (`ID`, `name`) VALUES
(1, 'vegan'),
(2, 'vegetarian'),
(3, 'gluten-free'),
(4, 'dairy-free'),
(5, 'nut-free'),
(6, 'egg-free'),
(7, 'low-carb'),
(8, 'low-fat'),
(9, 'high-protein'),
(10, 'sugar-free'),
(11, 'side-dishes'),
(12, 'main-dishes'),
(13, 'desserts');

ALTER TABLE `tags`
  ADD PRIMARY KEY (`ID`);

ALTER TABLE `tags`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;
"""