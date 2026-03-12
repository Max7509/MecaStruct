void resoSysteme(){
  // On initialise la matrice représentant les équations à résoudre
  float[][] matriceEquation = construMatrice();
  
  // On inverse cette matrice
  matriceEquation = inverseMatrice(matriceEquation);
  // On vérifie que la solution existe
  if(matriceEquation == null){
    println("Système irrésoluble, peut être pas statique ?");
  }else{
    // On multiplie l'inverse par le vecteurs des forces extérieures
    float[] solutions = resolution(matriceEquation);
    
    // Impressions des solutions du système :
    println("Solutions du système : ");
    for(int j = 0; j < solutions.length; j++){
      if(j < treillis.size()){
        println("N"+treillis.get(j).index+" = "+solutions[j]);
        // Changer la couleur des barres selon la cas compression/traction
        if(solutions[j] < -2){
          treillis.get(j).c = color(0,0,255);
        }else if(solutions[j] > 2){
          treillis.get(j).c = color(255,0,0);
        }
      }
    }
    int n = treillis.size();;
    for(int i = 0; i< noeuds.size(); i++){
      if(noeuds.get(i).typeAttache == 'x'){
        println("R"+noeuds.get(i).index+"y = "+solutions[n]);
        n++;
      }else if(noeuds.get(i).typeAttache == 'y'){
        println("R"+noeuds.get(i).index+"x = "+solutions[n]);
        n++;
      }else if(noeuds.get(i).typeAttache == 'f'){
        println("R"+noeuds.get(i).index+"x = "+solutions[n]);
        println("R"+noeuds.get(i).index+"y = "+solutions[n+1]);
        n+=2;
      }
    }
    println();
  }
}





float[][] construMatrice(){
  // Création de la matrice
  float[][] matrice = new float[nbrInco][nbrEqua];
  
  int attacheIndex = treillis.size(); // Permet de trouver la colonne où rajouter l'attaches
  // Boucle sur toutes les lignes de la matrice, deux lignes pour un noeud
  // Deux par deux car ont a une ligne en x et une en y à chaque fois
  for(int j = 0; j < nbrInco - 1; j+=2){
    // Boucle sur les premières colonnes correspondant à chaque barres
    for(int i = 0; i < treillis.size(); i++){
      // Si le noeud de la ligne est attaché à la barre de la colonne, la case est un cosinus ou sinus (x ou y)
      if(treillis.get(i).attaches.get(0) == noeuds.get(j/2)){
        matrice[i][j] = (treillis.get(i).attaches.get(1).pos.x - noeuds.get(j/2).pos.x)/treillis.get(i).len;
        matrice[i][j+1] = (treillis.get(i).attaches.get(1).pos.y - noeuds.get(j/2).pos.y)/treillis.get(i).len;
      }else if(treillis.get(i).attaches.get(1) == noeuds.get(j/2)){
        matrice[i][j] = (treillis.get(i).attaches.get(0).pos.x - noeuds.get(j/2).pos.x)/treillis.get(i).len;
        matrice[i][j+1] = (treillis.get(i).attaches.get(0).pos.y - noeuds.get(j/2).pos.y)/treillis.get(i).len;
      }
    }
    // Ensuite, chaque colonne représente une attache
    for(Noeud n : noeuds){
      if(n.typeAttache == 'x' && n == noeuds.get(j/2)){
        matrice[attacheIndex][j  ] = 0;
        matrice[attacheIndex][j+1] = 1;
        attacheIndex +=1;
      }else if(n.typeAttache == 'y' && n == noeuds.get(j/2)){
        matrice[attacheIndex][j  ] = 1;
        matrice[attacheIndex][j+1] = 0;
        attacheIndex +=1;
      }else if(n.typeAttache == 'f' && n == noeuds.get(j/2)){
        matrice[attacheIndex  ][j  ] = 1;
        matrice[attacheIndex  ][j+1] = 0;
        matrice[attacheIndex+1][j  ] = 0;
        matrice[attacheIndex+1][j+1] = 1;
        attacheIndex +=2;
      }
    }
  }
  
  return matrice;
}



// Fonction pour trouver l'inverse de la matrice algorithme de Gauss-Jordan
float[][] inverseMatrice(float[][] A) {
  int n = A.length;
  // Matrice matriceAugmentée [A | I]
  float[][] matriceAug = new float[n][2*n];
  for(int i = 0; i < n; i++){
    for(int j = 0; j < n; j++) matriceAug[i][j] = A[i][j];
    for(int j = 0; j < n; j++) matriceAug[i][n + j] = (i == j) ? 1.0 : 0.0;
  }

  float seuil = 1e-7; // seuil pour les matrices singulières (mécanismes, matrices pas inversibles)

  for(int col = 0; col < n; col++){
    // 1) Chercher le pivot
    int colPivot = col;
    float max = abs(matriceAug[col][col]);
    for(int row = col + 1; row < n; row++){
      float v = abs(matriceAug[row][col]);
      if(v > max){
        max = v;
        colPivot = row;
      }
    }
    // 2) Vérifier si il y a des singularités
    if (max < seuil) {
      println("Matrice singulière (pivot ~ 0) à col = " + col);
      return null;
    }
    // 3) Echanger colPivot et col
    if(colPivot != col){
      float[] temp = matriceAug[colPivot];
      matriceAug[colPivot] = matriceAug[col];
      matriceAug[col] = temp;
    }
    // 4) Normaliser la ligne pivot
    float pivot = matriceAug[col][col];
    for(int j = 0; j < 2*n; j++) matriceAug[col][j] /= pivot;
    // 5) Éliminer les autres lignes
    for(int row = 0; row < n; row++){
      if(row == col) continue;
      float facteur = matriceAug[row][col];
      if(abs(facteur) < seuil) continue;
      for(int j = 0; j < 2*n; j++){
        matriceAug[row][j] -= facteur * matriceAug[col][j];
      }
    }
  }
  // On retourne l'inverse
  float[][] inv = new float[n][n];
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) inv[i][j] = matriceAug[i][n + j];
  }
  return inv;
}



// Fonction qui permet de résoudre le système en multipliant l'inverse de notre fonction par le vecteurs des forces appliquées aux noeuds
float[] resolution(float[][] matrice){
  float[] solutions = new float[matrice.length];
  float[] forces = new float[matrice.length];
  println("Forces exterieures");
  for(int i = 0; i< forces.length; i+=2){
    forces[i  ] = -noeuds.get(i/2).forceExt.x;
    forces[i+1] = -noeuds.get(i/2).forceExt.y;
    println("F"+(i/2+1)+"x = "+(-forces[i  ]));
    println("F"+(i/2+1)+"y = "+(-forces[i+1]));
  }
  for(int j = 0; j< matrice.length; j++){
    solutions[j] = 0;
    for(int i = 0; i< matrice.length; i++){
      solutions[j] += matrice[i][j] * forces[i];
    }
  }
  return solutions;
}
