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

print("CREATING ADDRESS TABLE...COMPLETE")

def sep_reg(list_regs):
    all_reg, new_reg, v_reg = ([], [], {})
    start_f_n, end_f_n = ('First name = ', ' Middle')
    start_m_n, end_m_n = ('Middle name = ', ' Last')
    start_l_n, end_l_n = ('Last name = ', '')
    start_t_n, end_t_n = ('Title = ', ' Email')
    start_e_n, end_e_n = ('Email = ', '')
    start_af_n, end_af_n = ('Affiliation = ', '')
    start_ad_n, end_ad_n = ('Address = ', '')

    for i in list_regs:
        if i == '\n':
            if new_reg:
                v_reg = {'BASE' : 'han2', 'F_NAME' : '', 'M_NAME' : '',
                        'L_NAME' : '', 'TITLE' : '', 'EMAIL' : '',
                        'AFFILIATION' : '', 'ADDRESS' : ''}

                re_data = re.search('%s(.*)%s' % (start_f_n, end_f_n), new_reg[0])

                if re_data:
                    v_reg['F_NAME'] = re_data.group(1)

                re_data = re.search('%s(.*)%s' % (start_m_n, end_m_n), new_reg[0])

                if re_data:
                    v_reg['M_NAME'] = re_data.group(1)

                re_data = re.search('%s(.*)%s' % (start_l_n, end_l_n), new_reg[0])

                if re_data:
                    v_reg['L_NAME'] = re_data.group(1)

                re_data = re.search('%s(.*)%s' % (start_t_n, end_t_n), new_reg[1])

                if re_data:
                    v_reg['TITLE'] = re_data.group(1)

                re_data = re.search('%s(.*)%s' % (start_e_n, end_e_n), new_reg[1])

                if re_data:
                    v_reg['EMAIL'] = re_data.group(1)

                re_data = re.search('%s(.*)%s' % (start_af_n, end_af_n), new_reg[2])

                if re_data:
                    v_reg['AFFILIATION'] = re_data.group(1)

                re_data = re.search('%s(.*)%s' % (start_ad_n, end_ad_n), new_reg[3])

                if re_data:
                    v_reg['ADDRESS'] = re_data.group(1)

                all_reg.append(v_reg)
                new_reg = []
        else:
            new_reg.append(i.strip())
    return all_reg

print("INSERT FROM TXT TO DATABASE...")

with open('han2.txt', encoding = 'UTF-8')  as inf:
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
