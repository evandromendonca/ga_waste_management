dict_comb = {}

with open('./data/params_test/comb_params_tests.csv', 'r') as comb_files:
    comb_files.readline()
    comb_lines = comb_files.read().splitlines()
    for line in comb_lines:
        pretty_line = ';'.join(list(filter(lambda x: len(x) > 0, line.split(';'))))
        line_index = comb_lines.index(line) + 1
        dict_comb[pretty_line] = []
        with open('./data/params_test/params_test_'+str(line_index)+'.csv', 'r') as test_file:
            test_lines = test_file.read().splitlines()
            results_array = []
            for test_line in test_lines:
                results_array.append(test_line.split(';'))
            for j in range(0, 10000):
                avg = 0
                for k in range(0,10):
                    avg += float(results_array[k][j])
                avg = avg / float(10)
                dict_comb[pretty_line].append(avg)      

print 'finished reading'

with open('./data/params_test/tests_results.csv', 'w') as result_file:
    for comb in dict_comb:
        result_file.write(comb)
        result_file.write(';') # jump column
        result_file.write(';')
        for i in range(0, 10001, 200):
            if i == 10000:
                result_file.write(str(dict_comb[comb][9999]))
            else:
                result_file.write(str(dict_comb[comb][i]))
            result_file.write(';')
        result_file.write('\n')

print 'done'