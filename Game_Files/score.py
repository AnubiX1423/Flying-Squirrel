def read_score():
    with open("best_score.txt", "rt") as f:
        return int(f.read().strip())
    
def update_text(score):
    with open("best_score.txt", "wt") as v:
        v.write(str(score))