import csv, sqlite3, re

conn = sqlite3.connect("registers.db")
cur = conn.cursor()

print("CREATING ADDRESS TABLE...")

cur.executescript("""
    CREATE TABLE IF NOT EXISTS `REGISTERS` (
    `COD_REG` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `BASE` VARCHAR(10) NOT NULL,
    `F_NAME` VARCHAR(50) NOT NULL,
    `M_NAME` VARCHAR(50) NULL,
    `L_NAME` VARCHAR(50) NULL,
    `TITLE` VARCHAR(15) NULL,
    `EMAIL` VARCHAR(40) NOT NULL,
    `AFFILIATION` VARCHAR(50) NOT NULL,
    `ADDRESS` VARCHAR(100) NOT NULL);
""")

def find_aff(regs):
    aff, add, loc = ('', '', 0)

    all_aff = ['Department', 'University' , 'Institute', 'Laboratory', 'Universitá', 'Ecole', 'Dipartimento', 'Institut', 'Universität',
    'School', 'Informat', 'Science', 'Microsoft', 'Engineering', 'Intel',
    'College', 'Inc.', 'Research', 'Universit', 'Rech']

    for i in range(len(regs)):
        for j in all_aff:
            if j in regs[i]:
                aff += str(regs[i]) + ' '
                loc = i
                break

    for i in regs[loc+1:]:
        add += str(i) + ' '



    return (aff, add)

def find_title(name):
    titles = ['Mr', 'Dr' , 'Ms', 'Mr', 'Miss', 'Prof']
    new_name = name

    for t in titles:
        if t in name:
            new_name = name.replace(t, '')
            return (t, new_name)

    return ('', new_name)

print("CREATING ADDRESS TABLE...COMPLETE")

def sep_reg(list_regs):
    all_reg, new_reg, v_reg, l_name = ([], [], {}, '')

    for i in list_regs:
        if i == '\n':
            if new_reg:
                v_reg = {'BASE' : 'han1', 'F_NAME' : '', 'M_NAME' : '',
                        'L_NAME' : '', 'TITLE' : '', 'EMAIL' : '',
                        'AFFILIATION' : '', 'ADDRESS' : ''}
                l_name, r_name = ('', [])

                t_n = find_title(new_reg[0])

                v_reg['TITLE'] = t_n[0]

                all_name = t_n[1].split(' ')

                if len(all_name[0]) > 3:
                    v_reg['F_NAME'] = all_name[0]
                    r_name = all_name[1:]
                else:
                    v_reg['F_NAME'] = all_name[1]
                    r_name = all_name[2:]

                for i in r_name:
                    l_name += i + ' '

                v_reg['L_NAME'] = l_name

                aff_add = find_aff(new_reg[1:])

                v_reg['AFFILIATION'] = aff_add[0]
                v_reg['ADDRESS'] = aff_add[1]

                all_reg.append(v_reg)
                new_reg = []
        else:
            new_reg.append(i.strip())
    return all_reg

print("INSERT FROM TXT TO DATABASE...")

with open('han1.txt', encoding = 'UTF-8') as inf:
    cont = inf.readlines()
    all_reg_ok = sep_reg(cont)

    to_db = [(i['BASE'], i['F_NAME'], i['M_NAME'], i['L_NAME'],
            i['TITLE'], i['EMAIL'], i['AFFILIATION'],
            i['ADDRESS']) for i in all_reg_ok]

    if not to_db:
        print('ERROR TO CONVERT TXT TO DB...')
        exit()
    else:
        print('NUMBER OF REGISTERS : %s' % len(to_db))

cur.executemany("INSERT INTO REGISTERS ( \
                            BASE, \
                            F_NAME, \
                            M_NAME, \
                            L_NAME, \
                            TITLE, \
                            EMAIL, \
                            AFFILIATION, \
                            ADDRESS \
                            ) \
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

conn.close()

print("INSERT FROM TXT TO DATABASE...COMPLETE")
