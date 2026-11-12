import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, rdMolTransforms
from scipy.optimize import linear_sum_assignment
def emb(smi, straight=False, seed=7):
    m = Chem.AddHs(Chem.MolFromSmiles(smi)); Chem.Kekulize(m, clearAromaticFlags=True)
    if m.GetNumAtoms() == 1:
        return [(m.GetAtomWithIdx(0).GetSymbol(), np.zeros(3))], []
    AllChem.EmbedMolecule(m, randomSeed=seed); AllChem.MMFFOptimizeMolecule(m)
    conf = m.GetConformer()
    if straight:
        cs = [a.GetIdx() for a in m.GetAtoms() if a.GetSymbol() == "C"]
        for i in range(len(cs) - 3): rdMolTransforms.SetDihedralDeg(conf, cs[i], cs[i+1], cs[i+2], cs[i+3], 180.0)
        AllChem.MMFFOptimizeMolecule(m, maxIters=0)
    P = np.array([list(conf.GetAtomPosition(i)) for i in range(m.GetNumAtoms())])
    P -= P.mean(0)
    if len(P) > 2:  # axe principal horizontal (x), second axe vertical (y)
        u, s, vt = np.linalg.svd(P); P = P @ vt.T
    elif len(P) == 2: P = np.array([[np.linalg.norm(P[0]-P[1])/2, 0, 0], [-np.linalg.norm(P[0]-P[1])/2, 0, 0]])
    atoms = [(a.GetSymbol(), P[a.GetIdx()]) for a in m.GetAtoms()]
    bonds = [[b.GetBeginAtomIdx(), b.GetEndAtomIdx(), int(round(b.GetBondTypeAsDouble()))] for b in m.GetBonds()]
    return atoms, bonds
def R(v): return [round(float(x), 3) for x in v]
def single(smi, formula, straight=False, groups=None, **kw):
    a, b = emb(smi, straight)
    d = {"formula": formula, "atoms": [[s] + R(p) for s, p in a], "bonds": b}
    if groups: d["groups"] = groups(a, b)
    d.update(kw); return d
def layout(mols, gap=0.9):
    """mols = liste de (atoms,bonds) ; aligne les molécules sur x"""
    out, bonds, groups, x = [], [], [], 0
    widths = [(max(p[0] for _, p in a) - min(p[0] for _, p in a)) + 1.6 for a, b in mols]
    tot = sum(widths) + gap * (len(mols) - 1); x = -tot / 2
    for (a, b), w in zip(mols, widths):
        cx = x + w / 2; off = len(out)
        groups.append(list(range(off, off + len(a))))
        for s, p in a: out.append((s, p + np.array([cx, 0, 0])))
        bonds += [[i + off, j + off, o] for i, j, o in b]
        x += w + gap
    return out, bonds, groups
def reaction(reac, prod, f1, f2, **kw):
    """reac / prod = listes de SMILES (répétés selon les coefficients)"""
    A, Ab, Ag = layout([emb(s) for s in reac]); B, Bb, Bg = layout([emb(s) for s in prod])
    assert sorted(s for s, _ in A) == sorted(s for s, _ in B), "atomes non conservés"
    mapB = [None] * len(B)  # indice produit -> indice réactif
    for el in set(s for s, _ in A):
        ia = [i for i, (s, _) in enumerate(A) if s == el]; ib = [i for i, (s, _) in enumerate(B) if s == el]
        C = np.array([[np.linalg.norm(A[i][1] - B[j][1]) for j in ib] for i in ia])
        r, c = linear_sum_assignment(C)
        for k, l in zip(r, c): mapB[ib[l]] = ia[k]
    inv = {mapB[j]: j for j in range(len(B))}
    ppos = [R(B[inv[i]][1]) for i in range(len(A))]
    d = {"formula": f1, "atoms": [[s] + R(p) for s, p in A], "bonds": Ab, "groups": Ag,
         "product": {"formula": f2, "pos": ppos, "bonds": [[mapB[i], mapB[j], o] for i, j, o in Bb], "groups": [[mapB[i] for i in g] for g in Bg]}}
    d.update(kw); return d
def chain_groups(a, b):
    """motifs de 2 carbones avec leurs hydrogènes"""
    cs = [i for i, (s, _) in enumerate(a) if s == "C"]; cs.sort(key=lambda i: a[i][1][0])
    grp = {}
    for k, c in enumerate(cs): grp[c] = k // 2
    for i, j, o in b:
        if a[i][0] == "H": grp[i] = grp[j]
        if a[j][0] == "H": grp[j] = grp[i]
    ng = max(grp.values()) + 1
    return [[i for i in range(len(a)) if grp[i] == g] for g in range(ng)]
