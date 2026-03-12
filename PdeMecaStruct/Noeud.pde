// L'objet Noeud à une position et des barres qui lui sont accrochées

class Noeud {
  // Position du noeud
  PVector pos;
  // Liste des barres accrochées à ce noeud
  ArrayList<Barre> liaisons = new ArrayList<Barre>();
  char typeAttache = 'l'; // Par défaut les noeuds sont libres
  PVector forceExt = new PVector(0,0); // Force exterieure appliqué sur le noeud
  PVector reaction = new PVector(0,0); // Réaction du support sur le noeud
  int index; // Numéro du noeud. Juste pour l'affichage
  
  Noeud (int x_, int y_) {  
    // Le constructeur de cet objet lui donne sa postion
    pos = new PVector(x_, y_); 
    index = indexNoeud;
    indexNoeud++;
  } 
  
  void afficher() { 
    // Le noeud est déssiné comme un simple point noir avec son index
    fill(0);
    circle(pos.x, pos.y, 15);
    fill(255);
    text(index, pos.x, pos.y);
    
    // Afficher la force exterieure
    if(forceExt.mag() > 1){
      stroke(100);
      line(pos.x, pos.y, pos.x + forceExt.x, pos.y + forceExt.y);
    }
    
    // Afficher le type d'attache
    stroke(150);
    noFill();
    if(typeAttache == 'f'){
      triangle(pos.x, pos.y, pos.x + 20, pos.y + 30, pos.x - 20, pos.y + 30);
      rect(pos.x - 20, pos.y + 30, 40, 20);
    }else if(typeAttache == 'x'){
      // Noeud roulant sur x : reactions seulement en Y
      reaction.x = 0;
      triangle(pos.x, pos.y, pos.x + 20, pos.y + 30, pos.x - 20, pos.y + 30);
      circle(pos.x - 10, pos.y + 40, 20);
      circle(pos.x + 10, pos.y + 40, 20);
    }else if(typeAttache == 'y'){
      // Noeud roulant sur y : reactions seulement en X
      reaction.y = 0;
      triangle(pos.x, pos.y, pos.x - 30, pos.y + 20, pos.x - 30, pos.y - 20);
      circle(pos.x - 40, pos.y - 10, 20);
      circle(pos.x - 40, pos.y + 10, 20);
    }else{
      // Noeud sans attaches : pas de reactions du support
      reaction.x = 0;
      reaction.y = 0;
    }
    stroke(0);
  }
}
