// Cet onglet regroupe les fonctions du curseur


void ajoutNoeud(){
  // Vérifier si le noeud n'existe pas déjà
  boolean dejaNoeud = false;
  for(Noeud n : noeuds){
    if(dist(mouseX, mouseY, n.pos.x, n.pos.y) < 10){
      dejaNoeud = true;
    }
  }
  // Si il n'existe pas encore, le créer et le rajouter à l'ensemble de noeud
  if(!dejaNoeud){
    noeuds.add(new Noeud(mouseX, mouseY));
  }
}


void supNoeud(){
  // Verifier que la souris est sur un noeud
  for(int i = 0; i < noeuds.size(); i++){
    PVector npos = noeuds.get(i).pos;
    if(dist(mouseX, mouseY, npos.x, npos.y) < 10){
      // Si la souris est sur un noeud, trouver les barres connecté à ce noeud
      for(int j = treillis.size()-1; j >=0; j--){
        PVector n1 = treillis.get(j).attaches.get(0).pos;
        PVector n2 = treillis.get(j).attaches.get(1).pos;
        if(dist(n1.x,n1.y,npos.x,npos.y)<10 || dist(n2.x,n2.y,npos.x,npos.y)<10){
          // Les supprimer
          treillis.remove(j);
        }
      }
      // Supprimer le noeud
      noeuds.remove(i);
    }
  }
}


void ajoutBarre(){
  for(Noeud n : noeuds){
    // Si on clique bien sur un noeud
    if(dist(mouseX, mouseY, n.pos.x, n.pos.y) < 10){
      // Si c'est le premier noeud de la barre, le sauvegarder pour plus tard
      if(construTemp){
        noeudTemp = n;
        construTemp = false;
      }else{ // Si c'est le deuxième
        boolean dejaBarre = false;
        // Vérifier que cette barre n'existe pas déja
        for(Barre b : n.liaisons){
          if(b.attaches.get(0) == noeudTemp || b.attaches.get(1) == noeudTemp){
            dejaBarre = true;
          }
        }
        // Si la barre n'existe pas encore et que les deux noeuds ne sont pas les mêmes:
        if(!dejaBarre && noeudTemp != n){
          // Créer la barre et la rajouter à l'ensemble des barres
          treillis.add(new Barre(noeudTemp, n));
          // Lier la barre aux noeuds et les noeuds à la barre
          treillis.get(treillis.size()-1).attaches.add(noeudTemp);
          treillis.get(treillis.size()-1).attaches.add(n);
          n.liaisons.add(treillis.get(treillis.size()-1));
          treillis.get(treillis.size()-1).attaches.get(0).liaisons.add(treillis.get(treillis.size()-1));
          construTemp = true;
        }
      }
    }
  }
}


void supBarre(){
  for(int i = 0; i < treillis.size(); i++){
    // Verifier quelle barre se trouve sous le curseur (avec le produit vectorielle et scalaire)
    PVector posCurseur = new PVector(mouseX, mouseY);
    PVector A = treillis.get(i).n1.copy();
    PVector B = treillis.get(i).n2.copy();
    PVector AB = B.sub(A.copy());
    PVector AC = A.sub(posCurseur.copy());
    PVector d = AC.cross(AB.copy());
    if(d.mag() < 1000){
      float Kac = AB.copy().dot(AC.copy());
      float Kab = AB.copy().dot(AB.copy());
      if(Kac < 0 && abs(Kac) < Kab){
        // Si la barre est sous le curseur, supprimer cette barre des liaisons de ses deux attaches
        for(int j = treillis.get(i).attaches.size() - 1; j >= 0; j--){
          for(int k = treillis.get(i).attaches.get(j).liaisons.size() - 1; k >= 0 ; k--){
            PVector AA = treillis.get(i).attaches.get(j).liaisons.get(k).n1.copy();
            PVector BB = treillis.get(i).attaches.get(j).liaisons.get(k).n2.copy();
            PVector AABB = BB.sub(AA.copy());
            PVector D = AABB.cross(AB);
            if(D.mag() <= 1){
              treillis.get(i).attaches.get(j).liaisons.remove(k);
            }
          }
        }
        // Puis supprimer la barre
        treillis.remove(i);
      }
    }
  }
}



void ajoutForceExt(){
  if(construTemp){
    // Verifier que le curseur est sur un noeud
    for(Noeud n : noeuds){
      if(dist(mouseX, mouseY, n.pos.x, n.pos.y) < 10){
        // Créer une force sur ce noeud
        noeudTemp = n;
        construTemp = false;
        
      }
    }
  }else{
    noeudTemp.forceExt = new PVector(mouseX - noeudTemp.pos.x, mouseY - noeudTemp.pos.y);
    construTemp = true;
  }
}

void supForceExt(){
  // Verifier que le curseur est sur un noeud
  for(Noeud n : noeuds){
    if(dist(mouseX, mouseY, n.pos.x, n.pos.y) < 10){
      // Supprimer la force sur ce noeud
      n.forceExt = new PVector(0, 0);
    }
  }
}


void changeAttache(){
  // Verifier que le curseur est sur un noeud
  for(Noeud n : noeuds){
    if(dist(mouseX, mouseY, n.pos.x, n.pos.y) < 10){
      // Changer le type d'attache
      if(n.typeAttache == 'l'){
        n.typeAttache = 'x'; // Type roulant en x
      } else if(n.typeAttache == 'x'){
        n.typeAttache = 'y'; // Type roulant en y
      }else if(n.typeAttache == 'y'){
        n.typeAttache = 'f'; // Type fixe
      }else if(n.typeAttache == 'f'){
        n.typeAttache = 'l'; // Type libre
      }
    }
  }
}
