;// L'objet de type Barre à deux extremité n1 et n2

class Barre { 
  // Position des deux extemités
  PVector n1, n2;
  // Liste des deux noeuds qui lui servent d'extremités
  ArrayList<Noeud> attaches = new ArrayList<Noeud>();
  float len; // Longueur de la barre
  String index;
  color c;
  
  Barre (Noeud n1_, Noeud n2_) {  
    // Le constructeur de barre prend deux noeuds et donne leur position comme extremités de la barre
    n1 = n1_.pos; 
    n2 = n2_.pos;
    len = dist(n1.x, n1.y, n2.x, n2.y);
    index = str(n1_.index) + str(n2_.index);
    c = color(0);
  }
  
  void afficher() { 
    // La barre est déssinée comme une simple ligne
    stroke(c);
    line(n1.x, n1.y, n2.x, n2.y);
  }  
}
