import pymysql 
from datetime import datetime

con=pymysql.Connection(
    host='localhost',
    port=3306,
    user='root',
    password=None,
    database='nim_game'
    )

def initialiser_bd():
    with con.cursor() as cur:
        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS joueurs(
                            id            INT           PRIMARY KEY AUTO_INCREMENT ,
                            nom           VARCHAR(20)   NOT NULL UNIQUE,
                            date_creation DATETIME      DEFAULT NOW(),
                            score_total   INT           DEFAULT 0,
                            victoires     INT           DEFAULT 0,
                            defaites      INT           DEFAULT 0 """)
            con.commit()
        except pymysql.Error as e:
            con.rollback()

        try:
            cur.execute("""CREATE TABLE IF NOT EXISTS parties(
                            id              INT          AUTO_INCREMENT PRIMARY KEY,
                            joueur1_id      INT          NOT NULL,
                            joueur2_id      INT,
                            mode_jeu        VARCHAR(10)  NOT NULL,
                            niveau_ia       INT          DEFAULT 0,
                            piles_initiales VARCHAR(100) NOT NULL,
                            gagnant_id      INT,
                            perdant_id      INT,
                            date_partie     DATETIME     DEFAULT NOW(),
                            duree_secondes  INT          DEFAULT 0,
                            nb_coups        INT          DEFAULT 0,
                            FOREIGN KEY (joueur1_id) REFERENCES joueurs(id),
                            FOREIGN KEY (joueur2_id) REFERENCES joueurs(id))""")
            con.commit()
        except pymysql.Error as e:
            con.rollback()

def creer_joueur(nom):
    with con.cursor() as cur:
        try:
            cur.execute("INSERT INTO joueurs (nom) VALUES (%s)",(nom,))
            con.commit()
            joueur_id=cur.lastrowid
            return True,joueur_id
        except pymysql.err.IntegrityError:
            return False,"Ce pseudo est déjà utilisé."
        except Exception as e:
            return False,str(e)
        
def get_tous_joueurs():
    joueurs=[]
    with con.cursor() as cur:
        cur.execute("SELECT * FROM joueurs ORDER BY score_total DESC")
        joueurs=cur.fetchall()
    return joueurs

def get_joueur_par_id(joueur_id):
    row=[]
    with con.cursor() as cur:
        cur.execute("SELECT * FROM joueurs WHERE id=%s",(joueur_id,))
        row=cur.fetchone()
    return row

def get_joueur_par_nom(nom):
    row=[]
    with con.cursor() as cur:
        cur.execute("SELECT * FROM joueurs WHERE nom=%s",(nom.strip(),))
        row=cur.fetchone()
    return row

def mettre_a_jour_stats(joueur_id,victoire=0,defaite=0,points=0):
    with con.cursor() as cur:
        try:
            cur.execute("""UPDATE joueurs 
                        SET score_total=score_total+%s,
                            victoires=victoires+%s,
                            defaites=defaites+%s
                            WHERE id=%s """,(points,int(victoire),int(defaite),joueur_id))
            con.commit()
        except pymysql.Error as e:
            con.rollback()

def supprimer_joueur(joueur_id):
    with con.cursor() as cur:
        try:
            cur.execute("DELETE FROM parties WHERE joueur1_id=%s OR joueur2_id=%s",(joueur_id,joueur_id))
            cur.execute("DELETE FROM joueurs WHERE id=%s",(joueur_id,))
            con.commit()
        except pymysql.Error as e:
            con.rollback()

def enregistrer_partie(joueur1_id,joueur2_id,mode_jeu,niveau_ia,piles_initiales,gagnant_id,perdant_id,duree_secondes,nb_coups):
    piles_str=",".join(str(p) for p in piles_initiales)
    with con.cursor() as cur:
        try:
            cur.execute("""INSERT INTO parties
                    (joueur1_id, joueur2_id, mode_jeu, niveau_ia, piles_initiales,gagnant_id, perdant_id, duree_secondes, nb_coups)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,(joueur1_id,joueur2_id,mode_jeu,niveau_ia,piles_str,
                                                                    gagnant_id, perdant_id, duree_secondes, nb_coups))
            con.commit()
        except pymysql.Error as e:
            con.rollback()
            
def get_historique_joueur(joueur_id,limite=20):
    parties=[]
    with con.cursor() as cur:
        cur.execute("""SELECT parties.*,j1.nom,j2.nom,jg.nom FROM parties
                LEFT JOIN joueurs j1 ON parties.joueur1_id=j1.id
                LEFT JOIN joueurs j2 ON parties.joueur2_id=j2.id
                LEFT JOIN joueurs jg ON parties.gagnant_id=jg.id
                WHERE parties.joueur1_id=%s OR parties.joueur2_id=%s
                ORDER BY parties.date_partie DESC
                LIMIT %s """, (joueur_id,joueur_id,limite))
        parties=cur.fetchall()
        
    return parties

def get_statistiques_globales():
    with con.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM parties")
        total=cur.fetchone()

        cur.execute("SELECT AVG(duree_secondes) FROM parties WHERE duree_secondes>0")
        moy_row=cur.fetchone()
        moy=round(moy_row[0]) if moy_row and moy_row[0] is not None else 0

        cur.execute("""SELECT niveau_ia,COUNT(*) FROM parties WHERE mode_jeu='JcIA' GROUP BY niveau_ia ORDER BY niveau_ia """)
        par_niveau=cur.fetchall()

        cur.execute("""SELECT nom,score_total,victoires,defaites,(victoires+defaites+nuls) FROM joueurs WHERE (victoires+defaites)>0
                        ORDER BY score_total DESC,victoires DESC """)
        classement=cur.fetchall()

        return(total,moy,par_niveau,classement)
    
def get_evolution_score(joueur_id):
    parties=[]
    with con.cursor() as cur:
        cur.execute("""SELECT date_partie,CASE WHEN gagnant_id=%s THEN 1 ELSE 0 END
                        FROM parties
                        WHERE joueur1_id=%s OR joueur2_id=%s
                        ORDER BY date_partie ASC """,(joueur_id, joueur_id, joueur_id))
        parties=cur.fetchall()

    scores=[]
    score=0
    for p in parties:
        if p[1]==1:
            score+=10 
        else:
            score-=5 
        scores.append(score)
    return scores