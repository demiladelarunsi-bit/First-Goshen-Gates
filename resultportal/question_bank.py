""""
First Goshen Gate School — Question Bank Generator
Generates 5250+ questions across 9 grade levels procedurally.
"""

import random

# ═══════════════════════════════════════════════════════════
# DATA CONSTANTS
# ═══════════════════════════════════════════════════════════
FRUITS = ['apple','banana','mango','orange','grape','cherry','pear','peach','plum','kiwi',
          'melon','lemon','lime','fig','date','papaya','guava','coconut','pineapple','pomegranate',
          'watermelon','strawberry','blueberry','raspberry','apricot','avocado','jackfruit','lychee','tangerine']
VEGETABLES = ['carrot','potato','tomato','onion','cabbage','broccoli','spinach','corn','pepper',
              'cucumber','radish','turnip','beetroot','cauliflower','eggplant','celery','peas','beans',
              'pumpkin','zucchini','lettuce','ginger','garlic','mushroom','artichoke']
ANIMALS = ['dog','cat','cow','goat','sheep','horse','hen','duck','fish','lion','tiger','elephant',
           'monkey','rabbit','deer','bear','fox','wolf','frog','snake','parrot','eagle','crow',
           'sparrow','whale','dolphin','shark','turtle','lizard','crocodile','penguin','giraffe',
           'zebra','kangaroo','octopus','butterfly','ant','bee','spider','scorpion']
ANIMAL_SOUNDS = {'dog':'Bark','cat':'Meow','cow':'Moo','goat':'Bleat','sheep':'Baa','horse':'Neigh',
                 'hen':'Cluck','duck':'Quack','lion':'Roar','tiger':'Growl','elephant':'Trumpet',
                 'frog':'Croak','snake':'Hiss','crow':'Caw','owl':'Hoot','pig':'Oink','donkey':'Bray',
                 'rooster':'Crow','turkey':'Gobble','cricket':'Chirp'}
ANIMAL_BABIES = {'dog':'Puppy','cat':'Kitten','cow':'Calf','horse':'Foal','sheep':'Lamb','goat':'Kid',
                 'hen':'Chick','duck':'Duckling','lion':'Cub','tiger':'Cub','elephant':'Calf',
                 'bear':'Cub','deer':'Fawn','rabbit':'Bunny','swan':'Cygnet','goose':'Gosling',
                 'pig':'Piglet','frog':'Tadpole','butterfly':'Caterpillar','fish':'Fry'}
BODY_PARTS = ['head','eye','ear','nose','mouth','hand','foot','leg','arm','finger','toe','knee',
              'elbow','shoulder','neck','chest','back','stomach','hair','tooth','tongue','lip',
              'chin','wrist','ankle','thumb','heel','palm','forehead']
COLORS = ['red','blue','green','yellow','orange','purple','pink','white','black','brown','gray',
          'gold','silver','violet','indigo','turquoise','maroon','navy','beige','crimson']
SHAPES = ['circle','square','triangle','rectangle','oval','diamond','star','heart','hexagon',
          'pentagon','octagon','cube','sphere','cylinder','cone','pyramid']
OPPOSITES = [['big','small'],['hot','cold'],['up','down'],['in','out'],['happy','sad'],['fast','slow'],
             ['hard','soft'],['tall','short'],['heavy','light'],['dark','light'],['open','close'],
             ['wet','dry'],['clean','dirty'],['old','new'],['rich','poor'],['loud','quiet'],
             ['strong','weak'],['empty','full'],['rough','smooth'],['thin','thick'],['push','pull'],
             ['day','night'],['boy','girl'],['love','hate'],['laugh','cry'],['safe','dangerous'],
             ['sweet','sour'],['brave','cowardly'],['gentle','rough'],['smart','foolish'],['kind','cruel']]
PLURALS = [['cat','cats'],['dog','dogs'],['book','books'],['pen','pens'],['tree','trees'],['bird','birds'],
           ['car','cars'],['boy','boys'],['girl','girls'],['star','stars'],['flower','flowers'],
           ['door','doors'],['chair','chairs'],['table','tables'],['cup','cups'],['box','boxes'],
           ['bus','buses'],['brush','brushes'],['baby','babies'],['city','cities'],['leaf','leaves'],
           ['knife','knives'],['wolf','wolves'],['shelf','shelves'],['child','children'],['man','men'],
           ['woman','women'],['foot','feet'],['tooth','teeth'],['mouse','mice'],['goose','geese'],
           ['person','people'],['sheep','sheep'],['fish','fish'],['deer','deer'],['ox','oxen'],
           ['cactus','cacti'],['focus','foci'],['fungus','fungi'],['life','lives'],['wife','wives'],
           ['half','halves'],['self','selves'],['loaf','loaves']]
RHYMING = [['cat','bat','hat','mat','rat','sat','fat'],['dog','log','fog','hog','jog','bog'],
           ['sun','fun','run','bun','gun','nun'],['bed','red','fed','led','shed','wed'],
           ['ring','sing','king','wing','thing','string'],['fly','sky','high','tie','cry','dry'],
           ['cake','bake','make','lake','take','sake'],['boat','coat','goat','float','moat','note'],
           ['tree','bee','free','see','three','agree'],['light','night','right','fight','sight','might'],
           ['ball','tall','fall','call','wall','hall'],['rain','train','chain','pain','main','gain']]
TRANSPORTS = ['car','bus','train','bicycle','airplane','boat','ship','motorcycle','scooter','truck',
              'van','helicopter','subway','tram','rocket','ambulance','fire engine','tractor','taxi','jeep']
DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
SEASONS = ['Spring','Summer','Autumn','Winter']
FESTIVALS = ['Diwali','Christmas','Eid','Holi','Dussehra','Easter','Bakrid','Pongal','Onam',
             'Ganesh Chaturthi','Baisakhi','Lohri','Raksha Bandhan','Navratri','Makar Sankranti']
OCCUPATIONS = ['doctor','teacher','pilot','farmer','chef','driver','nurse','police','soldier','engineer',
               'artist','scientist','lawyer','judge','dentist','architect','plumber','electrician','carpenter','tailor']
PLACES = ['hospital','school','park','library','airport','station','market','museum','zoo','beach',
          'mountain','river','lake','forest','desert','island','village','city','country','planet']
MATERIALS = ['wood','metal','glass','plastic','paper','cloth','stone','rubber','leather','silk',
             'cotton','wool','clay','brick','concrete','iron','gold','silver','copper','aluminum']
FOODS = ['rice','bread','egg','milk','butter','cheese','sugar','salt','flour','honey','jam','soup',
         'salad','pasta','pizza','burger','noodles','roti','dal','curry','biscuit','cake','ice cream',
         'chocolate','sandwich']
BIRDS = ['parrot','eagle','crow','sparrow','pigeon','peacock','owl','duck','hen','ostrich','penguin',
         'flamingo','swan','robin','partridge','vulture','hawk','woodpecker','hummingbird','stork']
INSECTS = ['ant','bee','butterfly','spider','mosquito','fly','ladybug','dragonfly','grasshopper',
           'beetle','caterpillar','wasp','termite','moth','cricket','cockroach','scorpion','centipede',
           'millipede','snail']
WATER_BODIES = ['ocean','sea','river','lake','pond','stream','waterfall','creek','bay','gulf',
                'strait','canal','lagoon','glacier','spring']
PLANETS = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune']
CONTINENTS = ['Asia','Africa','North America','South America','Europe','Australia','Antarctica']
COUNTRIES = ['India','USA','UK','Japan','China','France','Germany','Brazil','Canada','Australia',
             'Russia','Italy','Spain','Mexico','South Korea','Egypt','South Africa','Nigeria','Thailand','Indonesia']
SPELLING_3 = ['cat','dog','bat','hat','rat','mat','sun','run','fun','bus','cup','red','bed','hen','pen',
              'ten','net','sit','bit','fit','pin','win','dig','big','pig','mop','top','hop','pop','box',
              'fox','mix','six','fix','yes','jet','wet','get','let','set']
SPELLING_4 = ['frog','tree','bird','fish','duck','goat','bear','lion','milk','rice','cake','ball','door',
              'book','hand','foot','leg','arm','nose','eye','ear','mouth','fire','rain','snow','star',
              'moon','cold','warm','blue','pink','gold','dark','road','home','farm','ship','boat','ring','king']
SPELLING_5 = ['apple','grape','mango','peach','lemon','melon','berry','horse','sheep','mouse','snake',
              'whale','eagle','green','brown','black','white','house','water','light','night','plant',
              'flower','grass','earth','stone','cloud','river','ocean','beach','chair','table','clock',
              'phone','bread','cheese','butter','sugar','honey','pasta']
SPELLING_6 = ['orange','banana','cherry','potato','tomato','onion','carrot','pepper','rabbit','monkey',
              'parrot','spider','turtle','lizard','purple','yellow','silver','bronze','window','garden',
              'kitchen','bedroom','winter','summer','spring','autumn','sunset','sunrise','forest','island',
              'mountain','basket','blanket','candle','dinner','family','friend','school','letter','number',
              'pencil','eraser']
SPELLING_7 = ['pineapple','coconut','pumpkin','broccoli','cucumber','dolphin','penguin','leopard','giraffe',
              'octopus','cricket','rainbow','thunder','weather','country','village','library','airport',
              'hospital','kitchen','bedroom','bathroom','curtain','picture','morning','evening','holiday',
              'birthday','present','balloon','soldier','emperor','kingdom','freedom','journey','comfort',
              'blanket','cushion','fireplace']
GRAMMAR_IS_ARE = [['The cat___on the mat.','is'],['Dogs___loyal animals.','are'],['She___my best friend.','is'],
                  ['They___going to school.','are'],['He___very tall.','is'],['We___happy today.','are'],
                  ['It___raining outside.','is'],['Birds___flying in the sky.','are'],['My mother___a teacher.','is'],
                  ['The flowers___beautiful.','are'],['The sun___bright.','is'],['The children___playing.','are'],
                  ['This___my book.','is'],['Those___my shoes.','are'],['Tom___at home.','is'],
                  ['Apples___sweet.','are'],['A dog___a faithful animal.','is'],['My friends___coming over.','are'],
                  ['The baby___crying.','is'],['The books___on the shelf.','are']]
GRAMMAR_A_AN = [['___apple a day keeps the doctor away.','An'],['I saw___elephant at the zoo.','an'],
                ['She is___honest woman.','an'],['He gave me___umbrella.','an'],['___hour has sixty minutes.','An'],
                ['This is___unique opportunity.','a'],['I need___new pen.','a'],['She wore___uniform to school.','a'],
                ['He is___European.','a'],['That was___interesting story.','an'],['I ate___orange for breakfast.','an'],
                ['She has___uncle in Delhi.','an'],['We had___great time.','a'],['He is___MBA graduate.','an'],
                ['___lion is a wild animal.','A'],['I found___egg in the nest.','an'],['She bought___new car.','a'],
                ['He is___artist.','an'],['It was___cold morning.','a'],['She is___Indian.','an']]
COLOR_OBJECTS = {'red':'Blood / Tomato','blue':'Sky / Ocean','green':'Grass / Leaves','yellow':'Sun / Banana',
                 'orange':'Orange fruit','purple':'Grapes / Eggplant','pink':'Rose / Flamingo',
                 'white':'Snow / Milk','black':'Night / Coal','brown':'Chocolate / Earth'}
SHAPE_DESC = {'circle':'A round shape with no corners','square':'A shape with 4 equal sides and 4 right angles',
              'triangle':'A shape with 3 sides','rectangle':'A shape with 4 sides, opposite sides equal',
              'oval':'An elongated round shape','diamond':'A shape like a tilted square',
              'star':'A shape with pointed rays from a center','hexagon':'A shape with 6 sides',
              'pentagon':'A shape with 5 sides'}
PART_FUNC = {'eye':'see','ear':'hear','nose':'smell','mouth':'eat and speak','hand':'hold things',
             'foot':'walk','leg':'walk and run','arm':'reach and lift','tongue':'taste food',
             'tooth':'chew food','finger':'pick up small things','skin':'feel touch','heart':'pump blood',
             'brain':'think','lung':'breathe','bone':'support the body','muscle':'move the body',
             'stomach':'digest food'}
FACTS_ANIMALS = [
    ['Which animal is the largest on land?','Elephant',['Lion','Giraffe','Hippo']],
    ['Which animal lives in water?','Fish',['Dog','Cat','Bird']],
    ['Which bird can fly?','Eagle',['Penguin','Ostrich','Kiwi']],
    ['Which animal has a trunk?','Elephant',['Lion','Tiger','Bear']],
    ['Which animal is the King of the Jungle?','Lion',['Tiger','Elephant','Bear']],
    ['Which animal gives us milk?','Cow',['Dog','Cat','Goat']],
    ['Which animal has a long neck?','Giraffe',['Elephant','Horse','Zebra']],
    ['Which insect makes honey?','Bee',['Ant','Butterfly','Spider']],
    ['Which animal hops?','Kangaroo',['Rabbit','Frog','Deer']],
    ['Which reptile has a shell?','Turtle',['Snake','Lizard','Crocodile']],
    ['Which animal is the fastest on land?','Cheetah',['Lion','Horse','Tiger']],
    ['Which bird has colourful feathers?','Peacock',['Crow','Sparrow','Eagle']],
    ['Which animal lives in the desert?','Camel',['Fish','Penguin','Frog']],
    ['Which pet animal purrs?','Cat',['Dog','Rabbit','Hamster']],
    ['Which sea animal is the largest?','Blue Whale',['Shark','Dolphin','Octopus']],
    ['Which animal has stripes?','Zebra',['Horse','Donkey','Cow']],
    ['Which animal changes colour?','Chameleon',['Lizard','Snake','Frog']],
    ['Which animal builds a web?','Spider',['Ant','Bee','Butterfly']],
    ['Which animal has wings but cannot fly?','Penguin',['Eagle','Parrot','Owl']],
    ['Which animal is a symbol of wisdom?','Owl',['Parrot','Crow','Pigeon']],
]
FACTS_SCIENCE = [
    ['What do plants need to grow?','Sunlight and Water',['Ice and Sand','Darkness and Oil','Salt and Pepper']],
    ['What is the closest star to Earth?','Sun',['Moon','Mars','Polaris']],
    ['What do we breathe in?','Oxygen',['Carbon Dioxide','Nitrogen','Hydrogen']],
    ['What falls from clouds?','Rain',['Snow only','Sunshine','Dust']],
    ['How many planets are in our solar system?','8',['7','9','10']],
    ['What is the largest planet?','Jupiter',['Saturn','Earth','Neptune']],
    ['What planet do we live on?','Earth',['Mars','Venus','Jupiter']],
    ['What is water made of?','Hydrogen and Oxygen',['Salt and Sugar','Iron and Copper','Carbon and Nitrogen']],
    ['What is the boiling point of water?','100\u00b0C',['50\u00b0C','75\u00b0C','120\u00b0C']],
    ['What is the freezing point of water?','0\u00b0C',['10\u00b0C','-10\u00b0C','32\u00b0C']],
    ['Which gas do plants absorb?','Carbon Dioxide',['Oxygen','Nitrogen','Helium']],
    ['Which gas do plants release?','Oxygen',['Carbon Dioxide','Nitrogen','Hydrogen']],
    ['What is the centre of the Earth called?','Core',['Crust','Mantle','Surface']],
    ['What causes day and night?','Earth rotating on its axis',['Sun moving','Moon rotating','Clouds moving']],
    ['What causes seasons?','Earth tilting on its axis',['Distance from Sun','Moon phases','Wind patterns']],
    ['What is the hardest natural substance?','Diamond',['Iron','Gold','Steel']],
    ['What organ pumps blood?','Heart',['Brain','Lungs','Stomach']],
    ['What is the largest organ of the body?','Skin',['Heart','Liver','Brain']],
    ['How many bones does an adult have?','206',['150','300','106']],
    ['What is the process of food breaking down?','Digestion',['Breathing','Circulation','Photosynthesis']],
    ['What force pulls things down?','Gravity',['Magnetism','Friction','Air pressure']],
    ['Which planet is the Red Planet?','Mars',['Venus','Jupiter','Saturn']],
    ['Which planet has rings?','Saturn',['Jupiter','Uranus','Neptune']],
    ['How does a plant make food?','Photosynthesis',['Respiration','Digestion','Evaporation']],
]
FACTS_GK = [
    ['What is the capital of India?','New Delhi',['Mumbai','Kolkata','Chennai']],
    ['What is the national animal of India?','Tiger',['Lion','Elephant','Peacock']],
    ['What is the national bird of India?','Peacock',['Parrot','Eagle','Sparrow']],
    ['What is the national flower of India?','Lotus',['Rose','Sunflower','Jasmine']],
    ['How many states are in India?','28',['29','30','27']],
    ['What is the largest continent?','Asia',['Africa','Europe','North America']],
    ['What is the largest ocean?','Pacific Ocean',['Atlantic Ocean','Indian Ocean','Arctic Ocean']],
    ['What is the longest river in the world?','Nile',['Amazon','Ganges','Mississippi']],
    ['What is the highest mountain?','Mount Everest',['K2','Kangchenjunga','Lhotse']],
    ['What is the currency of India?','Rupee',['Dollar','Pound','Yen']],
    ['Which festival is the Festival of Lights?','Diwali',['Holi','Eid','Christmas']],
    ['Which festival is the Festival of Colours?','Holi',['Diwali','Dussehra','Eid']],
    ['What sport is India famous for?','Cricket',['Hockey','Football','Tennis']],
    ['What is the main language of India?','Hindi',['English','Bengali','Tamil']],
    ['Who wrote the national anthem?','Rabindranath Tagore',['Mahatma Gandhi','Jawaharlal Nehru','Bankim Chandra']],
    ['What is the largest country?','Russia',['China','USA','Canada']],
    ['What is the smallest country?','Vatican City',['Monaco','Maldives','Nauru']],
    ['What is the capital of the USA?','Washington D.C.',['New York','Los Angeles','Chicago']],
]
ODD_ONE_OUT = [
    [['Apple','Mango','Carrot','Banana'],'Carrot'],
    [['Dog','Cat','Cow','Chair'],'Chair'],
    [['Red','Blue','Circle','Green'],'Circle'],
    [['Sun','Moon','Star','Table'],'Table'],
    [['Rose','Mango','Lily','Sunflower'],'Mango'],
    [['Eagle','Parrot','Fish','Crow'],'Fish'],
    [['Carrot','Potato','Onion','Apple'],'Apple'],
    [['Bus','Car','Bicycle','Tree'],'Tree'],
    [['Pen','Pencil','Book','Chair'],'Chair'],
    [['Monday','January','Tuesday','Wednesday'],'January'],
    [['Summer','Winter','Friday','Spring'],'Friday'],
    [['Milk','Water','Juice','Rock'],'Rock'],
    [['Iron','Wood','Gold','Silver'],'Wood'],
    [['Lion','Tiger','Shark','Elephant'],'Shark'],
    [['Nose','Eye','Ear','Leg'],'Leg'],
    [['Doctor','Teacher','Pilot','Table'],'Table'],
    [['Earth','Mars','Sun','Venus'],'Sun'],
    [['Triangle','Square','Circle','Red'],'Red'],
    [['Rice','Bread','Water','Roti'],'Water'],
    [['Hospital','School','Park','Pencil'],'Pencil'],
]


# ═══════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════
def pick_random(rng, pool, n):
    pool = list(pool)
    rng.shuffle(pool)
    return pool[:n]

def make_num_distractors(rng, correct, max_range=20):
    dists = set()
    offsets = [1, -1, 2, -2, 3, -3, 5, -5, 10, -10]
    attempts = 0
    while len(dists) < 3 and attempts < 50:
        off = rng.choice(offsets)
        d = correct + off
        if d >= 0 and d != correct:
            dists.add(d)
        attempts += 1
    while len(dists) < 3:
        dists.add(correct + len(dists) + 10)
    return list(dists)

def make_question(text, correct, distractors, marks=1):
    opts = [correct] + list(distractors[:3])
    while len(opts) < 4:
        opts.append(correct + ' (alt)')
    random.shuffle(opts)
    letters = ['A', 'B', 'C', 'D']
    correct_letter = letters[opts.index(correct)]
    return {
        'question_text': text,
        'question_type': 'multiple_choice',
        'option_a': str(opts[0]),
        'option_b': str(opts[1]),
        'option_c': str(opts[2]),
        'option_d': str(opts[3]),
        'correct_answer': correct_letter,
        'marks': marks,
    }

def make_spelling_distractors(word):
    w = word.lower()
    dists = []
    if len(w) >= 2:
        for i in range(len(w) - 1):
            d = w[:i] + w[i+1] + w[i] + w[i+2:]
            if d != w and len(dists) < 2:
                dists.append(d)
    if len(w) > 2 and len(dists) < 3:
        i = len(w) // 2
        dists.append(w[:i] + w[i+1:])
    if len(dists) < 3:
        for i in range(len(w)):
            if w[i] in 'aeiou':
                for v in 'aeiou':
                    if v != w[i]:
                        d = w[:i] + v + w[i+1:]
                        if d != w and d not in dists:
                            dists.append(d)
                            break
            if len(dists) >= 3:
                break
    if len(dists) < 3:
        i = len(w) // 2
        dists.append(w[:i] + 'e' + w[i:])
    return dists[:3]


# ═══════════════════════════════════════════════════════════
# QUESTION GENERATORS
# ═══════════════════════════════════════════════════════════
def gen_addition(rng, min_a, max_a, min_b, max_b, count):
    qs, seen = [], set()
    while len(qs) < count:
        a = rng.randint(min_a, max_a)
        b = rng.randint(min_b, max_b)
        c = a + b
        key = f'{a}+{b}'
        if key in seen:
            continue
        seen.add(key)
        dists = make_num_distractors(rng, c, 20)
        qs.append(make_question(f'What is {a} + {b}?', str(c), [str(d) for d in dists], 1))
    return qs

def gen_subtraction(rng, min_a, max_a, min_b, max_b, count):
    qs, seen = [], set()
    while len(qs) < count:
        a = rng.randint(min_a, max_a)
        b = rng.randint(min_b, max_b)
        if b > a:
            a, b = b, a
        c = a - b
        key = f'{a}-{b}'
        if key in seen:
            continue
        seen.add(key)
        dists = make_num_distractors(rng, c, 20)
        qs.append(make_question(f'What is {a} \u2212 {b}?', str(c), [str(d) for d in dists], 1))
    return qs

def gen_multiplication(rng, min_a, max_a, min_b, max_b, count):
    qs, seen = [], set()
    while len(qs) < count:
        a = rng.randint(min_a, max_a)
        b = rng.randint(min_b, max_b)
        c = a * b
        key = f'{a}x{b}'
        if key in seen:
            continue
        seen.add(key)
        dists = make_num_distractors(rng, c, max(c, 20))
        qs.append(make_question(f'What is {a} \u00d7 {b}?', str(c), [str(d) for d in dists], 2))
    return qs

def gen_division(rng, min_q, max_q, max_divisor, count):
    qs, seen = [], set()
    while len(qs) < count:
        q = rng.randint(min_q, max_q)
        d = rng.randint(2, max_divisor)
        a = q * d
        key = f'{a}/{d}'
        if key in seen:
            continue
        seen.add(key)
        dists = make_num_distractors(rng, q, 20)
        qs.append(make_question(f'What is {a} \u00f7 {d}?', str(q), [str(d) for d in dists], 2))
    return qs

def gen_bigger(rng, max_num, count):
    qs, seen = [], set()
    while len(qs) < count:
        a = rng.randint(1, max_num)
        b = rng.randint(1, max_num)
        if a == b:
            continue
        bigger = max(a, b)
        smaller = min(a, b)
        key = f'{smaller}_{bigger}'
        if key in seen:
            continue
        seen.add(key)
        dists = [str(smaller)]
        extra = rng.randint(1, max_num)
        if str(extra) != str(bigger) and str(extra) not in dists:
            dists.append(str(extra))
        else:
            dists.append(str(bigger + 1))
        extra2 = rng.randint(1, max_num)
        if str(extra2) != str(bigger) and str(extra2) not in dists:
            dists.append(str(extra2))
        else:
            dists.append(str(max(1, bigger - 2)))
        while len(dists) < 3:
            dists.append(str(bigger + len(dists) + 5))
        qs.append(make_question(f'Which number is bigger: {a} or {b}?', str(bigger), dists[:3], 1))
    return qs

def gen_before_after(rng, max_num, count):
    qs, seen = [], set()
    while len(qs) < count:
        n = rng.randint(2, max_num)
        is_before = rng.choice([True, False])
        ans = n - 1 if is_before else n + 1
        key = f'{n}_{"b" if is_before else "a"}'
        if key in seen:
            continue
        seen.add(key)
        text = f'What number comes before {n}?' if is_before else f'What number comes after {n}?'
        dists = make_num_distractors(rng, ans, 10)
        qs.append(make_question(text, str(ans), [str(d) for d in dists], 1))
    return qs

def gen_missing_number(rng, max_num, count):
    qs, seen = [], set()
    while len(qs) < count:
        step = rng.randint(1, 3)
        start = rng.randint(1, max(1, max_num - step * 4))
        pos = rng.randint(0, 3)
        nums = [start + step * i for i in range(4)]
        ans = nums[pos]
        display = ', '.join(['?' if i == pos else str(n) for i, n in enumerate(nums)])
        key = f'{start}_{step}_{pos}'
        if key in seen:
            continue
        seen.add(key)
        dists = make_num_distractors(rng, ans, step * 5)
        qs.append(make_question(f'What is the missing number: {display}?', str(ans), [str(d) for d in dists], 2))
    return qs

def gen_counting(rng, max_num, count):
    qs, seen = [], set()
    items = ['apples','mangoes','stars','balls','cats','dogs','birds','flowers','books','pens']
    while len(qs) < count:
        n = rng.randint(1, min(max_num, 20))
        item = rng.choice(items)
        key = f'{n}_{item}'
        if key in seen:
            continue
        seen.add(key)
        dists = make_num_distractors(rng, n, 10)
        qs.append(make_question(f'If you have {n} {item} and give away 0, how many do you have?', str(n), [str(d) for d in dists], 1))
    return qs

def gen_animal_sounds(rng, count):
    qs = []
    entries = list(ANIMAL_SOUNDS.items())
    rng.shuffle(entries)
    for animal, sound in entries[:count]:
        dists = pick_random(rng, [s for s in ANIMAL_SOUNDS.values() if s != sound], 3)
        qs.append(make_question(f'What sound does a {animal} make?', sound, dists, 1))
    return qs

def gen_animal_babies(rng, count):
    qs = []
    entries = list(ANIMAL_BABIES.items())
    rng.shuffle(entries)
    for animal, baby in entries[:count]:
        dists = pick_random(rng, [b for b in ANIMAL_BABIES.values() if b != baby], 3)
        qs.append(make_question(f'What is a baby {animal} called?', baby, dists, 1))
    return qs

def gen_spelling(rng, word_list, count):
    qs = []
    words = list(word_list)
    rng.shuffle(words)
    for word in words[:count]:
        dists = make_spelling_distractors(word)
        qs.append(make_question(f'How do you spell: "{word}"?', word, dists, 1))
    return qs

def gen_opposites(rng, count):
    qs = []
    pairs = list(OPPOSITES)
    rng.shuffle(pairs)
    for word, opp in pairs[:count]:
        dists = pick_random(rng, [p[1] for p in OPPOSITES if p[1] != opp], 3)
        qs.append(make_question(f'What is the opposite of "{word}"?', opp, dists, 1))
    return qs

def gen_plurals(rng, count):
    qs = []
    pairs = list(PLURALS)
    rng.shuffle(pairs)
    for singular, plural in pairs[:count]:
        dists = pick_random(rng, [p[1] for p in PLURALS if p[1] != plural], 3)
        qs.append(make_question(f'What is the plural of "{singular}"?', plural, dists, 1))
    return qs

def gen_rhyming(rng, count):
    qs = []
    groups = list(RHYMING)
    rng.shuffle(groups)
    for group in groups[:count]:
        word = group[0]
        correct = rng.choice(group[1:])
        all_others = [w for g in RHYMING for w in g if w != word and w not in group]
        dists = pick_random(rng, all_others, 3)
        qs.append(make_question(f'Which word rhymes with "{word}"?', correct, dists, 1))
    return qs

def gen_which_is(rng, category, correct_items, wrong_pool, count):
    qs, seen = [], set()
    while len(qs) < count:
        correct = rng.choice(correct_items)
        wrongs = pick_random(rng, [w for w in wrong_pool if w != correct], 3)
        if len(wrongs) < 3:
            continue
        key = '_'.join(sorted(wrongs)) + correct
        if key in seen:
            continue
        seen.add(key)
        qs.append(make_question(f'Which of these is a {category}?', correct, wrongs, 1))
    return qs

def gen_colors(rng, count):
    qs = []
    entries = list(COLOR_OBJECTS.items())
    rng.shuffle(entries)
    for color, hint in entries[:count]:
        dists = pick_random(rng, [c for c in COLORS if c != color], 3)
        qs.append(make_question(f'What colour is {hint}?', color, dists, 1))
    return qs

def gen_shapes(rng, count):
    qs = []
    entries = list(SHAPE_DESC.items())
    rng.shuffle(entries)
    for shape, desc in entries[:count]:
        dists = pick_random(rng, [s for s in SHAPES if s != shape], 3)
        qs.append(make_question(f'Which shape: "{desc}"?', shape, dists, 1))
    return qs

def gen_body_parts(rng, count):
    qs = []
    entries = list(PART_FUNC.items())
    rng.shuffle(entries)
    for part, func in entries[:count]:
        dists = pick_random(rng, [p for p in BODY_PARTS if p != part], 3)
        qs.append(make_question(f'Which body part is used to {func}?', part, dists, 1))
    return qs

def gen_days_months(rng, type_name, count):
    qs = []
    lst = DAYS if type_name == 'days' else MONTHS
    label = 'day of the week' if type_name == 'days' else 'month of the year'
    for _ in range(count):
        idx = rng.randint(0, len(lst) - 1)
        if idx == 0:
            q_text = f'What is the first {label}?'
        else:
            q_text = f'What {label} comes after {lst[idx-1]}?'
        dists = pick_random(rng, [x for x in lst if x != lst[idx]], 3)
        qs.append(make_question(q_text, lst[idx], dists, 1))
    return qs

def gen_grammar_is_are(rng, count):
    qs = []
    pairs = list(GRAMMAR_IS_ARE)
    rng.shuffle(pairs)
    for sentence, ans in pairs[:count]:
        display = sentence.replace('___', '____')
        dists = ['are', 'am', 'was'] if ans == 'is' else ['is', 'am', 'was']
        qs.append(make_question(f'Fill in the blank: {display}', ans, dists, 1))
    return qs

def gen_grammar_a_an(rng, count):
    qs = []
    pairs = list(GRAMMAR_A_AN)
    rng.shuffle(pairs)
    for sentence, ans in pairs[:count]:
        display = sentence.replace('___', '____')
        dists = ['an', 'the', 'one'] if ans == 'a' else ['a', 'the', 'one']
        qs.append(make_question(f'Fill in the blank: {display}', ans, dists, 1))
    return qs

def gen_vowels_consonants(rng, count):
    qs = []
    letters = list('abcdefghijklmnopqrstuvwxyz')
    rng.shuffle(letters)
    for letter in letters[:count]:
        ans = 'Vowel' if letter in 'aeiou' else 'Consonant'
        qs.append(make_question(f'Is "{letter.upper()}" a vowel or consonant?', ans,
                                ['Vowel', 'Consonant', 'Number', 'Symbol'], 1))
    return qs

def gen_capital_small(rng, count):
    qs = []
    letters = list('abcdefghijklmnopqrstuvwxyz')
    rng.shuffle(letters)
    for letter in letters[:count]:
        if rng.choice([True, False]):
            ans = letter.upper()
            dists = pick_random(rng, [l.upper() for l in letters if l != letter], 3)
            qs.append(make_question(f'Capital letter of "{letter}"?', ans, dists, 1))
        else:
            dists = pick_random(rng, [l for l in letters if l != letter], 3)
            qs.append(make_question(f'Small letter of "{letter.upper()}"?', letter, dists, 1))
    return qs

def gen_word_problems(rng, level, count):
    qs, seen = [], set()
    names = ['Ram','Priya','Arjun','Meera','Sita','Rahul','Anita','Vikram','Neha','Ravi',
             'Pooja','Amit','Kiran','Divya','Samuel','Grace','David','Faith','Hope','Joy']
    items = ['apples','mangoes','books','pens','balls','toys','stickers','coins','marbles','flowers']
    while len(qs) < count:
        name = rng.choice(names)
        item = rng.choice(items)
        ptype = rng.randint(0, 2)
        if ptype == 0:
            a = rng.randint(1, level * 10) if level > 2 else rng.randint(1, 9)
            b = rng.randint(1, level * 10) if level > 2 else rng.randint(1, 9)
            text = f'{name} has {a} {item} and buys {b} more. How many {item} now?'
            ans = a + b
        elif ptype == 1:
            a = rng.randint(5, level * 15) if level > 2 else rng.randint(5, 15)
            b = rng.randint(1, min(a - 1, level * 5))
            text = f'{name} has {a} {item} and gives {b} away. How many left?'
            ans = a - b
        else:
            a = rng.randint(2, level * 3 if level > 2 else 5)
            b = rng.randint(2, level * 3 if level > 2 else 3)
            text = f'{name} has {b} bags with {a} {item} each. How many {item} total?'
            ans = a * b
        if text in seen:
            continue
        seen.add(text)
        dists = make_num_distractors(rng, ans, max(20, ans))
        qs.append(make_question(text, str(ans), [str(d) for d in dists], level >= 3 and 2 or 1))
    return qs

def gen_facts(rng, facts, count):
    qs = []
    facts = list(facts)
    rng.shuffle(facts)
    for q_text, ans, wrongs in facts[:count]:
        qs.append(make_question(q_text, ans, wrongs[:3], 2))
    return qs

def gen_odd_one_out(rng, sets, count):
    qs = []
    sets = list(sets)
    rng.shuffle(sets)
    for items, odd in sets[:count]:
        opts = list(items)
        rng.shuffle(opts)
        letters = ['A', 'B', 'C', 'D']
        correct_letter = letters[opts.index(odd)]
        qs.append({
            'question_text': f'Which does NOT belong: {", ".join(opts)}?',
            'question_type': 'multiple_choice',
            'option_a': opts[0], 'option_b': opts[1],
            'option_c': opts[2], 'option_d': opts[3],
            'correct_answer': correct_letter, 'marks': 2,
        })
    return qs

def gen_fractions(rng, ftype, count):
    qs, seen = [], set()
    while len(qs) < count:
        if ftype == 'identify':
            d = rng.randint(2, 9)
            n = rng.randint(1, d - 1)
            key = f'id_{n}_{d}'
            if key in seen: continue
            seen.add(key)
            ans = f'{n}/{d}'
            dists = []
            while len(dists) < 3:
                dn = rng.randint(1, d)
                ds = f'{dn}/{d}'
                if ds != ans and ds not in dists:
                    dists.append(ds)
            qs.append(make_question(f'What fraction is {n} out of {d} equal parts?', ans, dists, 2))
        elif ftype == 'compare':
            d1, d2 = rng.randint(2, 7), rng.randint(2, 7)
            n1, n2 = rng.randint(1, d1-1), rng.randint(1, d2-1)
            v1, v2 = n1/d1, n2/d2
            if abs(v1 - v2) < 0.01: continue
            bigger = f'{n1}/{d1}' if v1 > v2 else f'{n2}/{d2}'
            smaller = f'{n2}/{d2}' if v1 > v2 else f'{n1}/{d1}'
            key = f'cmp_{n1}_{d1}_{n2}_{d2}'
            if key in seen: continue
            seen.add(key)
            d3 = rng.randint(2, 7)
            n3 = rng.randint(1, d3-1)
            ds = f'{n3}/{d3}'
            dists = [smaller]
            if ds != bigger and ds not in dists: dists.append(ds)
            while len(dists) < 3:
                dists.append(f'{rng.randint(1,5)}/{rng.randint(2,6)}')
            qs.append(make_question(f'Which is larger: {n1}/{d1} or {n2}/{d2}?', bigger, dists[:3], 3))
        else:
            d = rng.randint(2, 6)
            n1, n2 = rng.randint(1, d-1), rng.randint(1, d-1)
            ans_n = n1 + n2
            key = f'add_{n1}_{d}_{n2}'
            if key in seen: continue
            seen.add(key)
            ans = f'{ans_n}/{d}'
            dists = []
            while len(dists) < 3:
                dn = n1 + n2 + rng.choice([-2, -1, 1, 2])
                if dn > 0 and dn != ans_n:
                    ds = f'{dn}/{d}'
                    if ds not in dists: dists.append(ds)
            while len(dists) < 3:
                dists.append(f'{ans_n + len(dists) + 1}/{d}')
            qs.append(make_question(f'What is {n1}/{d} + {n2}/{d}?', ans, dists[:3], 3))
    return qs

def gen_geometry(rng, gtype, count):
    qs, seen = [], set()
    while len(qs) < count:
        if gtype == 'sides':
            shapes = {'triangle':3,'square':4,'rectangle':4,'pentagon':5,'hexagon':6,'octagon':8}
            shape, sides = rng.choice(list(shapes.items()))
            key = f'sides_{shape}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, sides, 10)
            qs.append(make_question(f'How many sides does a {shape} have?', str(sides), [str(d) for d in dists], 1))
        elif gtype == 'perimeter':
            l, w = rng.randint(2, 15), rng.randint(1, 15)
            p = 2 * (l + w)
            key = f'peri_{l}_{w}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, p, 40)
            qs.append(make_question(f'Perimeter of rectangle: length {l}, width {w}?', str(p), [str(d) for d in dists], 2))
        elif gtype == 'area':
            l, w = rng.randint(2, 12), rng.randint(2, 12)
            a = l * w
            key = f'area_{l}_{w}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, a, 50)
            qs.append(make_question(f'Area of rectangle: length {l}, width {w}?', str(a), [str(d) for d in dists], 2))
        elif gtype == 'angles':
            a = rng.choice(range(30, 130, 5))
            b = rng.choice(range(30, 130, 5))
            c = 180 - a - b
            if c <= 0: continue
            key = f'ang_{a}_{b}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, c, 60)
            qs.append(make_question(f'Triangle angles: {a}\u00b0 and {b}\u00b0. Third angle?', str(c), [str(d) for d in dists], 3))
    return qs

def gen_decimals(rng, dtype, count):
    qs, seen = [], set()
    while len(qs) < count:
        if dtype == 'add':
            a = round(rng.uniform(1, 9.9), 1)
            b = round(rng.uniform(1, 9.9), 1)
            ans = round(a + b, 1)
            key = f'da_{a}_{b}'
            if key in seen: continue
            seen.add(key)
            dists = [str(round(ans + 0.1, 1)), str(round(ans - 0.1, 1)), str(round(ans + 0.2, 1))]
            dists = [d for d in dists if d != str(ans)][:3]
            while len(dists) < 3:
                dists.append(str(round(ans + 0.1 * (len(dists) + 1), 1)))
            qs.append(make_question(f'What is {a} + {b}?', str(ans), dists[:3], 2))
        elif dtype == 'sub':
            a = round(rng.uniform(2, 9.9), 1)
            b = round(rng.uniform(1, 9.9), 1)
            if b > a: a, b = b, a
            ans = round(a - b, 1)
            key = f'ds_{a}_{b}'
            if key in seen: continue
            seen.add(key)
            dists = [str(round(ans + 0.1, 1)), str(round(ans - 0.1, 1)), str(round(ans + 0.2, 1))]
            dists = [d for d in dists if d != str(ans)][:3]
            while len(dists) < 3:
                dists.append(str(round(ans + 0.1 * (len(dists) + 1), 1)))
            qs.append(make_question(f'What is {a} \u2212 {b}?', str(ans), dists[:3], 2))
        else:
            denoms = [2, 4, 5, 10, 20, 25, 50]
            d = rng.choice(denoms)
            n = rng.randint(1, d - 1)
            ans = round(n / d, 2)
            key = f'fd_{n}_{d}'
            if key in seen: continue
            seen.add(key)
            dists = []
            while len(dists) < 3:
                dn = rng.randint(1, d - 1)
                ds = str(round(dn / d, 2))
                if ds != str(ans) and ds not in dists:
                    dists.append(ds)
            while len(dists) < 3:
                dists.append(str(round(ans + 0.1 * (len(dists) + 1), 2)))
            qs.append(make_question(f'What is {n}/{d} as a decimal?', str(ans), dists[:3], 3))
    return qs

def gen_percentage(rng, count):
    qs, seen = [], set()
    while len(qs) < count:
        ptype = rng.randint(0, 2)
        if ptype == 0:
            num = rng.choice(range(5, 100, 5))
            total = rng.choice([20, 40, 50, 60, 80, 100, 200])
            pct = round((num / total) * 100)
            key = f'f2p_{num}_{total}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, pct, 50)
            qs.append(make_question(f'What percentage is {num} out of {total}?', f'{pct}%',
                                    [f'{d}%' for d in dists], 3))
        elif ptype == 1:
            pct = rng.choice([10, 20, 25, 50, 75])
            total = rng.choice([20, 40, 50, 60, 80, 100, 200])
            num = int((pct / 100) * total)
            key = f'p2f_{pct}_{total}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, num, 50)
            qs.append(make_question(f'What is {pct}% of {total}?', str(num),
                                    [str(d) for d in dists], 3))
        else:
            num = rng.choice(range(10, 200, 5))
            pct = rng.choice([10, 20, 25, 50])
            total = int((num / pct) * 100)
            key = f'rev_{num}_{pct}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, total, 100)
            qs.append(make_question(f'{num} is {pct}% of what number?', str(total),
                                    [str(d) for d in dists], 3))
    return qs

def gen_ratio(rng, count):
    qs, seen = [], set()
    while len(qs) < count:
        a, b = rng.randint(1, 9), rng.randint(1, 9)
        if a == b: continue
        mult = rng.randint(2, 8)
        key = f'ratio_{a}_{b}_{mult}'
        if key in seen: continue
        seen.add(key)
        dists = make_num_distractors(rng, b * mult, 30)
        qs.append(make_question(f'If {a}:{b} = {a*mult}:x, what is x?', str(b * mult),
                                [str(d) for d in dists], 3))
    return qs

def gen_factors_multiples(rng, ftype, count):
    qs, seen = [], set()
    while len(qs) < count:
        if ftype == 'factors':
            num = rng.randint(4, 36)
            factors = [i for i in range(1, num+1) if num % i == 0]
            f = rng.choice(factors)
            key = f'fac_{num}_{f}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, f, 15)
            qs.append(make_question(f'Which is a factor of {num}?', str(f), [str(d) for d in dists], 2))
        elif ftype == 'multiples':
            num = rng.randint(2, 12)
            mult = rng.randint(2, 10)
            ans = num * mult
            key = f'mul_{num}_{ans}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, ans, 20)
            qs.append(make_question(f'Which is a multiple of {num}?', str(ans), [str(d) for d in dists], 2))
        else:
            a, b = rng.randint(4, 20), rng.randint(4, 20)
            if a == b: continue
            from math import gcd
            hcf = gcd(a, b)
            lcm = (a * b) // hcf
            is_hcf = rng.choice([True, False])
            ans = hcf if is_hcf else lcm
            label = 'HCF' if is_hcf else 'LCM'
            key = f'hl_{a}_{b}_{"h" if is_hcf else "l"}'
            if key in seen: continue
            seen.add(key)
            dists = make_num_distractors(rng, ans, max(30, ans))
            qs.append(make_question(f'What is the {label} of {a} and {b}?', str(ans),
                                    [str(d) for d in dists], 3))
    return qs


# ═══════════════════════════════════════════════════════════
# LEVEL CONFIGURATIONS
# ═══════════════════════════════════════════════════════════
LEVEL_CONFIGS = [
    {   # Nursery 1
        'name': 'Nursery 1', 'seed': 1001,
        'gens': [
            (lambda r, n: gen_colors(r, n), 40),
            (lambda r, n: gen_shapes(r, n), 30),
            (lambda r, n: gen_counting(r, 10, n), 50),
            (lambda r, n: gen_bigger(r, 10, n), 40),
            (lambda r, n: gen_before_after(r, 10, n), 40),
            (lambda r, n: gen_animal_sounds(r, n), 20),
            (lambda r, n: gen_which_is(r, 'fruit', FRUITS, VEGETABLES + ANIMALS[:10] + ['Chair','Book'], n), 45),
            (lambda r, n: gen_which_is(r, 'vegetable', VEGETABLES, FRUITS + ANIMALS[:10] + ['Table','Pen'], n), 45),
            (lambda r, n: gen_which_is(r, 'animal', ANIMALS[:20], FRUITS[:10] + ['Chair','Car','Book'], n), 40),
            (lambda r, n: gen_body_parts(r, n), 25),
            (lambda r, n: gen_opposites(r, n), 30),
            (lambda r, n: gen_which_is(r, 'bird', BIRDS, ANIMALS[:15], n), 20),
            (lambda r, n: gen_which_is(r, 'transport', TRANSPORTS, ANIMALS[:15], n), 20),
            (lambda r, n: gen_which_is(r, 'food item', FOODS, VEGETABLES, n), 20),
            (lambda r, n: gen_days_months(r, 'days', n), 15),
            (lambda r, n: gen_facts(r, FACTS_ANIMALS[:10], n), 10),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT[:8], n), 8),
        ]
    },
    {   # Nursery 2
        'name': 'Nursery 2', 'seed': 1002,
        'gens': [
            (lambda r, n: gen_counting(r, 20, n), 40),
            (lambda r, n: gen_addition(r, 1, 5, 1, 5, n), 65),
            (lambda r, n: gen_bigger(r, 20, n), 40),
            (lambda r, n: gen_before_after(r, 20, n), 40),
            (lambda r, n: gen_missing_number(r, 20, n), 40),
            (lambda r, n: gen_spelling(r, SPELLING_3, n), 50),
            (lambda r, n: gen_opposites(r, n), 30),
            (lambda r, n: gen_plurals(r, n), 35),
            (lambda r, n: gen_animal_babies(r, n), 20),
            (lambda r, n: gen_days_months(r, 'months', n), 20),
            (lambda r, n: gen_which_is(r, 'season', SEASONS, MONTHS[:8], n), 20),
            (lambda r, n: gen_rhyming(r, n), 25),
            (lambda r, n: gen_which_is(r, 'insect', INSECTS, ANIMALS[:15], n), 20),
            (lambda r, n: gen_which_is(r, 'festival', FESTIVALS, MONTHS[:10], n), 20),
            (lambda r, n: gen_facts(r, FACTS_ANIMALS[10:20], n), 10),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE[:8], n), 8),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT[8:14], n), 6),
            (lambda r, n: gen_word_problems(r, 1, n), 15),
        ]
    },
    {   # KG 1
        'name': 'KG 1', 'seed': 1003,
        'gens': [
            (lambda r, n: gen_counting(r, 50, n), 30),
            (lambda r, n: gen_addition(r, 1, 10, 1, 10, n), 75),
            (lambda r, n: gen_subtraction(r, 2, 10, 1, 5, n), 60),
            (lambda r, n: gen_bigger(r, 50, n), 25),
            (lambda r, n: gen_before_after(r, 50, n), 25),
            (lambda r, n: gen_missing_number(r, 50, n), 40),
            (lambda r, n: gen_spelling(r, SPELLING_4, n), 50),
            (lambda r, n: gen_opposites(r, n), 20),
            (lambda r, n: gen_plurals(r, n), 25),
            (lambda r, n: gen_vowels_consonants(r, n), 26),
            (lambda r, n: gen_capital_small(r, n), 20),
            (lambda r, n: gen_rhyming(r, n), 20),
            (lambda r, n: gen_grammar_is_are(r, n), 20),
            (lambda r, n: gen_word_problems(r, 2, n), 25),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE[8:16], n), 8),
            (lambda r, n: gen_facts(r, FACTS_GK[:10], n), 10),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT[14:20], n), 6),
            (lambda r, n: gen_which_is(r, 'water body', WATER_BODIES, CONTINENTS, n), 15),
            (lambda r, n: gen_which_is(r, 'planet', PLANETS, CONTINENTS, n), 10),
        ]
    },
    {   # KG 2
        'name': 'KG 2', 'seed': 1004,
        'gens': [
            (lambda r, n: gen_addition(r, 1, 20, 1, 20, n), 80),
            (lambda r, n: gen_subtraction(r, 2, 20, 1, 10, n), 60),
            (lambda r, n: gen_multiplication(r, 2, 5, 1, 10, n), 40),
            (lambda r, n: gen_multiplication(r, 10, 10, 1, 10, n), 20),
            (lambda r, n: gen_missing_number(r, 50, n), 30),
            (lambda r, n: gen_spelling(r, SPELLING_5, n), 50),
            (lambda r, n: gen_grammar_is_are(r, n), 20),
            (lambda r, n: gen_grammar_a_an(r, n), 20),
            (lambda r, n: gen_plurals(r, n), 20),
            (lambda r, n: gen_opposites(r, n), 15),
            (lambda r, n: gen_word_problems(r, 2, n), 30),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE[16:25], n), 9),
            (lambda r, n: gen_facts(r, FACTS_GK[10:18], n), 8),
            (lambda r, n: gen_facts(r, FACTS_ANIMALS, n), 15),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT, n), 10),
            (lambda r, n: gen_which_is(r, 'continent', CONTINENTS, COUNTRIES[:10], n), 10),
            (lambda r, n: gen_which_is(r, 'country', COUNTRIES[:15], ANIMALS[:10], n), 15),
            (lambda r, n: gen_which_is(r, 'occupation', OCCUPATIONS, ANIMALS[:10], n), 15),
            (lambda r, n: gen_which_is(r, 'material', MATERIALS, ANIMALS[:10], n), 15),
            (lambda r, n: gen_which_is(r, 'place', PLACES, ANIMALS[:10], n), 15),
            (lambda r, n: gen_bigger(r, 100, n), 20),
            (lambda r, n: gen_before_after(r, 100, n), 15),
        ]
    },
    {   # Primary 1
        'name': 'Primary 1', 'seed': 1005,
        'gens': [
            (lambda r, n: gen_addition(r, 10, 99, 1, 99, n), 80),
            (lambda r, n: gen_subtraction(r, 10, 99, 1, 50, n), 70),
            (lambda r, n: gen_multiplication(r, 2, 10, 1, 10, n), 80),
            (lambda r, n: gen_division(r, 1, 10, 10, n), 50),
            (lambda r, n: gen_spelling(r, SPELLING_5, n), 30),
            (lambda r, n: gen_spelling(r, SPELLING_6[:20], n), 20),
            (lambda r, n: gen_grammar_is_are(r, n), 15),
            (lambda r, n: gen_grammar_a_an(r, n), 15),
            (lambda r, n: gen_plurals(r, n), 15),
            (lambda r, n: gen_word_problems(r, 3, n), 35),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE, n), 20),
            (lambda r, n: gen_facts(r, FACTS_GK, n), 15),
            (lambda r, n: gen_facts(r, FACTS_ANIMALS, n), 10),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT, n), 8),
            (lambda r, n: gen_missing_number(r, 100, n), 30),
            (lambda r, n: gen_bigger(r, 999, n), 20),
            (lambda r, n: gen_before_after(r, 100, n), 15),
            (lambda r, n: gen_which_is(r, 'country', COUNTRIES, ANIMALS[:10], n), 20),
            (lambda r, n: gen_which_is(r, 'place', PLACES, MATERIALS, n), 15),
            (lambda r, n: gen_which_is(r, 'bird', BIRDS, INSECTS, n), 15),
            (lambda r, n: gen_which_is(r, 'festival', FESTIVALS, MONTHS, n), 12),
        ]
    },
    {   # Primary 2
        'name': 'Primary 2', 'seed': 1006,
        'gens': [
            (lambda r, n: gen_addition(r, 10, 999, 10, 999, n), 60),
            (lambda r, n: gen_subtraction(r, 10, 999, 10, 500, n), 60),
            (lambda r, n: gen_multiplication(r, 2, 12, 2, 12, n), 60),
            (lambda r, n: gen_multiplication(r, 10, 99, 2, 10, n), 30),
            (lambda r, n: gen_division(r, 2, 50, 12, n), 50),
            (lambda r, n: gen_word_problems(r, 3, n), 35),
            (lambda r, n: gen_spelling(r, SPELLING_6[10:], n), 25),
            (lambda r, n: gen_spelling(r, SPELLING_7[:20], n), 20),
            (lambda r, n: gen_plurals(r, n), 10),
            (lambda r, n: gen_grammar_is_are(r, n), 10),
            (lambda r, n: gen_grammar_a_an(r, n), 10),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE, n), 15),
            (lambda r, n: gen_facts(r, FACTS_GK, n), 12),
            (lambda r, n: gen_facts(r, FACTS_ANIMALS, n), 8),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT, n), 8),
            (lambda r, n: gen_missing_number(r, 200, n), 20),
            (lambda r, n: gen_geometry(r, 'perimeter', n), 15),
            (lambda r, n: gen_geometry(r, 'area', n), 15),
            (lambda r, n: gen_fractions(r, 'identify', n), 15),
            (lambda r, n: gen_fractions(r, 'compare', n), 15),
        ]
    },
    {   # Primary 3
        'name': 'Primary 3', 'seed': 1007,
        'gens': [
            (lambda r, n: gen_addition(r, 100, 9999, 100, 9999, n), 50),
            (lambda r, n: gen_subtraction(r, 100, 9999, 100, 5000, n), 50),
            (lambda r, n: gen_multiplication(r, 10, 99, 2, 20, n), 50),
            (lambda r, n: gen_division(r, 5, 50, 20, n), 40),
            (lambda r, n: gen_fractions(r, 'identify', n), 20),
            (lambda r, n: gen_fractions(r, 'compare', n), 30),
            (lambda r, n: gen_decimals(r, 'add', n), 30),
            (lambda r, n: gen_decimals(r, 'sub', n), 30),
            (lambda r, n: gen_geometry(r, 'perimeter', n), 25),
            (lambda r, n: gen_geometry(r, 'area', n), 25),
            (lambda r, n: gen_factors_multiples(r, 'factors', n), 25),
            (lambda r, n: gen_factors_multiples(r, 'multiples', n), 25),
            (lambda r, n: gen_spelling(r, SPELLING_6[10:], n), 25),
            (lambda r, n: gen_spelling(r, SPELLING_7[:20], n), 20),
            (lambda r, n: gen_plurals(r, n), 10),
            (lambda r, n: gen_word_problems(r, 4, n), 30),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE, n), 15),
            (lambda r, n: gen_facts(r, FACTS_GK, n), 12),
            (lambda r, n: gen_fractions(r, 'add', n), 20),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT, n), 8),
            (lambda r, n: gen_missing_number(r, 500, n), 15),
            (lambda r, n: gen_geometry(r, 'angles', n), 15),
        ]
    },
    {   # Primary 4
        'name': 'Primary 4', 'seed': 1008,
        'gens': [
            (lambda r, n: gen_addition(r, 1000, 99999, 1000, 99999, n), 40),
            (lambda r, n: gen_subtraction(r, 1000, 99999, 100, 9999, n), 40),
            (lambda r, n: gen_multiplication(r, 10, 99, 10, 99, n), 50),
            (lambda r, n: gen_division(r, 5, 99, 20, n), 40),
            (lambda r, n: gen_fractions(r, 'compare', n), 25),
            (lambda r, n: gen_fractions(r, 'add', n), 30),
            (lambda r, n: gen_decimals(r, 'add', n), 25),
            (lambda r, n: gen_decimals(r, 'sub', n), 25),
            (lambda r, n: gen_decimals(r, 'fraction', n), 20),
            (lambda r, n: gen_percentage(r, n), 30),
            (lambda r, n: gen_ratio(r, n), 20),
            (lambda r, n: gen_geometry(r, 'area', n), 20),
            (lambda r, n: gen_geometry(r, 'perimeter', n), 15),
            (lambda r, n: gen_geometry(r, 'angles', n), 15),
            (lambda r, n: gen_factors_multiples(r, 'factors', n), 20),
            (lambda r, n: gen_factors_multiples(r, 'multiples', n), 20),
            (lambda r, n: gen_factors_multiples(r, 'hcf_lcm', n), 20),
            (lambda r, n: gen_word_problems(r, 5, n), 35),
            (lambda r, n: gen_spelling(r, SPELLING_7, n), 20),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE, n), 15),
            (lambda r, n: gen_facts(r, FACTS_GK, n), 10),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT, n), 6),
            (lambda r, n: gen_missing_number(r, 1000, n), 10),
        ]
    },
    {   # Primary 5
        'name': 'Primary 5', 'seed': 1009,
        'gens': [
            (lambda r, n: gen_addition(r, 10000, 999999, 10000, 99999, n), 35),
            (lambda r, n: gen_subtraction(r, 10000, 999999, 1000, 99999, n), 35),
            (lambda r, n: gen_multiplication(r, 10, 99, 10, 99, n), 50),
            (lambda r, n: gen_division(r, 5, 99, 25, n), 40),
            (lambda r, n: gen_fractions(r, 'add', n), 30),
            (lambda r, n: gen_fractions(r, 'compare', n), 20),
            (lambda r, n: gen_decimals(r, 'add', n), 20),
            (lambda r, n: gen_decimals(r, 'sub', n), 20),
            (lambda r, n: gen_decimals(r, 'fraction', n), 15),
            (lambda r, n: gen_percentage(r, n), 35),
            (lambda r, n: gen_ratio(r, n), 25),
            (lambda r, n: gen_geometry(r, 'area', n), 20),
            (lambda r, n: gen_geometry(r, 'perimeter', n), 15),
            (lambda r, n: gen_geometry(r, 'angles', n), 15),
            (lambda r, n: gen_factors_multiples(r, 'factors', n), 20),
            (lambda r, n: gen_factors_multiples(r, 'multiples', n), 20),
            (lambda r, n: gen_factors_multiples(r, 'hcf_lcm', n), 25),
            (lambda r, n: gen_word_problems(r, 6, n), 40),
            (lambda r, n: gen_spelling(r, SPELLING_7, n), 15),
            (lambda r, n: gen_facts(r, FACTS_SCIENCE, n), 12),
            (lambda r, n: gen_facts(r, FACTS_GK, n), 10),
            (lambda r, n: gen_odd_one_out(r, ODD_ONE_OUT, n), 5),
            (lambda r, n: gen_missing_number(r, 10000, n), 8),
        ]
    },
]

# Subject ranges for splitting questions into subjects
NURSERY_RANGES = {
    0: ('English & Numbers', 0, 5),
    1: ('Basic Science & Nature', 5, 10),
    2: ('Social Studies & Habits', 10, 15),
    3: ('General Knowledge', 15, 20),
}

PRIMARY_RANGES = {
    0: ('English Language', 0, 12),
    1: ('Mathematics', 12, 24),
    2: ('Basic Science', 24, 32),
    3: ('Social Studies', 32, 40),
    4: ('Computer Studies & GK', 40, 50),
}


# ═══════════════════════════════════════════════════════════
# PUBLIC API FUNCTIONS
# ═══════════════════════════════════════════════════════════
def get_available_classes():
    return [cfg['name'] for cfg in LEVEL_CONFIGS]

def get_class_question_count(class_name):
    for cfg in LEVEL_CONFIGS:
        if cfg['name'] == class_name:
            return sum(n for _, n in cfg['gens'])
    return 0

def get_questions_for_class(class_name, subject_index=0):
    """Generate questions for a class, split by subject if subject_index given."""
    config = None
    for cfg in LEVEL_CONFIGS:
        if cfg['name'] == class_name:
            config = cfg
            break
    if not config:
        return [], class_name, class_name, '', ''

    rng = random.Random(config['seed'])

    # Generate all questions
    all_qs = []
    for gen_fn, count in config['gens']:
        try:
            all_qs.extend(gen_fn(rng, count))
        except Exception as e:
            print(f'Warning: generator failed for {class_name}: {e}')

    if not all_qs:
        return [], class_name, class_name, '', ''

    # Assign sequential IDs
    for i, q in enumerate(all_qs):
        q['id'] = i + 1

    # Determine subject ranges
    is_nursery = 'Nursery' in class_name
    ranges = NURSERY_RANGES if is_nursery else PRIMARY_RANGES

    subject_name, start, end = ranges.get(subject_index, ('Mixed', 0, len(all_qs)))
    end = min(end, len(all_qs))
    subject_qs = all_qs[start:end]

    # Re-index subject questions
    for i, q in enumerate(subject_qs):
        q['id'] = i + 1

    return subject_qs, subject_name, class_name, '', ''
