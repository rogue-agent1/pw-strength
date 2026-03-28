#!/usr/bin/env python3
"""pw_strength - Check password strength and generate suggestions."""
import sys, re, math, string, random

def check(pw):
    score = 0; feedback = []
    if len(pw) >= 8: score += 1
    else: feedback.append('Too short (min 8)')
    if len(pw) >= 12: score += 1
    if len(pw) >= 16: score += 1
    if re.search(r'[a-z]', pw): score += 1
    else: feedback.append('Add lowercase')
    if re.search(r'[A-Z]', pw): score += 1
    else: feedback.append('Add uppercase')
    if re.search(r'\d', pw): score += 1
    else: feedback.append('Add digits')
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', pw): score += 1
    else: feedback.append('Add symbols')
    if not re.search(r'(.)\1{2,}', pw): score += 1
    else: feedback.append('Repeated characters')
    # Entropy
    charset = 0
    if re.search(r'[a-z]', pw): charset += 26
    if re.search(r'[A-Z]', pw): charset += 26
    if re.search(r'\d', pw): charset += 10
    if re.search(r'[^a-zA-Z0-9]', pw): charset += 32
    entropy = len(pw) * math.log2(charset) if charset else 0
    levels = ['💀 Very Weak','🔴 Weak','🟡 Fair','🟢 Strong','💪 Very Strong']
    level = min(score // 2, 4)
    return {'score': score, 'max': 8, 'level': levels[level], 'entropy': entropy, 'feedback': feedback}

def generate(length=16, no_symbols=False):
    chars = string.ascii_letters + string.digits
    if not no_symbols: chars += '!@#$%^&*'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def main():
    args = sys.argv[1:]
    if not args or '-h' in args:
        print("Usage: pw_strength.py check PASSWORD | generate [LENGTH] [--no-symbols]"); return
    if args[0] == 'generate':
        length = int(args[1]) if len(args)>1 and args[1].isdigit() else 16
        print(generate(length, '--no-symbols' in args))
    elif args[0] == 'check':
        pw = args[1] if len(args)>1 else input('Password: ')
        r = check(pw)
        print(f"  {r['level']} ({r['score']}/{r['max']})")
        print(f"  Entropy: {r['entropy']:.1f} bits")
        if r['feedback']:
            for f in r['feedback']: print(f"  ⚠️  {f}")
    else:
        r = check(args[0])
        print(f"  {r['level']} ({r['score']}/{r['max']}) | {r['entropy']:.0f} bits entropy")

if __name__ == '__main__': main()
