import time, os, sys, random, msvcrt, json, base64

CHEMIN_DU_DOSSIER = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(CHEMIN_DU_DOSSIER, "save.json")
W, H = 10, 5
MSG = ""
LAST_INPUT = time.time()

def load():
    default = {"full_score": 0, "_fs_m": 0, "skins": {"P":"P","M":"M","#":"#","x":"x"}, "inv": ["P","M","#","x"], "hi": []}
    if not os.path.exists(FILE):
        with open(FILE, "w") as f: json.dump(default, f)
        return default
    try:
        data = json.load(open(FILE))
        for k, v in default.items():
            if k not in data: data[k] = v
        return data
    except: return default

D = load()

def save():
    D["_fs_m"] = D["full_score"]
    with open(FILE, "w") as f: json.dump(D, f)

def get_key():
    global LAST_INPUT
    if msvcrt.kbhit():
        now = time.time()
        if now - LAST_INPUT < 0.02: return "SPEED"
        LAST_INPUT = now
        ch = msvcrt.getch()
        if ch in [b'\x00', b'\xe0']:
            return {b'H':'up', b'P':'down', b'K':'left', b'M':'right'}.get(msvcrt.getch(), None)
        return ch.decode('utf-8').lower()
    return None

def screen(title, options):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== {title} ===")
    if MSG: print(f">> {MSG} <<")
    print("-" * 45)
    for o in options: print(o)
    print("=" * 45)

def editor():
    curr_w, curr_m = [], []
    ex, ey = 0, 0
    while True:
        os.system('cls')
        print("=== ÉDITEUR DE NIVEAU HAPPY PIXELZ ===")
        print("ZQSD: Bouger | M: Mur | Z: Zombie | S: Sauvegarder | ESC: Quitter")
        print("-" * 35)
        for y in range(H):
            ln = ""
            for x in range(W):
                char = "."
                if (x,y) == (ex,ey): char = "X"
                elif (x,y) in curr_w: char = "#"
                elif [x,y] in curr_m: char = "M"
                elif (x,y) == (9,4): char = "!"
                ln += char + " "
            print(ln)
        k = None
        while not k: k = get_key(); time.sleep(0.01)
        if k in ['up','down','left','right']:
            mv = {'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[k]
            ex = max(0, min(W-1, ex + mv[0]))
            ey = max(0, min(H-1, ey + mv[1]))
        elif k == 'm':
            if (ex,ey) in curr_w: curr_w.remove((ex,ey))
            else: curr_w.append((ex,ey))
        elif k == 'z':
            if [ex,ey] in curr_m: curr_m.remove([ex,ey])
            else: curr_m.append([ex,ey])
        elif k == 's':
            code = base64.b64encode(json.dumps({"w": curr_w, "m": curr_m}).encode()).decode()
            print(f"\nCODE NIVEAU :\n{code}\n")
            input("Appuie sur Entrée pour revenir..."); break
        elif k == '\x1b': break

def play(l_idx, custom=None):
    global MSG
    if abs(D["full_score"] - D["_fs_m"]) > 5: D["full_score"] = D["_fs_m"]

    lvls = [
        {"w": [(5,1),(5,2),(5,3)], "m": 1, "n": "Plaine"},
        {"w": [(2,0),(2,1),(2,2),(6,2),(6,3),(6,4)], "m": 2, "n": "Canyon"},
        {"w": [(3,1),(4,1),(5,1),(3,3),(4,3),(5,3),(0,2),(9,2)], "m": 3, "n": "Enfer"},
        {"w": [(1,1),(1,2),(1,3),(8,1),(8,2),(8,3),(4,0),(4,4)], "m": 4, "n": "Prison"},
        {"w": [(x,2) for x in range(1,9) if x!=5], "m": 5, "n": "L'Etroit"}
    ]
    
    if not custom and l_idx >= len(lvls): return "FINISHED", 0, 0, 0
    
    if custom:
        try:
            data = json.loads(base64.b64decode(custom))
            cfg = {"w": [tuple(x) for x in data["w"]], "m_pos": data["m"], "n": "Custom"}
        except: return "ERROR", 0, 0, 0
    else:
        cfg = lvls[l_idx]
        cfg["m_pos"] = [[random.randint(1,9), random.randint(0,4)] for _ in range(cfg["m"])]

    px, py, lives, bul, deaths = 0, 0, 2, True, 0
    m_d = [[m[0], m[1], False] for m in cfg["m_pos"]]
    st_t, c_msg = time.time(), ""

    while True:
        os.system('cls')
        print(f"MAP: {cfg['n']} | Vies: {lives} | Balle: {1 if bul else 0}")
        if c_msg: print(f"ACTION: {c_msg}")
        for y in range(H):
            ln = ""
            for x in range(W):
                c = D['skins']['x']
                if (x,y)==(px,py): c = D['skins']['P']
                elif (x,y) in cfg["w"]: c = D['skins']['#']
                else:
                    for m in m_d:
                        if [x,y]==m[:2]: c = D['skins']['M'] if not m[2] else "@"
                ln += c + " "
            print(ln)

        k = None
        while not k:
            r = get_key()
            if r in ['z','up','s','down','q','left','d','right','a','p']:
                k = {'z':'up','s':'down','q':'left','d':'right'}.get(r, r); break
            time.sleep(0.01)

        if k in ['up','down','left','right']:
            mv = {'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}[k]
            nx, ny = px + mv[0], py + mv[1]
            if 0 <= nx < W and 0 <= ny < H and (nx,ny) not in cfg["w"]:
                px, py = nx, ny
                for m in m_d:
                    if m[2] and random.random() < 0.4:
                        m[0]+=1 if px > m[0] else -1 if px < m[0] else 0
                        m[1]+=1 if py > m[1] else -1 if py < m[1] else 0
                    elif random.random() < 0.15:
                        m[0], m[1] = random.randint(0,9), random.randint(0,4)
                
                if any([px, py] == m[:2] for m in m_d):
                    lives -= 1; deaths += 1; c_msg = "TOUCHÉ !"
                    if lives <= 0: 
                        return "LOSE", deaths, 0, time.time()-st_t
                    # On continue le niveau : transformation et reset position
                    target = min(m_d, key=lambda m: (m[0]-px)**2 + (m[1]-py)**2)
                    target[2] = True
                    px, py = 0, 0
                    time.sleep(0.6)
                elif px == 9 and py == 4:
                    return "WIN", deaths, time.time()-st_t, time.time()-st_t
        elif k == 'a' and bul:
            bul = False
            if m_d and random.randint(0,1):
                idx = min(range(len(m_d)), key=lambda i: (m_d[i][0]-px)**2 + (m_d[i][1]-py)**2)
                m_d.pop(idx); c_msg = "ZOMBIE ABATTU !"
            else: c_msg = "RATÉ !"
        elif k == 'p': return "MENU", 0, 0, 0

while True:
    screen("COWBOY MAZE — HAPPY PIXELZ", ["[J] Jouer l'Histoire", "[C] Code Custom", "[E] Editeur", "[B] Boutique", "[H] Aide", "[K] Credits", "[S] Scores", "[Q] Quitter", f"\nPoints: {int(D['full_score'])}"])
    k = None
    while not k: k = get_key(); time.sleep(0.01)

    if k in ['j', 'c']:
        cd = input("Code Custom : ") if k == 'c' else None
        l_idx, td, twt, win, err = 0, 0, 0, False, False
        while True:
            res, d, wt, st = play(l_idx, cd)
            if res == "ERROR": err = True; break
            if res == "MENU": break
            td += d; twt += wt
            if res == "WIN":
                if cd: win = True; break
                l_idx += 1
                if l_idx >= 5: win = True; break
            elif res == "LOSE": win = False; break
            elif res == "FINISHED": win = True; break
        
        sc = 0
        if not err:
            if win: sc = max(20, int((600 - twt*2 - td*12)*3))
            else: sc = 5
        else: MSG = "CODE INVALIDE"
        D["full_score"] += sc; D["_fs_m"] = D["full_score"]
        if win: D["hi"] = sorted(D["hi"] + [sc], reverse=True)[:5]
        save(); input(f"FIN. Score : {sc} pts. [Entrée]")

    elif k == 'e': editor()
    
    elif k == 'h':
        os.system('cls')
        print("--- COMMENT SURVIVRE ---")
        print("BUT : Atteindre le coin (9,4).")
        print("\nCONTROLES : ZQSD/Flèches, A (Tir), P (Menu).")
        print(f"\n{D['skins']['P']}: Cowboy | {D['skins']['M']}: Zombie | @: Enragé | {D['skins']['#']}: Mur")
        input("\n[Entrée]...");

    elif k == 'k':
        os.system('cls')
        print("=== CRÉDITS COMPLETS — COWBOY MAZE ===")
        print("Ce jeu vous est présenté par Happy Pixelz, une branche de Studioz Development.\n")
        print("\"Il était une fois dans le futur d'un autre monde, la fin du monde.")
        print("Une apocalypse Zombie. Mais un héros était, et il se combattait")
        print("vaillamment contre ces créatures ignobles.\"\n")
        print("\"Mais un jour, il s'est blessé très fort. Alors il invoqua le démon")
        print("pour acheter les âmes des victimes des Zombies. Il est maintenant")
        print("voué à se combattre éternellement contre les Zombies...\"\n")
        print("\"Éternellement ? Non. Des héros peuvent le sauver de cet horrible destin.\"")
        print("\"Ces héros, c'est VOUS. Tant que des personnes joueront encore à ce jeu,")
        print("la fin du monde, de ce monde, n'arrivera pas.\"\n")
        print("--- Crédits ---")
        print("Développeur : ZedKa450 | Idées : ZedKa450")
        print("\n--- Remerciements ---")
        print("- Cortex pour les cerveaux.")
        print("- Hey Bobby! pour l'éditeur.")
        print("- Minecraft pour le poème.")
        input("\n[Entrée]...");

    elif k == 's':
        screen("SCORES", [f"{i+1}. {s} pts" for i, s in enumerate(D["hi"])]); input("[Entrée]")

    elif k == 'b':
        its = [
            {"n":"Joueur O","id":"O","t":"P","p":100},{"n":"Mur X","id":"X","t":"#","p":300},
            {"n":"Mur I","id":"I","t":"#","p":400},{"n":"Air .","id":".","t":"x","p":500},
            {"n":"Base Zombie Enragé @","id":"@","t":"M","p":0}, {"n":"Zombie Z","id":"Z","t":"M","p":600},
            {"n":"Base Joueur P","id":"P","t":"P","p":0},{"n":"Base Zombie M","id":"M","t":"M","p":0},
            {"n":"Base Mur #","id":"#","t":"#","p":0},{"n":"Base Air x","id":"x","t":"x","p":0},
            {"n":"Air [Vide]","id":"\u2800","t":"x","p":100}, {"n":"Mur e","id":"e","t":"#","p":500}
        ]
        while True:
            screen("BOUTIQUE", [f"{i+1}. {it['n']} {'[E]' if D['skins'][it['t']]==it['id'] else '[P]' if it['id'] in D['inv'] else f'({it['p']} pts)'}" for i, it in enumerate(its)]+["[Entrez le numéro ou 'q' pour quitter]"])
            
            choix = input("Votre choix : ").strip().lower()
            
            if choix == 'q' or choix == '': 
                break
            
            if choix.isdigit():
                num = int(choix)
                if 0 < num <= len(its):
                    it = its[num-1]
                    if it['id'] in D['inv']: 
                        D['skins'][it['t']] = it['id']
                    elif D['full_score'] >= it['p']:
                        D['full_score'] -= it['p']
                        D['inv'].append(it['id'])
                        D['skins'][it['t']] = it['id']
                        save()
                    D["_fs_m"] = D["full_score"]
                    save()
                else:
                    print("Ce numéro n'existe pas !")
                    time.sleep(1)
    elif k == 'q': sys.exit(0)
