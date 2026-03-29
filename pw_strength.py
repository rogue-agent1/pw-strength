#!/usr/bin/env python3
"""pw_strength - Password strength checker."""
import sys,argparse,json,math,re,string
def analyze(pw):
    length=len(pw);charset=0;checks={}
    checks["length"]=length>=8;checks["upper"]=bool(re.search(r"[A-Z]",pw));checks["lower"]=bool(re.search(r"[a-z]",pw))
    checks["digit"]=bool(re.search(r"\d",pw));checks["special"]=bool(re.search(r"[^a-zA-Z0-9]",pw))
    if checks["upper"]:charset+=26
    if checks["lower"]:charset+=26
    if checks["digit"]:charset+=10
    if checks["special"]:charset+=32
    entropy=length*math.log2(charset) if charset else 0
    score=sum(checks.values());strength=["very weak","weak","fair","good","strong","very strong"][min(score,5)]
    return {"length":length,"entropy_bits":round(entropy,1),"charset_size":charset,"strength":strength,"score":f"{score}/5","checks":checks}
def main():
    p=argparse.ArgumentParser(description="Password strength");p.add_argument("password")
    args=p.parse_args();print(json.dumps(analyze(args.password),indent=2))
if __name__=="__main__":main()
