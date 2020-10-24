def floorSqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def halfdPartialKeyRecoveryAttack(d0,d0BitSize,nBitSize="nBitSize",n="n",e="e"):

    test = pow(3, e, n)
    test2 = pow(5, e, n)
    if(d0BitSize < nBitSize//2):
        return "Not enough bits of d0"
    for k in range(1,e):
        print k
        d = ((k * n + 1) // e)
        d >>= d0BitSize
        d <<= d0BitSize
        d |= d0
        if((e * d) % k == 1):
            if pow(test, d, n) == 3:
                if pow(test2, d, n) == 5:
                    totientN = (e*d - 1) // k
                    b = totientN - n - 1
                    discriminant = b*b - 4*n

                    root = floorSqrt(discriminant)
                    if(root*root != discriminant):
                        continue
                    p = (-b + root) // 2
                    q = n // p
                    print("[*] Factors are: %s and %s" % (p,q))
                    break

                    
d0 = 0x5df3654da7872b00afad05bb8dcb9e8a160caadb76001266792a6432a0466b1b65b740d5a4f341c9f0e7dd438d62d3c4de5b23731b2ab39c7226251e56598d89fd903f5d4cb046fc378c6697868b011613fec8fface5264a3504ebb9bcaa9ba5383b91b073f69be6c679e16c7b5d1de2c38213db59f6b378c0a69672657347bb8b70283c3cee5c1721be4ca9a3284a34ecf047c4017562f4c95a4313fff50bab87b850f651d0086883ad9b1ef369f2c73feb22b8fc592c9656b0ab212c0a59af76aef5211e3884b66af57af10ecb6d939fd96ca026fbb57b2270b97dbe8acef41750d55c1da00f12c7dda321d9d5cf735698cfcd46c9862cd088afa5ce59a50f27829afa5111ba889501
d0BitSize = 2128

n = 0x18e07c942b8868cf814613b3520f265b4e9dfe3085abc2b1b465dd9db858f36f1ac536ed4dcaeddec73e405a7fdc6a0851e86819ec56e1adee4e05e028291e1651f7824f384195e197314ee707be1ffea254dfbb4df4d3f4416c18348340ab1ada581fd4a74625c5f9043af57aad3466458a892f5fceedf42e43aa125a12d5cee0cbb9a49a883f39543cd2ff9d6b951b2a10f149a341c762ac8bca4f5c07120871dc96c7b3d75670f8a1e36fab624428ebf0f72fe5df06c6b399f72e74473860a4454750005f7d23cc446a073974bd6dff2ffa35a324fab87006b76bdc62c0004be0a380f1fa3d48010a8654557cac7927279e686e6c0144bc35b048471b2d7f94bb8a9a089d6ad1918de5e4fe06367fe9f4dd9cc02eebc612a9dba4b2206c5f109778cad9befe1b581f1ad588155cfd6a8cc72997101d7fe0aa2128f79f4042fcc30d351bd8037536e84b329f99f910d27a34c48f989912d506ef23b2224fd8cadf7417a66009b5d20c8baf043a938f9236bf1e07d62d6a2fc0271136226ac00b68ea972b27aeb21fade07b062d6f70b2c36f761b6b1e2d72b387fbd6637f071729280b85622f6024e78b8b9847ea673adb042e25e2dcc1dc2870cc1b32c45bdc575e883d19ea66f7f1b5afd43806b14332aaa323eb5ac21b430bcf94f8b1cf946d5764d557df9a47acc6b71e7277c8f817bb981a52c9eab7e3b91219514e4d
nBitSize = 4096

e = 0x10001                    
                    
halfdPartialKeyRecoveryAttack(d0, d0BitSize, nBitSize, n, e)