u, v, s00, s01, s02, s03, s10, s11, s12, s13, s20, s21, s22, s23, s30, s31, s32, s33 = symbols("u v s00 s01 s02 s03 s10 s11 s12 s13 s20 s21 s22 s23 s30 s31 s32 s33")

def part(t, p0, p1): return p0*t+p1*(1-t)

def bezier(t, p0, p1, p2 ,p3):
    pp1 = part(t, p0, p1);
    pp2 = part(t, p1, p2);
    pp3 = part(t, p2, p3);
    return part(t, pp1, pp2), part(t, pp2, pp3);
    ppp1 = part(t, pp1, pp2);
    ppp2 = part(t, pp2, pp3);
    return part(t, ppp1, ppp2)

def bezier4d(u, v, s00, s01, s02, s03, s10, s11, s12, s13, s20, s21, s22, s23, s30, s31, s32, s33):
	a0 = bezier(u, s00, s01, s02, s03)
	a1 = bezier(u, s10, s11, s12, s13)
	a2 = bezier(u, s20, s21, s22, s23)
	a3 = bezier(u, s30, s31, s32, s33)
	return bezier(v, a0, a1, a2, a3)