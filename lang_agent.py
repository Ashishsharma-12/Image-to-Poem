l = ['', '                You are a poet;', '                You can generate a poem from a simple narrative, understand the theme, and use proper rhyming words.', '                The poem should not be shorter than 16 lines and not be longer than 20 lines.', '', '                Scenario: cartoon couple holding hands and walking in the grass', '', '                Write a poem based on the provided scenario.', '                ', '', '', '', '', 'Here is a poem based on the scenario:', '', 'Hand in hand, a tender hold', 'A love so strong, forever to be told', 'Two cartoon characters, a perfect pair', 'Walking in the grass, without a single care', '', 'Their love is pure, their bond is true', 'A joy to see, a story anew', 'The sun shines bright, the grass is green', 'A perfect day, a love serene', '', 'Their tiny hands, a sweet delight', 'A love so strong, a heart so bright'] 

l = l[15:]
s = ""
c = 0
for i in l:
    s += (i+"\n")

print(s)