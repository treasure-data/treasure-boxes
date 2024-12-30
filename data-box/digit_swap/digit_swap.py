import pandas as pd

def check_consecutive_digit_swap():
    df = pd.read_csv('data.csv', dtype=str)
    df = df.reset_index()  # Make sure indexes pair with number of rows.
    cnt = 0

    # init result csv
    f = open('res.csv','w+')
    f.write('phone1,phone2\n')
    f.close()

    f = open('res.csv', 'w')

    for index, row in df.iterrows():
        phone1 = row['ph1']
        phone2 = row['ph2']

        # Check if lengths are the same.
        if len(phone1) == len(phone2):

            # Find differing positions.
            differing_positions = [i for i in range(len(phone1)) if phone1[i] != phone2[i]]
            
            # Check if there are exactly two differing positions, and that they are consecutive.
            if len(differing_positions) == 2:
                i, j = differing_positions
                if (j == i + 1 and phone1[i] == phone2[j] and phone1[j] == phone2[i]):
                    cnt = cnt + 1
                    f.write(phone1 + ',' + phone2 + '\n')
                    #print(phone1, phone2, (j == i + 1
                    #    and phone1[i] == phone2[j]
                    #    and phone1[j] == phone2[i]))
    print(str(cnt))
    f.close()

check_consecutive_digit_swap()
