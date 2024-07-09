import streamlit as st
import numpy as np
import datetime
from weekly import main

st.set_page_config(layout = "wide")

days_of_week = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
]

all_colours = [
'darkseagreen',
'pink',
'cornflowerblue',
'skyblue',
'plum',
'darkorange',
'mediumpurple',
'lightgreen',
] * 5

events_file = "events.txt"

def create_class_element(i, column, row):
    with column:
        # everything needed for each class
        st.write(f"Class {i+1}")
        show = st.checkbox("Show in calendar", value=True, key = "show" + str(i) + str(row))

        code = st.text_input("Class code:", key = "code" + str(i) + str(row))

        credit = st.number_input("Credit weight:", value=2, step=1, min_value=2, max_value=4, key = "credit" + str(i) + str(row))
        description = st.text_input("Class description:", key = "desc" + str(i) + str(row))

        active_days = []
        sched = []

        for y, day in zip(range(5), days_of_week):
            with st.container():
                inner_cols = st.columns(3)
                tmp = inner_cols[0].checkbox(day, key=day + str(y) + str(i) + str(row))

                if tmp:
                    start = inner_cols[1].time_input(f"Start time on {day}:", 
                                                     value=datetime.time(9,0), 
                                                     key = "start" + str(y) + str(i) + str(row))    
                    end = inner_cols[2].time_input(f"End time on {day}:", 
                                                   value=datetime.time(11,0), 
                                                   key = "end" + str(y) + str(i) + str(row))
                    
                    sched.append(tuple([start, end]))
                    
                    active_days.append(y)
                
                else:
                    sched.append(tuple([]))
        
                
        exam_date = st.date_input("Exam date:", key = "exam" + str(i) + str(row))

        writing_req = st.radio("Writing requirements:", ["Yes", "No", "Maybe"], key = "writing" + str(i) + str(row))

        d = {
            "show" : show,
            "num" : i,
            "code" : code,
            "description" : description,
            "active_days" : active_days,
            "sched" : sched,
            "exam_date" : exam_date,
            "writing" : writing_req,
            "credits" : credit,
            "intersection" : [[],[],[],[],[]]
        }
    
    return d

def find_intersection(classes):
    for i, cl1 in enumerate(classes[:-1]):
        for j, cl2 in enumerate(classes[i+1:]):
            for days in range(5):
                # end of class 1 is between start and end of class 2
                try:
                    if days in cl1['active_days'] and days in cl2['active_days'] and cl2['sched'][days][0] <= cl1['sched'][days][1] <= cl2['sched'][days][1]:
                        classes[j + i + 1]['intersection'][days].append([days,i])
                        
                except:
                    pass

def class_to_text(cl, text_file, i):
    if cl['show']:
        days = ""
        try:
            colour = all_colours[i]
        
        except IndexError:
            pass
        try:
            for d in cl['active_days']:
                if d == 0:
                    days="Mon"
                elif d == 1:
                    days="Tue"
                elif d == 2:
                    days="Wed"
                elif d == 3:
                    days="Thu"
                elif d == 4:
                    days="Fri"

                time = rf"{cl['sched'][d][0].strftime('%H:%M')} - {cl['sched'][d][1].strftime('%H:%M')}"
                intersection = ''.join(str(ele) for ele in cl['intersection'][d])
            
                with open(text_file, 'a') as f:
                    out = f"""{cl['code']}\n{days}\n{time}\n{colour}\n{cl['credits']}\n{intersection}\n{cl['num']}\n{cl['writing']}\n\n"""
                    f.write(out)
        
        except UnboundLocalError:
            pass
    
    else:
        pass

show_threshold = int(st.number_input("Number of classes per row:", value=2, step=1, min_value=1, max_value=6))
num_classes = int(st.number_input("Number of classes:",value=1, step=1))
d_collection = []

with st.expander("Hide/Show Classes", expanded=True):

    if num_classes > show_threshold:

        num_rows = int(np.ceil(num_classes / show_threshold))

        num_cols_for_row = [show_threshold for _ in range(num_rows)]

        if num_classes % show_threshold !=0:
            num_cols_for_row[-1] = (num_classes % show_threshold)

        for r, col_count in enumerate(num_cols_for_row):
            row = st.columns(col_count)
            for i, column in enumerate(row):
                temp = create_class_element(int(i + r * show_threshold), column, row)
                d_collection.append(temp)

    else:
        row = st.columns(num_classes)
        for i, column in enumerate(row):
                temp = create_class_element(i, column, row)
                d_collection.append(temp)

find_intersection(d_collection)

with open(events_file, 'w') as f:
    f.write("")

for i, cl in enumerate(d_collection):
    class_to_text(cl, events_file, i)

main(events_file)

st.image(events_file + ".png")
