#!/usr/bin/env python3 -u

from cdapython import Q

for i in ["+", "-", "/", "*"]:
    
    bob = Q( f"days_to_birth >= 50 {i} 365" )
    dole =bob.subject.run() 


