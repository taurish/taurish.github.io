'''
Author: Shahan Ali Memon
Description: This code analyzes the
responses of the people from the 
Age Experiment Study
'''

import numpy as np
import sys
import csv
import generate_lb as glb
#import plotly.plotly as py
#import plotly.graph_objs as go
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import operator
plt.style.use('ggplot')

usr_to_day_missed = {}

def create_timeseries_perf(dictionary):
    days = sorted(map(lambda d: int(d), dictionary.keys()))
    #print days
    #sys.exit()
    users = sorted(dictionary[days[0]].keys())
    #print users
    #print(users.remove('correct'))
    perf_table = []
    usr_to_perf = {} #user->[perf1,perf2,...,perfd]
    for u in users:
        usr_perf_per_day = []
        day_missed = []
        #print u
        for d in days:
            print d
            if(u in dictionary[d].keys() and 'correct' in dictionary[d].keys() and dictionary[d][u][0][0] != '0' and dictionary[d][u][1][0] != '0'):
                #correct perf
                d_day_true = dictionary[d]['correct']
                #for mae
                d_day_perf = dictionary[d][u]
                mae_a = sum([abs(float(d_day_perf[0][i])-float(d_day_true[0][i])) for i in range(5)])/5
                mae_w = sum([abs(float(d_day_perf[1][i])-float(d_day_true[1][i])) for i in range(5)])/5
                mae_h = sum([abs(float(d_day_perf[2][i])-float(d_day_true[2][i])) for i in range(5)])/5
                #for underestimation and overestimation                                                                                                                     
                bin_a = Counter([(-1 if float(d_day_perf[0][i])-float(d_day_true[0][i]) < 0 else 1) for i in range(5)]).most_common(1)[0][0]
                bin_w = Counter([(-3 if float(d_day_perf[1][i])-float(d_day_true[1][i]) < 0 else 3) for i in range(5)]).most_common(1)[0][0]
                bin_h = Counter([(-2 if float(d_day_perf[2][i])-float(d_day_true[2][i]) < 0 else 2) for i in range(5)]).most_common(1)[0][0]
                usr_perf_per_day.append([mae_a,mae_w,mae_h,bin_a,bin_w,bin_h])
        #print usr_perf_per_day
        #sys.exit()
        usr_to_perf[u] = usr_perf_per_day

    #Here I amd doing some calc for leaderboard i.e. if you missed more than 4 days of exp, you cant be on leaderboard
    total_days = len(usr_to_perf['correct'])
    #print total_days
    #sys.exit()
    days_allowed_to_be_missed = 5
    not_leaders = []
    for u in usr_to_perf.keys():
        if(len(usr_to_perf[u]) < (total_days - days_allowed_to_be_missed)):
            not_leaders.append(u)
    

    #Now for each user we will create a graph for time series
    usr_to_running_age = {}
    usr_to_running_height = {}
    usr_to_running_weight = {}
    users.remove('correct')
    for u in users:
        #This will create their time-series graph
        #We have to create 3 lines for age,height and weight
        xy_age = [[],[]]
        xy_weight = [[],[]]
        xy_height = [[],[]]
        
        xy_age_est = [[],[]]
        xy_height_est = [[],[]]
        xy_weight_est = [[],[]]
        
        for day in range(len(usr_to_perf[u])):
            day_perf = usr_to_perf[u][day]
            xy_age[0].append(day+1)
            xy_weight[0].append(day+1)
            xy_height[0].append(day+1)
            xy_age[1].append(day_perf[0])
            xy_height[1].append(day_perf[1])
            xy_weight[1].append(day_perf[2])
            
            xy_age_est[0].append(day+1)
            xy_age_est[1].append(day_perf[3])

            xy_height_est[0].append(day+1)
            xy_height_est[1].append(day_perf[4])

            xy_weight_est[0].append(day+1)
            xy_weight_est[1].append(day_perf[5])
        plt.style.use('dark_background')    
        plt.title(u)
        plt.plot(xy_age[0],xy_age[1],color='r')
        plt.plot(xy_weight[0],xy_weight[1],color='b')
        plt.plot(xy_height[0],xy_height[1],color='g')
        
        plt.plot(xy_age_est[0],xy_age_est[1],'ro',color='r',markersize=5)
        plt.plot(xy_weight_est[0],xy_weight_est[1],'ro',color='b',markersize=5)
        plt.plot(xy_height_est[0],xy_height_est[1],'ro',color='g',markersize=5)
        plt.ylabel('mean absolute error')
        plt.xlabel('day')
        red_patch = mpatches.Patch(color='red', label='age')
        green_patch = mpatches.Patch(color='green', label='height')
        blue_patch = mpatches.Patch(color='blue', label='weight')
        plt.legend(handles=[red_patch,blue_patch,green_patch])
        plt.savefig("/Users/samemon/Documents/GitHub/samemon.github.io/images/performance/"+u)
    
        plt.clf()
        usr_to_running_age[u] = sum(xy_age[1])/len(xy_age[1])
        usr_to_running_height[u] = sum(xy_height[1])/len(xy_height[1])
        usr_to_running_weight[u] = sum(xy_weight[1])/len(xy_weight[1])
    

    leaders_age = filter(lambda (u,s): not(u in not_leaders), 
                         sorted(usr_to_running_age.items(), key=operator.itemgetter(1)))
    leaders_height = filter(lambda (u,s): not(u in not_leaders),
                            sorted(usr_to_running_height.items(), key=operator.itemgetter(1)))
    leaders_weight = filter(lambda (u,s): not(u in not_leaders),
                            sorted(usr_to_running_weight.items(), key=operator.itemgetter(1)))
    
    return leaders_age,leaders_height,leaders_weight
    
        
if __name__ == "__main__":
    argv = sys.argv[1:]
    #Accept only 1 argument i.e. the wav file
    if(len(argv) != 2):
        print("Usage: python analyze.py <csv file> <day>")
        sys.exit()
    else:
        #First thing we do is read the csv file
        #my_data = np.genfromtxt(argv[0], delimiter=',',dtype=None)[1:]
        #print my_data
        #Lets write down the orientation of data
        
        '''
        day: col[0]
        participants: col[1]
        
        Regression:
        age labels: col[2], col[5], col[8], col[11], col[14]
        height labels: col[3], col[6], col[9], col[12], col[15]
        weight labels: col[4], col[7], col[10], col[13], col[16]
        
        Classification:
        age labels: col[17], col[20]
        height labels: col[18], col[21]
        weight labels: col[19], col[22]
        '''
        today = argv[1]
        #Now let us first do individual analysis day by day
        #We want a nested dictionary from day -> user -> response 
        #But what are all the users?
        day_to_user_to_resp = {}
        with open(argv[0],'r') as data_file:
            data = csv.DictReader(data_file, delimiter=",")
            #print data
            for row in data:
                #print row
                item = day_to_user_to_resp.get(row["Day"], dict())
                #print item
                #sys.exit()
                #print row["Participant"]
                item[row["Participant"]] = [[row["Recording 1 Age"],
                                             row["Recording 2 Age"],
                                             row["Recording 3 Age"],
                                             row["Recording 4 Age"],
                                             row["Recording 5 Age"]],

                                            [row["Recording 1 Height"],
                                             row["Recording 2 Height"],
                                             row["Recording 3 Height"],
                                             row["Recording 4 Height"],
                                             row["Recording 5 Height"]],

                                            [row["Recording 1 Weight"],
                                             row["Recording 2 Weight"],
                                             row["Recording 3 Weight"],
                                             row["Recording 4 Weight"],
                                             row["Recording 5 Weight"]],

                                            [row["Who is older in 6 and 7?"],
                                             row["Who is older in 8 and 9?"]],
                                            
                                            [row["Who is taller in 6 and 7?"],
                                             row["Who is taller in 8 and 9?"]],

                                            [row["Who is heavier in 6 and 7?"],
                                             row["Who is heavier in 8 and 9?"]]
                                            ]

                day_to_user_to_resp[row['Day']] = item

        new_int_dict = {}
        for k in day_to_user_to_resp.keys():
            key = int(k)
            val = day_to_user_to_resp[k]
            new_int_dict[key] = val
            
        usr_to_perf =  day_to_user_to_resp[today]
        #Now here I need to create that thing about user to perf
        #Will do later

        #sys.exit()
        leaders_age,leaders_height,leaders_weight = create_timeseries_perf(new_int_dict)

        print glb.generate_leaderboard(leaders_age[:5])
        print glb.generate_leaderboard(leaders_height[:5])
        print glb.generate_leaderboard(leaders_weight[:5])
        
