#coding=utf-8
#author:MrLyn、我擦咧什么鬼
#team:米斯特安全
def peig(data):
    code = dict(A='aaaaa',B='aaaab',C='aaaba',D='aaabb',E='aabaa',F='aabab',
                G='aabba',H='aabbb',I='abaaa',J='abaab',K='ababa',L='ababb',
                M='abbaa',N='abbab',O='abbba',P='abbbb',Q='baaaa',R='baaab',
                S='baaba',T='baabb',U='babaa',V='babab',W='babba',X='babbb',
                Y='bbaaa',Z='bbaab',a='AAAAA',g='AABBA',n='ABBAA',t='BAABA',
                b='AAAAB',h='AABBB',o='ABBAB',u='BAABB',c='AAABA',i='ABAAA',
                j='ABAAA',p='ABBBA',d='AAABB',k='ABAAB',q='ABBBB',x='BABAB',
                e='AABAA',l='ABABA',r='BAAAA',y='BABBA',f='AABAB',m='ABABB',
                s='BAAAB',z='BABBB',v='BAABB',w='BABAA')
    num1 = 0
	#aaaab aaaaa aaaba abbab abbaa abaaa baaab abbaa abbab baaba aabab abbab abbab aaabb
    s = ''
    l=[]
    answer = ''
    for i in range(len(data)/5):
        l.append(data[num1:num1+5])
        num1+=5
    answer = ''.join(x[0] for i in l for x in code.items() if i == x[1] and x[0] != 'j')
    answer_list = ['']
    num = 2
    for i in answer:
	if i != 'i':
	    for key,value in enumerate(answer_list):
		answer_list[key] = answer_list[key] + i
	elif i == 'i':
	    for key,value in enumerate(answer_list):
		answer_list.append(value + 'j')
		answer_list[key] = answer_list[key] + 'i'
		if len(answer_list) == num:
		    num = num * 2
		    break
    return answer_list
def run(data):
    ans = '\n'.join(peig(data))
    return ans