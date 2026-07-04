"""Exploratory SPO' Baez-algebra activation engine.

Non-canonical prototype. The Sefirot names are symbolic labels; the
Cayley-Dickson carrier operations and coherence checks are executable.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple
import math

NAMES={0:"R",1:"C",2:"H",3:"O"}

@dataclass(frozen=True)
class CD:
    level:int
    comp:Tuple[float,...]
    def __post_init__(self):
        if len(self.comp)!=2**self.level:
            raise ValueError("component count does not match level")
    @classmethod
    def real(cls,x,level=0):
        c=[0.0]*(2**level); c[0]=float(x); return cls(level,tuple(c))
    def split(self):
        if self.level==0: raise ValueError("R cannot split")
        n=2**(self.level-1)
        return CD(self.level-1,self.comp[:n]),CD(self.level-1,self.comp[n:])
    def conj(self):
        if self.level==0: return self
        a,b=self.split()
        return CD(self.level,a.conj().comp+tuple(-x for x in b.comp))
    def check(self,o):
        if self.level!=o.level: raise TypeError("carrier mismatch")
    def __neg__(self): return CD(self.level,tuple(-x for x in self.comp))
    def __add__(self,o): self.check(o); return CD(self.level,tuple(a+b for a,b in zip(self.comp,o.comp)))
    def __sub__(self,o): return self+(-o)
    def __mul__(self,o):
        self.check(o)
        if self.level==0: return CD(0,(self.comp[0]*o.comp[0],))
        a,b=self.split(); c,d=o.split()
        return CD(self.level,(a*c-d.conj()*b).comp+(d*a+b*c.conj()).comp)
    def norm_sq(self): return sum(x*x for x in self.comp)
    def norm(self): return math.sqrt(self.norm_sq())
    def close(self,o,tol=1e-9): self.check(o); return (self-o).norm()<=tol
    def __repr__(self): return f"{NAMES.get(self.level,'A')}{self.comp}"

def R(x): return CD.real(x,0)
def C(a,b=0.0): return CD(1,(float(a),float(b)))
def H(a,b=0.0,c=0.0,d=0.0): return CD(2,(float(a),float(b),float(c),float(d)))
def O(*xs):
    if len(xs)>8: raise ValueError("octonions take at most 8 coordinates")
    return CD(3,tuple(float(x) for x in list(xs)+[0.0]*(8-len(xs))))

class Mode(Enum):
    NORM=auto(); LIE=auto(); JORDAN=auto(); CLIFFORD=auto(); ALTERNATIVE=auto(); EXCEPTIONAL_JORDAN=auto()

def compatible(level,mode):
    if level not in NAMES: return False
    if mode is Mode.NORM: return level<=3
    if mode is Mode.LIE: return level<=2
    if mode is Mode.JORDAN: return level<=3
    if mode is Mode.CLIFFORD: return level<=2
    if mode is Mode.ALTERNATIVE: return level==3
    if mode is Mode.EXCEPTIONAL_JORDAN: return level==3
    return False

def half(x): return CD(x.level,tuple(v*0.5 for v in x.comp))
def bracket(x,y): return x*y-y*x
def jordan(x,y): return half(x*y+y*x)

def norm_ok(x,y,tol=1e-9):
    return abs((x*y).norm_sq()-x.norm_sq()*y.norm_sq()) <= tol*max(1.0,x.norm_sq()*y.norm_sq())

def jacobi_ok(x,y,z,tol=1e-9):
    s=bracket(x,bracket(y,z))+bracket(y,bracket(z,x))+bracket(z,bracket(x,y))
    return s.norm()<=tol

def jordan_ok(x,y,tol=1e-9):
    x2=jordan(x,x)
    return (jordan(jordan(x,y),x2)-jordan(x,jordan(y,x2))).norm()<=tol

def clifford_ok(v,tol=1e-9):
    p=CD(v.level,(0.0,)+v.comp[1:]); q=p*p
    return abs(q.comp[0]+p.norm_sq())<=tol and all(abs(c)<=tol for c in q.comp[1:])

def moufang_ok(x,y,z,tol=1e-9):
    return ((x*y)*(z*x)-x*((y*z)*x)).norm()<=tol

def coherent(mode,*a):
    if mode is Mode.NORM: return len(a)<2 or norm_ok(a[0],a[1])
    if mode is Mode.LIE: return len(a)<3 or jacobi_ok(a[0],a[1],a[2])
    if mode is Mode.JORDAN: return len(a)<2 or jordan_ok(a[0],a[1])
    if mode is Mode.CLIFFORD: return len(a)<1 or clifford_ok(a[0])
    if mode in (Mode.ALTERNATIVE,Mode.EXCEPTIONAL_JORDAN): return len(a)<3 or moufang_ok(a[0],a[1],a[2])
    return False

@dataclass(frozen=True)
class S2:
    x:float; y:float; z:float
    def normed(self):
        n=math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z) or 1.0
        return S2(self.x/n,self.y/n,self.z/n)
    def angle(self,o):
        a=self.normed(); b=o.normed()
        d=max(-1.0,min(1.0,a.x*b.x+a.y*b.y+a.z*b.z))
        return math.acos(d)

def phase_match(a,b,eps=0.2): return a.angle(b)<eps

@dataclass
class Layer:
    name:str; carrier:int; mode:Mode; state:CD; phase:S2
    norm_bound:float=math.inf
    witnesses:Tuple[CD,...]=field(default_factory=tuple)
    def well_typed(self): return self.state.level==self.carrier and compatible(self.carrier,self.mode)
    def on_shell(self): return self.well_typed() and self.state.norm()<=self.norm_bound
    def is_coherent(self): return self.well_typed() and all(w.level==self.carrier for w in self.witnesses) and coherent(self.mode,*self.witnesses)

def activate(prev,nxt):
    checks={
        "prev_on_shell":prev.on_shell(),
        "next_well_typed":nxt.well_typed(),
        "phase_match":phase_match(prev.phase,nxt.phase),
        "next_coherent":nxt.is_coherent(),
        "carrier_permits":nxt.carrier in (prev.carrier,prev.carrier+1),
    }
    checks["activated"]=all(checks.values())
    return checks["activated"],checks

SEFIROT={
    "Malkhut":(0,Mode.NORM,"real grounding"),
    "Yesod":(1,Mode.NORM,"complex phase"),
    "Hod":(2,Mode.NORM,"quaternionic rotation"),
    "Netzach":(3,Mode.NORM,"octonionic emergence"),
    "Tiferet":(2,Mode.CLIFFORD,"boundary mediation"),
    "Gevurah":(1,Mode.JORDAN,"observables and judgment"),
    "Chesed":(2,Mode.JORDAN,"soft projection"),
    "Binah":(1,Mode.LIE,"Lie coherence placeholder"),
    "Chokhmah":(3,Mode.ALTERNATIVE,"Moufang branching"),
    "Keter":(3,Mode.EXCEPTIONAL_JORDAN,"h3(O)/F4 surrogate"),
}

def wit(level,seed):
    return CD(level,tuple(math.sin(seed+.73*k)+.1 for k in range(2**level)))

def layer(name,state=None,phase=None,witnesses=()):
    lvl,mode,_=SEFIROT[name]
    return Layer(name,lvl,mode,state or CD.real(1,lvl),phase or S2(0,0,1),witnesses=witnesses)

def run_self_test(verbose=True):
    qi,qj,qk=H(0,1,0,0),H(0,0,1,0),H(0,0,0,1)
    o1=O(1,.5,-.3,.7,.2,-.1,.4,.6); o2=O(.2,1.1,0,-.5,.3,.7,-.2,.1); o3=O(-.4,.6,.8,.1,-.3,.2,.5,-.7)
    sefirah={n: layer(n,witnesses=(wit(l,1.1),wit(l,2.3),wit(l,3.7))).is_coherent() for n,(l,_,__) in SEFIROT.items()}
    chain=[
        layer("Malkhut",R(1),S2(0,0,1),(R(1),R(2))),
        layer("Yesod",C(.7,.7),S2(.10,0,.995),(C(1),C(0,1))),
        layer("Hod",H(.5,.5,.5,.5),S2(.15,.05,.987),(H(1),H(0,1))),
        layer("Netzach",O(*([.35]*8)),S2(.18,.08,.980),(O(1),O(0,1),O(0,0,1))),
    ]
    out={
        "quaternion_identities":(qi*qj).close(qk) and (qj*qi).close(-qk),
        "norm_composition":all([norm_ok(R(2.3),R(-1.7)),norm_ok(C(1,2),C(-.5,3)),norm_ok(H(1,2,3,4),H(.5,-1,2,0)),norm_ok(o1,o2)]),
        "octonion_associator_defect":((o1*o2)*o3-o1*(o2*o3)).norm(),
        "octonion_moufang":moufang_ok(o1,o2,o3),
        "sefirah":sefirah,
        "bad_pairs_rejected":all([not compatible(3,Mode.LIE),not compatible(3,Mode.CLIFFORD),not compatible(0,Mode.ALTERNATIVE),not compatible(1,Mode.EXCEPTIONAL_JORDAN)]),
        "activation_cascade":[activate(a,b)[0] for a,b in zip(chain,chain[1:])],
    }
    out["all_checks_pass"]=out["quaternion_identities"] and out["norm_composition"] and out["octonion_associator_defect"]>1 and out["octonion_moufang"] and all(sefirah.values()) and out["bad_pairs_rejected"] and all(out["activation_cascade"])
    if verbose:
        print("SPO' ACTIVATION ENGINE -- self-test")
        for k,v in out.items(): print(f"{k}: {v}")
    return out

if __name__=="__main__":
    run_self_test()
