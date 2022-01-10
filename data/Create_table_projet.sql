


PRAGMA FOREIGN_KEYS=ON;

CREATE TABLE Clients (
	numero_client INTEGER NOT NULL,
	nom_client TEXT NOT NULL,
	prenom_client TEXT NOT NULL,
	adresse_client TEXT NOT NULL,
	email_client TEXT,
CONSTRAINT pk_client_c00 PRIMARY KEY (numero_client)
);

CREATE TABLE Commandes(
	numero_commande INTEGER NOT NULL,
	numero_client INTEGER NOT NULL,
	date_commande DATE NOT NULL,
CONSTRAINT pk_Commandes_c00 PRIMARY KEY (numero_commande),
CONSTRAINT fk_Commandes_c01 FOREIGN KEY (numero_client) REFERENCES Clients(numero_client)
);

CREATE TABLE Fournisseurs(
	numero_fournisseur INTEGER NOT NULL,
	nom_fournisseur TEXT NOT NULL,
	adresse_fournisseur TEXT NOT NULL,
	CONSTRAINT pk_Fournisseurs_c00 PRIMARY KEY (numero_fournisseur)
);

CREATE TABLE TypesArticles(
	type_article TEXT NOT NULL,
	categorie_type_article TEXT NOT NULL,
	prix_type_article REAL NOT NULL,
	numero_fournisseur INTEGER NOT NULL,
CONSTRAINT pk_TypesArticles_c00 PRIMARY KEY (type_article),
CONSTRAINT fk_TypesArticles_c01 FOREIGN KEY (numero_fournisseur) REFERENCES Fournisseurs (numero_fournisseur),
CONSTRAINT ck_TypesArticles_c03 CHECK  (categorie_type_article  in ("Fruits et Legumes","Boissonerie","Surgele","Boucherie","Epicerie","Boulangerie")),
CONSTRAINT ck_TypeArticle_c04 CHECK (prix_type_article > 0)
);

CREATE TABLE Articles(
    code_article TEXT NOT NULL,
    type_article TEXT NOT NULL,
    statut_article TEXT NOT NULL DEFAULT 'disponible',
CONSTRAINT pk_Articles_c00 PRIMARY KEY (code_article),
CONSTRAINT ck_Articles_c01 CHECK(statut_article in ("disponible","commande")),
CONSTRAINT fk_Articles_c02 FOREIGN KEY (type_article) REFERENCES TypesArticles(type_article) 
);

CREATE TABLE ArticlesCommandes(
	code_article TEXT NOT NULL,
	numero_commande INTEGER NOT NULL,
CONSTRAINT pk_ArticlesCommandes_c00 PRIMARY KEY (code_article),
CONSTRAINT fk_ArticlesCommandes_c01 FOREIGN KEY (code_article) REFERENCES Articles(code_article),
CONSTRAINT fk_ArticlesCommandes_c02 FOREIGN KEY (numero_commande) REFERENCES Commandes(numero_commande) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE VIEW Clients_View(
	numero_client,
	nom_client,
	prenom_client,
	adresse_client,
	email_client,
	nombre_commande_client
	) AS
	SELECT numero_client,
		   nom_client,
		   prenom_client,
		   adresse_client,
	       email_client,
	       COUNT(numero_commande)AS nombre_commande_client
	FROM Clients
	JOIN Commandes
	USING (numero_client)
	GROUP BY numero_client
	UNION
	SELECT numero_client,
		   nom_client,
		   prenom_client,
		   adresse_client,
	       email_client,
	       0 AS nombre_commande_client
	FROM Clients
	WHERE numero_client NOT IN(SELECT numero_client
								FROM Commandes);

CREATE VIEW Commandes_View(
	numero_commande,
	numero_client,
	date_commande,
	quantite_article
	) AS
	SELECT numero_commande,
		   numero_client,
		   date_commande,
		   COUNT(code_article ) AS quantite_article
	FROM Commandes
	JOIN ArticlesCommandes
	USING (numero_commande)
	GROUP BY numero_commande;
	
CREATE VIEW TypesArticles_View(
	type_article,
	categorie_type_article,
	prix_type_article,
	numero_fournisseur,
	quantite_disponible_article
	) AS
	SELECT type_article,
		   categorie_type_article,
		   prix_type_article,
		   numero_fournisseur,
		   COUNT(code_article) AS quantite_disponible_article
	FROM Articles
	JOIN TypesArticles
	USING (type_article)
	WHERE(statut_article="disponible")
	GROUP BY type_article;




	
	