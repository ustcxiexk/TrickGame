def turn(self, is_new_turn) -> dict:
    '''
    输入参数：   
        is_new_turn 崭新的一轮，在初始阶段或者是doubt之后执行，仅可以执行claim。
        ** 突然发现需要增加此参数 不然turn无法判断 或者可以写一个normal_turn和new_turn **
    返回值：  
    {
        'Win' : True/False,
        'Choice': 'Follow' | 'Doubt' | 'Claim' | 'Pass'
        ['Cards' : list(actually_played_cards)],        
        ['Claim' : dict(claim_length:int, claim_rank:card_rank)],
        
    }
    在开始新的一轮（Claim）的情况下， Cards, Claim参数均存在
    在跟牌（Follow）的情况下，仅存在Cards参数    #和第一种情况合并一下更好些。
    其他情况下不存在任何可选参数
    '''
    pass
