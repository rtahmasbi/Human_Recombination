
import numpy as np
import random

Glob_Debug_L1 = False
Glob_Debug_L2 = False

# it is in format [) for all parts
class Part:
    def __init__(self,st=0,en=0,root_hap=0):
        self.st = st
        self.en = en
        self.root_hap = root_hap
    def info(self):
        print("info: st=%s, en=%s, root_hap=%s" % (self.st, self.en, self.root_hap))



class Haplotype:
    def __init__(self,n):
        self.part = [Part() for i in range(n)]
    def info(self):
        print("number of parts: %s" % len(self.part))
        print("st\ten\troot_hap")
        n = min(30,len(self.part))
        for i in range(n):
            print("%s\t%s\t%s" % (self.part[i].st, self.part[i].en, self.part[i].root_hap))



class Chromosome:
    def __init__(self):
        self.hap = [Haplotype(1) for _ in range(2)]
        self.chr_name = ""



class Human:
    def __init__(self, id=0, sex=0, nchr=22):
        self.id = id
        self.sex = sex # 1=male, 2=female, 0=unknown
        self.chr = [Chromosome() for i in np.arange(nchr)]
        self.idf = 0
        self.idm = 0
    def info(self):
        print("info: id=%s, sex=%s, idf=%s, idm=%s, chr=%s" % (self.id, self.sex, self.idf, self.idm, len(self.chr)))



class Population:
    def __init__(self, nh=100, nchr=22):
        self.human = [Human(nchr) for i in range(nh)]
    def size(self):
        return(len(self.human))
    def info(self):
        print("pop size: %s" % self.size() )
    def get_males(self):
    	return([i for i in range(self.size()) if self.human[i].sex == 1])
    def get_females(self):
    	return([i for i in range(self.size()) if self.human[i].sex == 2])




hap1 = Haplotype(3)

hap1.part[1].en

this_chr = Chromosome()

print(vars(this_chr))


h = Human() # creates a human with 22 chromosome
h.info()


def random_hap(nparts=10, st=0, en=1000):
    hap = Haplotype(nparts)
    if (nparts==1):
    	hap.part[0].st = st
    	hap.part[0].en = en
    r = np.random.random_integers(st,en,nparts-1)
    r.sort()
    r = np.insert(r, 0, st)
    for i in range(nparts-1):
        hap.part[i].st = r[i]
        hap.part[i].en = r[i+1]
        hap.part[nparts-1].st = r[nparts-1]
        hap.part[nparts-1].en = en
    return(hap)


hap = random_hap()
hap.info()

h1 = Human(1,1,22)
h2 = Human(2,2,22)

chr_lens = np.repeat(1000,22)
for ichr in range(22):
    h1.chr[ichr].hap[0] = random_hap(1,0,chr_lens[ichr])
    h1.chr[ichr].hap[1] = random_hap(1,0,chr_lens[ichr])
    h2.chr[ichr].hap[0] = random_hap(1,0,chr_lens[ichr])
    h2.chr[ichr].hap[1] = random_hap(1,0,chr_lens[ichr])


h1.chr[0].hap[0].info()
h1.chr[0].hap[1].info()
h2.chr[0].hap[0].info()
h2.chr[0].hap[1].info()




# returns Haplotype, it will return randomly one of the haps if len(pos)<3 (no recombination)
# pos should be at least [st,en]
def recombine_chr(chr, pos):
    if (Glob_Debug_L2):
        print(pos)
    ret = Haplotype(0)
    hap_index = np.random.random_integers(0,1,1)
    if (len(pos)<3):
        return(chr.hap[hap_index])
    for i1 in range(1,len(pos)):
        i2 = 0
        while (len(chr.hap[hap_index].part)>i2 and chr.hap[hap_index].part[i2].en <= pos[i1-1]):
            i2 = i2 + 1
        if (len(chr.hap[hap_index].part)>i2 and chr.hap[hap_index].part[i2].st < pos[i1-1] and pos[i1-1] < chr.hap[hap_index].part[i2].en and pos[i1]<chr.hap[hap_index].part[i2].en):
            p = Part(chr.hap[hap_index].part[i2].st, chr.hap[hap_index].part[i2].en, chr.hap[hap_index].part[i2].root_hap)
            p.st = pos[i1-1]
            p.en = pos[i1]
            ret.part = np.append(ret.part, p)
            i2 = i2 + 1
        if (len(chr.hap[hap_index].part)>i2 and chr.hap[hap_index].part[i2].st < pos[i1-1] and pos[i1-1] < chr.hap[hap_index].part[i2].en and pos[i1] >= chr.hap[hap_index].part[i2].en):
            p = Part(chr.hap[hap_index].part[i2].st, chr.hap[hap_index].part[i2].en, chr.hap[hap_index].part[i2].root_hap)
            p.st=pos[i1-1];
            ret.part = np.append(ret.part, p)
            i2 = i2 + 1
        while(len(chr.hap[hap_index].part)>i2 and chr.hap[hap_index].part[i2].en <= pos[i1] and pos[i1-1]<= chr.hap[hap_index].part[i2].st):
            p = Part(chr.hap[hap_index].part[i2].st, chr.hap[hap_index].part[i2].en, chr.hap[hap_index].part[i2].root_hap)
            ret.part = np.append(ret.part, p)
            i2 = i2 + 1
        if(len(chr.hap[hap_index].part)>i2 and chr.hap[hap_index].part[i2].st < pos[i1] and pos[i1] < chr.hap[hap_index].part[i2].en):
            p = Part(chr.hap[hap_index].part[i2].st, chr.hap[hap_index].part[i2].en, chr.hap[hap_index].part[i2].root_hap)
            p.en = pos[i1]
            ret.part = np.append(ret.part, p)
        hap_index = (hap_index+1)%2
    return(ret)





# mix two inds with recombination_rate
def mate(human1, human2, recombination_rate=1e-6):
    nchr = len(human1.chr)
    h_ret = Human(nchr=nchr)
    h_ret.sex = np.asscalar(np.random.random_integers(1,2,1))
    h_ret.idf = human1.id
    h_ret.idm = human2.id
    if (nchr != len(human2.chr)):
        print("error")
        return(-1)
    for ichr in range(nchr):
        this_hap_st = human1.chr[ichr].hap[0].part[0].st
        this_hap_en = human1.chr[ichr].hap[0].part[-1].en
        this_hap_len = this_hap_en - this_hap_st
        nrec_rate = this_hap_len * recombination_rate
        nrec1 = np.random.poisson(nrec_rate)
        nrec2 = np.random.poisson(nrec_rate)
        if(Glob_Debug_L2):
	        print("\tichr=%s, this_hap_st=%s, this_hap_en=%s, this_hap_len=%s, nrec_rate =%s, nrec1=%s, nrec2=%s" % (ichr, this_hap_st , this_hap_en, this_hap_len, nrec_rate, nrec1, nrec2))
        recs1 = np.random.random_integers(this_hap_st+1,this_hap_en-1,nrec1) # generate recombination positions in (st,en)
        recs1.sort() # sort in place
        recs1 = np.insert(recs1, 0, this_hap_st) # always add st at the beginning 
        recs1 = np.append(recs1, this_hap_en)# always add en at the end
        h_ret.chr[ichr].hap[0] = recombine_chr(human1.chr[ichr], recs1)
        recs2 = np.random.random_integers(this_hap_st,this_hap_en-1,nrec2)
        recs2.sort() # sort in place
        if (len(recs2)==0):
            recs2 = np.array([this_hap_st, this_hap_en])
        if (recs2[0] != this_hap_st):
            recs2 = np.insert(recs2, 0, this_hap_st)
        if (recs2[-1] != this_hap_en):
            recs2 = np.append(recs2, this_hap_en)
        h_ret.chr[ichr].hap[1] = recombine_chr(human2.chr[ichr], recs2)
    return h_ret




recombination_rate = .01
h3 = mate(h1,h2,recombination_rate)
h3.info()


h3.chr[0].hap[0].info()
h3.chr[0].hap[1].info()
h3.chr[1].hap[0].info()
h3.chr[1].hap[1].info()

h1.chr[0].hap[0].info()




def sim_population(nind=100, nchr=22):
	pop = Population(nind, nchr)
	for ih in range(nind):
		for ichr in range(nchr):
			pop.human[ih].chr[ichr].hap[0].part[0] = Part(0, chr_lens[ichr], ih)
			pop.human[ih].id = ih
			pop.human[ih].sex = np.asscalar(np.random.random_integers(1,2,1))
	return(pop)


pop1 =  sim_population(100)   
pop1.info()
pop1.get_males()
pop1.get_females()


for i in range(4):
	pop1.human[i].info()


def create_couples(males, females, matying_type, n_couples=0):
	n_male = len(males)
	n_female = len(females)
	n_couples = min(n_male, n_female, n_couples)
	if (n_couples==0):
		n_couples = min(n_male, n_female)
	if matying_type == "random":
		rmale = np.random.choice(males,size=n_couples, replace=False)
		rfemale = np.random.choice(females,size=n_couples, replace=False)
		couples = np.array([rmale,rfemale])
	return(couples)



mating_type = "random"


def create_next_generation(pop, mating_type, recombination_rate):
	nchr = len(pop.human[0].chr)
	males   = pop.get_males()
	females = pop.get_females()
	couples = create_couples(males,females,mating_type)
	n_couples = len(couples[0])
	print("Number of couples = %s" % n_couples)
	n_child_per_couple = [1 for i in range(n_couples)]  # this could be an array of size n_couples
	n_childs = np.sum(n_child_per_couple)
	ret_pop = Population(n_childs, nchr)
	ih = 0
	for icouples in range(n_couples):
		for ichild in range(n_child_per_couple[icouples]):
			if Glob_Debug_L1:
				print("ind[%s] mates with ind[%s]" % (pop.human[couples[0,icouples]].id, pop.human[couples[1,icouples]].id))
			ret_pop.human[ih] = mate(pop.human[couples[0,icouples]], pop.human[couples[1,icouples]], recombination_rate)
			ih = ih + 1
	return(ret_pop)


Glob_Debug_L1 = True
pop2 = create_next_generation(pop1, mating_type, recombination_rate)
pop2.info()
pop2.human[0].info()
pop2.human[0].chr[0].hap[0].info()
pop2.human[1].chr[0].hap[0].info()

Glob_Debug_L2 = True
h4 = mate(pop1.human[0], pop1.human[1], recombination_rate)
h4.chr[0].hap[0].info()
pop1.human[0].chr[0].hap[0].info()
pop1.human[1].chr[0].hap[0].info()














