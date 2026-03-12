/*
Projet Calcul Mécanique des Structures
Commencé le 07/02/2026
Ce programme calcul les forces de réaction dans les barres d'un treillis
*/

// Création de l'ensemble de noeud et de l'ensemble de barre (pour l'instant vide)
ArrayList<Barre> treillis = new ArrayList<Barre>();
ArrayList<Noeud> noeuds = new ArrayList<Noeud>();

// Création de l'ensemble des outils
ArrayList<Outil> outils = new ArrayList<Outil>();
char typeOutil; // Permet de determiner le mode du curseur

int nbrInco, nbrEqua; // Nombre d'inconnues et d'équations à comparer pour resoudre le treillis
int indexNoeud = 0; // Index pour numéroter les noeuds

// Variables qui nous permettrons de construire une barre
boolean construTemp = true;
Noeud noeudTemp = new Noeud(0,0);


void setup(){
  // La fonction d'initialisation "setup" va définir la taille de notre fenêtre
  size(500,500);
  
  // Construction des outils
  outils.add(new Outil('S')); // Selection
  outils.add(new Outil('N')); // Ajout de noeud
  outils.add(new Outil('n')); // Suppression de noeud
  outils.add(new Outil('B')); // Ajout de barre
  outils.add(new Outil('b')); // Suppression de barre
  outils.add(new Outil('A')); // Modifier le type d'attache d'un noeud
  outils.add(new Outil('F')); // Ajouter une force extérieure à un noeud
  outils.add(new Outil('f')); // Supprimer une force extérieure à un noeud
  
  typeOutil = outils.get(0).type; // Le curseur est en mode selection
}


void draw(){
  // La fonction "draw" va tourner en boucle.
  background(255); // Fond d'ecran blanc
  
  // Couleur de fond du menu
  fill(200);
  noStroke();
  rect(0 ,0 ,width , 2*outils.get(0).pos.y);
  fill(255);
  stroke(0);
  
  // Positionner et Afficher tout les outils
  for(int i = 0; i < outils.size(); i++){
    float xOutil = map(i, -1, outils.size(), 0, width);
    int yOutil = 30;
    outils.get(i).afficher(new PVector(xOutil, yOutil));
  }
  
  // Dessiner tout les noeuds et les barres et compter le nombre d'inconnues et d'équations
  nbrEqua = 2*noeuds.size();
  nbrInco = treillis.size();
  for(Noeud n : noeuds){
    n.afficher();
    if(n.typeAttache == 'x' || n.typeAttache == 'y'){
      nbrInco += 1;
    }else if(n.typeAttache == 'f'){
      nbrInco += 2;
    }
  }
  for(Barre b : treillis){
    b.afficher();
  }
  fill(0);
  textSize(12);
  textAlign(CORNER);
  text("Nombre d'inconnues : "+nbrInco+"\nNombre d'équations : "+nbrEqua, 10, 80);
  fill(255);
}





void mousePressed(){ // Quand le bouton de souris est préssé:
  if(mouseY < 2*outils.get(0).pos.y){
    // Si le curseur est préssé dans la zone menu:
    for(Outil o : outils){
      if(dist(mouseX, mouseY, o.pos.x, o.pos.y) < o.pos.y){
        typeOutil = o.type;
      }
    }
    construTemp = true; // Retour à l'étape 0 de contruction de barre
  }
  else{
    // Sinon, selon le mode du curseur:
    switch(typeOutil){
      case 'S': // Cas sélection
        construTemp = true;
        break;
      case 'N': // Cas ajout de oeud
        ajoutNoeud();
        break;
      case 'n': // Cas suppression de noeud
        supNoeud();
        break;
      case 'B': // Cas ajout de barre
        ajoutBarre();
        break;
      case 'b': // Cas suppression de barre
        supBarre();
        break;
      case 'A': // Cas modification du type d'attache d'un noeud
        changeAttache();
        break;
      case 'F': // Cas ajout de force extérieure à un noeud
        ajoutForceExt();
        break;
      case 'f': // Cas suppression de force extérieure à un noeud
        supForceExt();
        break;
    }
  }
}

void keyPressed(){
  // Lorsqu'une touche est préssée, on résoud le système si le système est isostatique
  if(nbrEqua == nbrInco){
    resoSysteme();
  }else if(nbrEqua > nbrInco){
    println("Le système est hypotatique");
  }else{
    println("Le système est hyperstatique");
  }
  println();
}
