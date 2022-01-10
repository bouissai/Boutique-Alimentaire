CREATE TRIGGER update_status_commande AFTER INSERT ON ArticlesCommandes
  BEGIN
    UPDATE Articles SET statut_article='commande'
    WHERE code_article IN (
	SELECT code_article
	FROM ArticlesCommandes);
  END;
  \\


CREATE TRIGGER update_status_disponible AFTER DELETE ON ArticlesCommandes
  BEGIN
    UPDATE Articles SET statut_article='disponible'
    WHERE code_article NOT IN (
	SELECT code_article
	FROM ArticlesCommandes);
  END;
  \\