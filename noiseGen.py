import math

class NoiseGen:
    STRETCH_CONSTANT_2D = -0.211324865405187;    # (1/Math.sqrt(2+1)-1)/2;
    SQUISH_CONSTANT_2D = 0.366025403784439;      # (Math.sqrt(2+1)-1)/2;
    STRETCH_CONSTANT_3D = -1.0 / 6;              # (1/Math.sqrt(3+1)-1)/3;
    SQUISH_CONSTANT_3D = 1.0 / 3;                # (Math.sqrt(3+1)-1)/3;

    PSIZE = 2048;
    PMASK = 2047;

    perm = [0 for i in range(PSIZE)];
    permGrad2 = [];
    permGrad3 = [];

    N2 = 7.69084574549313;
    N3 = 26.92263139946168;
    tmp2D = [( 0.130526192220052,  0.99144486137381),
                ( 0.38268343236509,   0.923879532511287),
                ( 0.608761429008721,  0.793353340291235),
                ( 0.793353340291235,  0.608761429008721),
                ( 0.923879532511287,  0.38268343236509),
                ( 0.99144486137381,   0.130526192220051),
                ( 0.99144486137381,  -0.130526192220051),
                ( 0.923879532511287, -0.38268343236509),
                ( 0.793353340291235, -0.60876142900872),
                ( 0.608761429008721, -0.793353340291235),
                ( 0.38268343236509,  -0.923879532511287),
                ( 0.130526192220052, -0.99144486137381),
                (-0.130526192220052, -0.99144486137381),
                (-0.38268343236509,  -0.923879532511287),
                (-0.608761429008721, -0.793353340291235),
                (-0.793353340291235, -0.608761429008721),
                (-0.923879532511287, -0.38268343236509),
                (-0.99144486137381,  -0.130526192220052),
                (-0.99144486137381,   0.130526192220051),
                (-0.923879532511287,  0.38268343236509),
                (-0.793353340291235,  0.608761429008721),
                (-0.608761429008721,  0.793353340291235),
                (-0.38268343236509,   0.923879532511287),
                (-0.130526192220052,  0.99144486137381)]

    tmp3D = [(-1.4082482904633333,    -1.4082482904633333,    -2.6329931618533333),
                (-0.07491495712999985,   -0.07491495712999985,   -3.29965982852),
                ( 0.24732126143473554,   -1.6667938651159684,    -2.838945207362466),
                (-1.6667938651159684,     0.24732126143473554,   -2.838945207362466),
                (-1.4082482904633333,    -2.6329931618533333,    -1.4082482904633333),
                (-0.07491495712999985,   -3.29965982852,         -0.07491495712999985),
                (-1.6667938651159684,    -2.838945207362466,      0.24732126143473554),
                ( 0.24732126143473554,   -2.838945207362466,     -1.6667938651159684),
                ( 1.5580782047233335,     0.33333333333333337,   -2.8914115380566665),
                ( 2.8914115380566665,    -0.33333333333333337,   -1.5580782047233335),
                ( 1.8101897177633992,    -1.2760767510338025,    -2.4482280932803),
                ( 2.4482280932803,        1.2760767510338025,    -1.8101897177633992),
                ( 1.5580782047233335,    -2.8914115380566665,     0.33333333333333337),
                ( 2.8914115380566665,    -1.5580782047233335,    -0.33333333333333337),
                ( 2.4482280932803,       -1.8101897177633992,     1.2760767510338025),
                ( 1.8101897177633992,    -2.4482280932803,       -1.2760767510338025),
                (-2.6329931618533333,    -1.4082482904633333,    -1.4082482904633333),
                (-3.29965982852,         -0.07491495712999985,   -0.07491495712999985),
                (-2.838945207362466,      0.24732126143473554,   -1.6667938651159684),
                (-2.838945207362466,     -1.6667938651159684,     0.24732126143473554),
                ( 0.33333333333333337,    1.5580782047233335,    -2.8914115380566665),
                (-0.33333333333333337,    2.8914115380566665,    -1.5580782047233335),
                ( 1.2760767510338025,     2.4482280932803,       -1.8101897177633992),
                (-1.2760767510338025,     1.8101897177633992,    -2.4482280932803),
                ( 0.33333333333333337,   -2.8914115380566665,     1.5580782047233335),
                (-0.33333333333333337,   -1.5580782047233335,     2.8914115380566665),
                (-1.2760767510338025,    -2.4482280932803,        1.8101897177633992),
                ( 1.2760767510338025,    -1.8101897177633992,     2.4482280932803),
                ( 3.29965982852,          0.07491495712999985,    0.07491495712999985),
                ( 2.6329931618533333,     1.4082482904633333,     1.4082482904633333),
                ( 2.838945207362466,     -0.24732126143473554,    1.6667938651159684),
                ( 2.838945207362466,      1.6667938651159684,    -0.24732126143473554),
                (-2.8914115380566665,     1.5580782047233335,     0.33333333333333337),
                (-1.5580782047233335,     2.8914115380566665,    -0.33333333333333337),
                (-2.4482280932803,        1.8101897177633992,    -1.2760767510338025),
                (-1.8101897177633992,     2.4482280932803,        1.2760767510338025),
                (-2.8914115380566665,     0.33333333333333337,    1.5580782047233335),
                (-1.5580782047233335,    -0.33333333333333337,    2.8914115380566665),
                (-1.8101897177633992,     1.2760767510338025,     2.4482280932803),
                (-2.4482280932803,       -1.2760767510338025,     1.8101897177633992),
                ( 0.07491495712999985,    3.29965982852,          0.07491495712999985),
                ( 1.4082482904633333,     2.6329931618533333,     1.4082482904633333),
                ( 1.6667938651159684,     2.838945207362466,     -0.24732126143473554),
                (-0.24732126143473554,    2.838945207362466,      1.6667938651159684),
                ( 0.07491495712999985,    0.07491495712999985,    3.29965982852),
                ( 1.4082482904633333,     1.4082482904633333,     2.6329931618533333),
                (-0.24732126143473554,    1.6667938651159684,     2.838945207362466),
                ( 1.6667938651159684,    -0.24732126143473554,    2.838945207362466)]
    
    def __init__(self, seed):
        source = [i for i in range(self.PSIZE)]
        self.tmp2D = [(x / self.N2, y / self.N2) for x, y in self.tmp2D]
        self.GRADIENTS_2D = [self.tmp2D[i % len(self.tmp2D)] for i in range(self.PSIZE)]
        self.tmp3D = [(x / self.N3, y / self.N3, z / self.N3) for x, y, z in self.tmp3D]
        self.GRADIENTS_3D = [self.tmp3D[i % len(self.tmp3D)] for i in range(self.PSIZE)]
        for i in reversed(range(self.PSIZE)):
            seed = seed * 6364136223846793005 + 1442695040888963407;
            r = ((seed + 31) % (i + 1));
            if (r < 0):
                r += (i + 1);
            self.perm.append(source[r]);
            self.permGrad2.append(self.GRADIENTS_2D[self.perm[-1]]);
            self.permGrad3.append(self.GRADIENTS_3D[self.perm[-1]]);
            source[r] = source[i];

    def extrapolate2(self, xsb, ysb, dx, dy):
        x, y = self.permGrad2[self.perm[xsb & self.PMASK] ^ (ysb & self.PMASK)];
        return x * dx + y * dy;
        
    def extrapolate3(self, xsb, ysb, zsb, dx, dy, dz):
        x, y, z = self.permGrad3[self.perm[self.perm[xsb & self.PMASK] ^ (ysb & self.PMASK)] ^ (zsb & self.PMASK)];
        return x * dx + y * dy + z * dz;

    def NoiseAtPos2(self, x, y):
        #Place input coordinates onto grid.
        stretchOffset = (x + y) * self.STRETCH_CONSTANT_2D;
        xs = x + stretchOffset;
        ys = y + stretchOffset;

        #math.floor to get grid coordinates of rhombus (stretched square) super-cell origin.
        xsb = math.floor(xs);
        ysb = math.floor(ys);

        #Compute grid coordinates relative to rhombus origin.
        xins = xs - xsb;
        yins = ys - ysb;

        #Sum those together to get a value that determines which region we're in.
        inSum = xins + yins;

        #Positions relative to origin point.
        squishOffsetIns = inSum * self.SQUISH_CONSTANT_2D;
        dx0 = xins + squishOffsetIns;
        dy0 = yins + squishOffsetIns;

        #We'll be defining these inside the next block and using them afterwards.
        dx_ext = 0;
        dy_ext = 0;
        xsv_ext = 0;
        ysv_ext = 0;

        value = 0;

        #Contribution (1,0)
        dx1 = dx0 - 1 - self.SQUISH_CONSTANT_2D;
        dy1 = dy0 - 0 - self.SQUISH_CONSTANT_2D;
        attn1 = 2 - dx1 * dx1 - dy1 * dy1;
        if (attn1 > 0):
            attn1 *= attn1;
            value += attn1 * attn1 * self.extrapolate2(xsb + 1, ysb + 0, dx1, dy1);
        

        #Contribution (0,1)
        dx2 = dx0 - 0 - self.SQUISH_CONSTANT_2D;
        dy2 = dy0 - 1 - self.SQUISH_CONSTANT_2D;
        attn2 = 2 - dx2 * dx2 - dy2 * dy2;
        if (attn2 > 0):
            attn2 *= attn2;
            value += attn2 * attn2 * self.extrapolate2(xsb + 0, ysb + 1, dx2, dy2);
        

        if (inSum <= 1): # We're inside the triangle (2-Simplex) at (0,0)
            zins = 1 - inSum;
            if (zins > xins or zins > yins): # (0,0) is one of the closest two triangular vertices
                if (xins > yins):
                    xsv_ext = xsb + 1;
                    ysv_ext = ysb - 1;
                    dx_ext = dx0 - 1;
                    dy_ext = dy0 + 1;
                else:
                    xsv_ext = xsb - 1;
                    ysv_ext = ysb + 1;
                    dx_ext = dx0 + 1;
                    dy_ext = dy0 - 1;
            else: # (1,0) and (0,1) are the closest two vertices.
                xsv_ext = xsb + 1;
                ysv_ext = ysb + 1;
                dx_ext = dx0 - 1 - 2 * self.SQUISH_CONSTANT_2D;
                dy_ext = dy0 - 1 - 2 * self.SQUISH_CONSTANT_2D;
        else: # We're inside the triangle (2-Simplex) at (1,1)
            zins = 2 - inSum;
            if (zins < xins or zins < yins): # (0,0) is one of the closest two triangular vertices
                if (xins > yins):
                    xsv_ext = xsb + 2;
                    ysv_ext = ysb + 0;
                    dx_ext = dx0 - 2 - 2 * self.SQUISH_CONSTANT_2D;
                    dy_ext = dy0 + 0 - 2 * self.SQUISH_CONSTANT_2D;
                else:
                    xsv_ext = xsb + 0;
                    ysv_ext = ysb + 2;
                    dx_ext = dx0 + 0 - 2 * self.SQUISH_CONSTANT_2D;
                    dy_ext = dy0 - 2 - 2 * self.SQUISH_CONSTANT_2D;
            else: #(1,0) and (0,1) are the closest two vertices.
                dx_ext = dx0;
                dy_ext = dy0;
                xsv_ext = xsb;
                ysv_ext = ysb;
            xsb += 1;
            ysb += 1;
            dx0 = dx0 - 1 - 2 * self.SQUISH_CONSTANT_2D;
            dy0 = dy0 - 1 - 2 * self.SQUISH_CONSTANT_2D;
        #Contribution (0,0) or (1,1)
        attn0 = 2 - dx0 * dx0 - dy0 * dy0;
        if (attn0 > 0):
            attn0 *= attn0;
            value += attn0 * attn0 * self.extrapolate2(xsb, ysb, dx0, dy0);
        

        #Extra Vertex
        attn_ext = 2 - dx_ext * dx_ext - dy_ext * dy_ext;
        if (attn_ext > 0):
            attn_ext *= attn_ext;
            value += attn_ext * attn_ext * self.extrapolate2(xsv_ext, ysv_ext, dx_ext, dy_ext);
        

        return value;

    def eval3_Base(self, x, y, z):
        #math.floor to get simplectic honeycomb coordinates of rhombohedron (stretched cube) super-cell origin.
        xsb = math.floor(xs);
        ysb = math.floor(ys);
        zsb = math.floor(zs);
        
        #Compute simplectic honeycomb coordinates relative to rhombohedral origin.
        xins = xs - xsb;
        yins = ys - ysb;
        zins = zs - zsb;
        
        #Sum those together to get a value that determines which region we're in.
        inSum = xins + yins + zins;

        #Positions relative to origin point.
        squishOffsetIns = inSum * self.SQUISH_CONSTANT_3D;
        dx0 = xins + squishOffsetIns;
        dy0 = yins + squishOffsetIns;
        dz0 = zins + squishOffsetIns;
        
        #We'll be defining these inside the next block and using them afterwards.
        dx_ext0 = 0
        dy_ext0 = 0
        dz_ext0 = 0
        dx_ext1 = 0
        dy_ext1 = 0
        dz_ext1 = 0
        xsv_ext0 = 0
        ysv_ext0 = 0
        zsv_ext0 = 0
        xsv_ext1 = 0
        ysv_ext1 = 0
        zsv_ext1 = 0
        
        value = 0;
        if (inSum <= 1): #We're inside the tetrahedron (3-Simplex) at (0,0,0)
            
            #Determine which two of (0,0,1), (0,1,0), (1,0,0) are closest.
            aPoint = 0x01;
            aScore = xins;
            bPoint = 0x02;
            bScore = yins;
            if (aScore >= bScore and zins > bScore):
                bScore = zins;
                bPoint = 0x04;
            elif (aScore < bScore and zins > aScore):
                aScore = zins;
                aPoint = 0x04;
            
            
            #Now we determine the two lattice points not part of the tetrahedron that may contribute.
            #This depends on the closest two tetrahedral vertices, including (0,0,0)
            wins = 1 - inSum;
            if (wins > aScore or wins > bScore): #(0,0,0) is one of the closest two tetrahedral vertices.
                c = 0
                if (bScore > aScore):
                    c = bPoint
                else:
                    aPoint #Our other closest vertex is the closest out of a and b.
                
                if ((c & 0x01) == 0):
                    xsv_ext0 = xsb - 1;
                    xsv_ext1 = xsb;
                    dx_ext0 = dx0 + 1;
                    dx_ext1 = dx0;
                else:
                    xsv_ext0 = xsv_ext1 = xsb + 1;
                    dx_ext0 = dx_ext1 = dx0 - 1;
                

                if ((c & 0x02) == 0):
                    ysv_ext0 = ysv_ext1 = ysb;
                    dy_ext0 = dy_ext1 = dy0;
                    if ((c & 0x01) == 0):
                        ysv_ext1 -= 1;
                        dy_ext1 += 1;
                    else:
                        ysv_ext0 -= 1;
                        dy_ext0 += 1;
                    
                else:
                    ysv_ext0 = ysv_ext1 = ysb + 1;
                    dy_ext0 = dy_ext1 = dy0 - 1;
                

                if ((c & 0x04) == 0):
                    zsv_ext0 = zsb;
                    zsv_ext1 = zsb - 1;
                    dz_ext0 = dz0;
                    dz_ext1 = dz0 + 1;
                else:
                    zsv_ext0 = zsv_ext1 = zsb + 1;
                    dz_ext0 = dz_ext1 = dz0 - 1;
                
            else: #(0,0,0) is not one of the closest two tetrahedral vertices.
                c = (aPoint | bPoint); #Our two extra vertices are determined by the closest two.
                
                if ((c & 0x01) == 0):
                    xsv_ext0 = xsb;
                    xsv_ext1 = xsb - 1;
                    dx_ext0 = dx0 - 2 * self.SQUISH_CONSTANT_3D;
                    dx_ext1 = dx0 + 1 - self.SQUISH_CONSTANT_3D;
                else:
                    xsv_ext0 = xsv_ext1 = xsb + 1;
                    dx_ext0 = dx0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
                    dx_ext1 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
                

                if ((c & 0x02) == 0):
                    ysv_ext0 = ysb;
                    ysv_ext1 = ysb - 1;
                    dy_ext0 = dy0 - 2 * self.SQUISH_CONSTANT_3D;
                    dy_ext1 = dy0 + 1 - self.SQUISH_CONSTANT_3D;
                else:
                    ysv_ext0 = ysv_ext1 = ysb + 1;
                    dy_ext0 = dy0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
                    dy_ext1 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
                

                if ((c & 0x04) == 0):
                    zsv_ext0 = zsb;
                    zsv_ext1 = zsb - 1;
                    dz_ext0 = dz0 - 2 * self.SQUISH_CONSTANT_3D;
                    dz_ext1 = dz0 + 1 - self.SQUISH_CONSTANT_3D;
                else:
                    zsv_ext0 = zsv_ext1 = zsb + 1;
                    dz_ext0 = dz0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
                    dz_ext1 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
                
            

            #Contribution (0,0,0)
            attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0;
            if (attn0 > 0):
                attn0 *= attn0;
                value += attn0 * attn0 * self.extrapolate3(xsb + 0, ysb + 0, zsb + 0, dx0, dy0, dz0);
            

            #Contribution (1,0,0)
            dx1 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
            dy1 = dy0 - 0 - self.SQUISH_CONSTANT_3D;
            dz1 = dz0 - 0 - self.SQUISH_CONSTANT_3D;
            attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1;
            if (attn1 > 0):
                attn1 *= attn1;
                value += attn1 * attn1 * self.extrapolate3(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1);
            

            #Contribution (0,1,0)
            dx2 = dx0 - 0 - self.SQUISH_CONSTANT_3D;
            dy2 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
            dz2 = dz1;
            attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2;
            if (attn2 > 0):
                attn2 *= attn2;
                value += attn2 * attn2 * self.extrapolate3(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2);
            

            #Contribution (0,0,1)
            dx3 = dx2;
            dy3 = dy1;
            dz3 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
            attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3;
            if (attn3 > 0):
                attn3 *= attn3;
                value += attn3 * attn3 * self.extrapolate3(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3);
            
        elif (inSum >= 2): #We're inside the tetrahedron (3-Simplex) at (1,1,1)
        
            #Determine which two tetrahedral vertices are the closest, out of (1,1,0), (1,0,1), (0,1,1) but not (1,1,1).
            aPoint = 0x06;
            aScore = xins;
            bPoint = 0x05;
            bScore = yins;
            if (aScore <= bScore and zins < bScore):
                bScore = zins;
                bPoint = 0x03;
            elif (aScore > bScore and zins < aScore):
                aScore = zins;
                aPoint = 0x03;
            
            
            #Now we determine the two lattice points not part of the tetrahedron that may contribute.
            #This depends on the closest two tetrahedral vertices, including (1,1,1)
            wins = 3 - inSum;
            if (wins < aScore or wins < bScore): #(1,1,1) is one of the closest two tetrahedral vertices.
                c = 0
                if (bScore < aScore):
                    c = bPoint
                else:
                    aPoint; #Our other closest vertex is the closest out of a and b.
                
                if ((c & 0x01) != 0):
                    xsv_ext0 = xsb + 2;
                    xsv_ext1 = xsb + 1;
                    dx_ext0 = dx0 - 2 - 3 * self.SQUISH_CONSTANT_3D;
                    dx_ext1 = dx0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
                else:
                    xsv_ext0 = xsv_ext1 = xsb;
                    dx_ext0 = dx_ext1 = dx0 - 3 * self.SQUISH_CONSTANT_3D;
                

                if ((c & 0x02) != 0):
                    ysv_ext0 = ysv_ext1 = ysb + 1;
                    dy_ext0 = dy_ext1 = dy0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
                    if ((c & 0x01) != 0):
                        ysv_ext1 += 1;
                        dy_ext1 -= 1;
                    else:
                        ysv_ext0 += 1;
                        dy_ext0 -= 1;
                    
                else:
                    ysv_ext0 = ysv_ext1 = ysb;
                    dy_ext0 = dy_ext1 = dy0 - 3 * self.SQUISH_CONSTANT_3D;
                

                if ((c & 0x04) != 0):
                    zsv_ext0 = zsb + 1;
                    zsv_ext1 = zsb + 2;
                    dz_ext0 = dz0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
                    dz_ext1 = dz0 - 2 - 3 * self.SQUISH_CONSTANT_3D;
                else:
                    zsv_ext0 = zsv_ext1 = zsb;
                    dz_ext0 = dz_ext1 = dz0 - 3 * self.SQUISH_CONSTANT_3D;
                
            else: #(1,1,1) is not one of the closest two tetrahedral vertices.
                c = (byte)(aPoint & bPoint); #Our two extra vertices are determined by the closest two.
                
                if ((c & 0x01) != 0):
                    xsv_ext0 = xsb + 1;
                    xsv_ext1 = xsb + 2;
                    dx_ext0 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
                    dx_ext1 = dx0 - 2 - 2 * self.SQUISH_CONSTANT_3D;
                else:
                    xsv_ext0 = xsv_ext1 = xsb;
                    dx_ext0 = dx0 - self.SQUISH_CONSTANT_3D;
                    dx_ext1 = dx0 - 2 * self.SQUISH_CONSTANT_3D;
                

                if ((c & 0x02) != 0):
                    ysv_ext0 = ysb + 1;
                    ysv_ext1 = ysb + 2;
                    dy_ext0 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
                    dy_ext1 = dy0 - 2 - 2 * self.SQUISH_CONSTANT_3D;
                else:
                    ysv_ext0 = ysv_ext1 = ysb;
                    dy_ext0 = dy0 - self.SQUISH_CONSTANT_3D;
                    dy_ext1 = dy0 - 2 * self.SQUISH_CONSTANT_3D;
                

                if ((c & 0x04) != 0):
                    zsv_ext0 = zsb + 1;
                    zsv_ext1 = zsb + 2;
                    dz_ext0 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
                    dz_ext1 = dz0 - 2 - 2 * self.SQUISH_CONSTANT_3D;
                else:
                    zsv_ext0 = zsv_ext1 = zsb;
                    dz_ext0 = dz0 - self.SQUISH_CONSTANT_3D;
                    dz_ext1 = dz0 - 2 * self.SQUISH_CONSTANT_3D;
                
            
            
            #Contribution (1,1,0)
            dx3 = dx0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
            dy3 = dy0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
            dz3 = dz0 - 0 - 2 * self.SQUISH_CONSTANT_3D;
            attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3;
            if (attn3 > 0):
                attn3 *= attn3;
                value += attn3 * attn3 * self.extrapolate3(xsb + 1, ysb + 1, zsb + 0, dx3, dy3, dz3);
            

            #Contribution (1,0,1)
            dx2 = dx3;
            dy2 = dy0 - 0 - 2 * self.SQUISH_CONSTANT_3D;
            dz2 = dz0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
            attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2;
            if (attn2 > 0):
                attn2 *= attn2;
                value += attn2 * attn2 * self.extrapolate3(xsb + 1, ysb + 0, zsb + 1, dx2, dy2, dz2);
            

            #Contribution (0,1,1)
            dx1 = dx0 - 0 - 2 * self.SQUISH_CONSTANT_3D;
            dy1 = dy3;
            dz1 = dz2;
            attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1;
            if (attn1 > 0):
                attn1 *= attn1;
                value += attn1 * attn1 * self.extrapolate3(xsb + 0, ysb + 1, zsb + 1, dx1, dy1, dz1);
            

            #Contribution (1,1,1)
            dx0 = dx0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
            dy0 = dy0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
            dz0 = dz0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
            attn0 = 2 - dx0 * dx0 - dy0 * dy0 - dz0 * dz0;
            if (attn0 > 0):
                attn0 *= attn0;
                value += attn0 * attn0 * self.extrapolate3(xsb + 1, ysb + 1, zsb + 1, dx0, dy0, dz0);
            
        else: #We're inside the octahedron (Rectified 3-Simplex) in between.
            aScore = 0;
            aPoint = 0;
            aIsFurtherSide = True;
            bScore = 0;
            bPoint = 0;
            bIsFurtherSide = True;

            #Decide between point (0,0,1) and (1,1,0) as closest
            p1 = xins + yins;
            if (p1 > 1):
                aScore = p1 - 1;
                aPoint = 0x03;
                aIsFurtherSide = true;
            else:
                aScore = 1 - p1;
                aPoint = 0x04;
                aIsFurtherSide = false;
            

            #Decide between point (0,1,0) and (1,0,1) as closest
            p2 = xins + zins;
            if (p2 > 1):
                bScore = p2 - 1;
                bPoint = 0x05;
                bIsFurtherSide = true;
            else:
                bScore = 1 - p2;
                bPoint = 0x02;
                bIsFurtherSide = false;
            
            
            #The closest out of the two (1,0,0) and (0,1,1) will replace the furthest out of the two decided above, if closer.
            p3 = yins + zins;
            if (p3 > 1):
                score = p3 - 1;
                if (aScore <= bScore and aScore < score):
                    aScore = score;
                    aPoint = 0x06;
                    aIsFurtherSide = true;
                elif (aScore > bScore and bScore < score):
                    bScore = score;
                    bPoint = 0x06;
                    bIsFurtherSide = true;
                
            else:
                score = 1 - p3;
                if (aScore <= bScore and aScore < score):
                    aScore = score;
                    aPoint = 0x01;
                    aIsFurtherSide = false;
                elif (aScore > bScore and bScore < score):
                    bScore = score;
                    bPoint = 0x01;
                    bIsFurtherSide = false;
                
            
            
            #Where each of the two closest points are determines how the extra two vertices are calculated.
            if (aIsFurtherSide == bIsFurtherSide):
                if (aIsFurtherSide): #Both closest points on (1,1,1) side

                    #One of the two extra points is (1,1,1)
                    dx_ext0 = dx0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
                    dy_ext0 = dy0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
                    dz_ext0 = dz0 - 1 - 3 * self.SQUISH_CONSTANT_3D;
                    xsv_ext0 = xsb + 1;
                    ysv_ext0 = ysb + 1;
                    zsv_ext0 = zsb + 1;

                    #Other extra point is based on the shared axis.
                    c = (aPoint & bPoint);
                    if ((c & 0x01) != 0):
                        dx_ext1 = dx0 - 2 - 2 * self.SQUISH_CONSTANT_3D;
                        dy_ext1 = dy0 - 2 * self.SQUISH_CONSTANT_3D;
                        dz_ext1 = dz0 - 2 * self.SQUISH_CONSTANT_3D;
                        xsv_ext1 = xsb + 2;
                        ysv_ext1 = ysb;
                        zsv_ext1 = zsb;
                    elif ((c & 0x02) != 0):
                        dx_ext1 = dx0 - 2 * self.SQUISH_CONSTANT_3D;
                        dy_ext1 = dy0 - 2 - 2 * self.SQUISH_CONSTANT_3D;
                        dz_ext1 = dz0 - 2 * self.SQUISH_CONSTANT_3D;
                        xsv_ext1 = xsb;
                        ysv_ext1 = ysb + 2;
                        zsv_ext1 = zsb;
                    else:
                        dx_ext1 = dx0 - 2 * self.SQUISH_CONSTANT_3D;
                        dy_ext1 = dy0 - 2 * self.SQUISH_CONSTANT_3D;
                        dz_ext1 = dz0 - 2 - 2 * self.SQUISH_CONSTANT_3D;
                        xsv_ext1 = xsb;
                        ysv_ext1 = ysb;
                        zsv_ext1 = zsb + 2;
                    
                else:#Both closest points on (0,0,0) side

                    #One of the two extra points is (0,0,0)
                    dx_ext0 = dx0;
                    dy_ext0 = dy0;
                    dz_ext0 = dz0;
                    xsv_ext0 = xsb;
                    ysv_ext0 = ysb;
                    zsv_ext0 = zsb;

                    #Other extra point is based on the omitted axis.
                    c = (aPoint | bPoint);
                    if ((c & 0x01) == 0):
                        dx_ext1 = dx0 + 1 - self.SQUISH_CONSTANT_3D;
                        dy_ext1 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
                        dz_ext1 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
                        xsv_ext1 = xsb - 1;
                        ysv_ext1 = ysb + 1;
                        zsv_ext1 = zsb + 1;
                    elif ((c & 0x02) == 0):
                        dx_ext1 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
                        dy_ext1 = dy0 + 1 - self.SQUISH_CONSTANT_3D;
                        dz_ext1 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
                        xsv_ext1 = xsb + 1;
                        ysv_ext1 = ysb - 1;
                        zsv_ext1 = zsb + 1;
                    else:
                        dx_ext1 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
                        dy_ext1 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
                        dz_ext1 = dz0 + 1 - self.SQUISH_CONSTANT_3D;
                        xsv_ext1 = xsb + 1;
                        ysv_ext1 = ysb + 1;
                        zsv_ext1 = zsb - 1;
                    
                
            else: #One point on (0,0,0) side, one point on (1,1,1) side
                c1 = 0
                c2 = 0
                if (aIsFurtherSide):
                    c1 = aPoint;
                    c2 = bPoint;
                else:
                    c1 = bPoint;
                    c2 = aPoint;
                

                #One contribution is a self.permutation of (1,1,-1)
                if ((c1 & 0x01) == 0):
                    dx_ext0 = dx0 + 1 - self.SQUISH_CONSTANT_3D;
                    dy_ext0 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
                    dz_ext0 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
                    xsv_ext0 = xsb - 1;
                    ysv_ext0 = ysb + 1;
                    zsv_ext0 = zsb + 1;
                elif ((c1 & 0x02) == 0):
                    dx_ext0 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
                    dy_ext0 = dy0 + 1 - self.SQUISH_CONSTANT_3D;
                    dz_ext0 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
                    xsv_ext0 = xsb + 1;
                    ysv_ext0 = ysb - 1;
                    zsv_ext0 = zsb + 1;
                else:
                    dx_ext0 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
                    dy_ext0 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
                    dz_ext0 = dz0 + 1 - self.SQUISH_CONSTANT_3D;
                    xsv_ext0 = xsb + 1;
                    ysv_ext0 = ysb + 1;
                    zsv_ext0 = zsb - 1;
                

                #One contribution is a self.permutation of (0,0,2)
                dx_ext1 = dx0 - 2 * self.SQUISH_CONSTANT_3D;
                dy_ext1 = dy0 - 2 * self.SQUISH_CONSTANT_3D;
                dz_ext1 = dz0 - 2 * self.SQUISH_CONSTANT_3D;
                xsv_ext1 = xsb;
                ysv_ext1 = ysb;
                zsv_ext1 = zsb;
                if ((c2 & 0x01) != 0):
                    dx_ext1 -= 2;
                    xsv_ext1 += 2;
                elif ((c2 & 0x02) != 0):
                    dy_ext1 -= 2;
                    ysv_ext1 += 2;
                else:
                    dz_ext1 -= 2;
                    zsv_ext1 += 2;
                
            

            #Contribution (1,0,0)
            dx1 = dx0 - 1 - self.SQUISH_CONSTANT_3D;
            dy1 = dy0 - 0 - self.SQUISH_CONSTANT_3D;
            dz1 = dz0 - 0 - self.SQUISH_CONSTANT_3D;
            attn1 = 2 - dx1 * dx1 - dy1 * dy1 - dz1 * dz1;
            if (attn1 > 0):
                attn1 *= attn1;
                value += attn1 * attn1 * self.extrapolate3(xsb + 1, ysb + 0, zsb + 0, dx1, dy1, dz1);
            

            #Contribution (0,1,0)
            dx2 = dx0 - 0 - self.SQUISH_CONSTANT_3D;
            dy2 = dy0 - 1 - self.SQUISH_CONSTANT_3D;
            dz2 = dz1;
            attn2 = 2 - dx2 * dx2 - dy2 * dy2 - dz2 * dz2;
            if (attn2 > 0):
                attn2 *= attn2;
                value += attn2 * attn2 * self.extrapolate3(xsb + 0, ysb + 1, zsb + 0, dx2, dy2, dz2);
            

            #Contribution (0,0,1)
            dx3 = dx2;
            dy3 = dy1;
            dz3 = dz0 - 1 - self.SQUISH_CONSTANT_3D;
            attn3 = 2 - dx3 * dx3 - dy3 * dy3 - dz3 * dz3;
            if (attn3 > 0):
                attn3 *= attn3;
                value += attn3 * attn3 * self.extrapolate3(xsb + 0, ysb + 0, zsb + 1, dx3, dy3, dz3);
            

            # Contribution (1,1,0)
            dx4 = dx0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
            dy4 = dy0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
            dz4 = dz0 - 0 - 2 * self.SQUISH_CONSTANT_3D;
            attn4 = 2 - dx4 * dx4 - dy4 * dy4 - dz4 * dz4;
            if (attn4 > 0):
                attn4 *= attn4;
                value += attn4 * attn4 * self.extrapolate3(xsb + 1, ysb + 1, zsb + 0, dx4, dy4, dz4);
            

            # Contribution (1,0,1)
            dx5 = dx4;
            dy5 = dy0 - 0 - 2 * self.SQUISH_CONSTANT_3D;
            dz5 = dz0 - 1 - 2 * self.SQUISH_CONSTANT_3D;
            attn5 = 2 - dx5 * dx5 - dy5 * dy5 - dz5 * dz5;
            if (attn5 > 0):
                attn5 *= attn5;
                value += attn5 * attn5 * self.extrapolate3(xsb + 1, ysb + 0, zsb + 1, dx5, dy5, dz5);
            

            # Contribution (0,1,1)
            dx6 = dx0 - 0 - 2 * self.SQUISH_CONSTANT_3D;
            dy6 = dy4;
            dz6 = dz5;
            attn6 = 2 - dx6 * dx6 - dy6 * dy6 - dz6 * dz6;
            if (attn6 > 0):
                attn6 *= attn6;
                value += attn6 * attn6 * self.extrapolate3(xsb + 0, ysb + 1, zsb + 1, dx6, dy6, dz6);
            
        

        #First extra vertex
        attn_ext0 = 2 - dx_ext0 * dx_ext0 - dy_ext0 * dy_ext0 - dz_ext0 * dz_ext0;
        if (attn_ext0 > 0):
            attn_ext0 *= attn_ext0;
            value += attn_ext0 * attn_ext0 * self.extrapolate3(xsv_ext0, ysv_ext0, zsv_ext0, dx_ext0, dy_ext0, dz_ext0);
        

        #Second extra vertex
        attn_ext1 = 2 - dx_ext1 * dx_ext1 - dy_ext1 * dy_ext1 - dz_ext1 * dz_ext1;
        if (attn_ext1 > 0):
            attn_ext1 *= attn_ext1;
            value += attn_ext1 * attn_ext1 * self.extrapolate3(xsv_ext1, ysv_ext1, zsv_ext1, dx_ext1, dy_ext1, dz_ext1);
        
        
        return value;

    def NoiseAtPos3(self, x, y, z):
        #Place input coordinates on simplectic honeycomb.
        stretchOffset = (x + y + z) * self.STRETCH_CONSTANT_3D;
        xs = x + stretchOffset;
        ys = y + stretchOffset;
        zs = z + stretchOffset;
        
        return eval3_Base(xs, ys, zs);

    def NoiseAtPos3OverZ(self, x, y, z):
        #Combine rotation with skew transform.
        xy = x + y;
        s2 = xy * 0.211324865405187;
        zz = z * 0.288675134594813;
        xs = s2 - x + zz
        ys = s2 - y + zz;
        zs = xy * 0.577350269189626 + zz;

        return eval3_Base(xs, ys, zs);