--Insertions NOK (après avoir executé OK)

--Fournisseurs
--Erreur pk fournisseur 1 déjà utulisé
INSERT INTO  Fournisseurs VALUES (1,'AVS','4 Rue Lainerie, 69005 Lyon');


--TypesArticles
--Erreur ck enum Boulangerie n'existe pas dans l'enum
INSERT INTO  TypesArticles VALUES ('Baguette','Boulangerie',1.1,1);
--Erreur pk Poulet existe deja
INSERT INTO  TypesArticles VALUES ('Poulet','Epicerie',10.5,1);
--Erreur fk Fournisseurs 5 et 3 n'existent pas
INSERT INTO  TypesArticles VALUES ('Poivre','Epicerie',0.55,5);
INSERT INTO  TypesArticles VALUES ('Steak','Boucherie',10.5,3);
--Erreur ck prix doit être >0
INSERT INTO  TypesArticles VALUES ('Steak','Boucherie',-10,2);


--Articles
--Erreur pk P1 existe déjà
INSERT INTO  Articles (code_article, type_article) VALUES ('P1','Poulet');
INSERT INTO  Articles (code_article, type_article) VALUES ('P1','Poulet');
--Erreur fk type poivre n'existe pas
INSERT INTO  Articles (code_article, type_article) VALUES ('Po1','Poivre');


--Clients
--Erreur pk
INSERT INTO Clients VALUES (0,'Mahi','Riad','21 rue de l ivrogne','bebou_le_pilo@Hotmail.com');


--Commandes
--Erreur ck manque la date
INSERT INTO Commandes VALUES (3,0);
--Erreur pk 1 commande existe déjà
INSERT INTO Commandes VALUES (1,0,'2021-04-15');
--Erreur fk client 2 n'existe pas
INSERT INTO Commandes VALUES (1,2,'2021-04-15');


--ArticlesCommandes
--Erreur pk article p3 déjà commandé dans une autre commande
INSERT INTO  ArticlesCommandes VALUES ('P2',2);
--Erreur fk p6 n'existe pas
INSERT INTO  ArticlesCommandes VALUES ('P6',1);
--Erreur fk article p3 n'existe pas
INSERT INTO  ArticlesCommandes VALUES ('P3',3);



