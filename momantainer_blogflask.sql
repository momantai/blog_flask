-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: momantaiter_blogflask
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.16.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Comentario`
--

DROP TABLE IF EXISTS `Comentario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Comentario` (
  `idComentario` int(11) NOT NULL AUTO_INCREMENT,
  `Comentario` varchar(45) DEFAULT NULL,
  `fechaComentario` varchar(45) DEFAULT NULL,
  `Usuario_idUsuarioC` int(11) DEFAULT NULL,
  `Publicacion_idPublicacionC` int(11) DEFAULT NULL,
  PRIMARY KEY (`idComentario`),
  KEY `fk_Comentario_1_idx` (`Usuario_idUsuarioC`),
  KEY `fk_Comentario_2_idx` (`Publicacion_idPublicacionC`),
  CONSTRAINT `fk_Comentario_1` FOREIGN KEY (`Usuario_idUsuarioC`) REFERENCES `Usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_Comentario_2` FOREIGN KEY (`Publicacion_idPublicacionC`) REFERENCES `Publicacion` (`idPublicacion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comentario`
--

LOCK TABLES `Comentario` WRITE;
/*!40000 ALTER TABLE `Comentario` DISABLE KEYS */;
INSERT INTO `Comentario` VALUES (1,'holas','19/04/14',2,1);
/*!40000 ALTER TABLE `Comentario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Publicacion`
--

DROP TABLE IF EXISTS `Publicacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Publicacion` (
  `idPublicacion` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(45) DEFAULT NULL,
  `cuerpo` varchar(45) DEFAULT NULL,
  `categoria` varchar(45) DEFAULT NULL,
  `fechaPublicacion` varchar(45) DEFAULT NULL,
  `subCategoria` varchar(45) DEFAULT NULL,
  `Usuario_idUsuario` int(11) DEFAULT NULL,
  `portada` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idPublicacion`),
  KEY `fk_Publicacion_1_idx` (`Usuario_idUsuario`),
  CONSTRAINT `fk_Publicacion_1` FOREIGN KEY (`Usuario_idUsuario`) REFERENCES `Usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Publicacion`
--

LOCK TABLES `Publicacion` WRITE;
/*!40000 ALTER TABLE `Publicacion` DISABLE KEYS */;
INSERT INTO `Publicacion` VALUES (1,'Prueba','<p>dasdasd</p>\r\n','1','19/04/14','C',2,'wpid-videoplayback_0003838877_1.jpg');
/*!40000 ALTER TABLE `Publicacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `Usuario_datos_idUsuario_datos` int(11) DEFAULT NULL,
  `correo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `fk_Usuario_1_idx` (`Usuario_datos_idUsuario_datos`),
  CONSTRAINT `fk_Usuario_1` FOREIGN KEY (`Usuario_datos_idUsuario_datos`) REFERENCES `Usuario_datos` (`idUsuario_datos`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (2,'Reykarma','a01b02264d7a5473065d7c1f95c55ca19807c33c',6,'armando567@hotmail.com');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario_datos`
--

DROP TABLE IF EXISTS `Usuario_datos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Usuario_datos` (
  `idUsuario_datos` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(45) DEFAULT NULL,
  `Ape_pat` varchar(45) DEFAULT NULL,
  `Ape_Mat` varchar(45) DEFAULT NULL,
  `imagen_perfil` varchar(45) DEFAULT NULL,
  `firma` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idUsuario_datos`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario_datos`
--

LOCK TABLES `Usuario_datos` WRITE;
/*!40000 ALTER TABLE `Usuario_datos` DISABLE KEYS */;
INSERT INTO `Usuario_datos` VALUES (6,'Armando','Colmenares','Hernandez','defaultprofile.png','¡Soy nuevo aquí!');
/*!40000 ALTER TABLE `Usuario_datos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-14 15:11:01
