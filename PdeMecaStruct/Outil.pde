// L'objet de type Outil sert à proposer des outils pour l'élaboration du treillis.
// Ces objets sont affichés en haut de la fenêtre dans le menu

class Outil { 
  // Position de l'outil
  PVector pos = new PVector(0,0);
  // Type de l'outil
  char type;
  
  Outil (char type_) {  
    // Le constructeur de l'outil lui assigne un type représenté par un simple charactère
    type = type_;
  }
  
  void afficher(PVector pos_) { 
    // Afficher un cercle avec le type de l'outil écrit au centre
    pos = pos_;
    float rayon = pos.y;
    circle(pos.x, pos.y, rayon);
    fill(0);
    textSize(20);
    textAlign(CENTER, CENTER);
    text(type, pos.x, pos.y);
    // Surligner l'outil sur laquelle se trouve la souris
    if(dist(mouseX, mouseY, pos.x, pos.y) < rayon/2){
      fill(100,100);
      circle(pos.x, pos.y, rayon);
    }
    fill(255);
  }  
}
