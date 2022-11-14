# read in model results files and output results to a csv file for calculation
import json

output_csv = open("output_metrics.csv", 'w', encoding = 'utf-8')
output_csv.write("round" + "\t" + "type" + "\t" + 'ents_p' + "\t" + 'ents_r' + "\t" + 'ents_f' + "\n")

round = 0

while round < 10:

    output_file = open('./none-ex/output_{}/model-best/meta.json'.format(round))
    # output_file = open('./output_{}/model-best/meta.json'.format(round))

    output_data = json.load(output_file)

    # print(output_data['performance'])

    output_csv.write(str(round) + "\t" + "overall" + "\t" + str(output_data['performance']['ents_p']) + "\t" + str(output_data['performance']['ents_r']) + "\t" + str(output_data['performance']['ents_f']) + "\n")

    for i in output_data['performance']['ents_per_type']:
        # print(output_data['performance']['ents_per_type'][i])

        output_csv.write(str(round) + "\t" + i + "\t" + str(output_data['performance']['ents_per_type'][i]['p']) + "\t" + str(output_data['performance']['ents_per_type'][i]['r']) + "\t" + str(output_data['performance']['ents_per_type'][i]['f']) + "\n")

    round += 1