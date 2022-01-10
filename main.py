#!/usr/bin/python3
from utils import db
import os
import random
import time


def select_tous_type_article(conn):
    """
    Affiche la liste de tous les clients.
    :param conn: Connexion à la base de données
    """
    l=[]
    cur = conn.cursor()
    cur.execute("SELECT type_article FROM TypesArticles")
    rows = cur.fetchall()
    for row in rows:
        l.append(row[0])
    return l

def menu_principal(): 
    """
    Affiche la menu principale.
    """
    os.system("cls||clear")
    print("\n\t\t\t\t\BIENVENUE DANS LA BOUTIQUE/\n\n")
    print("Bonjour, vous êtes sur le MENU PRINCIPAL\n")
    print("Nous sommes le ",time.strftime('%Y-%d-%m.\nIl est %H:%M:%S.',time.localtime()))
    print("\n\t\t\t\t----MENU PRINCIPAL----")
    print("Entrez ce qu'il y'a dans ('...')\n")
    print("\n\t\t\t\tQui êtes vous ?")
    user = input("- Client ('client')\n- Administrateur ('admin')\n- Quitter ('quit') \n")
    while user not in ['client','quit','admin']:
      user = input("Qui êtes vous ? ")
    return user

def inscription(conn):
  """
  Permet d'inscrire un nouveau client dans la table Clients de la BDD.
  :param conn: Connexion à la base de données
  """
  os.system("cls||clear")
  print()
  print("\n\t\t\t\t----INSCRIPTION----")
  cur = conn.cursor()
  cur.execute("SELECT MAX(numero_client) FROM Clients")
  maxi = cur.fetchall()
  maxi = maxi[0][0]
  new_nbr = int(maxi) + 1 

  nom = input("Quelle est votre nom ?\n")
  while nom in [' ','\n']:
    nom = input("Quelle est votre nom ?\n")
  prenom = input("Quelle est votre prenom ?\n")
  while prenom in [' ','\n']:
    prenom = input("Quelle est votre prenom ?\n")
  adresse = input("Quelle est votre adresse ?\n")
  d = input("Souhaitez vous ajouter votre email ?o/n\n")
  while d not in ['o','n']:
    d = input("Souhaitez vous ajouter votre email ?o/n\n")
  if d=='o': 
    email = input("Quelle est votre email ?")
    cur.execute("""INSERT INTO Clients VALUES(?,?,?,?,?)""", (int(new_nbr), nom, prenom, adresse,email))
    conn.commit()###############Validé######################
  elif d=='n':
    email="None"
    cur.execute("""INSERT INTO Clients VALUES(?,?,?,?,?)""", (int(new_nbr), nom, prenom, adresse,email))
    conn.commit()###############Validé######################
  print("\nVous voilà inscrit !\nVoici votre numero de client :",new_nbr)
  input("\nTapez pour retourner au menu ")
  return int(new_nbr)

def connexion(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t\BIENVENUE DANS LA BOUTIQUE/\n\n")
  print("Bonjour, vous êtes sur le MENU CLIENT\n")
  print("Nous sommes le ",time.strftime('%Y-%d-%m.\nIl est %H:%M:%S.',time.localtime()))
  print("\n\t\t\t\t----CONNECTION----\n")
  numc = input("Entrez votre numéro client : ")

  while numc.isdigit()==False:
    numc = input("Entrez votre numéro client : ")

  nom = input("Entrez votre nom : ")
  prenom = input("Entrez votre prénom : ")
  cur = conn.cursor()

  list_verif_numc=[]
  cur.execute("SELECT numero_client FROM Clients")
  [list_verif_numc.append(row[0]) for row in cur.fetchall()]
  if int(numc) in list_verif_numc:
    cur.execute("SELECT nom_client FROM Clients WHERE numero_client=?",(int(numc),))
    verifnom = cur.fetchall()
    verifnom = verifnom[0][0]
    cur.execute("SELECT prenom_client FROM Clients WHERE numero_client=?",(int(numc),))
    verifprenom = cur.fetchall()
    verifprenom = verifprenom[0][0]  
    if verifnom.lower()==nom.lower() and verifprenom.lower()==prenom.lower():
      print("\n\t\t\t\Bienvenue ",nom.upper()," ",prenom.upper(),end="/\n")

      input("\nTapez pour allez dans votre menu client ")
      d=True
      while d==True:
        os.system("cls||clear")
        print("\n\t\t\t\t\BIENVENUE DANS LA BOUTIQUE/\n\n")
        print("Bonjour",nom.upper(),prenom.upper(),"\nVous êtes sur le MENU CLIENT\n")
        print("Nous sommes le ",time.strftime('%Y-%d-%m.\nIl est %H:%M:%S.',time.localtime()))
        


        print("\n\t\t\t\t----ESPACE CLIENT----")
        print("\n\t\t\t\tQue voulez vous faire?\n")
        co = input("- Commander/Catalogue ('c')\n- Voir mes commandes ('v')\n- Retour ('r') \n")
        while co not in ['c','v','r'] :
          co = input("Que voulez vous faire? ")
        if co=='c':
          commander_catalogue(numc,conn)
        if co=='v':
          voir_commande(numc,conn)
        if co=='r':
          d=False
          print("Retour au menu principal\n")      
    else:
      print("Vous n'existez pas dans la base de donnée")
      print("Réessayez ou Inscrivez vous")
      print()
      input("\nEntrez quelque chose pour revenir au menu Client... ")
  else:
    print("Vous n'existez pas dans la base de donnée")
    print("Réessayez ou Inscrivez vous")
    print()
    input("\nEntrez quelque chose pour revenir au menu Client... ")

def voir_commande(numc,conn):
  os.system("cls||clear")
  cur = conn.cursor()
  print("\n\t\t\t\t----VOIR MES COMMANDES----\n") 
  print("Que voulez vous faire? ")
  co = input("- Voir une commande ('v')\n- Retour ('r') \n")
  while co not in ['c','v','r']:
    co = input("Que voulez vous faire? ")



  if co=='v':
    os.system("cls||clear")
    liste_commande=[]
    #print("\n\t\t\t\t----LISTE DE NUM COMMANDES----\n")
    cur.execute("SELECT numero_commande FROM Commandes WHERE numero_client = (?)",((numc),))
    rows = cur.fetchall()
    for row in rows:
      liste_commande.append(row[0])
    
    print("\n\t\t\t\t----TOUTES MES COMMANDES----\n")
    cur.execute("SELECT numero_commande,date_commande FROM Commandes WHERE numero_client = (?)",((numc),))
    rows = cur.fetchall()

    print("\t\t+------------------------------------+")
    for row in rows:
      longeur = len("| Commande n°")+len(str(row[0]))+len("| date :")+len(str(row[1]))
      print("\t\t| Commande n°",row[0],"| date :",row[1]," |",end=' \n')
      print('\t\t+--','-'*longeur,'--+',sep="")
    
    if len(liste_commande)==0:
      print("Vous n'avez pas encore effectué de commande\n")
      input("Tapez pour revenir au menu Client ")

    else:
      co = input("Quelle commande voulez vous voir? ")

      while (not(co.isdigit() and int(co) in liste_commande)) :
        co = input("Quelle commande voulez vous voir? ")


      print()
      cur.execute("SELECT numero_commande, code_article ,categorie_type_article,prix_type_article, date_commande FROM Commandes JOIN ArticlesCommandes USING (numero_commande) JOIN Articles USING (code_article) JOIN TypesArticles USING (type_article) WHERE numero_client = (?) AND numero_commande= (?)" ,(int(numc),[co][0]))
      
      rows = cur.fetchall()
      for row in rows:
        print(row)
      cur.execute("SELECT SUM(prix_type_article) FROM Commandes JOIN ArticlesCommandes USING (numero_commande) JOIN Articles USING (code_article) JOIN TypesArticles USING (type_article) WHERE numero_client = (?) AND numero_commande= (?) GROUP BY (numero_commande)" ,(int(numc),[co][0]))
      rows = cur.fetchall()
      print("Le prix total de cette commande est de ",rows[0][0])
      input("\nEntrez quelque chose pour revenir au menu Client... ")
    

  if co=='r':
    input("\nEntrez quelque chose pour revenir au menu Client... ")

def catalogue_categorie(conn):
    os.system('cls||clear')
    print("\n\t\t\t\t----AFFICHAGE CATEGORIE----")
    #Afficher chaque categorie
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT categorie_type_article FROM TypesArticles")
    rows = cur.fetchall()
    rayon_valide = []
    for row in rows:
      print("+",'-'*len(row[0]),"+")
      print("| ",end="")
      print(row[0],end =' | ')
      rayon_valide.append(row[0])
      print()
      print("+",'-'*len(row[0]),"+")
    categ = input("Quels rayons souhaitez-vous voir? ")
    while categ not in  rayon_valide:
      categ = input("Quels rayons souhaitez-vous voir? ")
    #Afficher les type articles  pour chaque categorie
    print("\n\t\t\t\t---- AFFICHAGE PRODUITS DU RAYON",categ,"----",end='')
    print()
    cur = conn.cursor()
    cur.execute("SELECT type_article FROM TypesArticles WHERE categorie_type_article = (?)",[categ])
    rows = cur.fetchall()
    liste_type_article=[]
    print()
    for row in rows:
      print("+",'-'*len(row[0]),"+")
      print("| ",end="")
      print(row[0],end =' | ')
      liste_type_article.append(row[0])
      print()
      print("+",'-'*len(row[0]),"+")
    print()

def creer_commande(numc,conn):
    cur = conn.cursor()
    cur.execute("SELECT MAX(numero_commande) FROM Commandes")
    maxi = cur.fetchall()
    maxi = maxi[0][0]
    new_num_commande = int(maxi) + 1 
    date_commande = time.strftime('%Y-%m-%d',time.localtime())
    cur.execute("INSERT INTO Commandes VALUES(?,?,?)", (new_num_commande,numc,date_commande))
    conn.commit()###############Validé######################
    rows = cur.fetchall()
    for row in rows:
      print(row)
    print (new_num_commande)
    return new_num_commande

def voulez_vous_continuer(numc,numero_commande,conn):
  print("Voulez-vous ajouter des articles à votre commande ?")
  choix=input("o/n... ")  
  while choix not in ['o','n']:
    choix=input("o/n... ")  
  if choix == 'o':
    poursuivre_commande(numc,numero_commande,conn)
  if choix == 'n':
    input("\nEntrez quelque chose pour revenir au menu Client... ")
    #os.system("cls||clear")

def poursuivre_commande(numc,numero_commande,conn):
    cur = conn.cursor()
    cur.execute("SELECT type_article FROM TypesArticles")
    liste_type_article = [row[0] for row in cur.fetchall()]
    
    cur = conn.cursor()
    cur.execute("SELECT type_article FROM TypesArticles")
    rows = cur.fetchall()
    liste_typ_art=[]
    for row in rows:
      liste_typ_art.append(row[0])
    os.system("cls||clear")
    print("\n\t\t\t\t----AFFICHAGE ARTICLES----\n")
    print("Articles de la boutique : ",liste_typ_art)
    print()
    type_article = input("Que voulez vous acheter ? ...")
    while (type_article not in liste_type_article): 
      #Réessayer si l'utulisateur entre un type qui n'existe pas
      type_article = input("Que voulez vous acheter ? ...")
      
    cur.execute("SELECT count(code_article) FROM Articles WHERE type_article = (?) AND statut_article = 'disponible'", ( [type_article]))
    nbr_dispo = (cur.fetchall())[0][0]
    print("\nIl en reste :",nbr_dispo)
    if(nbr_dispo == 0):
      print("Désolé, ce produit est épuisé :(\n")
      print("\n----MA COMMANDE----")      
      print("Aucun produit n'a été ajouté")
      print("-------------------\n")
      

    else:
      flag=True
      while flag:
        qte = input("Combien en voulez vous ?") 
        while (qte.isdigit()==False): 
          qte = input("Réessayer : combien en voulez vous ?")   
        if (int(qte)<=nbr_dispo) and (int(qte)>=0):
          flag=False
        else:
          print("Réessayer : Quantité suppérieure au stock")
      qte=int(qte)
      article_dispo = article_disponible(conn,type_article)
      #print(article_dispo)
      print("\n----MA COMMANDE----")      
      
      if qte==0:
        print("Aucun produit n'a été ajouté")
      else:
        i=0
        for i in range(qte):
          #Commander n quantité
          n = random.randint(0,len(article_dispo))
          print("J'ai commandé : ",article_dispo[n-1])
          cur.execute("INSERT INTO ArticlesCommandes VALUES(?,?)", (article_dispo[n-1],numero_commande))
          conn.commit()###############Validé######################
          article_dispo.remove(article_dispo[n-1])
        rows = cur.fetchall()
        for row in rows:
          print(row)
        print("-------------------\n")

    #conn.commit()#####################SAVE INSERTION
    affichage_panier(conn,numero_commande) 
    voulez_vous_continuer(numc,numero_commande,conn)
        
def affichage_panier(conn,numero_commande):
  cur = conn.cursor()
  print("\n----MON PANIER----")
  cur.execute("SELECT code_article, type_article FROM ArticlesCommandes JOIN Articles USING (code_article) WHERE numero_commande = (?)", (int(numero_commande),))
  rows = cur.fetchall()
  for row2 in rows:
    print(row2)
  print("------------------\n")

def article_disponible(conn,type_article):
  cur = conn.cursor()
  l = []
  cur.execute("SELECT code_article FROM Articles WHERE type_article = (?) AND statut_article = 'disponible'",[type_article])
  rows = cur.fetchall()
  for row in rows:
    l.append(row[0])
  return l

def commander_catalogue(numc,conn):
  #os.system("cls||clear")
  #print()
  #print("\n\t\t\t\t----COMMANDE/CATALOGUE----\n")
  #print("Que voulez vous faire?\n")
  #co = input(" - nouvelle commande ('c')\n - Voir tous les produits ('t') \n - Voir par catégorie ('v') \n - Retour ('r') \n")

  d=True
  while d==True :
    os.system("cls||clear")

    print("\n\t\t\t\t----COMMANDE/CATALOGUE----")
    print("\n\t\t\t\tQue voulez vous faire?\n")
    co=input(" - nouvelle commande ('c')\n - Voir tous les produits ('t') \n - Voir par catégorie ('v') \n - Retour ('r') \n")
    while co not in ['c','t','v','r']:
      #co = input(" - nouvelle commande ('c')\n - Voir tous les produits ('t') \n - Voir par catégorie ('v') \n - Retour ('r') \n")
      co = input("Que voulez vous faire? ")

    if co =='t':#VOIR TOUS LES PRODUITS
      print("\n\t\t\t\t----AFFICHAGE PRODUITS----")
      cur = conn.cursor()
      cur.execute("SELECT type_article FROM TypesArticles")
      rows = cur.fetchall()
      liste_typ_art=[]
      for row in rows:
        print("+",'-'*len(row[0]),"+")
        print("| ",end="")
        print(row[0],end =' | ')
        liste_typ_art.append(row[0])
        print()
        print("+",'-'*len(row[0]),"+")
      #print(liste_typ_art)
      print()
      print("\t\t\t\tQue voulez vous faire? ")
      print(" - Acheter un produit ('a')\n - Voir les caractéristiques d'un produit ('c') \n - Retour ('r') \n")
      co = input("Je choisis ")
      while co not in ['a','c','r']:
        co = input("Je choisis : ")
      if co == 'a':
        numero_commande = creer_commande(numc,conn)
        poursuivre_commande(numc,numero_commande,conn)
        d=True

      if co == 'c':
        co = input("Je veux voir : ")
        voir_caracteristiques(conn,co)
        input("\nEntrez quelque chose pour revenir au menu Client/Catalogue?... ")
        d=True
        
      if co=='r':
        print("Retour au menu Client/Catalogue")

    if co =='v':#VOIR PRODUITS PAR CATEGORIE
      print("\n\t\t\t\t----AFFICHAGE CATEGORIE----")
      catalogue_categorie(conn)
      print()
      print("\t\t\t\tQue voulez vous faire? ")
      print(" - Acheter un produit ('a')\n - Voir les caractéristiques d'un produit ('c') \n - Retour ('r') \n")
      co = input("Je choisis ")
      while co not in ['a','c','r']:
        co = input("Je choisis : ")
      if co == 'a':
        numero_commande = creer_commande(numc,conn)
        poursuivre_commande(numc,numero_commande,conn)
        d=True

      if co == 'c':
        co = input("Je veux voir : ")
        voir_caracteristiques(conn,co)
        input("\nEntrez quelque chose pour revenir au menu Client/Catalogue?... ")
        d=True
        
      if co=='r':
        print("Retour au menu Client/Catalogue")
      commander_catalogue(numc,conn)
      d=True

    if co=='c':     
      numero_commande = creer_commande(numc,conn)
      poursuivre_commande(numc,numero_commande,conn)

      d=True

    if co=='r':
      d=False
      print("Retour au menu principal\n")

def voir_caracteristiques(conn,co):
  type_article = select_tous_type_article(conn)
  while co not in type_article:
    co = input("Je veux voir: ...")
  #os.system("cls||clear")
  print("\n\t\t\t\t----CARACTERISTIQUES DU PRODUIT----\n")
  cur = conn.cursor()
  print("Voici les caractéristiques du produit :",co,end="\n")
  #print("| Prix | Catégorie | Nom fournisseur | Quantié disponible |")
  cur.execute("SELECT prix_type_article FROM TypesArticles JOIN Fournisseurs USING (numero_fournisseur) WHERE type_article = (?)",[co])
  prix =  cur.fetchall()
  for row in prix:
    print("- prix :",row[0])

  cur.execute("SELECT categorie_type_article FROM TypesArticles JOIN Fournisseurs USING (numero_fournisseur) WHERE type_article = (?)",[co])
  categorie =  cur.fetchall()
  for row in categorie:
    print("- categorie :",row[0])
  cur.execute("SELECT nom_fournisseur FROM TypesArticles JOIN Fournisseurs USING (numero_fournisseur) WHERE type_article = (?)",[co])
  fournisseur =  cur.fetchall()
  for row in fournisseur:
    print("- fournisseur :",row[0])


  cur.execute("SELECT count(code_article) FROM Articles WHERE type_article = (?) AND statut_article = 'disponible'", ( [co]))
  nbr_dispo = (cur.fetchall())[0][0]
  if nbr_dispo==0:
    print("- épuisé")
  else:
    print("- disponible : ",nbr_dispo)

def main():
    # Nom de la BD à créer
    db_file = "data/Projet_sql.db"

    # Créer une connexion a la BD
    conn = db.creer_connexion(db_file)

    # Remplir la BD
    #print("1. On crée la bd et on l'initialise avec des premières valeurs.")
    #db.mise_a_jour_bd(conn, "data/Create_table_projet.sql")
    #db.mise_a_jour_trigger(conn, "data/Trigger_projet.sql")
    #db.mise_a_jour_bd(conn, "data/Insert_Ok_projet.sql")
    
    coo=True
    while coo==True:
      user = menu_principal()
      
      if user=='quit':
        coo=False

      if user=='client': #Inteface client
        os.system("cls||clear")
        print("\n\t\t\t\t\BIENVENUE DANS LA BOUTIQUE/\n\n")
        print("Bonjour, vous êtes sur le MENU PRINCIPAL\n")
        print("Nous sommes le ",time.strftime('%Y-%d-%m.\nIl est %H:%M:%S.',time.localtime()))
        
        print("\n\t\t\t\t----MENU CLIENT----")
        print("\n\t\t\t\tQue voulez vous faire?")
        co = input("- S'inscrire ('i')\n- Se connecter ('c')\n- Retour ('r')\n")
        while co not in ['i','r','c']:
          co = input("Que voulez vous faire? ")

        if co=='i':
          numc = inscription(conn)      
          inscri = input("Voulez vous commandez ?o/n ")
          while inscri not in ['o','n'] :
            inscri = input("Voulez vous commandez ?o/n ")
          if inscri == 'o': 
            commander_catalogue(numc,conn)
          else : 
            input("Entrez quelque chose pour revenir au menu Principal\n")
        elif co=='c':
          connexion(conn)
        elif co=='r':
          print("...Retour au menu principal...\n")

      

      elif user=='admin': #Inteface admin
        mdp ="403"#403
        entrer_mdp=input("Entrez le mot de passe de l'admin ou ('quit')... \n")
        while (mdp != entrer_mdp) or (entrer_mdp=='quit'):
          entrer_mdp=input("Entrez le mot de passe de l'admin ou ('quit')... ")
        
        if entrer_mdp=='quit':
          input("Retour au menu Principal ")
          
        if entrer_mdp==mdp:
          cooo=True
          while cooo==True:
            os.system("cls||clear")
            print("\n\t\t\t\t\BIENVENUE DANS LA BOUTIQUE/\n\n")
            print("Bonjour, vous êtes sur le MENU ADMINISTRATEUR\n")
            print("Nous sommes le ",time.strftime('%Y-%d-%m.\nIl est %H:%M:%S.',time.localtime()))
            
            print("\n\t\t\t\t----MENU ADMINISTRATEUR----")
            print("\n\t\t\t\tQue voulez vous faire chef?\n")
            user = input(" - Ajouter Fournisseurs ('1')\n - Ajouter TypesArticle ('2')\n - Ajouter Articles ('3')\n - Ajouter Clients ('4')\n - Ajouter Commandes ('5')\n - Ajouter ArticlesCommandes ('6')\n\n - Changer un prix ('7') \n\n - Supprimer Articles ('8')\n - Supprimer Clients ('9')\n - Supprimer Commandes ('10')\n - Annuler ArticlesCommandes ('11')\n\n - Afficher toutes les tables ('12')\n - Réinitialisé les tables ('13')\n\n - Quitter ('quit')\n\n...")
            
            numero = ['1','2','3','4','5','6','7','8','9','10','11','12','13','quit']
            while user not in numero:
              user = input("Que voulez vous faire ? ")

            if  user == '1' :
              Ajouter_Fournisseurs(conn)
            if  user == '2' :
              Ajouter_TypesArticles(conn)
            if  user == '3' :
              Ajouter_Articles(conn)
            if  user == '4' :
              Ajouter_Clients(conn)
            if  user == '5' :
              Ajouter_Commandes(conn)
            if  user == '6' :
              Ajouter_ArticlesCommandes(conn)
            if user == '7' : 
              Changer_prix(conn)
            if  user == '8' :
              Supprimer_Articles(conn)
            if  user == '9':
              Supprimer_Clients(conn)
            if  user == '10':
              Supprimer_Commandes(conn)
            if  user == '11':
              Supprimer_ArticlesCommandes(conn)
            if  user == '12':
              Afficher_Toutes_Les_Tables(conn)
            if  user == '13':
              Reinitialiser_tables(conn)
              input("Taper au clavier ...")
            
            if user == 'quit':
              cooo=False
              input("Entrez quelque chose pour revenir au menu Principal\n")
    # Lire la BD
    #print("2. Liste de tous les CLIENTS")
    #select_tous_type_article(conn)

def numero_fournisseur_OK(conn):
  l = []
  cur = conn.cursor()
  cur.execute("SELECT numero_fournisseur FROM Fournisseurs")
  rows = cur.fetchall()
  for row in rows:
    l.append(row[0])
  print(l)
  return l

def Categorie_OK():
  l = ["Fruits et Legumes","Boissonerie","Surgele","Boucherie","Epicerie","Boulangerie"]
  return l

def Ajouter_Fournisseurs(conn): 
  cur = conn.cursor()
  print("\n\t\t\t\t----AJOUT Fournisseurs----")
  nomf = input("Entrez le nom du nouveau Fournisseur : ")
  adrs = input("Entrez l'adresse de ce fournisseur Fournisseur : ")
  
  print("Etes vous sûr d'insérer ",nomf," à l'adresse ",adrs," ? o/n")
  aff=input("")
  while aff not in ['o','n']:
    aff=input("Etes vous sûr? o/n ")
  if aff=='o':
    cur = conn.cursor()
    cur.execute("SELECT MAX(numero_fournisseur) FROM Fournisseurs ")
    maxi = cur.fetchall()
    maxi = maxi[0][0]
    idf = int(maxi) + 1 

    print(idf)
    cur.execute("INSERT INTO  Fournisseurs VALUES (?,?,?); ",(idf,nomf,adrs))
    conn.commit()###############Validé######################

    print("Le fournisseur ",nomf," à l'adresse",adrs," attribué au numéro ",idf," a été inséré avec succés !\n")
    input("Tapez pour retourner au menu Administrateur \n")

  if aff=='n':
    input("Annulation de l'insertion\nTapez pour retourner au menu Administrateur \n")

def Ajouter_TypesArticles(conn,tp='erreur input aj typesarticles',manuel=False): 
  cur = conn.cursor()
  os.system("cls||clear")
  print("\n\t\t\t\t----Ajout TypesArticles----\n")
  if manuel==False:
    type_article_ajouter = input("Quel type article ? ")
  else:
    type_article_ajouter=tp
  print(Categorie_OK)
  categorie_type_article = input("Dans quel rayon ? ")
  while categorie_type_article not in Categorie_OK:
    categorie_type_article = input("Dans quel rayon ? ")

  prix = input("\nEntrer prix :")
  while prix.isdigit()==False:
    prix = input("Entrer prix :")

  fournisseur_OK = numero_fournisseur_OK(conn)
  print("\nLes numeros de fournisseur_OK sont:",fournisseur_OK)
  numero_fournisseur = input("N° Fournisseur : ")
  while numero_fournisseur.isdigit()==False:
    numero_fournisseur = input("N° Fournisseur : ")
  fournisseur_OK = numero_fournisseur_OK(conn)
  Categorie_OK()
  while int(numero_fournisseur) not in fournisseur_OK:
    numero_fournisseur = input("N° Fournisseur :")  
  cur.execute("INSERT INTO TypesArticles VALUES(?,?,?,?) ",(type_article_ajouter,categorie_type_article,prix,int(numero_fournisseur)))
  conn.commit()###############Validé######################
  print("\nLe nouveau type article a été ajouté avec succé !")
  if manuel==False:
    input("\nTapez pour retourner au menu Administrateur ")   

def Ajouter_Articles(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Ajout Articles----\n\n")
  cur = conn.cursor()
  cur.execute("SELECT type_article FROM TypesArticles")
  [print(row[0]) for row in cur.fetchall()]
  liste_type_article = []
  cur.execute("SELECT type_article FROM TypesArticles")
  [liste_type_article.append(row[0]) for row in cur.fetchall()]
  #print(liste_type_article)

  type_article = input("\nQuel type d'article voulez vous inserer ? ... ") 
  d=True
  d2=True
  while (type_article not in liste_type_article) and d==True and d2==True: 
    #Réessayer si l'utulisateur entre un type qui n'existe pas
    print()
    choix=input("Est-ce un nouvel article ('o') ou bien existe-t-il déjà ('n')? ")
    while choix not in ['o','n']:
      choix=input("Est-ce un nouvel article ? o/n")

    if choix=='o':
      d=False
      print("\nVous devez d'abord inserer ce nouveau type de produit dand TypesArticles !\n")
      choix2=input("Voulez vous le faire? o/n ")
      while choix2 not in ['o','n']:
        choix2=input("Voulez vous le faire? o/n ")
      if choix2=='o':
        print("je dis oui")
        Ajouter_TypesArticles(conn,type_article,True)
      if choix2=='n':
        d2=False

    if choix=='n':
      type_article = input("Quel type d'article voulez vous inserer ? ... ")    

  if d2==False:
    input("\nTapez pour retourner au menu Administrateur ")
  
  else:
    cur.execute("SELECT count(code_article) FROM Articles WHERE type_article = (?) AND statut_article = 'disponible'", ( [type_article]))
    nbr_dispo = (cur.fetchall())[0][0]
    if(nbr_dispo == 0):
      print("\nCe produit est épuisé")
    else :
      print("\nIl en reste :",nbr_dispo)
    
    d3=True
    qte = input("\nCombiez voulez-vous en insérer : ")
    while d3==True:
      while (qte.isdigit()==False) and d3==True:
        qte = input("Combiez voulez-vous en insérer : ")
      if int(qte)>1000:
        print("Quantité limitée à 1000")
      else:
        d3=False

    if int(qte)>0:
      for i in range(0,int(qte)):
        code_article_utulise = []
        cur.execute("SELECT code_article FROM Articles")
        [code_article_utulise.append(row[0]) for row in cur.fetchall()]
        code_article_random = type_article+str(random.randint(0,1000))
        while code_article_random in code_article_utulise:
          code_article_random = type_article+str(random.randint(0,1000))
          
        cur.execute("INSERT INTO  Articles (code_article, type_article) VALUES (?,?)", (code_article_random,type_article) ) 
        conn.commit()###############Validé######################
      print("Les produits on été inséré avec succé !\n")
    else:
      print("Aucun produit n'a été ajouté !\n")
    input("\nTapez pour revenir au menu Administrateur ")

def Ajouter_Clients(conn):
  inscription(conn)

def Ajouter_Commandes(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Ajout Commandes----\n\n")

  d=True
  while d:
    numero_client_ok=[]
    cur = conn.cursor()
    cur.execute("SELECT numero_client FROM Clients")
    [numero_client_ok.append(row[0]) for row in cur.fetchall()]
    print(numero_client_ok)
    numc = input("\nQuel est le numero du client de la nouvelle commandes? \n")
    f=True
    while f:
      while not(numc.isdigit()):
        numc = input("Entrez son numero de client: ... ")
      if int(numc) in numero_client_ok :
        f=False
      else:
        numc = input("Entrez son numero de client: ... ")
    
    numero_commande = creer_commande(numc,conn)
    poursuivre_commande(numc,numero_commande,conn)
    print("La commande N°",numero_commande," a bien été ajouté",sep="")
    choix = input("Voulez vous ajouter une nouvelle commande ?o/n ... ")
    while choix not in ['o','n']:
      choix = input("Voulez vous ajouter une nouvelle commande ?o/n ... ")
    if choix=='n':
      d=False

  input("Tapez pour retourner au menu Administrateur ")
  
def Ajouter_ArticlesCommandes(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Ajout ArticlesCommandes----\n\n")

  numero_client_ok=[]
  cur = conn.cursor()
  cur.execute("SELECT numero_client FROM Clients")
  [numero_client_ok.append(row[0]) for row in cur.fetchall()]
  print(numero_client_ok)
  numc = input("\nQuel est le numero du client de la nouvelle commandes? \n")

  f=True
    
  while f:
    while not(numc.isdigit()):
      numc = input("Entrez son numero de client: ... ")
    if int(numc) in numero_client_ok :
      f=False
    else:
      numc = input("Entrez son numero de client: ... ")
      
    
  choix = input("\nVotre commande existe-t-elle ('o') ou est-ce une nouvelle commande ('n') ?")
  while choix not in ['o','n']:
    choix = input("o/n ... ")
  if choix=='n':
    numero_commande = creer_commande(numc,conn)
    
  if choix =='o':   
    liste_commande_client=[]
    cur = conn.cursor()
    cur.execute("SELECT numero_commande FROM Commandes WHERE numero_client = ? ",(numc,) )
    [liste_commande_client.append(row[0]) for row in cur.fetchall()]
    print(liste_commande_client)
    numero_commande = input("\nEntrez son numero de commande \n")

    d=True
    while d:
      while not(numero_commande.isdigit()):
        numero_commande = input("Entrez son numero de commande: ... ")
      if int(numero_commande) in liste_commande_client :
        d=False
      else:
        numero_commande = input("Entrez son numero de commande: ... ")

  poursuivre_commande(numc,numero_commande,conn)
  print("\nLa ou les commandes ont été ajoué avec succé !\n")
  input("Tapez pour retourner au menu Administrateur ")
  
def Supprimer_Articles(conn): 
  os.system("cls||clear")
  print("\n\t\t\t\t----Supprimer Articles----\n\n")
  
  liste_type_article=[]
  cur = conn.cursor()
  cur.execute("SELECT DISTINCT type_article FROM TypesArticles")
  [liste_type_article.append(row[0]) for row in cur.fetchall()]
  print(liste_type_article)
  articles_supp = input(" Quel article voulez vous supprimez ?  ")
  while articles_supp not in liste_type_article :
    articles_supp = input(" Quel  article voulez vous supprimez ?  ")

  print()
  cur.execute("SELECT count(code_article) FROM Articles WHERE type_article = (?) AND statut_article = 'disponible'", ( [articles_supp]))
  nbr_dispo = (cur.fetchall())[0][0]
  print("\nIl en reste :",nbr_dispo)
  if(nbr_dispo == 0):
    print("Ce produit est déjà epuisé ou pas présent en boutique\n")
    print("Aucun produit n'a été supprimé")
    
  else:
    d=True
    while d:
      choix=input("Combien d'articles voulez-vous supprimer? ")
      while not(choix.isdigit()):
        choix=input("Combien d'articles voulez-vous supprimer? ")
      if int(choix)<0 or int(choix)>nbr_dispo:
        print("Erreur sur la quantité")
      else:
        d=False
    
    code_article_dispo = []
    cur.execute("SELECT code_article FROM Articles WHERE type_article = (?) AND statut_article = 'disponible'",([articles_supp]))
    [code_article_dispo.append(row[0]) for row in cur.fetchall()]
    for i in range (0,int(choix)):
      celui_sup = code_article_dispo[random.randint(0,len(code_article_dispo)-1)]
      print("le produit : ",celui_sup," a été supprimé")
      cur.execute("DELETE  FROM Articles WHERE code_article = (?)",[celui_sup])
      conn.commit()###########################
      code_article_dispo.remove(celui_sup)
    print("Les Produits ont été supprimé avec succé !\n")
  input("Tapez pour retourner au menu Administrateur ")

def Changer_prix(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Changer prix----\n\n")
  liste_type_article = []
  cur = conn.cursor()
  cur.execute("SELECT DISTINCT type_article FROM TypesArticles")
  [liste_type_article.append(row[0]) for row in cur.fetchall()]
  print(liste_type_article)
  type_article = input("Quel type d'article doit changer de prix ? ")
  while type_article not in liste_type_article :
    type_article = input("Quel type d'article doit changer de prix ?" )
  new_price = input("Quel est le nouveau prix ? ")
  while not(new_price.replace(".", "", 1).isdigit()) :
    new_price = input("Quel est le nouveau prix ? ")
  
  are_you_sure = input("En êtes-vous sûr ? o/n ... ")
  while are_you_sure not in ['o','n']:
    are_you_sure = input("En êtes-vous sûr ? o/n ... ")
  if are_you_sure == 'o':
    cur.execute("UPDATE TypesArticles SET prix_type_article=(?) WHERE type_article=(?) ",(float(new_price),type_article))
          
    conn.commit()#############################Validé######################
    print("Le prix a été modifié ")
    input("Retour tapez ... ")
  if are_you_sure == 'n':
    input("Tapez pour retourer au menu Admin ")

def Supprimer_Clients(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Supprimer Clients----\n\n")
  liste_numc = []
  liste_aff_nom = []
  liste_aff_prenom = []
  cur = conn.cursor()
  cur.execute("SELECT numero_client FROM Clients")
  [liste_numc.append(row[0]) for row in cur.fetchall()]
  #print(liste_numc)

  cur.execute("SELECT nom_client FROM Clients")
  [liste_aff_nom.append(row[0]) for row in cur.fetchall()]

  cur.execute("SELECT prenom_client FROM Clients")
  [liste_aff_prenom.append(row[0]) for row in cur.fetchall()]

  print("Client N° / Nom / Prenom\n")
  for i in range(0,len(liste_numc)):
    print("N°",liste_numc[i],liste_aff_nom[i],liste_aff_prenom[i])
  
  print()
  if len(liste_numc)!=0:
    numc = input("Je supprime le client N°")
    while not(numc.isdigit()) :
      numc = input("Je supprime le client N°")  
    while  int(numc) not in liste_numc :
      numc = input("Je supprime le client N°") 
    are_you_sure = input("En êtes-vous sûr ? o/n ... ")
    while are_you_sure not in ['o','n']:
      are_you_sure = input("En êtes-vous sûr ? o/n ... ")
    if are_you_sure == 'o':
      cur.execute("DELETE FROM Clients WHERE numero_client = (?)",(int(numc),))
      conn.commit()##############
      print("Le client a été supprimé \n")
      input("Tapez pour retourer au menu Admin ")
    if are_you_sure == 'n':
      print("Aucun client n'a été supprimé\n")

  else:
    print("Il n'y a pas de client dans la base de donnée\n")
  input("Tapez pour retourer au menu Admin ")


def Supprimer_Commandes(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Supprimer Commandes----\n\n")
  liste_numero_commande = []
  cur = conn.cursor()
  cur.execute("SELECT numero_commande FROM Commandes")
  [liste_numero_commande.append(row[0]) for row in cur.fetchall()]
  print(liste_numero_commande)
  if len(liste_numero_commande)!=0:
    d=True
    while d:
      numero_commande_supp = input("Je supprime la commande N°")
      while not(numero_commande_supp.isdigit()) :
        numero_commande_supp = input("Je supprime la commande N°")  
      if  int(numero_commande_supp) in liste_numero_commande :
        d=False


    are_you_sure = input("\nEn êtes-vous sûr ? o/n ... ")
    while are_you_sure not in ['o','n']:
      are_you_sure = input("En êtes-vous sûr ? o/n ... ")
    if are_you_sure == 'o':
      cur.execute("DELETE FROM Commandes WHERE numero_commande = (?)",(int(numero_commande_supp),))
      conn.commit()##############
      print("La commande a été supprimé ")
      input("Retour tapez ... ")
    if are_you_sure == 'n':
      input("Tapez pour retourer au menu Admin ")  
  else:
    print("Il n'y a pas de commande")
    input("Tapez pour retourer au menu Admin ")

def Supprimer_ArticlesCommandes(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----Supprimer Articles Commandés----\n\n")
  liste_code_article_commande = []
  cur = conn.cursor()
  cur.execute("SELECT code_article FROM ArticlesCommandes")
  [liste_code_article_commande.append(row[0]) for row in cur.fetchall()]
  print(liste_code_article_commande)
  code_article_supp = input("Entrez le code article commandé à supprimé  ")
  while  (code_article_supp) not in liste_code_article_commande :
    code_article_supp = input("Entrez le code article commandé à supprimé ") 
  are_you_sure = input("En êtes-vous sûr ? o/n ... ")
  while are_you_sure not in ['o','n']:
    are_you_sure = input("En êtes-vous sûr ? o/n ... ")
  if are_you_sure == 'o':
    cur.execute("DELETE FROM ArticlesCommandes WHERE code_article = (?)",((code_article_supp),))
    conn.commit()##############
    print("L'article commandé a été supprimé ")
    input("Retour tapez ... ")
  if are_you_sure == 'n':
    input("Tapez pour retourer au menu Admin ")    
  return True
def Afficher_Toutes_Les_Tables(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----AFFICHAGE DE TOUTES LES TABLES----\n\n")

  cur = conn.cursor()
  print("--TABLES Fournisseurs--\n")
  cur.execute("SELECT * FROM Fournisseurs")
  [print(row) for row in cur.fetchall()]

  print("\n--TABLES TypesArticles--\n")
  cur.execute("SELECT * FROM TypesArticles")
  [print(row) for row in cur.fetchall()]
  
  print("\n--TABLES Articles--\n")
  cur.execute("SELECT * FROM Articles")
  [print(row) for row in cur.fetchall()]
  
  print("\n--TABLES Clients--\n")
  cur.execute("SELECT * FROM Clients")
  [print(row) for row in cur.fetchall()]

  print("\n--TABLES Commandes--\n")
  cur.execute("SELECT * FROM Commandes")
  [print(row) for row in cur.fetchall()]
  
  print("\n--TABLES ArticlesCommandes--\n")
  cur.execute("SELECT * FROM ArticlesCommandes")
  [print(row) for row in cur.fetchall()]

  print("\n--VIEW Clients_View--\n")
  cur.execute("SELECT * FROM Clients_View")
  [print(row) for row in cur.fetchall()]

  print("\n--VIEW Commandes_View--\n")
  cur.execute("SELECT * FROM Commandes_View")
  [print(row) for row in cur.fetchall()]

  print("\n--VIEW TypesArticles_View--\n")
  cur.execute("SELECT * FROM TypesArticles_View")
  [print(row) for row in cur.fetchall()]

  input("\nTapez pour retourner au menu Administrateur \n")
  
def Reinitialiser_tables(conn):
  os.system("cls||clear")
  print("\n\t\t\t\t----REINITIALISATION TABLES----\n\n")

  print("Etes vous sûr de réinitialiser toutes les tables? ")
  print("Les fichiers \n  Create_table_projet_drop_sql\n  Insert_Ok_projet\nseront mis à jour et supprimeront\n toutes les autres données n'y figurant pas\n\n")
  choix=input("OUI/NON ? ")
  while choix not in ['OUI','NON']:
    choix=input("OUI/NON ? ")

  if choix =='OUI':
    db.mise_a_jour_bd(conn, "data/Create_table_projet_drop.sql")
    db.mise_a_jour_trigger(conn, "data/Trigger_projet.sql")
    db.mise_a_jour_bd(conn, "data/Insert_Ok_projet.sql")
    Afficher_Toutes_Les_Tables(conn)

  if choix =='NON':
    os.system("cls||clear")
    print("\n\t\t\t\t----REINITIALISATION TABLES----\n\n")
    print("Rien a été modifié\n")
    input("Tapez pour retourner au menu Administrateur")








if __name__ == "__main__":
    main()