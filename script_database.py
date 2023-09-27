from itertools import permutations
import argparse

base_de_donnees = {
    "Cacao": {"vert"},
    "Lait": {"bleu", "jaune"},
    "Beurre": {"bleu", "jaune", "blanc"},
    "Noisette": {"rouge"},
    "Savourine": {"bleu", "vert", "blanc"}
}


def filtrer_cles_base_de_donnees(list_jetons):
    resultats = []
    for key in base_de_donnees :
        valid_key=True
        for elem in base_de_donnees[key] :
            if list_jetons[elem] == 0 :
                valid_key=False
                break
        if valid_key :
            resultats.append(key)
    return resultats
    


def renvois_max_possible(couleurs, vert_fc, bleu_fc, jaune_fc, blanc_fc, rouge_fc) :
    coefficients = {
        "vert": vert_fc,
        "bleu": bleu_fc,
        "jaune": jaune_fc,
        "blanc": blanc_fc,
        "rouge": rouge_fc
    }           
    if isinstance(couleurs, str):
        couleurs = [couleurs]  # Si couleurs est une chaîne, convertissez-la en une liste
    nb_possibilites = min(coefficients[couleur] for couleur in couleurs)
    new_coefficients = coefficients.copy()
    for couleur in couleurs:
        new_coefficients[couleur] -= nb_possibilites
    return nb_possibilites, new_coefficients["vert"], new_coefficients["bleu"], new_coefficients["jaune"], new_coefficients["blanc"], new_coefficients["rouge"]


def find_best_combi(list_key, vert, bleu, jaune, blanc, rouge) :
    vert_tmp = vert
    bleu_tmp = bleu
    jaune_tmp = jaune
    blanc_tmp = blanc
    rouge_tmp = rouge
    permutations_possibles = list(permutations(list_key))
    resultats = {}
    tmp_resultats={}
    nb_ingredient_max=vert_tmp+bleu_tmp+jaune_tmp+blanc_tmp+rouge_tmp
    
    for permutation in permutations_possibles:
        number_jetons = vert + bleu + jaune + blanc + rouge
        for ingredient in permutation :
            couleurs=base_de_donnees[ingredient]
            nb_ingredient, vert_tmp, bleu_tmp, jaune_tmp, blanc_tmp, rouge_tmp = renvois_max_possible(couleurs,vert_tmp, bleu_tmp, jaune_tmp, blanc_tmp, rouge_tmp)
            tmp_resultats[ingredient]= nb_ingredient
        if vert_tmp + bleu_tmp + jaune_tmp + blanc_tmp + rouge_tmp == 0 :
            return tmp_resultats
        if vert_tmp + bleu_tmp + jaune_tmp + blanc_tmp + rouge_tmp < nb_ingredient_max :
            nb_ingredient_max = vert_tmp + bleu_tmp + jaune_tmp + blanc_tmp + rouge_tmp
            resultats = tmp_resultats
        ##reset
        nb_ingredient = number_jetons
        vert_tmp = vert
        bleu_tmp = bleu
        jaune_tmp = jaune
        blanc_tmp = blanc
        rouge_tmp = rouge
    return resultats



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Donne les ingrédients à partir du nombre de jeton')
    parser.add_argument("-vert",type=int,help="Nombre de jetons vert")
    parser.add_argument("-bleu",type=int,help="Nombre de jetons bleu")
    parser.add_argument("-jaune",type=int,help="Nombre de jetons jaune")
    parser.add_argument("-blanc",type=int,help="Nombre de jetons blanc")
    parser.add_argument("-rouge",type=int,help="Nombre de jetons rouge")
    args=parser.parse_args()
    list_jetons={
        "vert" : args.vert,
        "bleu" : args.bleu,
        "jaune" : args.jaune,
        "blanc" : args.blanc,
        "rouge" : args.rouge
    }
    resultat = filtrer_cles_base_de_donnees(list_jetons)
    print(find_best_combi(resultat, args.vert, args.bleu, args.jaune, args.blanc,args.rouge))
