from os import system

class ChessGame:
    def __init__(self, down="w", up="b", white="w", black="b"):
        if down==up or white==" " or black==" " or len(white)!=1 or len(black)!=1 or white!=down and white!=up or black!=down and black!=up:
            raise ValueError()
        self.down=down
        self.up=up
        self.wht=white
        self.blck=black
        self.is_check=False
        self.number_of_checks=0
        self.check_from=[]
        self.check_to=[]
        self.legit_move={"p": self.PawnLegitMove, "R": self.RookLegitMove, "N": self.KnightLegitMove, "B": self.BishopLegitMove, "Q": self.QueenLegitMove, "K": self.KingLegitMove}
        
        self.table = [["  " for i in range(8)] for j in range(8)]
        pieces=["R","N","B","Q","K","p"]
        for i in range(2):
            for j in range(8):
                if i==0:
                    self.table[i][j]=down+pieces[j] if j<5 else down+pieces[2-(j-5)]
                elif i==1:
                    self.table[i][j]=down+pieces[5]
        for i in range(6,8):
            for j in range(8):
                if i==7:
                    self.table[i][j]=up+pieces[j] if j<5 else up+pieces[2-(j-5)]
                elif i==6:
                    self.table[i][j]=up+pieces[5]
    def StartGame(self):
        wmove=True
        self.ShowTable()
        while(1):
            if self.IsCheckMate(self.wht if(wmove) else self.blck):
                if wmove:
                    print("Black Wins!!!")
                else:
                    print("White Wins!!!")
                break
            elif self.IsStealMate():
                print("Draw!!!")
                break
            if self.LegalMove(input("White moves: " if(wmove) else "Black moves:"), self.wht if(wmove) else self.blck):
                self.ShowTable()
                wmove=not wmove
    def LegalMove(self, notation, mov):
        dec_n=self.DecodeNotation(notation)
        if(not dec_n[0]):
            print("Illegal notation, try again!\n")
            return False
        else:
            #[True,"norm",movepiece,s_field,capture[0],e_field]
            #[True,"spec","smallc"]
            #[True,"spec","bigc"]

            if dec_n[1]=="norm":
                s_rowcol_known=[True if dec_n[3][0]>-1 else False, True if dec_n[3][1]>-1 else False]

            movepiece=dec_n[2]
            s_field_mov=[]
            e_field_mov=dec_n[5]
            if movepiece!="p":
                if not s_rowcol_known[0] and not s_rowcol_known[1]:
                    for i in range(8):
                        for j in range(8):
                            if self.table[i][j]==mov+movepiece:
                                s_field_mov.append([i,j])
                elif not s_rowcol_known[1]:
                    for j in range(8):
                        if self.table[dec_n[3][0]][j]==mov+movepiece:
                            s_field_mov.append([dec_n[3][0],j])
                elif not s_rowcol_known[0]:
                    for i in range(8):
                        if self.table[i][dec_n[3][1]]==mov+movepiece:
                            s_field_mov.append([i,dec_n[3][1]])
                else:
                    s_field_mov.append(dec_n[3])
            else:
                if dec_n[4]:
                    for i in range(8):
                        if self.table[i][dec_n[3][1]]==mov+movepiece:
                            s_field_mov.append([i,dec_n[3][1]])
                else:
                    for i in range(8):
                        if self.table[i][dec_n[5][1]]==mov+movepiece:
                            s_field_mov.append([i,dec_n[5][1]])
            
            land_on_oppnt=self.table[e_field_mov[0]][e_field_mov[1]][0]==(self.blck if mov==self.wht else self.wht)
            n_can_move=0
            if dec_n[1]=="norm":
                for s_kfield in s_field_mov:
                    can_move=False
                    if movepiece=="p":
                        if self.legit_move["p"](mov, s_kfield, dec_n[4], land_on_oppnt, e_field_mov):
                            can_move=True
                    elif self.legit_move[movepiece](s_kfield, dec_n[4], land_on_oppnt, e_field_mov):
                        can_move=True
                    if can_move:
                        n_can_move+=1
                        s_field=s_kfield
                        if movepiece=="p": break
                if n_can_move==1:
                    if not self.InCheck(True, mov, movepiece, s_field, e_field_mov): #ko igra da nije u checku
                        self.is_check=self.InCheck(False, mov, movepiece, s_field, e_field_mov) #protivnik u checku
                        self.table[e_field_mov[0]][e_field_mov[1]]=mov+movepiece
                        self.table[s_field[0]][s_field[1]]="  "
                        return True
                    else:
                        print("Can't be in check!")
                        return False
                elif n_can_move>=2:
                    print("Specify which piece, try again!\n")
                    return False
                else:
                    print("Illegal move, try again!\n")
                    return False
            elif dec_n[1]=="spec":
                if dec_n[2]=="smallc":
                    return True
                elif dec_n[2]=="bigc":
                    return True
    def InCheck(self, self_check, mov, movepiece, s_field, e_field):
        e_stuff=self.table[e_field[0]][e_field[1]]
        self.table[e_field[0]][e_field[1]]=mov+movepiece
        self.table[s_field[0]][s_field[1]]="  "
        
        opnnt_mov=self.blck if mov==self.wht else self.wht
        found_k=False
        for i in range(8):
            if found_k: break
            for j in range(8):
                if found_k: break
                if self.table[i][j]==(mov+"K" if self_check else opnnt_mov+"K"):
                    king_pos=[i,j]
                    found_k=True
        self.number_of_checks=0
        temp_num_checks=0
        for i in range(8):
            for j in range(8):
                if self.table[i][j][0]==(opnnt_mov if self_check else mov):
                    if self.table[i][j][1]=="p":
                        if self.legit_move["p"](opnnt_mov if self_check else mov, [i,j], True, True, king_pos): self.number_of_checks+=1
                    elif self.legit_move[self.table[i][j][1]]([i,j], True, True, king_pos): self.number_of_checks+=1
                    if self.number_of_checks>temp_num_checks:
                        temp_num_checks+=1
                        self.check_from=[i,j]
                        self.check_to=king_pos
        self.table[e_field[0]][e_field[1]]=e_stuff
        self.table[s_field[0]][s_field[1]]=mov+movepiece
        if self.number_of_checks>0:
            return True
        return False
    def IsCheckMate(self, mov):
        if self.is_check:
            print("Check!")
            if self.number_of_checks==1:
                vert=self.check_from[0]-self.check_to[0]
                hor=self.check_from[1]-self.check_to[1]
                #da neko stane u path od checka
                if abs(vert)>1 or abs(hor)>1:
                    if vert!=0: steprow=int(vert/abs(vert))
                    if hor!=0: stepcol=int(hor/abs(hor))
                    if vert==0:
                        for h in range(1, abs(hor)):
                            for i in range(8):
                                for j in range(8):
                                    if self.table[i][j][0]==mov and self.table[i][j][1]!="K":
                                        if self.table[i][j][1]=="p":
                                            if self.legit_move["p"](mov, [i,j], False, False, [self.check_to[0], self.check_to[1]+h*stepcol]) and not self.InCheck(True, mov, "p", [i,j], [self.check_to[0], self.check_to[1]+h*stepcol]): return False
                                        elif self.legit_move[self.table[i][j][1]]([i,j], False, False, [self.check_to[0], self.check_to[1]+h*stepcol]) and not self.InCheck(True, mov, self.table[i][j][1], [i,j], [self.check_to[0], self.check_to[1]+h*stepcol]): return False
                    if hor==0:
                        for v in range(1, abs(vert)):
                            for i in range(8):
                                for j in range(8):
                                    if self.table[i][j][0]==mov and self.table[i][j][1]!="K":
                                        if self.table[i][j][1]=="p":
                                            if self.legit_move["p"](mov, [i,j], False, False, [self.check_to[0]+h*steprow, self.check_to[1]]) and not self.InCheck(True, mov, "p", [i,j], [self.check_to[0]+h*steprow, self.check_to[1]]): return False
                                        elif self.legit_move[self.table[i][j][1]]([i,j], False, False, [self.check_to[0]+h*steprow, self.check_to[1]]) and not self.InCheck(True, mov, self.table[i][j][1], [i,j], [self.check_to[0]+h*steprow, self.check_to[1]]): return False
                    if abs(vert)==abs(hor):
                        for k in range(1, abs(vert)):
                            for i in range(8):
                                for j in range(8):
                                    if self.table[i][j][0]==mov and self.table[i][j][1]!="K":
                                        if self.table[i][j][1]=="p":
                                            if self.legit_move["p"](mov, [i,j], False, False, [self.check_to[0]+k*steprow, self.check_to[1]+k*stepcol]) and not self.InCheck(True, mov, "p", [i,j], [self.check_to[0]+k*steprow, self.check_to[1]+k*stepcol]): return False
                                        elif self.legit_move[self.table[i][j][1]]([i,j], False, False, [self.check_to[0]+k*steprow, self.check_to[1]+k*stepcol]) and not self.InCheck(True, mov, self.table[i][j][1], [i,j], [self.check_to[0]+k*steprow, self.check_to[1]+k*stepcol]):return False
                #da unisti ko ga checkuje
                for i in range(8):
                    for j in range(8):
                        if self.table[i][j][0]==mov:
                            if self.table[i][j][1]=="p":
                                if self.legit_move["p"](mov, [i,j], True, True, self.check_from) and not self.InCheck(True, mov, "p", [i,j], self.check_from): return False
                            elif self.legit_move[self.table[i][j][1]]([i,j], True, True, self.check_from) and not self.InCheck(True, mov, self.table[i][j][1], [i,j], self.check_from): return False
            #da pobjegne sa kraljem (opcija za svaki number_of_check>0 naravno)
            king_moves=[[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]
            for kmove in king_moves:
                if 0<=self.check_to[0]+kmove[0]<8 and 0<=self.check_to[1]+kmove[1]<8:
                    if self.legit_move["K"](self.check_to, False, False, self.check_to+kmove) and not self.InCheck(True, mov, "K", self.check_to, self.check_to+kmove):
                        return False
                    elif self.legit_move["K"](self.check_to, True, True, self.check_to+kmove) and not self.InCheck(True, mov, "K", self.check_to, self.check_to+kmove):
                        return False
            print("CHECK MATE!!!")
            return True
        else:
            return False
    def IsStealMate(self):
        return False
    def PawnLegitMove(self, mov, s_field, capture, land_on_oppnt, e_field):
        vert=e_field[0]-s_field[0]
        hor=e_field[1]-s_field[1]
        to_side=1
        if(mov==self.up):
            vert*=-1
            to_side=-1
        if not capture:
            if hor!=0: return False
            if s_field[0]==1 and to_side==1 or s_field[0]==6 and to_side==-1:
                if vert==1 or vert==2:
                    cant_pass=False
                    for i in range(s_field[0], s_field[0]+to_side*vert, to_side):
                        if self.table[i+to_side][e_field[1]] != "  ":
                            cant_pass=True
                            break
                    if not cant_pass: return True
            else:
                if vert==1 and self.table[e_field[0]][e_field[1]]=="  ":
                    return True
        else:
            if abs(hor)!=1: return False
            if vert==1 and land_on_oppnt:
                return True
        return False
    def RookLegitMove(self, s_field, capture, land_on_oppnt, e_field):
        vert=e_field[0]-s_field[0]
        hor=e_field[1]-s_field[1]
        if vert==0 and hor!=0 and capture==land_on_oppnt:
            step=int(hor/abs(hor))
            cant_pass=False
            for j in range(s_field[1], s_field[1]+hor, step):
                if self.table[e_field[0]][j+step] != "  " and not(j+step==e_field[1] and land_on_oppnt):
                    cant_pass=True
                    break
            if not cant_pass: return True
        elif vert!=0 and hor==0 and capture==land_on_oppnt:
            step=int(vert/abs(vert))
            cant_pass=False
            for i in range(s_field[0], s_field[0]+vert, step):
                if self.table[i+step][e_field[1]] != "  " and not(i+step==e_field[0] and land_on_oppnt):
                    cant_pass=True
                    break
            if not cant_pass: return True
        return False
    def KnightLegitMove(self, s_field, capture, land_on_oppnt, e_field):
        vert=e_field[0]-s_field[0]
        hor=e_field[1]-s_field[1]
        if (abs(hor)==1 and abs(vert)==2 or abs(hor)==2 and abs(vert)==1) and capture==land_on_oppnt:
            if land_on_oppnt or self.table[e_field[0]][e_field[1]]=="  ":
                return True
        return False
    def BishopLegitMove(self, s_field, capture, land_on_oppnt, e_field):
        vert=e_field[0]-s_field[0]
        hor=e_field[1]-s_field[1]
        if vert!=0 and abs(vert)==abs(hor) and capture==land_on_oppnt:
            steprow=int(vert/abs(vert))
            stepcol=int(hor/abs(hor))
            cant_pass=False
            for b in range(abs(vert)):
                if self.table[s_field[0]+steprow*(b+1)][s_field[1]+stepcol*(b+1)] != "  ":
                    if not (s_field[0]+steprow*(b+1)==e_field[0] and land_on_oppnt):
                        cant_pass=True
                        break
            if not cant_pass: return True
        return False
    def QueenLegitMove(self, s_field, capture, land_on_oppnt, e_field):
        if self.BishopLegitMove(s_field, capture, land_on_oppnt, e_field) or self.RookLegitMove(s_field, capture, land_on_oppnt, e_field):
            return True
        return False
    def KingLegitMove(self, s_field, capture, land_on_oppnt, e_field):
        vert=e_field[0]-s_field[0]
        hor=e_field[1]-s_field[1]
        if (abs(vert)==abs(hor)==1 or abs(vert)==1 and hor==0 or abs(hor)==1 and vert==0) and capture==land_on_oppnt:
            if land_on_oppnt or self.table[e_field[0]][e_field[1]]=="  ":
                return True
        return False
    def DecodeNotation(self, ntc):
        if len(ntc)<2 or len(ntc)>6: return [False]
        if(ntc=="O-O" or ntc=="0-0"): return [True,"spec","smallc"]
        if(ntc=="O-O-O" or ntc=="0-0-0"): return [True,"spec","bigc"]
        
        major_pieces=["R","N","B","Q","K"]
        columns=["a","b","c","d","e","f","g","h"]
        rows=["1","2","3","4","5","6","7","8"]
        movepiece="p" #ship
        major=False
        s_field=[-1,-1] #ship
        e_field=[]  #ship
        capture=[False,False] #ship
        s_wasrow=False
        s_wascol=False
        
        for i in range(1,len(ntc)+1):
            if major: return [False]
            if i==1 and ntc[-i] in rows:
                e_field.append(rows.index(ntc[-1]))
            if i==2 and ntc[-i] in columns:
                e_field.append(columns.index(ntc[-2]))
            if i==3:
                if ntc[-i] in major_pieces:
                    movepiece=ntc[-i]
                    major=True
                elif ntc[-i]=="x":
                    capture[0]=True
                elif ntc[-i] in rows:
                    s_field[0]=rows.index(ntc[-i])
                    s_wasrow=True
                elif ntc[-i] in columns:
                    s_field[1]=columns.index(ntc[-i])
                    s_wascol=True
                else: return [False]
            if i>3 and i<7:
                if ntc[-i] in major_pieces:
                    if capture[0]:
                        capture[1]=True
                    movepiece=ntc[-i]
                    major=True
                elif not s_wascol and not s_wasrow and ntc[-i] in rows:
                    s_field[0]=rows.index(ntc[-i])
                    s_wasrow=True
                elif not s_wascol and ntc[-i] in columns:
                    s_field[1]=columns.index(ntc[-i])
                    s_wascol=True
                else: return [False]

        if len(e_field)==2:
            if movepiece=="p":
                if not s_wasrow and (not capture[0] and not s_wascol or capture[0] and s_wascol):
                    return [True,"norm",movepiece,s_field,capture[0],e_field]
                else: return [False]
            else:
                if capture[0]==capture[1]:
                    return [True,"norm",movepiece,s_field,capture[0],e_field]
                else: return [False]
        else: return [False]
            
    def ShowTable(self):
        system("cls")
        print("    -------------------------")
        for i in range(7,-1,-1):
            print("{}   |{}|{}|{}|{}|{}|{}|{}|{}|".format(i+1, self.table[i][0],self.table[i][1],
                                                   self.table[i][2],self.table[i][3],
                                                   self.table[i][4],self.table[i][5],
                                                   self.table[i][6],self.table[i][7]))
            print("    -------------------------")
        print("\n      a  b  c  d  e  f  g  h")

chess=ChessGame("#",".","#",".")
chess.StartGame()
