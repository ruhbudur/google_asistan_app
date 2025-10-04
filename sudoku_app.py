import streamlit as st
import random
import pandas as pd
from copy import deepcopy
from time import sleep

# ---------- UI ----------
st.set_page_config(page_title="Sudoku Çözücü", page_icon="🧩", layout="centered")
st.title("🧩 Sudoku Çözücü + Adım-Adım Görselleştirici")

# ---------- Yardımcılar ----------
def empty_board():
    return [[0 for _ in range(9)] for _ in range(9)]

def find_empty(b):
    for r in range(9):
        for c in range(9):
            if b[r][c] == 0:
                return r, c
    return None

def valid(b, r, c, v):
    if any(b[r][x] == v for x in range(9)): return False
    if any(b[x][c] == v for x in range(9)): return False
    br, bc = 3*(r//3), 3*(c//3)
    for i in range(br, br+3):
        for j in range(bc, bc+3):
            if b[i][j] == v: return False
    return True

def solve_with_steps(b):
    steps = []
    def backtrack():
        pos = find_empty(b)
        if not pos:
            return True
        r, c = pos
        for v in range(1, 10):
            if valid(b, r, c, v):
                b[r][c] = v
                steps.append(("place", r, c, v))
                if backtrack():
                    return True
                b[r][c] = 0
                steps.append(("backtrack", r, c, 0))
        return False
    ok = backtrack()
    return ok, steps

def count_solutions(b, limit=2):
    cnt = 0
    def dfs():
        nonlocal cnt
        if cnt >= limit: 
            return
        pos = find_empty(b)
        if not pos:
            cnt += 1
            return
        r, c = pos
        for v in range(1,10):
            if valid(b, r, c, v):
                b[r][c] = v
                dfs()
                b[r][c] = 0
    dfs()
    return cnt

def fill_full_board(b):
    nums = list(range(1,10))
    def fill():
        pos = find_empty(b)
        if not pos:
            return True
        r, c = pos
        random.shuffle(nums)
        for v in nums:
            if valid(b, r, c, v):
                b[r][c] = v
                if fill():
                    return True
                b[r][c] = 0
        return False
    fill()
    return b

def generate_puzzle(remove_target=45, max_tries=400):
    """Tekil çözümlü sudoku üretir (makul hızda)."""
    b = empty_board()
    fill_full_board(b)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0
    tries = 0
    while cells and removed < remove_target and tries < max_tries:
        r, c = cells.pop()
        save = b[r][c]
        b[r][c] = 0
        # tekil çözüm mü?
        test = deepcopy(b)
        if count_solutions(test, limit=2) != 1:
            b[r][c] = save  # tekil değilse geri al
        else:
            removed += 1
        tries += 1
    return b

def board_to_df(b, highlight=None):
    """highlight=(typ, r, c) -> 'place' ise yeşil, 'backtrack' ise kırmızı."""
    data = [[("" if b[r][c]==0 else str(b[r][c])) for c in range(9)] for r in range(9)]
    df = pd.DataFrame(data, index=[f"R{r+1}" for r in range(9)], columns=[f"C{c+1}" for c in range(9)])
    if highlight is None:
        return df.style.set_properties(**{"text-align": "center", "font-weight": "600"})
    typ, rr, cc, _ = highlight
    def color_fn(val, r, c):
        if r == rr and c == cc:
            return "background-color: #b7f7b0;" if typ == "place" else "background-color: #ffb3b3;"
        return ""
    return df.style.apply(lambda x: [color_fn(v, x.index, i) for i, v in enumerate(x)], axis=1)\
                   .set_properties(**{"text-align": "center", "font-weight": "600"})

# ---------- Session State ----------
if "board" not in st.session_state:
    st.session_state.board = empty_board()

def set_board(b):
    st.session_state.board = deepcopy(b)

# ---------- Kontroller ----------
colA, colB, colC, colD = st.columns(4)
with colA:
    if st.button("🧪 Örnek Bulmaca Yükle"):
        sample = [
            [0,0,0, 2,6,0, 7,0,1],
            [6,8,0, 0,7,0, 0,9,0],
            [1,9,0, 0,0,4, 5,0,0],
            [8,2,0, 1,0,0, 0,4,0],
            [0,0,4, 6,0,2, 9,0,0],
            [0,5,0, 0,0,3, 0,2,8],
            [0,0,9, 3,0,0, 0,7,4],
            [0,4,0, 0,5,0, 0,3,6],
            [7,0,3, 0,1,8, 0,0,0],
        ]
        set_board(sample)
with colB:
    if st.button("🧹 Temizle"):
        set_board(empty_board())
with colC:
    if st.button("✨ Yeni Bulmaca (tekil)"):
        with st.spinner("Üretiliyor… (tekil çözüm kontrol ediliyor)"):
            puzzle = generate_puzzle(remove_target=45)
        set_board(puzzle)
with colD:
    solve_clicked = st.button("🚀 Çöz (Animasyonlu)")

# ---------- Grid Girişi ----------
st.caption("Hücreye 1-9 yazabilirsin; boş için boş bırak.")
grid = []
for r in range(9):
    cols = st.columns(9)
    row = []
    for c in range(9):
        key = f"cell_{r}_{c}"
        val = "" if st.session_state.board[r][c] == 0 else str(st.session_state.board[r][c])
        text = cols[c].text_input("", value=val, key=key, max_chars=1)
        if text.strip().isdigit() and 1 <= int(text) <= 9:
            row.append(int(text))
        else:
            row.append(0)
    grid.append(row)

set_board(grid)  # kullanıcı girdisini board'a yaz

# ---------- Çöz / Adım adım ----------
placeholder = st.empty()
placeholder.table(board_to_df(st.session_state.board))

if solve_clicked:
    work = deepcopy(st.session_state.board)
    ok, steps = solve_with_steps(work)
    if not ok:
        st.error("Çözüm bulunamadı. (Girdi geçersiz olabilir.)")
    else:
        for step in steps:
            # adım görselleştir
            typ, r, c, v = step
            if typ == "place":
                st.session_state.board[r][c] = v
            elif typ == "backtrack":
                st.session_state.board[r][c] = 0
            placeholder.table(board_to_df(st.session_state.board, highlight=step))
            sleep(0.03)  # animasyon hızı

        placeholder.table(board_to_df(st.session_state.board))
        st.success("✅ Çözüldü!")

