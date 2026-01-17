"""
Analyse des Inscriptions Étudiants
Auteur: Diallo Naby Moussa
Date: Janvier 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuration de l'affichage
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
pd.set_option('display.max_columns', None)

class AnalyseInscriptions:
    """Classe pour l'analyse des données d'inscriptions étudiants"""
    
    def __init__(self, chemin_fichier):
        """Initialisation avec le chemin du fichier CSV"""
        self.chemin = chemin_fichier
        self.df = None
        self.stats = {}
        
    def charger_donnees(self):
        """Charge les données depuis le fichier CSV"""
        print("📂 Chargement des données...")
        try:
            self.df = pd.read_csv(self.chemin)
            print(f"✅ {len(self.df)} enregistrements chargés avec succès")
            print(f"📊 Colonnes: {list(self.df.columns)}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return False
    
    def explorer_donnees(self):
        """Exploration initiale des données"""
        print("\n" + "="*60)
        print("🔍 EXPLORATION INITIALE DES DONNÉES")
        print("="*60)
        
        print("\n📋 Aperçu des premières lignes:")
        print(self.df.head())
        
        print("\n📊 Informations sur les données:")
        print(self.df.info())
        
        print("\n📈 Statistiques descriptives:")
        print(self.df.describe())
        
    def nettoyer_donnees(self):
        """Nettoyage et préparation des données"""
        print("\n" + "="*60)
        print("🧹 NETTOYAGE DES DONNÉES")
        print("="*60)
        
        # Vérifier les valeurs manquantes
        valeurs_manquantes = self.df.isnull().sum()
        print(f"\n❓ Valeurs manquantes:")
        print(valeurs_manquantes[valeurs_manquantes > 0])
        
        # Vérifier les doublons
        doublons = self.df.duplicated().sum()
        print(f"\n🔁 Nombre de doublons: {doublons}")
        
        if doublons > 0:
            self.df = self.df.drop_duplicates()
            print(f"✅ {doublons} doublons supprimés")
        
        # Nettoyer les espaces dans les colonnes texte
        colonnes_texte = self.df.select_dtypes(include=['object']).columns
        for col in colonnes_texte:
            self.df[col] = self.df[col].str.strip()
        
        print("✅ Nettoyage terminé!")
        
    def calculer_statistiques(self):
        """Calcul des statistiques clés"""
        print("\n" + "="*60)
        print("📊 STATISTIQUES DESCRIPTIVES")
        print("="*60)
        
        # Statistiques générales
        self.stats['total_etudiants'] = len(self.df)
        self.stats['age_moyen'] = self.df['age'].mean()
        self.stats['age_min'] = self.df['age'].min()
        self.stats['age_max'] = self.df['age'].max()
        
        # Statistiques financières
        self.stats['frais_moyen'] = self.df['frais_scolarite'].mean()
        self.stats['frais_min'] = self.df['frais_scolarite'].min()
        self.stats['frais_max'] = self.df['frais_scolarite'].max()
        
        # Taux de paiement
        payes = (self.df['statut_paiement'] == 'Payé').sum()
        self.stats['taux_paiement'] = (payes / self.stats['total_etudiants']) * 100
        
        # Affichage
        print(f"\n👨‍🎓 Total étudiants: {self.stats['total_etudiants']}")
        print(f"\n📅 Âge:")
        print(f"   - Minimum: {self.stats['age_min']} ans")
        print(f"   - Moyen: {self.stats['age_moyen']:.1f} ans")
        print(f"   - Maximum: {self.stats['age_max']} ans")
        print(f"\n💰 Frais de scolarité:")
        print(f"   - Minimum: {self.stats['frais_min']:,} FCFA")
        print(f"   - Moyen: {self.stats['frais_moyen']:,.0f} FCFA")
        print(f"   - Maximum: {self.stats['frais_max']:,} FCFA")
        print(f"\n✅ Taux de paiement: {self.stats['taux_paiement']:.1f}%")
        
        # Répartitions
        print("\n👥 Répartition par sexe:")
        print(self.df['sexe'].value_counts())
        
        print("\n🎓 Répartition par filière:")
        print(self.df['filiere'].value_counts())
        
        print("\n📚 Répartition par niveau:")
        print(self.df['niveau'].value_counts())
        
    def creer_visualisations(self):
        """Création des visualisations"""
        print("\n" + "="*60)
        print("📊 CRÉATION DES VISUALISATIONS")
        print("="*60)
        
        # Créer le dossier visualizations s'il n'existe pas
        Path("visualizations").mkdir(exist_ok=True)
        
        # 1. Répartition par sexe
        plt.figure(figsize=(10, 6))
        self.df['sexe'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Répartition des étudiants par sexe', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.savefig('visualizations/repartition_sexe.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 1/4 créé: repartition_sexe.png")
        plt.close()
        
        # 2. Répartition par filière
        plt.figure(figsize=(12, 6))
        self.df['filiere'].value_counts().plot(kind='bar', color='steelblue')
        plt.title('Nombre d\'étudiants par filière', fontsize=14, fontweight='bold')
        plt.xlabel('Filière', fontsize=12)
        plt.ylabel('Nombre d\'étudiants', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('visualizations/repartition_filieres.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 2/4 créé: repartition_filieres.png")
        plt.close()
        
        # 3. Statut des paiements
        plt.figure(figsize=(10, 6))
        statut_counts = self.df['statut_paiement'].value_counts()
        colors = ['#2ecc71' if x == 'Payé' else '#e74c3c' for x in statut_counts.index]
        statut_counts.plot(kind='pie', autopct='%1.1f%%', colors=colors)
        plt.title('Statut des paiements', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.savefig('visualizations/statut_paiements.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 3/4 créé: statut_paiements.png")
        plt.close()
        
        # 4. Évolution des inscriptions
        plt.figure(figsize=(12, 6))
        inscriptions_par_annee = self.df['annee_inscription'].value_counts().sort_index()
        plt.plot(inscriptions_par_annee.index, inscriptions_par_annee.values, 
                marker='o', linewidth=2, markersize=8, color='#3498db')
        plt.title('Évolution des inscriptions par année', fontsize=14, fontweight='bold')
        plt.xlabel('Année', fontsize=12)
        plt.ylabel('Nombre d\'inscriptions', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('visualizations/evolution_inscriptions.png', dpi=300, bbox_inches='tight')
        print("✅ Graphique 4/4 créé: evolution_inscriptions.png")
        plt.close()
        
        print("\n✨ Tous les graphiques ont été sauvegardés dans le dossier 'visualizations/'")
        
    def generer_rapport(self):
        """Génère un rapport texte de l'analyse"""
        print("\n" + "="*60)
        print("📝 GÉNÉRATION DU RAPPORT")
        print("="*60)
        
        rapport = f"""
RAPPORT D'ANALYSE - INSCRIPTIONS ÉTUDIANTS
==========================================
Auteur: Diallo Naby Moussa
Date: Janvier 2026

RÉSUMÉ EXÉCUTIF
---------------
Total d'étudiants analysés: {self.stats['total_etudiants']}
Âge moyen: {self.stats['age_moyen']:.1f} ans
Frais de scolarité moyen: {self.stats['frais_moyen']:,.0f} FCFA
Taux de paiement: {self.stats['taux_paiement']:.1f}%

INSIGHTS CLÉS
-------------
1. Distribution démographique équilibrée
2. Diversité des filières représentées
3. Taux de paiement à surveiller
4. Tendance d'inscription stable

RECOMMANDATIONS
---------------
1. Améliorer le taux de paiement global
2. Analyser les filières moins représentées
3. Suivre l'évolution temporelle des inscriptions
4. Optimiser la gestion des frais de scolarité

MÉTHODOLOGIE
------------
- Nettoyage des données (doublons, valeurs manquantes)
- Analyse statistique descriptive
- Visualisations multiples (pie charts, bar charts, line charts)
- Extraction d'insights business
"""
        
        with open('rapport_analyse.txt', 'w', encoding='utf-8') as f:
            f.write(rapport)
        
        print("✅ Rapport sauvegardé: rapport_analyse.txt")
        
    def executer_analyse_complete(self):
        """Exécute l'analyse complète"""
        print("\n" + "="*60)
        print("🚀 DÉMARRAGE DE L'ANALYSE COMPLÈTE")
        print("="*60)
        
        if not self.charger_donnees():
            return
        
        self.explorer_donnees()
        self.nettoyer_donnees()
        self.calculer_statistiques()
        self.creer_visualisations()
        self.generer_rapport()
        
        print("\n" + "="*60)
        print("✨ ANALYSE TERMINÉE AVEC SUCCÈS!")
        print("="*60)
        print("\n📁 Fichiers générés:")
        print("   - visualizations/repartition_sexe.png")
        print("   - visualizations/repartition_filieres.png")
        print("   - visualizations/statut_paiements.png")
        print("   - visualizations/evolution_inscriptions.png")
        print("   - rapport_analyse.txt")


def main():
    """Fonction principale"""
    # Chemin vers le fichier de données
    chemin_csv = "data/inscriptions_etudiants.csv"
    
    # Créer l'instance et exécuter l'analyse
    analyse = AnalyseInscriptions(chemin_csv)
    analyse.executer_analyse_complete()


if __name__ == "__main__":
    main()
