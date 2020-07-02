-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 02-Jul-2020 às 05:19
-- Versão do servidor: 5.6.17
-- PHP Version: 5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `padaria`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `compromissos`
--

CREATE TABLE IF NOT EXISTS `compromissos` (
  `id_compromisso` int(11) NOT NULL AUTO_INCREMENT,
  `evento` varchar(1000) DEFAULT NULL,
  `data_evento` date DEFAULT NULL,
  PRIMARY KEY (`id_compromisso`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Extraindo dados da tabela `compromissos`
--

INSERT INTO `compromissos` (`id_compromisso`, `evento`, `data_evento`) VALUES
(2, 'CHEGADA DE MERCADORIA', '2020-02-14'),
(3, 'CHEGADA DE 100 KG DE FRANGO', '2020-02-17'),
(4, 'ENTREGA DO SEU JOÃO', '2020-03-05'),
(5, 'VENDA PARA O JORGE', '2020-03-10'),
(6, 'APRESENTAR O PROGRAMA PARA O RAIMUNDO', '2020-02-17');

-- --------------------------------------------------------

--
-- Estrutura da tabela `estoque`
--

CREATE TABLE IF NOT EXISTS `estoque` (
  `id_produto` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `preco` float NOT NULL,
  `quantidade` int(11) NOT NULL,
  `total` float NOT NULL,
  `data_cadastro` date NOT NULL,
  PRIMARY KEY (`id_produto`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

--
-- Extraindo dados da tabela `estoque`
--

INSERT INTO `estoque` (`id_produto`, `nome`, `preco`, `quantidade`, `total`, `data_cadastro`) VALUES
(1, 'MASSA FINA', 17, 13, 221, '2020-01-09'),
(2, 'FRANGO', 9.9, 15, 148.5, '2020-01-09'),
(3, 'CALABRESA', 6.75, 20, 135, '2020-01-09'),
(5, 'PICANHA', 45, 20, 900, '2020-01-28'),
(6, 'FITA ISOLANTE', 3.5, 10, 35, '2020-01-29'),
(8, 'MENTOS', 1, 37, 37, '2020-01-30'),
(9, 'CARNE DE PORCO', 12.5, 40, 500, '2020-01-30'),
(10, 'FILÉ DE PEIXE', 23.99, 50, 1199.5, '2020-01-30'),
(11, 'BAUNILHA', 1.5, 48, 72, '2020-01-30'),
(12, 'ACHOCOLATADO', 6.99, 30, 209.7, '2020-01-30'),
(13, 'COPOS DESCARTÁVEIS', 5, 20, 100, '2020-01-30');

-- --------------------------------------------------------

--
-- Estrutura da tabela `login`
--

CREATE TABLE IF NOT EXISTS `login` (
  `id_login` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(100) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `cargo` varchar(100) NOT NULL,
  `nivel` int(11) NOT NULL,
  PRIMARY KEY (`id_login`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Extraindo dados da tabela `login`
--

INSERT INTO `login` (`id_login`, `usuario`, `senha`, `cargo`, `nivel`) VALUES
(1, 'emesonfilho', '88319322', 'GERENTE', 100),
(2, 'worior', '1234', 'ATENDENTE', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `saidas`
--

CREATE TABLE IF NOT EXISTS `saidas` (
  `data_saida` date NOT NULL,
  `horario_saida` time NOT NULL,
  `id_produto` int(11) NOT NULL,
  `produto` varchar(1000) NOT NULL,
  `quantidade` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Extraindo dados da tabela `saidas`
--

INSERT INTO `saidas` (`data_saida`, `horario_saida`, `id_produto`, `produto`, `quantidade`) VALUES
('2020-01-30', '23:43:59', 11, 'BAUNILHA', 2),
('2020-01-30', '23:44:42', 8, 'MENTOS', 30),
('2020-02-11', '09:57:04', 15, 'TESTE_TIMBÓ', 27);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
